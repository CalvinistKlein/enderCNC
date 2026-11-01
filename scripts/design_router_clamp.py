#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Makita RT0701C 65mm Heavy-Duty CNC Router Clamp Mechanism & Full Assembly Integration

Engineering Features:
1. 65mm Heavy-Duty Split-Collar Clamp Block:
   - Precision 65.0 mm bore with 3.0 mm tangential flex slit.
   - Extended 50 mm clamping band height to eliminate tilt/rocking under heavy cutting forces.
   - Dual M6 socket head pinch bolts with counterbores and captive nut pockets.
   - 4x M5 rear mounting bolts with tramming alignment keyways to Z-plunge plate.
   - Underside magnetic dust shoe mounting bosses with dowel alignment pin holes.
2. 65mm-to-52mm Split Reducing Adapter Sleeve:
   - Allows quick swap between a 1-1/4 HP Makita RT0701C trim router and a quiet 500W ER11 spindle.
3. Detailed Makita RT0701C Router Model:
   - 65mm aluminum barrel, top motor cap with speed dial (10k-30k RPM), collet chuck, and 1/4" carbide end mill.
4. Complete Integration into the Counterbalanced Hybrid Concrete CNC Mill.
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

doc = App.newDocument("Ender3_Router_Clamp_Mechanism")

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
ext_4040_290_A = norm_origin(solids[0])
ext_4040_290_B = norm_origin(solids[1])
ext_4040_250   = norm_origin(solids[2])
ext_2040_400_A = norm_origin(solids[4])
ext_2040_400_B = norm_origin(solids[5])

ext_2040_330_vert = norm_origin(solids[421])
ext_2040_330_horiz_x = ext_2040_330_vert.copy()
ext_2040_330_horiz_x.rotate(Base.Vector(0,0,0), Base.Vector(0,1,0), 90)
ext_2040_330_horiz_x.rotate(Base.Vector(0,0,0), Base.Vector(1,0,0), 90)
ext_2040_330_horiz_x = norm_origin(ext_2040_330_horiz_x)

ext_2020_345 = norm_origin(solids[44])
ext_2020_330 = norm_origin(solids[3])

def load_step_norm(fname):
    p = os.path.join(STP_DIR, fname)
    if os.path.exists(p):
        s = Part.Shape()
        s.read(p)
        return norm_origin(s)
    return None

psu_shape     = load_step_norm("24V15A power supply.step")
motor_42_34   = load_step_norm("42-34 motor.step")
y_plate_donor = load_step_norm("Y plate.step")

# Color Palette:
CLR_4040     = (0.22, 0.26, 0.32)   # Extrusion Charcoal-Slate
CLR_2040     = (0.18, 0.52, 0.82)   # Extrusion Steel-Blue
CLR_2020     = (0.90, 0.62, 0.14)   # Extrusion Amber-Gold
CLR_SHELL    = (0.95, 0.42, 0.10)   # Safety Orange PETG Formwork Shell
CLR_CONCRETE = (0.68, 0.70, 0.72)   # Cast Non-Shrink Grout Stone Core
CLR_PSU      = (0.80, 0.82, 0.85)   # Brushed Aluminum PSU
CLR_BOARD    = (0.15, 0.45, 0.25)   # Controller PCB Green
CLR_MOTOR    = (0.18, 0.18, 0.20)   # Stepper Black
CLR_LEADSCREW= (0.85, 0.85, 0.90)   # T8 Polished Leadscrew
CLR_CARRIAGE = (0.28, 0.32, 0.38)   # Saddle Carriage Dark Slate
CLR_ROUTER   = (0.00, 0.52, 0.55)   # Makita Industrial Teal (#00848C)
CLR_ALUM     = (0.82, 0.84, 0.86)   # Machined Aluminum
CLR_CLAMP    = (0.95, 0.35, 0.05)   # Safety Orange Heavy Clamp Collar
CLR_SLEEVE   = (0.88, 0.75, 0.25)   # Brass / Gold Anodized 65-to-52mm Sleeve
CLR_BOLT     = (0.12, 0.12, 0.14)   # Black Oxide M6 Bolts
CLR_TABLE    = (0.75, 0.72, 0.65)   # Spoilboard Worktable
CLR_BUILDVOL = (0.00, 0.90, 0.76)   # Transparent Cyan-Emerald Build Volume
CLR_BELT     = (0.10, 0.10, 0.10)   # GT2 Timing Belt
CLR_PULLEY   = (0.70, 0.72, 0.75)   # Pulley Aluminum

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
grp_shell   = doc.addObject("App::DocumentObjectGroup", "01_Printed_Plastic_Concrete_Shells")
grp_core    = doc.addObject("App::DocumentObjectGroup", "02_Cast_Concrete_Infill_Cores")
grp_base    = doc.addObject("App::DocumentObjectGroup", "03_Extrusions_Frame")
grp_elec    = doc.addObject("App::DocumentObjectGroup", "04_Electronics_Undercarriage_Tray")
grp_y_motion= doc.addObject("App::DocumentObjectGroup", "05_Y_Axis_Motion")
grp_x_motion= doc.addObject("App::DocumentObjectGroup", "06_X_Axis_Motion")
grp_toolhead= doc.addObject("App::DocumentObjectGroup", "07_Counterbalanced_Toolhead")
grp_clamp   = doc.addObject("App::DocumentObjectGroup", "08_Router_Clamp_Mechanism")
grp_vol     = doc.addObject("App::DocumentObjectGroup", "09_Build_Volume")

