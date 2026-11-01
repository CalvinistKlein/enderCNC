#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Option 1: Fixed-Bridge Mill — Hybrid Concrete-Filled Plastic Shell Foundation

Design Updates:
1. Removed all donor sheet metal enclosure parts.
2. Z-Axis uses the stock Ender 3 T8 Leadscrew (370 mm / trimmed to fit) with top synchronous belt.
3. Permanent Stay-in-Place 3D-Printed Plastic Shells filled with Concrete:
   - Ground-contact left and right massive foundation sills (Z = 0 to 115 mm).
   - Precision alignment sockets for:
     * Vertical 4040 columns (embedded 60 mm into concrete pockets).
     * Twin 2040 Y-bed ways.
     * Front 2020x345 mm and Rear 2020x330 mm base ties.
   - Internal concrete pour cavities with top funnel ports.
   - Ground-touching base with workbench mounting bolt lugs.
   - Protected central undercarriage electronics bay between the concrete sills.
4. Visualizes both the 3D-printed plastic shell (Safety Orange) and the internal dense concrete core (Cast Stone Grey).
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

doc = App.newDocument("Ender3_Concrete_Hybrid_CNC")

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

# Load Donor Hardware (Steppers, Leadscrews, PSU):
def load_step_norm(fname):
    p = os.path.join(STP_DIR, fname)
    if os.path.exists(p):
        s = Part.Shape()
        s.read(p)
        return norm_origin(s)
    return None

psu_shape     = load_step_norm("24V15A power supply.step")
motor_42_34   = load_step_norm("42-34 motor.step")
z_rod_t8      = load_step_norm("Z threaded rod.step")
y_plate_donor = load_step_norm("Y plate.step")

# Color Palette:
CLR_4040     = (0.22, 0.26, 0.32)   # Extrusion Charcoal-Slate
CLR_2040     = (0.18, 0.52, 0.82)   # Extrusion Steel-Blue
CLR_2020     = (0.90, 0.62, 0.14)   # Extrusion Amber-Gold
CLR_SHELL    = (0.95, 0.42, 0.10)   # 3D-Printed Plastic Formwork Shell (Safety Orange)
CLR_CONCRETE = (0.68, 0.70, 0.72)   # Dense Cast Concrete / Non-Shrink Grout (Stone Grey)
CLR_PSU      = (0.80, 0.82, 0.85)   # Brushed Aluminum PSU
CLR_BOARD    = (0.15, 0.45, 0.25)   # Driver Board PCB Green
CLR_MOTOR    = (0.18, 0.18, 0.20)   # Stepper Black
CLR_LEADSCREW= (0.85, 0.85, 0.90)   # T8 Polished Leadscrew
CLR_CARRIAGE = (0.28, 0.32, 0.38)   # Saddle Carriage
CLR_SPINDLE  = (0.75, 0.77, 0.80)   # 52mm Spindle Body
CLR_TABLE    = (0.75, 0.72, 0.65)   # Spoilboard Worktable
CLR_BUILDVOL = (0.00, 0.90, 0.76)   # Transparent Cyan-Emerald Build Volume
CLR_BELT     = (0.10, 0.10, 0.10)   # GT2 Timing Belt
CLR_PULLEY   = (0.70, 0.72, 0.75)   # Pulley

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
grp_shell   = doc.addObject("App::DocumentObjectGroup", "01_Printed_Plastic_Concrete_Shells")
grp_core    = doc.addObject("App::DocumentObjectGroup", "02_Cast_Concrete_Infill_Cores")
grp_base    = doc.addObject("App::DocumentObjectGroup", "03_Extrusions_Frame")
grp_elec    = doc.addObject("App::DocumentObjectGroup", "04_Electronics_Undercarriage_Tray")
grp_y_motion= doc.addObject("App::DocumentObjectGroup", "05_Y_Axis_Motion")
grp_x_motion= doc.addObject("App::DocumentObjectGroup", "06_X_Axis_Motion")
grp_toolhead= doc.addObject("App::DocumentObjectGroup", "07_Counterbalanced_Toolhead")
grp_vol     = doc.addObject("App::DocumentObjectGroup", "08_Build_Volume")

