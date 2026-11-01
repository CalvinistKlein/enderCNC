#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Option 1 Fixed-Bridge Mill — Counterbalanced "Split-Weight" Router Head

Weight Distribution Architecture:
- FRONT: 52 mm Spindle (Router) + Safety Orange Clamp Collar + Z-Plunge Slide
- MIDDLE (IN BETWEEN): X-Axis Guide Rail + Compound X-Bridge (2040+4040)
- BACK: Z-Axis Stepper Motor (NEMA 17) + Rear Counterweight Bracket + Top Belt Transfer

Benefits:
- Neutralizes forward cantilever tipping moment on the linear guide bearings.
- Significantly increases cutting stiffness and eliminates spindle chatter.
- Lower overall center of gravity.
"""

import os
from freecad_mcp.freecad_client import FreeCADConnection

PROJECT_DIR = "/home/calvin/.gemini/antigravity/scratch/ender3-router-project"
STP_MAIN    = os.path.join(PROJECT_DIR, "ender3_cad_repo/Ender-3 Mechanical/STP/01 MAIN ASM Ender_3.STEP")
STP_DIR     = os.path.join(PROJECT_DIR, "ender3_cad_repo/Ender-3 Mechanical/STP")
RENDER_DIR  = os.path.join(PROJECT_DIR, "renders")
CAD_DIR     = os.path.join(PROJECT_DIR, "cad")
os.makedirs(RENDER_DIR, exist_ok=True)
os.makedirs(CAD_DIR, exist_ok=True)

FREECAD_CODE = f"""
import os, math
import FreeCAD as App
import FreeCADGui as Gui
import Part
from FreeCAD import Base

STP_MAIN   = {STP_MAIN!r}
STP_DIR    = {STP_DIR!r}
RENDER_DIR = {RENDER_DIR!r}
CAD_DIR    = {CAD_DIR!r}

for doc_name in list(App.listDocuments().keys()):
    App.closeDocument(doc_name)

doc = App.newDocument("Ender3_Option1_Counterbalanced_CNC")

# Load Donor Solids from 01 MAIN ASM Ender_3.STEP
main_asm = Part.Shape()
main_asm.read(STP_MAIN)
solids = main_asm.Solids

def norm_origin(shape):
    s = shape.copy()
    bb = s.BoundBox
    cx = (bb.XMin + bb.XMax) / 2.0
    cy = (bb.YMin + bb.YMax) / 2.0
    s.translate(Base.Vector(-cx, -cy, -bb.ZMin))
    return s

def place(shape, x=0.0, y=0.0, z=0.0):
    s = shape.copy()
    s.translate(Base.Vector(x, y, z))
    return s

# 8 Stock Aluminum Extrusions:
# 1) 4040 x 290 mm (vertical Z = 0..290)
ext_4040_290_A = norm_origin(solids[0])
ext_4040_290_B = norm_origin(solids[1])

# 2) 4040 x 250 mm (along X = -125..125, Y = -20..20, Z = 0..40)
ext_4040_250 = norm_origin(solids[2])

# 3) 2040 x 400 mm (along Y = -200..200, X = -20..20, Z = 0..20)
ext_2040_400_A = norm_origin(solids[4])
ext_2040_400_B = norm_origin(solids[5])

# 4) 2040 x 330 mm (along X = -165..165, Y = -10..10, Z = 0..40)
ext_2040_330_vert = norm_origin(solids[421])
ext_2040_330_horiz_x = ext_2040_330_vert.copy()
ext_2040_330_horiz_x.rotate(Base.Vector(0,0,0), Base.Vector(0,1,0), 90)
ext_2040_330_horiz_x.rotate(Base.Vector(0,0,0), Base.Vector(1,0,0), 90)
ext_2040_330_horiz_x = norm_origin(ext_2040_330_horiz_x)

# 5) 2020 x 345 mm (along X = -172.5..172.5, Y = -10..10, Z = 0..20)
ext_2020_345 = norm_origin(solids[44])

# 6) 2020 x 330 mm (along X = -165..165, Y = -10..10, Z = 0..20)
ext_2020_330 = norm_origin(solids[3])

# Load Individual STEP files for donor hardware:
def load_step_norm(fname):
    p = os.path.join(STP_DIR, fname)
    if os.path.exists(p):
        s = Part.Shape()
        s.read(p)
        return norm_origin(s)
    return None