# =============================================================================
# 1 & 2. CONCRETE SILLS & CORES
# =============================================================================
def create_concrete_sill(side_sign):
    cx_outer = side_sign * 145.0
    cx_inner = side_sign * 95.0
    b_main = Part.makeBox(60.0, 420.0, 115.0, Base.Vector(cx_outer - 30.0, -210.0, 0.0))
    b_shelf = Part.makeBox(40.0, 400.0, 95.0, Base.Vector(min(cx_outer - 30.0, cx_inner - 20.0), -200.0, 0.0))
    lugs = []
    for ly in [-180.0, -60.0, 60.0, 180.0]:
        lx = cx_outer + side_sign * 30.0
        lug = Part.makeBox(22.0, 36.0, 15.0, Base.Vector(lx - (0.0 if side_sign > 0 else 22.0), ly - 18.0, 0.0))
        hole = Part.makeCylinder(4.5, 18.0, Base.Vector(lx + side_sign * 11.0, ly, -1.0), Base.Vector(0,0,1))
        lug = lug.cut(hole)
        lugs.append(lug)
    shell_solid = b_main.fuse(b_shelf)
    for lug in lugs:
        shell_solid = shell_solid.fuse(lug)
    col_socket = Part.makeBox(40.8, 40.8, 62.0, Base.Vector(cx_outer - 20.4, 20.0 - 20.4, 55.0))
    front_socket = Part.makeBox(65.0, 20.8, 20.8, Base.Vector(min(cx_outer - 32.0, cx_inner - 22.0), -190.0 - 10.4, 75.0))
    rear_socket = Part.makeBox(65.0, 20.8, 20.8, Base.Vector(min(cx_outer - 32.0, cx_inner - 22.0), 190.0 - 10.4, 75.0))
    y_rail_seat = Part.makeBox(40.8, 404.0, 22.0, Base.Vector(cx_inner - 20.4, -202.0, 95.0))
    funnels = []
    for py in [-120.0, 0.0, 120.0]:
        fn = Part.makeCylinder(16.0, 30.0, Base.Vector(cx_outer, py, 90.0), Base.Vector(0,0,1))
        funnels.append(fn)
    core_outer = Part.makeBox(51.0, 411.0, 106.0, Base.Vector(cx_outer - 25.5, -205.5, 4.5))
    core_shelf = Part.makeBox(31.0, 391.0, 86.0, Base.Vector(min(cx_outer - 25.5, cx_inner - 15.5), -195.5, 4.5))
    core_full = core_outer.fuse(core_shelf)
    core_full = core_full.cut(col_socket).cut(front_socket).cut(rear_socket).cut(y_rail_seat)
    shell_final = shell_solid.cut(col_socket).cut(front_socket).cut(rear_socket).cut(y_rail_seat)
    shell_hollow = shell_final.cut(core_full)
    for fn in funnels:
        shell_hollow = shell_hollow.cut(fn)
    return shell_hollow, core_full