# =============================================================================
# 1 & 2. 3D-PRINTED PLASTIC SHELLS & CAST CONCRETE CORES (Touching Ground: Z = 0..115 mm)
# =============================================================================
# Two heavy foundation sills (Left & Right) that touch the workbench directly.
# Each sill has:
#   - Outer Main Body: X = 115..175 mm (60 mm wide), Y = -210..+210 mm (420 mm long), Z = 0..115 mm (touches ground!)
#   - Inward Saddle Shelf: X = 75..115 mm under the twin 2040 Y-ways (Z = 0..95 mm)
#   - Column Socket: 40.5 x 40.5 mm vertical pocket at X = 145, Y = 20, Z = 55..115 mm (column embedded 60 mm!)
#   - Front Crossbar Pocket: 20.5 x 20.5 mm transverse pocket at Y = -190 mm, Z = 75..95 mm
#   - Rear Crossbar Pocket: 20.5 x 20.5 mm transverse pocket at Y = +190 mm, Z = 75..95 mm
#   - 4x Pour Ports on top (funnel spouts for concrete slurry)
#   - 4x Ground Mount Flanges with bolt slots for securing to workbench.

def create_concrete_sill(side_sign):
    # side_sign is -1.0 for Left, +1.0 for Right
    # Shell Outer:
    cx_outer = side_sign * 145.0
    cx_inner = side_sign * 95.0
    
    # 1) Main Column & Outer Beam Block (Z = 0 .. 115 mm)
    b_main = Part.makeBox(60.0, 420.0, 115.0, 
                          Base.Vector(cx_outer - 30.0, -210.0, 0.0))
    
    # 2) Inward Y-Rail Support Shelf (Z = 0 .. 95 mm)
    b_shelf = Part.makeBox(40.0, 400.0, 95.0,
                           Base.Vector(min(cx_outer - 30.0, cx_inner - 20.0), -200.0, 0.0))
    
    # 3) Bench Bolt Lugs (4x on outer side, touching ground at Z = 0..15 mm)
    lugs = []
    for ly in [-180.0, -60.0, 60.0, 180.0]:
        lx = cx_outer + side_sign * 30.0
        lug = Part.makeBox(22.0, 36.0, 15.0, 
                            Base.Vector(lx - (0.0 if side_sign > 0 else 22.0), ly - 18.0, 0.0))
        hole = Part.makeCylinder(4.5, 18.0, Base.Vector(lx + side_sign * 11.0, ly, -1.0), Base.Vector(0,0,1))
        lug = lug.cut(hole)
        lugs.append(lug)
        
    shell_solid = b_main.fuse(b_shelf)
    for lug in lugs:
        shell_solid = shell_solid.fuse(lug)
        
    # Extrusion Sockets to cut out:
    # A) Vertical 4040 Column Socket (40.8 x 40.8 mm, Z = 55..116 mm)
    col_socket = Part.makeBox(40.8, 40.8, 62.0,
                              Base.Vector(cx_outer - 20.4, 20.0 - 20.4, 55.0))
    # B) Front 2020 Tie Socket (20.5 x 20.5 mm, Z = 75..96 mm, Y = -190)
    front_socket = Part.makeBox(65.0, 20.8, 20.8,
                                Base.Vector(min(cx_outer - 32.0, cx_inner - 22.0), -190.0 - 10.4, 75.0))
    # C) Rear 2020 Tie Socket (20.5 x 20.5 mm, Z = 75..96 mm, Y = +190)
    rear_socket = Part.makeBox(65.0, 20.8, 20.8,
                               Base.Vector(min(cx_outer - 32.0, cx_inner - 22.0), 190.0 - 10.4, 75.0))
    # D) Top 2040 Y-Rail Seat (40.5 x 402 mm, Z = 95..116 mm)
    y_rail_seat = Part.makeBox(40.8, 404.0, 22.0,
                               Base.Vector(cx_inner - 20.4, -202.0, 95.0))
    
    # E) Concrete Pour Ports (3 conical/cylindrical funnels on top of outer beam)
    funnels = []
    for py in [-120.0, 0.0, 120.0]:
        fn = Part.makeCylinder(16.0, 30.0, Base.Vector(cx_outer, py, 90.0), Base.Vector(0,0,1))
        funnels.append(fn)

    # Internal Concrete Core Cavity (Shell wall thickness = 4.5 mm):
    core_outer = Part.makeBox(51.0, 411.0, 106.0,
                              Base.Vector(cx_outer - 25.5, -205.5, 4.5))
    core_shelf = Part.makeBox(31.0, 391.0, 86.0,
                              Base.Vector(min(cx_outer - 25.5, cx_inner - 15.5), -195.5, 4.5))
    core_full = core_outer.fuse(core_shelf)
    # Subtract extrusion sockets from core too so concrete forms right around the extrusions!
    core_full = core_full.cut(col_socket).cut(front_socket).cut(rear_socket).cut(y_rail_seat)
    
    # Plastic Shell is the hollow form:
    shell_final = shell_solid.cut(col_socket).cut(front_socket).cut(rear_socket).cut(y_rail_seat)
    # Subtract inner hollow from shell so shell has hollow interior:
    shell_hollow = shell_final.cut(core_full)
    for fn in funnels:
        shell_hollow = shell_hollow.cut(fn)
        
    return shell_hollow, core_full