psu_shape     = load_step_norm("24V15A power supply.step")
board_box_bot = load_step_norm("Sheetmetal enclosure bottom.step")
board_box_top = load_step_norm("Sheetmetal enclosure top.step")
motor_42_34   = load_step_norm("42-34 motor.step")
z_rod_t8      = load_step_norm("Z threaded rod.step")
y_plate_donor = load_step_norm("Y plate.step")

# Color Palette:
CLR_4040     = (0.22, 0.26, 0.32)   # Charcoal-Slate
CLR_2040     = (0.18, 0.52, 0.82)   # Industrial Steel-Blue
CLR_2020     = (0.90, 0.62, 0.14)   # Amber-Gold
CLR_FEET     = (0.15, 0.15, 0.16)   # Matte Black Riser Feet
CLR_PSU      = (0.80, 0.82, 0.85)   # Brushed Aluminum PSU
CLR_ENCL     = (0.12, 0.14, 0.18)   # Black Sheet Metal Enclosure
CLR_MOTOR    = (0.18, 0.18, 0.20)   # Stepper Black & Metallic
CLR_LEADSCREW= (0.85, 0.85, 0.90)   # Polished Stainless Steel Leadscrew
CLR_CARRIAGE = (0.28, 0.32, 0.38)   # Anodized Aluminum Saddle Carriage
CLR_SPINDLE  = (0.75, 0.77, 0.80)   # 52mm Spindle Body
CLR_COLLAR   = (0.95, 0.38, 0.08)   # Safety Orange CNC Clamp Collar
CLR_TABLE    = (0.75, 0.72, 0.65)   # Spoilboard Worktable
CLR_BUILDVOL = (0.00, 0.90, 0.76)   # Transparent Cyan-Emerald Build Volume
CLR_BELT     = (0.10, 0.10, 0.10)   # Matte Black GT2 Belt
CLR_PULLEY   = (0.70, 0.72, 0.75)   # Aluminum GT2 Pulley

def add_part(doc, grp, name, shape, rgb, transparency=0, line_rgb=(0.08, 0.10, 0.12), line_width=1.6):
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = shape
    if grp:
        grp.addObject(obj)
    if App.GuiUp and obj.ViewObject:
        vo = obj.ViewObject
        vo.ShapeColor = rgb
        vo.Transparency = transparency
        try:
            vo.LineColor = line_rgb
            vo.LineWidth = line_width
        except Exception:
            pass
    return obj

# Organization Groups:
grp_feet    = doc.addObject("App::DocumentObjectGroup", "01_Ground_Riser_Feet")
grp_base    = doc.addObject("App::DocumentObjectGroup", "02_Extrusions_Frame")
grp_elec    = doc.addObject("App::DocumentObjectGroup", "03_Undercarriage_Electronics")
grp_y_motion= doc.addObject("App::DocumentObjectGroup", "04_Y_Axis_Motion")
grp_x_motion= doc.addObject("App::DocumentObjectGroup", "05_X_Axis_Motion")
grp_toolhead= doc.addObject("App::DocumentObjectGroup", "06_Counterbalanced_Toolhead")
grp_vol     = doc.addObject("App::DocumentObjectGroup", "07_Build_Volume")

# =============================================================================
# 1. 6 GROUND-SUPPORT RISER FEET (Z = 0 .. 75 mm)
# =============================================================================
FOOT_H = 75.0
foot_coords = [
    ("Front_Left",  -145.0, -190.0),
    ("Front_Right",  145.0, -190.0),
    ("Rear_Left",   -145.0,  190.0),
    ("Rear_Right",   145.0,  190.0),
    ("Column_Left", -145.0,   20.0),
    ("Column_Right", 145.0,   20.0),
]

for label, fx, fy in foot_coords:
    block = Part.makeBox(44.0, 44.0, FOOT_H, Base.Vector(fx - 22.0, fy - 22.0, 0.0))
    pad = Part.makeBox(52.0, 52.0, 8.0, Base.Vector(fx - 26.0, fy - 26.0, 0.0))
    f_shape = block.fuse(pad)
    flange = Part.makeBox(40.0, 40.0, 6.0, Base.Vector(fx - 20.0, fy - 20.0, FOOT_H - 6.0))
    f_shape = f_shape.fuse(flange)
    add_part(doc, grp_feet, f"Riser_Foot_{{label}}", f_shape, CLR_FEET)