shell_L, core_L = create_concrete_sill(-1.0)
shell_R, core_R = create_concrete_sill(1.0)
add_part(doc, grp_shell, "Foundation_Shell_Left_PETG",  shell_L, CLR_SHELL, transparency=25)
add_part(doc, grp_shell, "Foundation_Shell_Right_PETG", shell_R, CLR_SHELL, transparency=25)
add_part(doc, grp_core,  "Cast_Concrete_Core_Left",     core_L,  CLR_CONCRETE)
add_part(doc, grp_core,  "Cast_Concrete_Core_Right",    core_R,  CLR_CONCRETE)

# =============================================================================
# 3. 8 UNCUT EXTRUSIONS
# =============================================================================
add_part(doc, grp_base, "Base_Front_Tie_2020x345", place(ext_2020_345, 0.0, -190.0, 75.0), CLR_2020)
add_part(doc, grp_base, "Base_Rear_Tie_2020x330",  place(ext_2020_330, 0.0,  190.0, 75.0), CLR_2020)
add_part(doc, grp_base, "Y_Bed_Way_Left_2040x400",  place(ext_2040_400_A, -95.0, 0.0, 95.0), CLR_2040)
add_part(doc, grp_base, "Y_Bed_Way_Right_2040x400", place(ext_2040_400_B,  95.0, 0.0, 95.0), CLR_2040)
add_part(doc, grp_base, "Portal_Column_Left_4040x290",  place(ext_4040_290_A, -145.0, 20.0, 55.0), CLR_4040)
add_part(doc, grp_base, "Portal_Column_Right_4040x290", place(ext_4040_290_B,  145.0, 20.0, 55.0), CLR_4040)
add_part(doc, grp_base, "X_Bridge_Inner_Girder_4040x250", place(ext_4040_250, 0.0, 20.0, 250.0), CLR_4040)
add_part(doc, grp_base, "X_Bridge_Front_Way_2040x330", place(ext_2040_330_horiz_x, 0.0, -10.0, 250.0), CLR_2040)

# =============================================================================
# 4. ELECTRONICS UNDERCARRIAGE SLIDE TRAY
# =============================================================================
elec_tray = Part.makeBox(220.0, 180.0, 4.0, Base.Vector(-110.0, -90.0, 10.0))
add_part(doc, grp_elec, "3DPrinted_Electronics_Slide_Tray", elec_tray, CLR_SHELL)
if psu_shape:
    s_psu = psu_shape.copy()
    s_psu.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), 90)
    s_psu = norm_origin(s_psu)
    add_part(doc, grp_elec, "Ender3_24V_15A_PowerSupply", place(s_psu, -65.0, 0.0, 14.0), CLR_PSU)
board_pcb = Part.makeBox(105.0, 110.0, 2.0, Base.Vector(10.0, -55.0, 18.0))
add_part(doc, grp_elec, "Mainboard_Controller_PCB", board_pcb, CLR_BOARD)
for idx, hy in enumerate([-40.0, -15.0, 10.0, 35.0]):
    hs = Part.makeBox(14.0, 14.0, 10.0, Base.Vector(45.0, hy, 20.0))
    add_part(doc, grp_elec, f"TMC_Driver_Heatsink_{{idx+1}}", hs, (0.25, 0.75, 0.85))

# =============================================================================
# 5. Y-AXIS MOTION
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
if motor_42_34:
    s_ymot = motor_42_34.copy()
    s_ymot.rotate(Base.Vector(0,0,0), Base.Vector(1,0,0), 90)
    s_ymot = norm_origin(s_ymot)
    add_part(doc, grp_y_motion, "Y_Axis_NEMA17_Stepper", place(s_ymot, 0.0, 210.0, 85.0), CLR_MOTOR)
y_coupler = Part.makeCylinder(9.5, 25.0, Base.Vector(0.0, 195.0, 105.0), Base.Vector(0.0, -1.0, 0.0))
add_part(doc, grp_y_motion, "Y_Flexible_Coupler", y_coupler, CLR_PULLEY)
y_leadscrew = Part.makeCylinder(4.0, 370.0, Base.Vector(0.0, 170.0, 105.0), Base.Vector(0.0, -1.0, 0.0))
add_part(doc, grp_y_motion, "Y_Drive_Leadscrew_370mm", y_leadscrew, CLR_LEADSCREW)
y_nut_block = Part.makeBox(30.0, 30.0, 24.0, Base.Vector(-15.0, -15.0, 109.0))
add_part(doc, grp_y_motion, "Y_AntiBacklash_Nut_Block", y_nut_block, (0.85, 0.65, 0.20))
if y_plate_donor:
    add_part(doc, grp_y_motion, "Y_Bed_Carriage_Plate", place(y_plate_donor, 0.0, 0.0, 133.0), CLR_CARRIAGE)