# Build Left & Right Foundation Sills:
shell_L, core_L = create_concrete_sill(-1.0)
shell_R, core_R = create_concrete_sill(1.0)

# Add to Doc (Shell rendered in Safety Orange PETG, Core rendered in Cast Stone Grey):
add_part(doc, grp_shell, "Foundation_Shell_Left_PETG",   shell_L, CLR_SHELL, transparency=25)
add_part(doc, grp_shell, "Foundation_Shell_Right_PETG",  shell_R, CLR_SHELL, transparency=25)

add_part(doc, grp_core,  "Cast_Concrete_Core_Left",      core_L,  CLR_CONCRETE)
add_part(doc, grp_core,  "Cast_Concrete_Core_Right",     core_R,  CLR_CONCRETE)


# =============================================================================
# 3. 8 UNCUT EXTRUSIONS (Seated in Concrete Sockets)
# =============================================================================
# 1) Front Base Tie (2020 x 345 mm): Seated in front transverse sockets at Y = -190 mm, Z = 75..95 mm
add_part(doc, grp_base, "Base_Front_Tie_2020x345",
         place(ext_2020_345, 0.0, -190.0, 75.0), CLR_2020)

# 2) Rear Base Tie (2020 x 330 mm): Seated in rear transverse sockets at Y = +190 mm, Z = 75..95 mm
add_part(doc, grp_base, "Base_Rear_Tie_2020x330",
         place(ext_2020_330, 0.0,  190.0, 75.0), CLR_2020)

# 3 & 4) Twin Y-Axis Bed Ways (2x 2040 x 400 mm):
# Seated directly on top of the concrete shelf beds at X = +/-95 mm, Z = 95..115 mm
add_part(doc, grp_base, "Y_Bed_Way_Left_2040x400",
         place(ext_2040_400_A, -95.0, 0.0, 95.0), CLR_2040)
add_part(doc, grp_base, "Y_Bed_Way_Right_2040x400",
         place(ext_2040_400_B,  95.0, 0.0, 95.0), CLR_2040)

# 5 & 6) Fixed Portal Columns (2x 4040 x 290 mm):
# Bottom 60 mm embedded directly into the concrete column socket (Z = 55 .. 345 mm)!
add_part(doc, grp_base, "Portal_Column_Left_4040x290",
         place(ext_4040_290_A, -145.0, 20.0, 55.0), CLR_4040)
add_part(doc, grp_base, "Portal_Column_Right_4040x290",
         place(ext_4040_290_B,  145.0, 20.0, 55.0), CLR_4040)

# 7) Inner X-Bridge Girder (1x 4040 x 250 mm):
# Bolted between columns at Z = 250..290 mm (Y = 20 mm)
add_part(doc, grp_base, "X_Bridge_Inner_Girder_4040x250",
         place(ext_4040_250, 0.0, 20.0, 250.0), CLR_4040)