# =============================================================================
# 2. 8 UNCUT EXTRUSIONS (Option 1 Geometry, Elevated to Z >= 75 mm)
# =============================================================================
# 1) Front Base Tie (2020 x 345 mm): Y = -190 mm, Z = 75..95 mm
add_part(doc, grp_base, "Base_Front_Tie_2020x345",
         place(ext_2020_345, 0.0, -190.0, FOOT_H), CLR_2020)

# 2) Rear Base Tie (2020 x 330 mm): Y = +190 mm, Z = 75..95 mm
add_part(doc, grp_base, "Base_Rear_Tie_2020x330",
         place(ext_2020_330, 0.0,  190.0, FOOT_H), CLR_2020)

# 3 & 4) Twin Y-Axis Bed Ways (2x 2040 x 400 mm):
# Spanning Y = -200..+200 mm at X = +/-95 mm, Z = 95..115 mm
add_part(doc, grp_base, "Y_Bed_Way_Left_2040x400",
         place(ext_2040_400_A, -95.0, 0.0, FOOT_H + 20.0), CLR_2040)
add_part(doc, grp_base, "Y_Bed_Way_Right_2040x400",
         place(ext_2040_400_B,  95.0, 0.0, FOOT_H + 20.0), CLR_2040)

# 5 & 6) Fixed Portal Columns (2x 4040 x 290 mm):
# Standing vertically at X = +/-145 mm, Y = [0, 40] (center Y = 20 mm), Z = 75..365 mm
add_part(doc, grp_base, "Portal_Column_Left_4040x290",
         place(ext_4040_290_A, -145.0, 20.0, FOOT_H), CLR_4040)
add_part(doc, grp_base, "Portal_Column_Right_4040x290",
         place(ext_4040_290_B,  145.0, 20.0, FOOT_H), CLR_4040)

# 7) Inner X-Bridge Girder (1x 4040 x 250 mm):
# Bolted between column inner faces (X = -125..125 mm), Y = [0, 40] (center Y = 20 mm), Z = 250..290 mm
add_part(doc, grp_base, "X_Bridge_Inner_Girder_4040x250",
         place(ext_4040_250, 0.0, 20.0, FOOT_H + 175.0), CLR_4040)

# 8) Front X-Bridge Way (1x 2040 x 330 mm):
# Spans full 330 mm across front faces of columns:
# X = -165..165 mm, Y = [-20, 0] (center Y = -10 mm), Z = 250..290 mm
add_part(doc, grp_base, "X_Bridge_Front_Way_2040x330",
         place(ext_2040_330_horiz_x, 0.0, -10.0, FOOT_H + 175.0), CLR_2040)


# =============================================================================
# 3. UNDERCARRIAGE BASEMENT ELECTRONICS (Z = 10 .. 65 mm)
# =============================================================================
# Left: Creality 24V 15A Power Supply (215 x 113 x 50 mm) at X = -72 mm
if psu_shape:
    s_psu = psu_shape.copy()
    s_psu.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), 90)
    s_psu = norm_origin(s_psu)
    add_part(doc, grp_elec, "Ender3_24V_15A_PowerSupply",
             place(s_psu, -72.0, 0.0, 10.0), CLR_PSU)
else:
    psu_box = Part.makeBox(113.0, 215.0, 50.0, Base.Vector(-128.5, -107.5, 10.0))
    add_part(doc, grp_elec, "Ender3_24V_15A_PowerSupply", psu_box, CLR_PSU)

# Right: Creality Mainboard & Stepper Driver Enclosure at X = +78 mm
if board_box_bot:
    s_box = board_box_bot.copy()
    s_box.rotate(Base.Vector(0,0,0), Base.Vector(1,0,0), 90)
    if board_box_top:
        s_top = board_box_top.copy()
        s_top.rotate(Base.Vector(0,0,0), Base.Vector(1,0,0), 90)
        s_box = s_box.fuse(s_top)
    s_box = norm_origin(s_box)
    add_part(doc, grp_elec, "Ender3_Mainboard_Driver_Enclosure",
             place(s_box, 78.0, 0.0, 15.0), CLR_ENCL)