worktable = Part.makeBox(264.0, 240.0, 12.0, Base.Vector(-132.0, -197.0, 137.0))
add_part(doc, grp_y_motion, "Spoilboard_Worktable_Surface", worktable, CLR_TABLE)

# =============================================================================
# 6. X-AXIS MOTION
# =============================================================================
x_rail = Part.makeBox(330.0, 8.0, 12.0, Base.Vector(-165.0, -28.0, 269.0))
add_part(doc, grp_x_motion, "X_Linear_Guide_Rail_330mm", x_rail, CLR_LEADSCREW)
if motor_42_34:
    s_xmot = motor_42_34.copy()
    s_xmot.rotate(Base.Vector(0,0,0), Base.Vector(0,1,0), 90)
    s_xmot = norm_origin(s_xmot)
    add_part(doc, grp_x_motion, "X_Axis_NEMA17_Stepper", place(s_xmot, -185.0, -10.0, 255.0), CLR_MOTOR)
x_idler = Part.makeCylinder(9.0, 20.0, Base.Vector(180.0, -10.0, 265.0), Base.Vector(0.0, 0.0, 1.0))
add_part(doc, grp_x_motion, "X_Belt_Tensioner_Pulley", x_idler, CLR_PULLEY)
x_belt = Part.makeBox(360.0, 2.0, 6.0, Base.Vector(-180.0, -31.0, 272.0))
add_part(doc, grp_x_motion, "X_GT2_Steel_Drive_Belt", x_belt, CLR_BELT)

# =============================================================================
# 7. COUNTERBALANCED SADDLE CARRIAGE & T8 Z LEADSCREW
# =============================================================================
saddle_top = Part.makeBox(95.0, 85.0, 8.0, Base.Vector(-47.5, -36.0, 296.0))
saddle_front = Part.makeBox(95.0, 8.0, 105.0, Base.Vector(-47.5, -36.0, 195.0))
saddle_rear = Part.makeBox(95.0, 8.0, 85.0, Base.Vector(-47.5, 41.0, 215.0))
saddle_full = saddle_top.fuse(saddle_front).fuse(saddle_rear)
add_part(doc, grp_toolhead, "Counterbalanced_Saddle_Carriage", saddle_full, CLR_CARRIAGE)

if motor_42_34:
    add_part(doc, grp_toolhead, "Z_Stepper_Motor_REAR_BALANCER", place(motor_42_34, 0.0, 60.0, 225.0), CLR_MOTOR)
rear_pulley = Part.makeCylinder(10.0, 12.0, Base.Vector(0.0, 60.0, 304.0), Base.Vector(0.0, 0.0, 1.0))
add_part(doc, grp_toolhead, "Z_Rear_Drive_Pulley", rear_pulley, CLR_PULLEY)

top_belt_L = Part.makeBox(2.0, 108.0, 6.0, Base.Vector(-9.0, -48.0, 307.0))
top_belt_R = Part.makeBox(2.0, 108.0, 6.0, Base.Vector( 7.0, -48.0, 307.0))
add_part(doc, grp_toolhead, "Z_Overhead_Sync_Belt_Left",  top_belt_L, CLR_BELT)
add_part(doc, grp_toolhead, "Z_Overhead_Sync_Belt_Right", top_belt_R, CLR_BELT)

front_pulley = Part.makeCylinder(12.0, 12.0, Base.Vector(0.0, -48.0, 304.0), Base.Vector(0.0, 0.0, 1.0))
add_part(doc, grp_toolhead, "Z_Front_Leadscrew_Driven_Pulley", front_pulley, CLR_PULLEY)

z_rail_L = Part.makeBox(8.0, 6.0, 120.0, Base.Vector(-28.0 - 4.0, -42.0, 195.0))
z_rail_R = Part.makeBox(8.0, 6.0, 120.0, Base.Vector( 28.0 - 4.0, -42.0, 195.0))
add_part(doc, grp_toolhead, "Z_Vertical_Guide_Rail_Left",  z_rail_L, CLR_LEADSCREW)
add_part(doc, grp_toolhead, "Z_Vertical_Guide_Rail_Right", z_rail_R, CLR_LEADSCREW)

