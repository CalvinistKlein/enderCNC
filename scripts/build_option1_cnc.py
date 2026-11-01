#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Option 1: Fixed-Bridge Portal Mill — Full Motion Systems & Undercarriage Assembly

Features:
1. 8 Uncut Aluminum Extrusions from Creality Ender 3 STEP:
   - 2x 4040 x 290 mm: Fixed Vertical Columns (X = +/-145 mm)
   - 1x 4040 x 250 mm: Inner X-Bridge Girder (bolted between columns)
   - 1x 2040 x 330 mm: Front X-Bridge Way (spanning full 330 mm across front of columns)
   - 2x 2040 x 400 mm: Twin Y-Axis Bed Ways (X = +/-95 mm)
   - 1x 2020 x 345 mm: Front Lower Base Tie (Y = -190 mm)
   - 1x 2020 x 330 mm: Rear Lower Base Tie (Y = +190 mm)

2. 4 Heavy-Duty Corner Riser Feet:
   - Elevates frame 75 mm off workbench to create a dedicated Undercarriage Basement.

3. Undercarriage Basement Electronics:
   - Creality 24V 15A Power Supply (215 x 113 x 50 mm) mounted under bed on left.
   - Creality Mainboard & Stepper Driver Enclosure (145 x 153 x 40 mm) mounted under bed on right.
   - Clearance for cables, cooling fans, and front-facing SD card / USB access.

4. Complete Motion Systems:
   - Y-Axis:
     * Twin 400 mm linear ways on the 2040x400 extrusions.
     * Bed Carriage Plate (190 x 190 mm) with dual bearing guide sets.
     * Rear NEMA 17 Stepper Motor + Coupler + Central T8 Leadscrew (370 mm) + Anti-backlash Nut.
     * 260 x 240 mm Spoilboard Worktable surface.
     * Full 9.0" (228.6 mm) travel stroke.
   - X-Axis:
     * Linear guide rail across the 2040x330 front bridge.
     * X-Carriage Plate with bearing blocks.
     * Left Column NEMA 17 Stepper Motor + GT2 drive belt + Right tensioner idler.
     * Full 10.0" (254.0 mm) travel stroke.
   - Z-Axis:
     * Twin vertical 150 mm guide rails on X-carriage.
     * Top-mounted NEMA 17 Stepper + T8 Leadscrew + Anti-backlash Nut.
     * 52 mm Spindle Clamp Collar + 500W ER11 Brushless Milling Spindle.
     * Full 3.0" (76.2 mm) vertical plunge stroke.

5. Translucent 10" x 9" x 3" Build Volume Box:
   - 254.0 mm (X) x 228.6 mm (Y) x 76.2 mm (Z) Cyan-Emerald volume.