else:
    encl_box = Part.makeBox(125.0, 153.0, 40.0, Base.Vector(15.5, -76.5, 15.0))
    add_part(doc, grp_elec, "Ender3_Mainboard_Driver_Enclosure", encl_box, CLR_ENCL)


# =============================================================================
# 4. Y-AXIS MOTION SYSTEM (Moving Table)
# =============================================================================
# Linear rails on top of twin 2040 ways:
y_rail_L = Part.makeBox(12.0, 396.0, 8.0, Base.Vector(-95.0 - 6.0, -198.0, FOOT_H + 40.0))
y_rail_R = Part.makeBox(12.0, 396.0, 8.0, Base.Vector( 95.0 - 6.0, -198.0, FOOT_H + 40.0))
add_part(doc, grp_y_motion, "Y_Linear_Guide_Rail_Left",  y_rail_L, CLR_LEADSCREW)
add_part(doc, grp_y_motion, "Y_Linear_Guide_Rail_Right", y_rail_R, CLR_LEADSCREW)

for side_x in [-95.0, 95.0]:
    for block_y in [-60.0, 60.0]:
        bk = Part.makeBox(27.0, 45.0, 10.0, Base.Vector(side_x - 13.5, block_y - 22.5, FOOT_H + 48.0))
        lbl = "L" if side_x < 0 else "R"
        pos = "F" if block_y < 0 else "R"
        add_part(doc, grp_y_motion, f"Y_BearingBlock_{{lbl}}_{{pos}}", bk, CLR_CARRIAGE)

# Rear Y-Axis Stepper Motor + Coupler + Central Leadscrew:
if motor_42_34:
    s_ymot = motor_42_34.copy()
    s_ymot.rotate(Base.Vector(0,0,0), Base.Vector(1,0,0), 90)
    s_ymot = norm_origin(s_ymot)
    add_part(doc, grp_y_motion, "Y_Axis_NEMA17_Stepper",
             place(s_ymot, 0.0, 210.0, FOOT_H + 10.0), CLR_MOTOR)
else:
    ymot_box = Part.makeBox(42.0, 34.0, 42.0, Base.Vector(-21.0, 205.0, FOOT_H + 10.0))
    add_part(doc, grp_y_motion, "Y_Axis_NEMA17_Stepper", ymot_box, CLR_MOTOR)

y_coupler = Part.makeCylinder(9.5, 25.0, Base.Vector(0.0, 195.0, FOOT_H + 30.0), Base.Vector(0.0, -1.0, 0.0))
add_part(doc, grp_y_motion, "Y_Flexible_Coupler", y_coupler, CLR_SPINDLE)

y_leadscrew = Part.makeCylinder(4.0, 370.0, Base.Vector(0.0, 170.0, FOOT_H + 30.0), Base.Vector(0.0, -1.0, 0.0))
add_part(doc, grp_y_motion, "Y_T8_Leadscrew_370mm", y_leadscrew, CLR_LEADSCREW)

y_nut_block = Part.makeBox(30.0, 30.0, 24.0, Base.Vector(-15.0, -15.0, FOOT_H + 34.0))
add_part(doc, grp_y_motion, "Y_AntiBacklash_Nut_Block", y_nut_block, (0.85, 0.65, 0.20))

# Bed Carriage Plate & Spoilboard Worktable:
if y_plate_donor:
    add_part(doc, grp_y_motion, "Y_Bed_Carriage_Plate",
             place(y_plate_donor, 0.0, 0.0, FOOT_H + 58.0), CLR_CARRIAGE)
else:
    bed_plate = Part.makeBox(190.0, 190.0, 4.0, Base.Vector(-95.0, -95.0, FOOT_H + 58.0))
    add_part(doc, grp_y_motion, "Y_Bed_Carriage_Plate", bed_plate, CLR_CARRIAGE)

worktable = Part.makeBox(264.0, 240.0, 12.0, Base.Vector(-132.0, -197.0, FOOT_H + 62.0))
add_part(doc, grp_y_motion, "Spoilboard_Worktable_Surface", worktable, CLR_TABLE)