# 8) Front X-Bridge Way (1x 2040 x 330 mm):
# Spans full 330 mm across front faces of columns at Z = 250..290 mm (Y = -10 mm)
add_part(doc, grp_base, "X_Bridge_Front_Way_2040x330",
         place(ext_2040_330_horiz_x, 0.0, -10.0, 250.0), CLR_2040)


# =============================================================================
# 4. ELECTRONICS UNDERCARRIAGE TRAY (No Sheet Metal!)
# =============================================================================
# 3D-printed lightweight electronics slide tray mounted between the two concrete beams.
# Ground clearance: Z = 12 .. 72 mm, sheltered directly under the bed and worktable.
# 1) Printed Electronics Tray Base (230 x 180 x 4 mm) with mounting bosses
elec_tray = Part.makeBox(220.0, 180.0, 4.0, Base.Vector(-110.0, -90.0, 10.0))
# Cable pass-through slots
slot1 = Part.makeBox(30.0, 10.0, 10.0, Base.Vector(-80.0, -85.0, 5.0))
slot2 = Part.makeBox(30.0, 10.0, 10.0, Base.Vector( 50.0, -85.0, 5.0))
elec_tray = elec_tray.cut(slot1).cut(slot2)
add_part(doc, grp_elec, "3DPrinted_Electronics_Slide_Tray", elec_tray, CLR_SHELL)

# 2) 24V 15A Power Supply (mounted on left side of tray at X = -65 mm)
if psu_shape:
    s_psu = psu_shape.copy()
    s_psu.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), 90)
    s_psu = norm_origin(s_psu)
    add_part(doc, grp_elec, "Ender3_24V_15A_PowerSupply",
             place(s_psu, -65.0, 0.0, 14.0), CLR_PSU)
else:
    psu_box = Part.makeBox(113.0, 215.0, 50.0, Base.Vector(-121.5, -107.5, 14.0))
    add_part(doc, grp_elec, "Ender3_24V_15A_PowerSupply", psu_box, CLR_PSU)

# 3) Driver Boards (32-bit silent TMC controller board mounted on standoffs at X = +55 mm, Z = 18 mm)
board_pcb = Part.makeBox(105.0, 110.0, 2.0, Base.Vector(10.0, -55.0, 18.0))
add_part(doc, grp_elec, "Mainboard_Controller_PCB", board_pcb, CLR_BOARD)

# TMC Silent Stepper Driver Heat Sinks (4x miniature aluminum heat sinks)
for idx, hy in enumerate([-40.0, -15.0, 10.0, 35.0]):
    hs = Part.makeBox(14.0, 14.0, 10.0, Base.Vector(45.0, hy, 20.0))
    add_part(doc, grp_elec, f"TMC_Driver_Heatsink_{{idx+1}}", hs, (0.25, 0.75, 0.85))


# =============================================================================
# 5. Y-AXIS MOTION SYSTEM (Twin Linear Rails + Bed + Leadscrew/Belt)
# =============================================================================
y_rail_L = Part.makeBox(12.0, 396.0, 8.0, Base.Vector(-95.0 - 6.0, -198.0, 115.0))
y_rail_R = Part.makeBox(12.0, 396.0, 8.0, Base.Vector( 95.0 - 6.0, -198.0, 115.0))
add_part(doc, grp_y_motion, "Y_Linear_Guide_Rail_Left",  y_rail_L, CLR_LEADSCREW)
add_part(doc, grp_y_motion, "Y_Linear_Guide_Rail_Right", y_rail_R, CLR_LEADSCREW)

for side_x in [-95.0, 95.0]:
    for block_y in [-60.0, 60.0]:
        bk = Part.makeBox(27.0, 45.0, 10.0, Base.Vector(side_x - 13.5, block_y - 22.5, 123.0))
        lbl = "L" if side_x < 0 else "R"
        pos = "F" if block_y < 0 else "R"
        add_part(doc, grp_y_motion, f"Y_BearingBlock_{{lbl}}_{{pos}}", bk, CLR_CARRIAGE)