"""

import os, json
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

doc = App.newDocument("Ender3_Option1_Full_CNC")

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
z_coupler     = load_step_norm("Z coupler.step")
z_nut         = load_step_norm("z nut.step")

# Color Palette:
CLR_4040     = (0.22, 0.26, 0.32)   # Charcoal-Slate
CLR_2040     = (0.18, 0.52, 0.82)   # Industrial Steel-Blue
CLR_2020     = (0.90, 0.62, 0.14)   # Amber-Gold
CLR_FEET     = (0.15, 0.15, 0.16)   # Matte Black Riser Feet
CLR_PSU      = (0.80, 0.82, 0.85)   # Brushed Aluminum PSU
CLR_ENCL     = (0.12, 0.14, 0.18)   # Black Sheet Metal Enclosure
CLR_MOTOR    = (0.18, 0.18, 0.20)   # Stepper Black & Metallic
CLR_LEADSCREW= (0.85, 0.85, 0.90)   # Polished Stainless Steel Leadscrew
CLR_CARRIAGE = (0.30, 0.32, 0.36)   # Anodized Aluminum Carriage Plate
CLR_SPINDLE  = (0.70, 0.72, 0.75)   # 52mm Spindle Body
CLR_COLLAR   = (0.92, 0.40, 0.10)   # Safety Orange CNC Clamp Collar
CLR_TABLE    = (0.75, 0.72, 0.65)   # Spoilboard Worktable
CLR_BUILDVOL = (0.00, 0.90, 0.76)   # Transparent Cyan-Emerald Build Volume

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

# Groups:
grp_feet   = doc.addObject("App::DocumentObjectGroup", "01_Corner_Riser_Feet")
grp_base   = doc.addObject("App::DocumentObjectGroup", "02_Extrusions_Base_And_Portal")
grp_elec   = doc.addObject("App::DocumentObjectGroup", "03_Undercarriage_Electronics")
grp_motion = doc.addObject("App::DocumentObjectGroup", "04_Motion_Systems_XYZ")
grp_spindle= doc.addObject("App::DocumentObjectGroup", "05_Spindle_And_Worktable")
grp_vol    = doc.addObject("App::DocumentObjectGroup", "06_Predicted_Build_Volume")

# =============================================================================
# 1. CORNER RISER FEET (Z = 0 .. 75 mm)
# =============================================================================
# 4 heavy-duty corner riser feet elevating frame 75 mm off bench surface.
# Foot footprint: 60 x 60 mm base tapering to 40 x 40 mm top with rubber damping pad.
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
    # Main Riser Block (chamfered block)
    block = Part.makeBox(44.0, 44.0, FOOT_H, Base.Vector(fx - 22.0, fy - 22.0, 0.0))
    # Add rubber bench pad (5 mm tall, 52 x 52 mm)
    pad = Part.makeBox(52.0, 52.0, 8.0, Base.Vector(fx - 26.0, fy - 26.0, 0.0))
    # Combine foot
    f_shape = block.fuse(pad)
    # Flange plate for bolting into extrusion T-nuts
    flange = Part.makeBox(40.0, 40.0, 6.0, Base.Vector(fx - 20.0, fy - 20.0, FOOT_H - 6.0))
    f_shape = f_shape.fuse(flange)
    add_part(doc, grp_feet, f"Corner_Riser_Foot_{{label}}", f_shape, CLR_FEET)


# =============================================================================
# 2. 8 UNCUT EXTRUSIONS (Option 1 Geometry, Elevated to Z >= 75 mm)
# =============================================================================
# Z_BASE_BOTTOM = 75 mm
# 1) Front Base Tie (2020 x 345 mm): X centered, Y = -190 mm, Z = 75..95 mm
add_part(doc, grp_base, "Base_Front_Tie_2020x345",
         place(ext_2020_345, 0.0, -190.0, FOOT_H), CLR_2020)

# 2) Rear Base Tie (2020 x 330 mm): X centered, Y = +190 mm, Z = 75..95 mm
add_part(doc, grp_base, "Base_Rear_Tie_2020x330",
         place(ext_2020_330, 0.0,  190.0, FOOT_H), CLR_2020)

# 3 & 4) Twin Y-Axis Bed Ways (2x 2040 x 400 mm):
# Spanning Y = -200..+200 mm at X = +/-95 mm, resting on top of front & rear ties (Z = 95..115 mm)
add_part(doc, grp_base, "Y_Bed_Way_Left_2040x400",
         place(ext_2040_400_A, -95.0, 0.0, FOOT_H + 20.0), CLR_2040)
add_part(doc, grp_base, "Y_Bed_Way_Right_2040x400",
         place(ext_2040_400_B,  95.0, 0.0, FOOT_H + 20.0), CLR_2040)

# 5 & 6) Fixed Portal Columns (2x 4040 x 290 mm):
# Standing vertically at stock Ender 3 width X = +/-145 mm (outer 330 mm, inner gap 250 mm)
# Sitting directly on top of the front/rear foot plane at Z = 75..365 mm, Y = [0, 40] (center Y = 20 mm)
add_part(doc, grp_base, "Portal_Column_Left_4040x290",
         place(ext_4040_290_A, -145.0, 20.0, FOOT_H), CLR_4040)
add_part(doc, grp_base, "Portal_Column_Right_4040x290",
         place(ext_4040_290_B,  145.0, 20.0, FOOT_H), CLR_4040)

# 7) Inner X-Bridge Girder (1x 4040 x 250 mm):
# Bolted between the inner faces of columns (X = -125..125 mm), Y = [0, 40] (center Y = 20 mm), Z = 250..290 mm
add_part(doc, grp_base, "X_Bridge_Inner_Girder_4040x250",
         place(ext_4040_250, 0.0, 20.0, FOOT_H + 175.0), CLR_4040)

# 8) Front X-Bridge Way (1x 2040 x 330 mm):
# Spans the entire 330 mm width across the front faces of both columns:
# X = -165..165 mm, Y = [-20, 0] (center Y = -10 mm), Z = 250..290 mm
add_part(doc, grp_base, "X_Bridge_Front_Way_2040x330",
         place(ext_2040_330_horiz_x, 0.0, -10.0, FOOT_H + 175.0), CLR_2040)


# =============================================================================
# 3. UNDERCARRIAGE BASEMENT ELECTRONICS (Z = 10 .. 65 mm)
# =============================================================================
# Room underbed: X = [-120, +120], Y = [-160, +160], Z = [0, 75 mm]
# Left: Creality 24V 15A Power Supply (215 x 113 x 50 mm)
# Orient PSU along Y: length 215 mm along Y, width 113 mm along X, height 50 mm in Z
# Placed at X = -72 mm (X = -128.5 .. -15.5), leaving central clearance for T8 leadscrew at X=0
if psu_shape:
    s_psu = psu_shape.copy()
    s_psu.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), 90)
    s_psu = norm_origin(s_psu)
    add_part(doc, grp_elec, "Ender3_24V_15A_PowerSupply",
             place(s_psu, -72.0, 0.0, 10.0), CLR_PSU)
else:
    psu_box = Part.makeBox(113.0, 215.0, 50.0, Base.Vector(-128.5, -107.5, 10.0))
    add_part(doc, grp_elec, "Ender3_24V_15A_PowerSupply", psu_box, CLR_PSU)

# Right: Creality Mainboard & Stepper Driver Enclosure
# Rotate so 40 mm is along Z (height), 145 mm along X, 153 mm along Y
# Placed at X = +78 mm (X = +15.5 .. +140.5), leaving central clearance for T8 leadscrew at X=0
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
# 4. MOTION SYSTEMS XYZ
# =============================================================================

# --- A. Y-AXIS MOTION SYSTEM (Moving Table) ---
# 1) Y Linear Rails: Dual MGN12H linear guide rails (12 x 8 x 400 mm) on top of the twin 2040 ways
y_rail_L = Part.makeBox(12.0, 396.0, 8.0, Base.Vector(-95.0 - 6.0, -198.0, FOOT_H + 40.0))
y_rail_R = Part.makeBox(12.0, 396.0, 8.0, Base.Vector( 95.0 - 6.0, -198.0, FOOT_H + 40.0))
add_part(doc, grp_motion, "Y_Linear_Guide_Rail_Left",  y_rail_L, CLR_LEADSCREW)
add_part(doc, grp_motion, "Y_Linear_Guide_Rail_Right", y_rail_R, CLR_LEADSCREW)

# 2) Dual Bearing Blocks on each rail (4 blocks total, 27 x 45 x 10 mm)
for side_x in [-95.0, 95.0]:
    for block_y in [-60.0, 60.0]:
        bk = Part.makeBox(27.0, 45.0, 10.0, Base.Vector(side_x - 13.5, block_y - 22.5, FOOT_H + 48.0))
        lbl = "L" if side_x < 0 else "R"
        pos = "F" if block_y < 0 else "R"
        add_part(doc, grp_motion, f"Y_Carriage_BearingBlock_{{lbl}}_{{pos}}", bk, CLR_CARRIAGE)

# 3) Rear Y-Axis Stepper Motor (NEMA 17, 42 x 42 x 34 mm):
# Mounted at the rear base tie (Y = +215 mm, X = 0 mm, Z = FOOT_H + 20 mm)
if motor_42_34:
    s_ymot = motor_42_34.copy()
    s_ymot.rotate(Base.Vector(0,0,0), Base.Vector(1,0,0), 90)
    s_ymot = norm_origin(s_ymot)
    add_part(doc, grp_motion, "Y_Axis_NEMA17_Stepper",
             place(s_ymot, 0.0, 210.0, FOOT_H + 10.0), CLR_MOTOR)
else:
    ymot_box = Part.makeBox(42.0, 34.0, 42.0, Base.Vector(-21.0, 205.0, FOOT_H + 10.0))
    add_part(doc, grp_motion, "Y_Axis_NEMA17_Stepper", ymot_box, CLR_MOTOR)

# 4) Flexible Coupler & Central T8 Leadscrew (370 mm along Y at X = 0 mm, Z = FOOT_H + 30 mm)
y_coupler = Part.makeCylinder(9.5, 25.0, Base.Vector(0.0, 195.0, FOOT_H + 30.0), Base.Vector(0.0, -1.0, 0.0))
add_part(doc, grp_motion, "Y_Axis_Flexible_Coupler", y_coupler, CLR_SPINDLE)

y_leadscrew = Part.makeCylinder(4.0, 370.0, Base.Vector(0.0, 170.0, FOOT_H + 30.0), Base.Vector(0.0, -1.0, 0.0))
add_part(doc, grp_motion, "Y_Axis_T8_Leadscrew_370mm", y_leadscrew, CLR_LEADSCREW)

# 5) Brass Anti-Backlash Nut & Bracket on Bed Underside
y_nut_block = Part.makeBox(30.0, 30.0, 24.0, Base.Vector(-15.0, -15.0, FOOT_H + 34.0))
add_part(doc, grp_motion, "Y_Axis_AntiBacklash_Nut_Block", y_nut_block, (0.85, 0.65, 0.20))

# 6) Aluminum Bed Carriage Plate (190 x 190 x 4 mm) riding on the bearing blocks
if y_plate_donor:
    add_part(doc, grp_motion, "Y_Bed_Carriage_Plate",
             place(y_plate_donor, 0.0, 0.0, FOOT_H + 58.0), CLR_CARRIAGE)
else:
    bed_plate = Part.makeBox(190.0, 190.0, 4.0, Base.Vector(-95.0, -95.0, FOOT_H + 58.0))
    add_part(doc, grp_motion, "Y_Bed_Carriage_Plate", bed_plate, CLR_CARRIAGE)


# --- B. X-AXIS MOTION SYSTEM (Crossbar Carriage) ---
# 1) Front Linear Guide Rail (MGN12H, 12 x 8 x 330 mm) along X across the 2040x330 front face:
# X = [-165, +165], Y = -28 mm, Z = FOOT_H + 195 mm
x_rail = Part.makeBox(330.0, 8.0, 12.0, Base.Vector(-165.0, -28.0, FOOT_H + 189.0))
add_part(doc, grp_motion, "X_Linear_Guide_Rail_330mm", x_rail, CLR_LEADSCREW)

# 2) Left Column X-Drive Stepper Motor (NEMA 17):
# Mounted on an outrigger bracket on the left column (X = -195 mm, Y = 0 mm, Z = FOOT_H + 195 mm)
if motor_42_34:
    s_xmot = motor_42_34.copy()
    s_xmot.rotate(Base.Vector(0,0,0), Base.Vector(0,1,0), 90)
    s_xmot = norm_origin(s_xmot)
    add_part(doc, grp_motion, "X_Axis_NEMA17_Stepper",
             place(s_xmot, -185.0, -10.0, FOOT_H + 175.0), CLR_MOTOR)
else:
    xmot_box = Part.makeBox(34.0, 42.0, 42.0, Base.Vector(-205.0, -31.0, FOOT_H + 175.0))
    add_part(doc, grp_motion, "X_Axis_NEMA17_Stepper", xmot_box, CLR_MOTOR)

# Right Column Belt Tensioner Idler (X = +185 mm)
x_idler = Part.makeCylinder(9.0, 20.0, Base.Vector(180.0, -10.0, FOOT_H + 185.0), Base.Vector(0.0, 0.0, 1.0))
add_part(doc, grp_motion, "X_Belt_Tensioner_Idler", x_idler, CLR_SPINDLE)

# GT2 Steel-Reinforced Drive Belt across Bridge (X = -180..+180 mm)
x_belt = Part.makeBox(360.0, 2.0, 6.0, Base.Vector(-180.0, -31.0, FOOT_H + 192.0))
add_part(doc, grp_motion, "X_GT2_Steel_Drive_Belt", x_belt, (0.10, 0.10, 0.10))

# 3) X-Carriage Plate (90 mm wide, 110 mm tall, 8 mm thick) at X = 0 mm, Y = -36 mm
x_carriage = Part.makeBox(90.0, 8.0, 110.0, Base.Vector(-45.0, -36.0, FOOT_H + 140.0))
add_part(doc, grp_motion, "X_Carriage_Base_Plate", x_carriage, CLR_CARRIAGE)


# --- C. Z-AXIS MOTION SYSTEM (Vertical Plunge Toolhead) ---
# 1) Twin Vertical Guide Rails (12 x 8 x 140 mm) mounted on front of X-carriage:
# X = +/-28 mm, Y = -44 mm, Z = FOOT_H + 125..265 mm
z_rail_L = Part.makeBox(8.0, 8.0, 140.0, Base.Vector(-28.0 - 4.0, -44.0, FOOT_H + 125.0))
z_rail_R = Part.makeBox(8.0, 8.0, 140.0, Base.Vector( 28.0 - 4.0, -44.0, FOOT_H + 125.0))
add_part(doc, grp_motion, "Z_Vertical_Guide_Rail_Left",  z_rail_L, CLR_LEADSCREW)
add_part(doc, grp_motion, "Z_Vertical_Guide_Rail_Right", z_rail_R, CLR_LEADSCREW)

# 2) Top Z-Axis NEMA 17 Stepper Motor:
# Mounted on top of X-carriage arch (X = 0, Y = -52 mm, Z = FOOT_H + 250 mm)
if motor_42_34:
    add_part(doc, grp_motion, "Z_Axis_NEMA17_Stepper",
             place(motor_42_34, 0.0, -52.0, FOOT_H + 252.0), CLR_MOTOR)
else:
    zmot_box = Part.makeBox(42.0, 42.0, 34.0, Base.Vector(-21.0, -73.0, FOOT_H + 252.0))
    add_part(doc, grp_motion, "Z_Axis_NEMA17_Stepper", zmot_box, CLR_MOTOR)

# 3) Vertical T8 Leadscrew (150 mm) & Coupler
z_coupler_cyl = Part.makeCylinder(9.5, 20.0, Base.Vector(0.0, -52.0, FOOT_H + 232.0), Base.Vector(0.0, 0.0, 1.0))
add_part(doc, grp_motion, "Z_Axis_Flexible_Coupler", z_coupler_cyl, CLR_SPINDLE)

z_leadscrew_cyl = Part.makeCylinder(4.0, 130.0, Base.Vector(0.0, -52.0, FOOT_H + 105.0), Base.Vector(0.0, 0.0, 1.0))
add_part(doc, grp_motion, "Z_Axis_T8_Leadscrew_130mm", z_leadscrew_cyl, CLR_LEADSCREW)

# 4) Z-Plunge Plate (75 mm wide, 90 mm tall, 8 mm thick) carrying the spindle collar
z_plunge_plate = Part.makeBox(75.0, 8.0, 90.0, Base.Vector(-37.5, -52.0, FOOT_H + 115.0))
add_part(doc, grp_motion, "Z_Plunge_Plate", z_plunge_plate, CLR_CARRIAGE)


# =============================================================================
# 5. SPINDLE & SPOILBOARD WORKTABLE
# =============================================================================
# 1) Spindle Clamp Collar (Safety Orange, 70 x 70 x 30 mm clamp block with 52 mm bore)
collar_box = Part.makeBox(70.0, 70.0, 30.0, Base.Vector(-35.0, -112.0, FOOT_H + 130.0))
collar_bore = Part.makeCylinder(26.0, 32.0, Base.Vector(0.0, -77.0, FOOT_H + 129.0), Base.Vector(0.0, 0.0, 1.0))
clamp_collar = collar_box.cut(collar_bore)
add_part(doc, grp_spindle, "Spindle_Mount_Clamp_Collar_52mm", clamp_collar, CLR_COLLAR)

# 2) 500W High-Speed Brushless ER11 Milling Spindle (52 mm diameter, 180 mm body)
spindle_body = Part.makeCylinder(26.0, 175.0, Base.Vector(0.0, -77.0, FOOT_H + 70.0), Base.Vector(0.0, 0.0, 1.0))
spindle_collet = Part.makeCylinder(10.0, 25.0, Base.Vector(0.0, -77.0, FOOT_H + 45.0), Base.Vector(0.0, 0.0, 1.0))
spindle_endmill = Part.makeCylinder(1.58, 20.0, Base.Vector(0.0, -77.0, FOOT_H + 25.0), Base.Vector(0.0, 0.0, 1.0))
spindle_full = spindle_body.fuse(spindle_collet).fuse(spindle_endmill)
add_part(doc, grp_spindle, "ER11_500W_Brushless_Milling_Spindle", spindle_full, CLR_SPINDLE)

# 3) Spoilboard Worktable Surface (264 x 240 x 12 mm):
# Mounted on top of the Y-carriage plate at Z = FOOT_H + 62..74 mm (Z = 137..149 mm)
# Spindle centerline is at Y = -77 mm; table is centered directly under spindle motion!
worktable = Part.makeBox(264.0, 240.0, 12.0, Base.Vector(-132.0, -197.0, FOOT_H + 62.0))
add_part(doc, grp_spindle, "Spoilboard_Worktable_Surface", worktable, CLR_TABLE)


# =============================================================================
# 6. TRANSPARENT PREDICTED BUILD VOLUME BOX
# =============================================================================
# Target: 10.0" (X = 254.0 mm) x 9.0" (Y = 228.6 mm) x 3.0" (Z = 76.2 mm)
# Located right on the spoilboard worktable surface (Z = FOOT_H + 74.0 mm to FOOT_H + 150.2 mm)
# Centered directly under the milling spindle nose:
# X = [-127.0, +127.0 mm]
# Y = [-77.0 - 114.3, -77.0 + 114.3 mm] = [-191.3, +37.3 mm]
# Z = [FOOT_H + 74.0, FOOT_H + 74.0 + 76.2 mm] = [149.0, 225.2 mm]
IN_10 = 254.0
IN_9  = 228.6
IN_3  = 76.2
vol_box = Part.makeBox(IN_10, IN_9, IN_3, Base.Vector(-IN_10/2.0, -77.0 - IN_9/2.0, FOOT_H + 74.0))
add_part(doc, grp_vol, "Predicted_Build_Volume_10x9x3in",
         vol_box, CLR_BUILDVOL, transparency=65, line_rgb=(0.0, 1.0, 0.85), line_width=3.0)

doc.recompute()

view = Gui.ActiveDocument.ActiveView
view.setAnimationEnabled(False)

render_configs = [
    ("iso",       "viewIsometric", 1600, 1200),
    ("front",     "viewFront",     1600, 1200),
    ("right",     "viewRight",     1600, 1200),
    ("top",       "viewTop",       1600, 1200),
]

for vname, vfn, w, h in render_configs:
    getattr(view, vfn)()
    view.fitAll()
    Gui.updateGui()
    view.saveImage(os.path.join(RENDER_DIR, f"opt1_full_{{vname}}.png"), w, h, "Current")

# Undercarriage Closeup Render (Axonometric underside view)
view.viewBottom()
view.fitAll()
Gui.updateGui()
view.saveImage(os.path.join(RENDER_DIR, "opt1_undercarriage_bottom.png"), 1600, 1200, "Current")

fcstd_path = os.path.join(CAD_DIR, "Ender3_Option1_Full_CNC.FCStd")
doc.saveAs(fcstd_path)
print("SAVED_OPTION1_CAD:" + fcstd_path)
"""

def main():
    fc = FreeCADConnection(host="127.0.0.1", port=9875)
    res = fc.execute_code(FREECAD_CODE, timeout=120)
    print(res)

if __name__ == "__main__":
    main()