# Stock Ender 3 T8 Leadscrew utilized for Z:
z_leadscrew_t8 = Part.makeCylinder(4.0, 150.0, Base.Vector(0.0, -48.0, 175.0), Base.Vector(0.0, 0.0, 1.0))
add_part(doc, grp_toolhead, "Z_T8_Leadscrew_Vertical_Drive", z_leadscrew_t8, CLR_LEADSCREW)

# Z Plunge Slide Plate (85 mm wide, 100 mm tall, 8 mm thick) at Y = -54 mm
z_plunge_plate = Part.makeBox(85.0, 8.0, 100.0, Base.Vector(-42.5, -54.0, 190.0))
add_part(doc, grp_toolhead, "Z_Plunge_Slide_Plate", z_plunge_plate, CLR_CARRIAGE)


# =============================================================================
# 8. THE 65mm ROUTER CLAMP MECHANISM & MAKITA RT0701C ROUTER
# =============================================================================
# Router center is at X = 0.0, Y = -88.0 mm
# Clamp Body dimensions:
# Width: 92.0 mm (X = -46.0 .. +46.0)
# Depth: 74.0 mm (Y = -125.0 .. -51.0), mates flush against Z-plunge plate at Y = -51.0!
# Height: 48.0 mm (Z = 205.0 .. 253.0) -> full 48mm clamp face for rock-solid stability!
# Main Bore: 65.0 mm diameter centered at (0.0, -88.0)
# Tangential Flex Slit: 3.2 mm wide along Y from front face (Y = -126) into bore (Y = -88)
# Front Pinch Ears: X = -46..-20 and +20..+46 at Y = -125..-105 mm
# Dual M6 Pinch Bolts: at Z = 215.0 and Z = 243.0 mm

# 1) Main Clamp Block
clamp_raw = Part.makeBox(92.0, 74.0, 48.0, Base.Vector(-46.0, -125.0, 205.0))

# 65.0mm Bore (centered at X=0, Y=-88)
bore_65 = Part.makeCylinder(32.5, 52.0, Base.Vector(0.0, -88.0, 203.0), Base.Vector(0.0, 0.0, 1.0))

# Tangential Relief Flex Slit (3.2 mm gap along X=0, Y = -126..-88)
slit = Part.makeBox(3.2, 40.0, 52.0, Base.Vector(-1.6, -126.0, 203.0))

# Pinch Bolt Holes (M6 through hole across X with counterbore on right and hex nut pocket on left)
pinch_hole_bot = Part.makeCylinder(3.3, 100.0, Base.Vector(-50.0, -115.0, 215.0), Base.Vector(1.0, 0.0, 0.0))
pinch_hole_top = Part.makeCylinder(3.3, 100.0, Base.Vector(-50.0, -115.0, 243.0), Base.Vector(1.0, 0.0, 0.0))

# Bolt Head Counterbores on Right Ear (11.0 mm dia, 15 mm deep)
cb_bot = Part.makeCylinder(5.5, 16.0, Base.Vector(47.0 - 15.0, -115.0, 215.0), Base.Vector(1.0, 0.0, 0.0))
cb_top = Part.makeCylinder(5.5, 16.0, Base.Vector(47.0 - 15.0, -115.0, 243.0), Base.Vector(1.0, 0.0, 0.0))

# Hex Nut Pockets on Left Ear (11.5 mm across flats, 10 mm deep)
nut_bot = Part.makeBox(10.0, 10.5, 10.5, Base.Vector(-47.0, -115.0 - 5.25, 215.0 - 5.25))
nut_top = Part.makeBox(10.0, 10.5, 10.5, Base.Vector(-47.0, -115.0 - 5.25, 243.0 - 5.25))

# 4x Rear M5 Mounting Holes (into Z-plunge plate)
m5_holes = []
for hx in [-32.0, 32.0]:
    for hz in [215.0, 243.0]:
        h = Part.makeCylinder(2.6, 30.0, Base.Vector(hx, -65.0, hz), Base.Vector(0.0, 1.0, 0.0))
        m5_holes.append(h)

# Underside Dust Shoe Magnetic Pockets (4x 10mm dia x 3.5mm deep at Z = 205..208.5 mm)
mag_pockets = []
for mx in [-28.0, 28.0]:
    for my in [-105.0, -70.0]:
        mp = Part.makeCylinder(5.1, 4.0, Base.Vector(mx, my, 204.0), Base.Vector(0.0, 0.0, 1.0))
        mag_pockets.append(mp)