# =============================================================================
# 5. X-AXIS MOTION SYSTEM (Bridge Rails & X Drive)
# =============================================================================
# The X-axis has a precision linear guide rail mounted on the front face of 2040x330:
# X = [-165, +165], Y = -28 mm, Z = FOOT_H + 195 mm
x_rail = Part.makeBox(330.0, 8.0, 12.0, Base.Vector(-165.0, -28.0, FOOT_H + 189.0))
add_part(doc, grp_x_motion, "X_Linear_Guide_Rail_330mm", x_rail, CLR_LEADSCREW)

# Left Column X-Drive Stepper Motor:
if motor_42_34:
    s_xmot = motor_42_34.copy()
    s_xmot.rotate(Base.Vector(0,0,0), Base.Vector(0,1,0), 90)
    s_xmot = norm_origin(s_xmot)
    add_part(doc, grp_x_motion, "X_Axis_NEMA17_Stepper",
             place(s_xmot, -185.0, -10.0, FOOT_H + 175.0), CLR_MOTOR)
else:
    xmot_box = Part.makeBox(34.0, 42.0, 42.0, Base.Vector(-205.0, -31.0, FOOT_H + 175.0))
    add_part(doc, grp_x_motion, "X_Axis_NEMA17_Stepper", xmot_box, CLR_MOTOR)

x_idler = Part.makeCylinder(9.0, 20.0, Base.Vector(180.0, -10.0, FOOT_H + 185.0), Base.Vector(0.0, 0.0, 1.0))
add_part(doc, grp_x_motion, "X_Belt_Tensioner_Pulley", x_idler, CLR_PULLEY)

x_belt = Part.makeBox(360.0, 2.0, 6.0, Base.Vector(-180.0, -31.0, FOOT_H + 192.0))
add_part(doc, grp_x_motion, "X_GT2_Steel_Drive_Belt", x_belt, CLR_BELT)


# =============================================================================
# 6. COUNTERBALANCED "SPLIT-WEIGHT" ROUTER HEAD (The Core Request!)
# =============================================================================
# Split-Weight Layout:
# - FRONT:  52mm ER11 Milling Spindle / Router (Y = -80 mm) + Orange Clamp Collar + Z-Plunge Plate
# - MIDDLE: X-Bridge (Y = -20..+40 mm) + X Linear Guide Rail (Y = -28 mm)
# - BACK:   Z-Axis Stepper Motor (Y = +52 mm) + Rear Counterweight Bracket
# - OVERHEAD: GT2 Timing Belt Transfer running across the top from back stepper to front leadscrew!

# A. Saddle Carriage Body (Straddles the X-Bridge):
# 1) Top Bridge Plate: passes over top of crossbar at Z = FOOT_H + 215 mm (Z = 290 mm)
saddle_top = Part.makeBox(95.0, 85.0, 8.0, Base.Vector(-47.5, -36.0, FOOT_H + 216.0))

# 2) Front Drop Plate: carries the front Z linear guide rails and leadscrew
saddle_front = Part.makeBox(95.0, 8.0, 105.0, Base.Vector(-47.5, -36.0, FOOT_H + 115.0))

# 3) Rear Drop Plate: hangs behind the bridge to hold the Z stepper motor
saddle_rear = Part.makeBox(95.0, 8.0, 85.0, Base.Vector(-47.5, 41.0, FOOT_H + 135.0))

saddle_full = saddle_top.fuse(saddle_front).fuse(saddle_rear)
add_part(doc, grp_toolhead, "Counterbalanced_Saddle_Carriage", saddle_full, CLR_CARRIAGE)

# B. BACK: Z-Axis Stepper Motor (Behind the Rail / Crossbar):
# Mounted securely to the rear drop plate at Y = +55 mm, Z = FOOT_H + 155 mm
# Motor shaft points UP through the rear bracket flange!
if motor_42_34:
    add_part(doc, grp_toolhead, "Z_Stepper_Motor_REAR_BALANCER",
             place(motor_42_34, 0.0, 60.0, FOOT_H + 145.0), CLR_MOTOR)
else:
    z_mot_box = Part.makeBox(42.0, 42.0, 34.0, Base.Vector(-21.0, 39.0, FOOT_H + 145.0))
    add_part(doc, grp_toolhead, "Z_Stepper_Motor_REAR_BALANCER", z_mot_box, CLR_MOTOR)