# Rear Y-Axis Stepper Motor (at Y = +210 mm, Z = 85 mm)
if motor_42_34:
    s_ymot = motor_42_34.copy()
    s_ymot.rotate(Base.Vector(0,0,0), Base.Vector(1,0,0), 90)
    s_ymot = norm_origin(s_ymot)
    add_part(doc, grp_y_motion, "Y_Axis_NEMA17_Stepper",
             place(s_ymot, 0.0, 210.0, 85.0), CLR_MOTOR)
else:
    ymot_box = Part.makeBox(42.0, 34.0, 42.0, Base.Vector(-21.0, 205.0, 85.0))
    add_part(doc, grp_y_motion, "Y_Axis_NEMA17_Stepper", ymot_box, CLR_MOTOR)

y_coupler = Part.makeCylinder(9.5, 25.0, Base.Vector(0.0, 195.0, 105.0), Base.Vector(0.0, -1.0, 0.0))
add_part(doc, grp_y_motion, "Y_Flexible_Coupler", y_coupler, CLR_PULLEY)

y_leadscrew = Part.makeCylinder(4.0, 370.0, Base.Vector(0.0, 170.0, 105.0), Base.Vector(0.0, -1.0, 0.0))
add_part(doc, grp_y_motion, "Y_Drive_Leadscrew_370mm", y_leadscrew, CLR_LEADSCREW)

y_nut_block = Part.makeBox(30.0, 30.0, 24.0, Base.Vector(-15.0, -15.0, 109.0))
add_part(doc, grp_y_motion, "Y_AntiBacklash_Nut_Block", y_nut_block, (0.85, 0.65, 0.20))

# Bed Carriage Plate & Spoilboard Worktable:
if y_plate_donor:
    add_part(doc, grp_y_motion, "Y_Bed_Carriage_Plate",
             place(y_plate_donor, 0.0, 0.0, 133.0), CLR_CARRIAGE)
else:
    bed_plate = Part.makeBox(190.0, 190.0, 4.0, Base.Vector(-95.0, -95.0, 133.0))
    add_part(doc, grp_y_motion, "Y_Bed_Carriage_Plate", bed_plate, CLR_CARRIAGE)

worktable = Part.makeBox(264.0, 240.0, 12.0, Base.Vector(-132.0, -197.0, 137.0))
add_part(doc, grp_y_motion, "Spoilboard_Worktable_Surface", worktable, CLR_TABLE)


# =============================================================================
# 6. X-AXIS MOTION SYSTEM (Bridge Way & Drive)
# =============================================================================
x_rail = Part.makeBox(330.0, 8.0, 12.0, Base.Vector(-165.0, -28.0, 269.0))
add_part(doc, grp_x_motion, "X_Linear_Guide_Rail_330mm", x_rail, CLR_LEADSCREW)

if motor_42_34:
    s_xmot = motor_42_34.copy()
    s_xmot.rotate(Base.Vector(0,0,0), Base.Vector(0,1,0), 90)
    s_xmot = norm_origin(s_xmot)
    add_part(doc, grp_x_motion, "X_Axis_NEMA17_Stepper",
             place(s_xmot, -185.0, -10.0, 255.0), CLR_MOTOR)
else:
    xmot_box = Part.makeBox(34.0, 42.0, 42.0, Base.Vector(-205.0, -31.0, 255.0))
    add_part(doc, grp_x_motion, "X_Axis_NEMA17_Stepper", xmot_box, CLR_MOTOR)

x_idler = Part.makeCylinder(9.0, 20.0, Base.Vector(180.0, -10.0, 265.0), Base.Vector(0.0, 0.0, 1.0))
add_part(doc, grp_x_motion, "X_Belt_Tensioner_Pulley", x_idler, CLR_PULLEY)

x_belt = Part.makeBox(360.0, 2.0, 6.0, Base.Vector(-180.0, -31.0, 272.0))
add_part(doc, grp_x_motion, "X_GT2_Steel_Drive_Belt", x_belt, CLR_BELT)