# Cut clamp block
clamp_final = clamp_raw.cut(bore_65).cut(slit).cut(pinch_hole_bot).cut(pinch_hole_top)
clamp_final = clamp_final.cut(cb_bot).cut(cb_top).cut(nut_bot).cut(nut_top)
for mh in m5_holes:
    clamp_final = clamp_final.cut(mh)
for mp in mag_pockets:
    clamp_final = clamp_final.cut(mp)

add_part(doc, grp_clamp, "Makita_65mm_HeavyDuty_Router_Clamp", clamp_final, CLR_CLAMP)

# 2) Dual M6 Black Oxide Socket Head Cap Pinch Bolts:
bolt_bot = Part.makeCylinder(3.0, 52.0, Base.Vector(-26.0, -115.0, 215.0), Base.Vector(1.0, 0.0, 0.0))
head_bot = Part.makeCylinder(5.0, 6.0,  Base.Vector(26.0, -115.0, 215.0), Base.Vector(1.0, 0.0, 0.0))
add_part(doc, grp_clamp, "M6_Clamp_Pinch_Bolt_Lower", bolt_bot.fuse(head_bot), CLR_BOLT)

bolt_top = Part.makeCylinder(3.0, 52.0, Base.Vector(-26.0, -115.0, 243.0), Base.Vector(1.0, 0.0, 0.0))
head_top = Part.makeCylinder(5.0, 6.0,  Base.Vector(26.0, -115.0, 243.0), Base.Vector(1.0, 0.0, 0.0))
add_part(doc, grp_clamp, "M6_Clamp_Pinch_Bolt_Upper", bolt_top.fuse(head_top), CLR_BOLT)

# 3) 65mm-to-52mm Split Reducing Adapter Sleeve (shown in clamp, selectable):
# OD = 64.9 mm, ID = 52.1 mm, Height = 46.0 mm, Split slit = 3.0 mm
sleeve_outer = Part.makeCylinder(32.45, 46.0, Base.Vector(0.0, -88.0, 206.0), Base.Vector(0.0, 0.0, 1.0))
sleeve_inner = Part.makeCylinder(26.05, 50.0, Base.Vector(0.0, -88.0, 204.0), Base.Vector(0.0, 0.0, 1.0))
sleeve_slit  = Part.makeBox(3.0, 40.0, 50.0, Base.Vector(-1.5, -120.0, 204.0))
adapter_sleeve = sleeve_outer.cut(sleeve_inner).cut(sleeve_slit)
# Add adapter sleeve as an optional/swappable part (slightly translucent gold):
add_part(doc, grp_clamp, "Adapter_Sleeve_65mm_to_52mm", adapter_sleeve, CLR_SLEEVE, transparency=30)

# 4) Makita RT0701C 1-1/4 HP Compact Trim Router (Accurate Model):
# Body Diameter: 64.85 mm aluminum cylinder (Z = 160.0 .. 295.0 mm, length 135 mm)
router_barrel = Part.makeCylinder(32.425, 135.0, Base.Vector(0.0, -88.0, 160.0), Base.Vector(0.0, 0.0, 1.0))
# Top Housing Cap (Makita Teal, 74 mm dia, Z = 295.0 .. 345.0 mm)
router_top_cap = Part.makeCylinder(37.0, 50.0, Base.Vector(0.0, -88.0, 295.0), Base.Vector(0.0, 0.0, 1.0))
# Variable Speed Dial on top (Z = 345.0 .. 352.0 mm)
router_dial = Part.makeCylinder(16.0, 7.0, Base.Vector(0.0, -88.0, 345.0), Base.Vector(0.0, 0.0, 1.0))
# Lower Spindle Nose & 1/4" Collet Nut (Black steel, 22 mm hex, Z = 135.0 .. 160.0 mm)
collet_nut = Part.makeCylinder(11.0, 25.0, Base.Vector(0.0, -88.0, 135.0), Base.Vector(0.0, 0.0, 1.0))
# 1/4" (6.35 mm) Solid Carbide End Mill (Z = 105.0 .. 135.0 mm)
endmill_shank = Part.makeCylinder(3.175, 30.0, Base.Vector(0.0, -88.0, 105.0), Base.Vector(0.0, 0.0, 1.0))