# Rear Stepper GT2 Pulley on top (Z = FOOT_H + 225 mm, Y = +60 mm)
rear_pulley = Part.makeCylinder(10.0, 12.0, Base.Vector(0.0, 60.0, FOOT_H + 224.0), Base.Vector(0.0, 0.0, 1.0))
add_part(doc, grp_toolhead, "Z_Rear_Drive_Pulley", rear_pulley, CLR_PULLEY)

# C. OVERHEAD: Belt Transmission connecting Rear Stepper to Front Leadscrew:
# Top GT2 Belt spanning Y = +60 mm (rear) to Y = -48 mm (front) at Z = FOOT_H + 228 mm
top_belt_L = Part.makeBox(2.0, 108.0, 6.0, Base.Vector(-9.0, -48.0, FOOT_H + 227.0))
top_belt_R = Part.makeBox(2.0, 108.0, 6.0, Base.Vector( 7.0, -48.0, FOOT_H + 227.0))
add_part(doc, grp_toolhead, "Z_Overhead_Sync_Belt_Left",  top_belt_L, CLR_BELT)
add_part(doc, grp_toolhead, "Z_Overhead_Sync_Belt_Right", top_belt_R, CLR_BELT)

# Front Leadscrew Top Pulley (Z = FOOT_H + 224 mm, Y = -48 mm)
front_pulley = Part.makeCylinder(12.0, 12.0, Base.Vector(0.0, -48.0, FOOT_H + 224.0), Base.Vector(0.0, 0.0, 1.0))
add_part(doc, grp_toolhead, "Z_Front_Leadscrew_Driven_Pulley", front_pulley, CLR_PULLEY)

# D. FRONT: Vertical Motion Slide & Spindle:
# 1) Front Vertical Guide Rails (spaced at X = +/-28 mm, Y = -42 mm)
z_rail_L = Part.makeBox(8.0, 6.0, 120.0, Base.Vector(-28.0 - 4.0, -42.0, FOOT_H + 115.0))
z_rail_R = Part.makeBox(8.0, 6.0, 120.0, Base.Vector( 28.0 - 4.0, -42.0, FOOT_H + 115.0))
add_part(doc, grp_toolhead, "Z_Vertical_Guide_Rail_Left",  z_rail_L, CLR_LEADSCREW)
add_part(doc, grp_toolhead, "Z_Vertical_Guide_Rail_Right", z_rail_R, CLR_LEADSCREW)

# 2) Front Vertical T8 Leadscrew (130 mm long along Z at X = 0, Y = -48 mm)
z_leadscrew_front = Part.makeCylinder(4.0, 125.0, Base.Vector(0.0, -48.0, FOOT_H + 105.0), Base.Vector(0.0, 0.0, 1.0))
add_part(doc, grp_toolhead, "Z_Front_T8_Leadscrew_125mm", z_leadscrew_front, CLR_LEADSCREW)

# 3) Z-Plunge Plate (75 mm wide, 85 mm tall, 8 mm thick) at Y = -54 mm
z_plunge_plate = Part.makeBox(75.0, 8.0, 85.0, Base.Vector(-37.5, -54.0, FOOT_H + 115.0))
add_part(doc, grp_toolhead, "Z_Plunge_Slide_Plate", z_plunge_plate, CLR_CARRIAGE)

# 4) Spindle Clamp Collar (Safety Orange, 70 x 70 x 30 mm clamp block with 52 mm bore)
# Located out in FRONT at Y = -80 mm!
collar_box = Part.makeBox(70.0, 64.0, 30.0, Base.Vector(-35.0, -112.0, FOOT_H + 125.0))
collar_bore = Part.makeCylinder(26.0, 32.0, Base.Vector(0.0, -80.0, FOOT_H + 124.0), Base.Vector(0.0, 0.0, 1.0))
clamp_collar = collar_box.cut(collar_bore)
add_part(doc, grp_toolhead, "Spindle_Mount_Clamp_Collar_52mm", clamp_collar, CLR_COLLAR)