# =============================================================================
# 7. COUNTERBALANCED ROUTER HEAD WITH T8 LEADSCREW FOR Z
# =============================================================================
# Split-Weight:
# - FRONT: 52 mm Spindle / Router (Y = -80 mm) + Orange Clamp Collar + Z-Plunge Plate
# - MIDDLE: Compound X-Bridge (Y = -20..+40 mm) + X Linear Rail (Y = -28 mm)
# - BACK: Z-Axis NEMA 17 Stepper (Y = +60 mm) + Top GT2 Timing Belt to Leadscrew
# - Z-AXIS DRIVE: Stock Ender 3 T8 Leadscrew utilized for vertical plunge!

# A. Saddle Carriage Body:
saddle_top = Part.makeBox(95.0, 85.0, 8.0, Base.Vector(-47.5, -36.0, 296.0))
saddle_front = Part.makeBox(95.0, 8.0, 105.0, Base.Vector(-47.5, -36.0, 195.0))
saddle_rear = Part.makeBox(95.0, 8.0, 85.0, Base.Vector(-47.5, 41.0, 215.0))
saddle_full = saddle_top.fuse(saddle_front).fuse(saddle_rear)
add_part(doc, grp_toolhead, "Counterbalanced_Saddle_Carriage", saddle_full, CLR_CARRIAGE)

# B. BACK: Z Stepper Motor
if motor_42_34:
    add_part(doc, grp_toolhead, "Z_Stepper_Motor_REAR_BALANCER",
             place(motor_42_34, 0.0, 60.0, 225.0), CLR_MOTOR)
else:
    z_mot_box = Part.makeBox(42.0, 42.0, 34.0, Base.Vector(-21.0, 39.0, 225.0))
    add_part(doc, grp_toolhead, "Z_Stepper_Motor_REAR_BALANCER", z_mot_box, CLR_MOTOR)

rear_pulley = Part.makeCylinder(10.0, 12.0, Base.Vector(0.0, 60.0, 304.0), Base.Vector(0.0, 0.0, 1.0))
add_part(doc, grp_toolhead, "Z_Rear_Drive_Pulley", rear_pulley, CLR_PULLEY)

# C. OVERHEAD: GT2 Sync Belt connecting Rear Stepper to Front Leadscrew
top_belt_L = Part.makeBox(2.0, 108.0, 6.0, Base.Vector(-9.0, -48.0, 307.0))
top_belt_R = Part.makeBox(2.0, 108.0, 6.0, Base.Vector( 7.0, -48.0, 307.0))
add_part(doc, grp_toolhead, "Z_Overhead_Sync_Belt_Left",  top_belt_L, CLR_BELT)
add_part(doc, grp_toolhead, "Z_Overhead_Sync_Belt_Right", top_belt_R, CLR_BELT)

front_pulley = Part.makeCylinder(12.0, 12.0, Base.Vector(0.0, -48.0, 304.0), Base.Vector(0.0, 0.0, 1.0))
add_part(doc, grp_toolhead, "Z_Front_Leadscrew_Driven_Pulley", front_pulley, CLR_PULLEY)

# D. FRONT: Vertical Slide & T8 Leadscrew for Z
z_rail_L = Part.makeBox(8.0, 6.0, 120.0, Base.Vector(-28.0 - 4.0, -42.0, 195.0))
z_rail_R = Part.makeBox(8.0, 6.0, 120.0, Base.Vector( 28.0 - 4.0, -42.0, 195.0))
add_part(doc, grp_toolhead, "Z_Vertical_Guide_Rail_Left",  z_rail_L, CLR_LEADSCREW)
add_part(doc, grp_toolhead, "Z_Vertical_Guide_Rail_Right", z_rail_R, CLR_LEADSCREW)

# The T8 Leadscrew utilized for Z:
z_leadscrew_t8 = Part.makeCylinder(4.0, 150.0, Base.Vector(0.0, -48.0, 175.0), Base.Vector(0.0, 0.0, 1.0))
add_part(doc, grp_toolhead, "Z_T8_Leadscrew_Vertical_Drive", z_leadscrew_t8, CLR_LEADSCREW)