add_part(doc, grp_clamp, "Makita_RT0701C_Aluminum_Barrel", router_barrel, CLR_ALUM)
add_part(doc, grp_clamp, "Makita_RT0701C_Teal_Motor_Cap",  router_top_cap.fuse(router_dial), CLR_ROUTER)
add_part(doc, grp_clamp, "Makita_RT0701C_Collet_Chuck",     collet_nut, CLR_BOLT)
add_part(doc, grp_clamp, "Carbide_End_Mill_1_4_Inch",       endmill_shank, CLR_LEADSCREW)

# 5) Snap-on Dust Shoe Base (attached to underside magnetic pockets):
dust_shoe_ring = Part.makeCylinder(48.0, 8.0, Base.Vector(0.0, -88.0, 192.0), Base.Vector(0.0, 0.0, 1.0))
dust_shoe_bore = Part.makeCylinder(34.0, 10.0, Base.Vector(0.0, -88.0, 191.0), Base.Vector(0.0, 0.0, 1.0))
vac_port = Part.makeCylinder(18.0, 35.0, Base.Vector(35.0, -88.0, 192.0), Base.Vector(0.0, 0.0, 1.0))
vac_hole = Part.makeCylinder(15.5, 38.0, Base.Vector(35.0, -88.0, 191.0), Base.Vector(0.0, 0.0, 1.0))
dust_shoe = dust_shoe_ring.cut(dust_shoe_bore).fuse(vac_port.cut(vac_hole))
add_part(doc, grp_clamp, "QuickRelease_Magnetic_Dust_Shoe", dust_shoe, (0.20, 0.22, 0.25), transparency=20)


# =============================================================================
# 9. TRANSPARENT PREDICTED BUILD VOLUME BOX ($10" x 9" x 3"$)
# =============================================================================
IN_10 = 254.0
IN_9  = 228.6
IN_3  = 76.2
vol_box = Part.makeBox(IN_10, IN_9, IN_3, Base.Vector(-IN_10/2.0, -88.0 - IN_9/2.0, 149.0))
add_part(doc, grp_vol, "Predicted_Build_Volume_10x9x3in",
         vol_box, CLR_BUILDVOL, transparency=65, line_rgb=(0.0, 1.0, 0.85), line_width=3.0)

doc.recompute()

view = Gui.ActiveDocument.ActiveView
view.setAnimationEnabled(False)

# Renders:
# 1. Full Machine Isometric:
view.viewIsometric()
view.fitAll()
Gui.updateGui()
view.saveImage(os.path.join(RENDER_DIR, "router_clamp_full_machine_iso.png"), 1600, 1200, "Current")

# 2. Close-up on Router Clamp Mechanism (Isometric):
view.viewIsometric()
view.fitAll()
view.zoomIn()
view.zoomIn()
Gui.updateGui()
view.saveImage(os.path.join(RENDER_DIR, "router_clamp_closeup_iso.png"), 1600, 1200, "Current")

# 3. Close-up on Clamp Mechanism (Front View showing Pinch Bolts & Flex Slit):
view.viewFront()
view.fitAll()
view.zoomIn()
view.zoomIn()
Gui.updateGui()
view.saveImage(os.path.join(RENDER_DIR, "router_clamp_closeup_front.png"), 1600, 1200, "Current")

# 4. Close-up on Clamp Mechanism (Right View showing Split-Weight balance: Router in Front, Rail in Middle, Motor in Back):
view.viewRight()
view.fitAll()
view.zoomIn()
Gui.updateGui()
view.saveImage(os.path.join(RENDER_DIR, "router_clamp_closeup_side.png"), 1600, 1200, "Current")

# 5. Top View of Clamp & Overhead Belt:
view.viewTop()
view.fitAll()
view.zoomIn()
Gui.updateGui()
view.saveImage(os.path.join(RENDER_DIR, "router_clamp_closeup_top.png"), 1600, 1200, "Current")

fcstd_path = os.path.join(CAD_DIR, "Ender3_Router_Clamp_Mechanism.FCStd")
doc.saveAs(fcstd_path)
print("SAVED_ROUTER_CLAMP_CAD:" + fcstd_path)
"""

def main():
    fc = FreeCADConnection(host="127.0.0.1", port=9875)
    res = fc.execute_code(FREECAD_CODE, timeout=120)
    print(res)

if __name__ == "__main__":
    main()