# 5) 500W ER11 High-Speed Brushless Milling Spindle (Router) in FRONT:
# Centerline at X = 0.0, Y = -80.0 mm
spindle_body = Part.makeCylinder(26.0, 175.0, Base.Vector(0.0, -80.0, FOOT_H + 65.0), Base.Vector(0.0, 0.0, 1.0))
spindle_collet = Part.makeCylinder(10.0, 25.0, Base.Vector(0.0, -80.0, FOOT_H + 40.0), Base.Vector(0.0, 0.0, 1.0))
spindle_endmill = Part.makeCylinder(1.58, 20.0, Base.Vector(0.0, -80.0, FOOT_H + 20.0), Base.Vector(0.0, 0.0, 1.0))
spindle_full = spindle_body.fuse(spindle_collet).fuse(spindle_endmill)
add_part(doc, grp_toolhead, "ER11_500W_Brushless_Milling_Spindle", spindle_full, CLR_SPINDLE)


# =============================================================================
# 7. TRANSPARENT PREDICTED BUILD VOLUME BOX
# =============================================================================
# 10.0" (X = 254.0 mm) x 9.0" (Y = 228.6 mm) x 3.0" (Z = 76.2 mm)
# Directly below the milling spindle nose (spindle at Y = -80.0 mm):
# X = [-127.0, +127.0 mm]
# Y = [-80.0 - 114.3, -80.0 + 114.3 mm] = [-194.3, +34.3 mm]
# Z = [FOOT_H + 74.0, FOOT_H + 74.0 + 76.2 mm] = [149.0, 225.2 mm]
IN_10 = 254.0
IN_9  = 228.6
IN_3  = 76.2
vol_box = Part.makeBox(IN_10, IN_9, IN_3, Base.Vector(-IN_10/2.0, -80.0 - IN_9/2.0, FOOT_H + 74.0))
add_part(doc, grp_vol, "Predicted_Build_Volume_10x9x3in",
         vol_box, CLR_BUILDVOL, transparency=65, line_rgb=(0.0, 1.0, 0.85), line_width=3.0)

doc.recompute()

view = Gui.ActiveDocument.ActiveView
view.setAnimationEnabled(False)

# 1. Full Machine Views:
for vname, vfn in [("iso", "viewIsometric"), ("front", "viewFront"), ("right", "viewRight"), ("top", "viewTop")]:
    getattr(view, vfn)()
    view.fitAll()
    Gui.updateGui()
    view.saveImage(os.path.join(RENDER_DIR, f"opt1_counterbalanced_{{vname}}.png"), 1600, 1200, "Current")

# 2. Dedicated Toolhead Close-Up Views (Showing the Split-Weight Balance):
# Hide base ties & undercarriage for clean toolhead closeup:
for obj in grp_feet.Group + grp_elec.Group:
    if obj.ViewObject:
        obj.ViewObject.Visibility = False

# Right Side Elevation Close-Up (Clearly shows Router FRONT - Rail MIDDLE - Motor BACK):
view.viewRight()
view.fitAll()
# Zoom in slightly on toolhead:
view.zoomIn()
Gui.updateGui()
view.saveImage(os.path.join(RENDER_DIR, "opt1_toolhead_split_weight_side.png"), 1600, 1200, "Current")

# Top Close-Up (Showing overhead belt sync and front-to-back balance):
view.viewTop()
view.fitAll()
view.zoomIn()
Gui.updateGui()
view.saveImage(os.path.join(RENDER_DIR, "opt1_toolhead_split_weight_top.png"), 1600, 1200, "Current")

# Isometric Close-Up:
view.viewIsometric()
view.fitAll()
view.zoomIn()
Gui.updateGui()
view.saveImage(os.path.join(RENDER_DIR, "opt1_toolhead_split_weight_iso.png"), 1600, 1200, "Current")

# Restore full visibility and save CAD:
for obj in grp_feet.Group + grp_elec.Group:
    if obj.ViewObject:
        obj.ViewObject.Visibility = True

doc.recompute()
fcstd_path = os.path.join(CAD_DIR, "Ender3_Option1_Counterbalanced_CNC.FCStd")
doc.saveAs(fcstd_path)
print("SAVED_COUNTERBALANCED_CAD:" + fcstd_path)
"""

def main():
    fc = FreeCADConnection(host="127.0.0.1", port=9875)
    res = fc.execute_code(FREECAD_CODE, timeout=120)
    print(res)

if __name__ == "__main__":
    main()