# Z Plunge Slide Plate & Spindle Clamp
z_plunge_plate = Part.makeBox(75.0, 8.0, 85.0, Base.Vector(-37.5, -54.0, 195.0))
add_part(doc, grp_toolhead, "Z_Plunge_Slide_Plate", z_plunge_plate, CLR_CARRIAGE)

collar_box = Part.makeBox(70.0, 64.0, 30.0, Base.Vector(-35.0, -112.0, 205.0))
collar_bore = Part.makeCylinder(26.0, 32.0, Base.Vector(0.0, -80.0, 204.0), Base.Vector(0.0, 0.0, 1.0))
clamp_collar = collar_box.cut(collar_bore)
add_part(doc, grp_toolhead, "Spindle_Mount_Clamp_Collar_52mm", clamp_collar, CLR_SHELL)

spindle_body = Part.makeCylinder(26.0, 175.0, Base.Vector(0.0, -80.0, 145.0), Base.Vector(0.0, 0.0, 1.0))
spindle_collet = Part.makeCylinder(10.0, 25.0, Base.Vector(0.0, -80.0, 120.0), Base.Vector(0.0, 0.0, 1.0))
spindle_endmill = Part.makeCylinder(1.58, 20.0, Base.Vector(0.0, -80.0, 100.0), Base.Vector(0.0, 0.0, 1.0))
spindle_full = spindle_body.fuse(spindle_collet).fuse(spindle_endmill)
add_part(doc, grp_toolhead, "ER11_500W_Brushless_Milling_Spindle", spindle_full, CLR_SPINDLE)


# =============================================================================
# 8. TRANSPARENT PREDICTED BUILD VOLUME BOX ($10" x 9" x 3"$)
# =============================================================================
IN_10 = 254.0
IN_9  = 228.6
IN_3  = 76.2
vol_box = Part.makeBox(IN_10, IN_9, IN_3, Base.Vector(-IN_10/2.0, -80.0 - IN_9/2.0, 149.0))
add_part(doc, grp_vol, "Predicted_Build_Volume_10x9x3in",
         vol_box, CLR_BUILDVOL, transparency=65, line_rgb=(0.0, 1.0, 0.85), line_width=3.0)

doc.recompute()

view = Gui.ActiveDocument.ActiveView
view.setAnimationEnabled(False)

# Renders:
# 1. Full Isometric:
view.viewIsometric()
view.fitAll()
Gui.updateGui()
view.saveImage(os.path.join(RENDER_DIR, "hybrid_concrete_iso.png"), 1600, 1200, "Current")

# 2. Front Elevation (Showing ground-touching concrete sills & extrusion seating):
view.viewFront()
view.fitAll()
Gui.updateGui()
view.saveImage(os.path.join(RENDER_DIR, "hybrid_concrete_front.png"), 1600, 1200, "Current")

# 3. Right Side View (Showing 420mm long concrete foundation beam & bench mount lugs):
view.viewRight()
view.fitAll()
Gui.updateGui()
view.saveImage(os.path.join(RENDER_DIR, "hybrid_concrete_right.png"), 1600, 1200, "Current")

# 4. Top View (Showing pour ports, sockets, and undercarriage electronics):
view.viewTop()
view.fitAll()
Gui.updateGui()
view.saveImage(os.path.join(RENDER_DIR, "hybrid_concrete_top.png"), 1600, 1200, "Current")

# 5. Close-up on Concrete Foundation Sill & Extrusion Sockets:
view.viewIsometric()
view.fitAll()
view.zoomIn()
Gui.updateGui()
view.saveImage(os.path.join(RENDER_DIR, "hybrid_concrete_closeup_sill.png"), 1600, 1200, "Current")

fcstd_path = os.path.join(CAD_DIR, "Ender3_Concrete_Hybrid_CNC.FCStd")
doc.saveAs(fcstd_path)
print("SAVED_HYBRID_CONCRETE_CAD:" + fcstd_path)
"""

def main():
    fc = FreeCADConnection(host="127.0.0.1", port=9875)
    res = fc.execute_code(FREECAD_CODE, timeout=120)
    print(res)

if __name__ == "__main__":
    main()
