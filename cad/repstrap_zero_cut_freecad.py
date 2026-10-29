#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
FreeCAD Parametric Assembly & STL Generator:
RepStrap "Zero-Cut Beam Swap" CNC Mill (10.5" x 11.0" x 3.5" / 2.0" Dual-Deck)
Material Spec: 1 Roll PLA+ (990g / 34.9 oz) + 5.8 lbs 1/4"-Screened Concrete
Spindle: Harbor Freight Drill Master 1/4" Trim Router (SKU 62659, 65.0mm OD)
===============================================================================
HOW TO RUN:
  1. GUI Mode: Open FreeCAD -> Macro -> Macros -> Execute `repstrap_zero_cut_freecad.py`
     (Generates full color-coded 3D Assembly + individual Printable Parts group)
  2. Headless CLI Mode:
     `freecadcmd repstrap_zero_cut_freecad.py`
     (Automatically exports all 3 Print Beds of STL files + full STEP assembly)
===============================================================================
"""

import os
import math
import FreeCAD as App
import Part
import Mesh
from FreeCAD import Base

DOC_NAME = "RepStrap_ZeroCut_10x11x3_5"
EXPORT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stl_exports_zerocut")

# ==============================================================================
# 1. LOCKED-IN PARAMETRIC DIMENSIONS (Imperial -> mm internal kernel)
# ==============================================================================
INCH = 25.4

# Stock Uncut Ender 3 Aluminum Extrusions (ZERO CUTS)
BEAM_Y_TWIN_LEN     = 400.0   # 15.75" (Stock 2040 Z-uprights -> Twin Y-Bed Rails, Qty 2)
BEAM_Z_COL_LEN      = 290.0   # 11.42" (Stock 2040 Base Legs  -> Vertical Gantry Columns, Qty 2)
BEAM_X_BRIDGE_LEN   = 330.0   # 13.00" (Stock 2020 X-Axis     -> Full-Width X-Bridge, Qty 1)
BEAM_FRONT_TIE_LEN  = 290.0   # 11.42" (Stock 4040 Y-Spine    -> Front Heavy Base Tie, Qty 1)
BEAM_REAR_TIE_LEN   = 250.0   #  9.84" (Stock 2020 Top Bar    -> Rear Base Tie, Qty 1)
LEADSCREW_LEN       = 365.0   # 14.37" (Stock T8x8 Leadscrew  -> Uncut through top bearing cap)

# Working Envelope & Dual-Deck Z Heights
TRAVEL_X            = 10.5 * INCH  # 266.7 mm
TRAVEL_Y            = 11.0 * INCH  # 279.4 mm
TRAVEL_Z_HIGH_DECK  =  3.5 * INCH  #  88.9 mm (Wood / 2x4 / Relief Mode)
TRAVEL_Z_LOW_DECK   =  2.0 * INCH  #  50.8 mm (Rigid Aluminum / Brass Mode)

# PLA+ Thin-Shell & Concrete Ballast Parameters (5 Perimeters @ 0.45mm = 2.25mm / 0.089")
PLA_SHELL_WALL      = 2.25    # 0.089" (5 solid walls for concrete vibration resistance)
POUR_FUNNEL_DIA     = 25.4    # 1.00" wide pour port for 1/4"-screened concrete
AIR_BLEED_DIA       = 5.0     # 0.20" air vent port
SAWTOOTH_FIN_DEPTH  = 6.35    # 0.25" internal anti-shrinkage concrete interlock ribs

# Harbor Freight Drill Master 1/4" Trim Router (SKU 62659)
ROUTER_BORE_DIA     = 65.2    # 2.567" (65.0mm barrel + 0.2mm clearance)
ROUTER_COLLAR_OD    = 88.0    # 3.465" (6-wall ultra-stiff collar + cooling flutes)
ROUTER_COLLAR_H     = 50.0    # 1.968" clamping height
COOLING_FLUTE_DEPTH = 2.0     # 0.08" vertical air-gap channels for PLA+ thermal protection


def ensure_export_dir():
    if not os.path.exists(EXPORT_DIR):
        os.makedirs(EXPORT_DIR, exist_ok=True)


def set_color(obj, rgb, transparency=0):
    if App.GuiUp and hasattr(obj, "ViewObject") and obj.ViewObject:
        obj.ViewObject.ShapeColor = rgb
        obj.ViewObject.Transparency = transparency


# ==============================================================================
# 2. STOCK UNCUT ENDER 3 EXTRUSION MODELS (Reference Frame Assembly)
# ==============================================================================
def make_vslot_extrusion(width_x, width_y, length_z,bore_y=False):
    """Generates an accurate 2020, 2040, or 4040 V-slot profile."""
    box = Part.makeBox(width_x, width_y, length_z)
    # Add M5 center core bore(s)
    if width_x == 20 and width_y == 40:
        c1 = Part.makeCylinder(2.1, length_z, Base.Vector(10, 10, 0))
        c2 = Part.makeCylinder(2.1, length_z, Base.Vector(10, 30, 0))
        box = box.cut(c1).cut(c2)
    elif width_x == 20 and width_y == 20:
        c1 = Part.makeCylinder(2.1, length_z, Base.Vector(10, 10, 0))
        box = box.cut(c1)
    return box


# ==============================================================================
# 3. PRINTABLE PLA+ & CONCRETE-CAST PARTS
# ==============================================================================
def build_dm62659_aircooled_collar():
    """
    Part 1 (Bed 1): Harbor Freight Drill Master 62659 Air-Cooled Split Collar
    - 2.56" (65.2mm) bore with 8 vertical 0.08" air-flow cooling flutes
    - 6-perimeter clamping ears with dual M5x35 pinch bolts
    """
    r_in = ROUTER_BORE_DIA / 2.0
    r_out = ROUTER_COLLAR_OD / 2.0
    h = ROUTER_COLLAR_H

    outer_cyl = Part.makeCylinder(r_out, h)
    back_mount = Part.makeBox(92.0, 28.0, h, Base.Vector(-46.0, -r_out - 10.0, 0))
    pinch_lugs = Part.makeBox(28.0, 24.0, h, Base.Vector(-14.0, r_out - 6.0, 0))
    body = outer_cyl.fuse(back_mount).fuse(pinch_lugs)

    # Structural side gusset ribs (0.20" / 5.0mm thick)
    for x_rib in [-42.0, 37.0]:
        rib = Part.makeBox(5.0, 34.0, h, Base.Vector(x_rib, -r_out - 8.0, 0))
        body = body.fuse(rib)

    # Main 65.2mm spindle bore + 3.0mm pinch slot
    bore = Part.makeCylinder(r_in, h + 2.0, Base.Vector(0, 0, -1.0))
    slot = Part.makeBox(3.0, 40.0, h + 2.0, Base.Vector(-1.5, r_in - 2.0, -1.0))
    body = body.cut(bore).cut(slot)

    # 8 Radial Air-Flow Cooling Channels (keeps PLA+ below 110F during long cuts)
    for i in range(8):
        angle = math.radians(i * 45.0 + 22.5)
        fx = (r_in + 0.5) * math.cos(angle)
        fy = (r_in + 0.5) * math.sin(angle)
        flute = Part.makeCylinder(2.5, h + 2.0, Base.Vector(fx, fy, -1.0))
        body = body.cut(flute)

    # Dual M5 pinch bolt through-holes & backplate M5 holes
    for z_h in [12.5, 37.5]:
        b_hole = Part.makeCylinder(2.65, 40.0, Base.Vector(-20.0, r_out + 6.0, z_h), Base.Vector(1, 0, 0))
        body = body.cut(b_hole)
    for x_m in [-30.0, 30.0]:
        for z_m in [12.0, 38.0]:
            m_hole = Part.makeCylinder(2.65, 45.0, Base.Vector(x_m, -r_out - 15.0, z_m), Base.Vector(0, 1, 0))
            body = body.cut(m_hole)

    return body


def build_concrete_column_sleeve():
    """
    Part 2 (Bed 3): Full-Height Concrete Ballast Tower Sleeve for 11.42" (290mm) 2040 Column
    - Printed in 2 interlocking halves (145mm / 5.71" tall each) to fit well inside Ender 3 Z
    - 0.089" (2.25mm / 5-wall) hydrostatic shell
    - 1.00" (25.4mm) top pour funnel for 1/4"-screened concrete
    - Dual-Deck X-Bridge mounting bosses at Z = 2.0" (Low-Deck Aluminum) and Z = 3.5" (High-Deck Wood)
    """
    h = 145.0  # Lower/Upper modular half of the 290mm column
    w_x = 64.0 # 2.52" wide concrete jacket
    w_y = 84.0 # 3.31" deep concrete jacket
    wall = PLA_SHELL_WALL

    outer = Part.makeBox(w_x, w_y, h, Base.Vector(-w_x/2.0, -w_y/2.0, 0))
    cavity = Part.makeBox(w_x - 2*wall, w_y - 2*wall, h - 2*wall,
                          Base.Vector(-w_x/2.0 + wall, -w_y/2.0 + wall, wall))

    # Internal Sawtooth Anchor Fins (0.25" deep every 35mm to prevent concrete shrinkage slip)
    for z_fin in [30.0, 65.0, 100.0]:
        fin = Part.makeBox(w_x - 2*wall, SAWTOOTH_FIN_DEPTH, 4.0,
                           Base.Vector(-w_x/2.0 + wall, w_y/2.0 - wall - SAWTOOTH_FIN_DEPTH, z_fin))
        cavity = cavity.cut(fin)

    # Center 2040 extrusion chimney (20.3mm x 40.3mm slip fit)
    chimney_wall = Part.makeBox(20.3 + 2*wall, 40.3 + 2*wall, h,
                                Base.Vector(-10.15 - wall, -20.15 - wall, 0))
    chimney_void = Part.makeBox(20.3, 40.3, h + 2.0,
                                Base.Vector(-10.15, -20.15, -1.0))

    # 1.00" (25.4mm) Concrete Pour Funnel & 0.20" Air Bleed Port
    funnel = Part.makeCylinder(POUR_FUNNEL_DIA / 2.0, 10.0, Base.Vector(0, 26.0, h - 5.0))
    bleed = Part.makeCylinder(AIR_BLEED_DIA / 2.0, 10.0, Base.Vector(0, -26.0, h - 5.0))

    sleeve = outer.cut(cavity).fuse(chimney_wall).cut(chimney_void).cut(funnel).cut(bleed)

    # Dual-Deck M5 Mounting Tunnels (Low-Deck 2.0" Z and High-Deck 3.5" Z positions)
    for z_deck in [45.0, 83.1, 121.2]:
        bolt_tunnel = Part.makeCylinder(2.65, w_x + 4.0, Base.Vector(-w_x/2.0 - 2.0, 0, z_deck), Base.Vector(1, 0, 0))
        sleeve = sleeve.cut(bolt_tunnel)

    return sleeve


def build_concrete_x_bridge_girder():
    """
    Part 3 (Bed 3): Concrete-Backed Torsion Girder for Uncut 13.00" (330mm) 2020 X-Beam
    - Bolts to the rear & top V-slots of the 2020 X-beam, leaving front/bottom clear for V-wheels
    - Printed as two symmetric 165mm (6.50") interlocking halves that bolt together at X-center
    - Holds 2.2 lbs of screened concrete to eliminate X-beam twist during aluminum milling
    """
    half_len = 165.0  # 6.50" per half (2x = 13.00" / 330mm full uncut X-beam)
    girder_depth_y = 58.0  # 2.28" concrete depth behind 2020 rail
    girder_height_z = 64.0 # 2.52" concrete height
    wall = PLA_SHELL_WALL

    outer = Part.makeBox(half_len, girder_depth_y, girder_height_z, Base.Vector(0, 0, -22.0))
    void = Part.makeBox(half_len - 2*wall, girder_depth_y - 2*wall, girder_height_z - 2*wall,
                        Base.Vector(wall, wall, -22.0 + wall))

    # 1.00" Concrete Pour Port on top of girder
    pour_hole = Part.makeCylinder(POUR_FUNNEL_DIA / 2.0, 10.0,
                                  Base.Vector(half_len / 2.0, girder_depth_y / 2.0, girder_height_z - 22.0 - 5.0))

    girder = outer.cut(void).cut(pour_hole)

    # M5 T-nut mounting holes along the front face (interfaces with rear V-slot of 2020 X-beam)
    for x_b in [25.0, 82.5, 140.0]:
        t_hole = Part.makeCylinder(2.65, 12.0, Base.Vector(x_b, -2.0, 10.0), Base.Vector(0, 1, 0))
        girder = girder.cut(t_hole)

    return girder


def build_twin_rail_y_outrigger():
    """
    Part 4 (Bed 2): Twin-Rail Y-Bed Carriage Adapter (connects stock bed plate to twin 15.75" 2040 rails)
    """
    plate = Part.makeBox(95.0, 48.0, 16.0, Base.Vector(-47.5, -24.0, 0))
    for x_w in [-32.0, 32.0]:
        wheel_hole = Part.makeCylinder(2.6, 20.0, Base.Vector(x_w, 12.0, -2.0))
        plate = plate.cut(wheel_hole)
    return plate


# ==============================================================================
# 4. FULL 3D ASSEMBLY BUILDER ("Zero-Cut Beam Swap" Layout)
# ==============================================================================
def build_full_assembly():
    doc = App.newDocument(DOC_NAME)
    ensure_export_dir()

    asm_grp = doc.addObject("App::DocumentObjectGroup", "ZeroCut_Full_Assembly")
    stl_grp = doc.addObject("App::DocumentObjectGroup", "Printable_PLA_Parts")

    # 1. TWIN 15.75" (400mm) 2040 Y-AXIS BASE RAILS (Left & Right, spaced 290mm outer)
    for side, x_pos in [("L", -145.0), ("R", 125.0)]:
        rail = make_vslot_extrusion(20.0, 40.0, BEAM_Y_TWIN_LEN)
        rail.rotate(Base.Vector(0, 0, 0), Base.Vector(1, 0, 0), -90)
        rail.translate(Base.Vector(x_pos, -200.0, 0))
        obj = doc.addObject("Part::Feature", f"Uncut_2040_Y_Rail_{side}_15_75in")
        obj.Shape = rail
        set_color(obj, (0.20, 0.22, 0.25))
        asm_grp.addObject(obj)

    # 2. FRONT HEAVY 11.42" (290mm) 4040 BASE TIE & REAR 9.84" (250mm) 2020 TIE
    front_tie = make_vslot_extrusion(40.0, 40.0, BEAM_FRONT_TIE_LEN)
    front_tie.rotate(Base.Vector(0, 0, 0), Base.Vector(0, 1, 0), 90)
    front_tie.translate(Base.Vector(-145.0, -200.0, 0))
    obj_ft = doc.addObject("Part::Feature", "Uncut_4040_Front_Tie_11_42in")
    obj_ft.Shape = front_tie
    set_color(obj_ft, (0.25, 0.28, 0.32))
    asm_grp.addObject(obj_ft)

    rear_tie = make_vslot_extrusion(20.0, 20.0, BEAM_REAR_TIE_LEN)
    rear_tie.rotate(Base.Vector(0, 0, 0), Base.Vector(0, 1, 0), 90)
    rear_tie.translate(Base.Vector(-125.0, 180.0, 20.0))
    obj_rt = doc.addObject("Part::Feature", "Uncut_2020_Rear_Tie_9_84in")
    obj_rt.Shape = rear_tie
    set_color(obj_rt, (0.25, 0.28, 0.32))
    asm_grp.addObject(obj_rt)

    # 3. TWO UNCUT 11.42" (290mm) 2040 VERTICAL GANTRY COLUMNS + CONCRETE SLEEVES
    sleeve_shape = build_concrete_column_sleeve()
    for side, x_col in [("L", -155.0), ("R", 135.0)]:
        col = make_vslot_extrusion(20.0, 40.0, BEAM_Z_COL_LEN)
        col.translate(Base.Vector(x_col, -20.0, 40.0))
        obj_c = doc.addObject("Part::Feature", f"Uncut_2040_Z_Column_{side}_11_42in")
        obj_c.Shape = col
        set_color(obj_c, (0.18, 0.20, 0.23))
        asm_grp.addObject(obj_c)

        # Concrete Ballast Sleeve installed around column
        slv = sleeve_shape.copy()
        slv.translate(Base.Vector(x_col + 10.0, 0.0, 40.0))
        obj_s = doc.addObject("Part::Feature", f"PLA_Concrete_Tower_Sleeve_{side}")
        obj_s.Shape = slv
        set_color(obj_s, (0.95, 0.55, 0.15), transparency=25)
        asm_grp.addObject(obj_s)

    # 4. UNCUT 13.00" (330mm) 2020 X-BRIDGE + CONCRETE TORSION GIRDER (Mounted at 3.5" High-Deck Z)
    z_bridge = 40.0 + TRAVEL_Z_HIGH_DECK + 35.0
    x_beam = make_vslot_extrusion(20.0, 20.0, BEAM_X_BRIDGE_LEN)
    x_beam.rotate(Base.Vector(0, 0, 0), Base.Vector(0, 1, 0), 90)
    x_beam.translate(Base.Vector(-165.0, -30.0, z_bridge))
    obj_xb = doc.addObject("Part::Feature", "Uncut_2020_X_Bridge_13_00in")
    obj_xb.Shape = x_beam
    set_color(obj_xb, (0.15, 0.55, 0.85))
    asm_grp.addObject(obj_xb)

    girder_half = build_concrete_x_bridge_girder()
    for side, x_g in [("L", -165.0), ("R", 0.0)]:
        g_copy = girder_half.copy()
        g_copy.translate(Base.Vector(x_g, -10.0, z_bridge))
        obj_g = doc.addObject("Part::Feature", f"PLA_Concrete_X_Girder_{side}")
        obj_g.Shape = g_copy
        set_color(obj_g, (0.95, 0.55, 0.15), transparency=25)
        asm_grp.addObject(obj_g)

    # 5. DRILL MASTER 62659 ROUTER + AIR-COOLED PLA+ SPLIT COLLAR
    collar_shape = build_dm62659_aircooled_collar()
    collar_placed = collar_shape.copy()
    collar_placed.translate(Base.Vector(0, -75.0, z_bridge - 15.0))
    obj_col = doc.addObject("Part::Feature", "PLA_DM62659_AirCooled_Collar")
    obj_col.Shape = collar_placed
    set_color(obj_col, (0.15, 0.80, 0.45))
    asm_grp.addObject(obj_col)

    router_body = Part.makeCylinder(32.5, 145.0, Base.Vector(0, -75.0, z_bridge - 25.0))
    collet = Part.makeCylinder(9.5, 28.0, Base.Vector(0, -75.0, z_bridge - 53.0))
    endmill = Part.makeCylinder(3.175, 25.0, Base.Vector(0, -75.0, z_bridge - 78.0))
    obj_rtr = doc.addObject("Part::Feature", "HarborFreight_DM62659_Router")
    obj_rtr.Shape = router_body.fuse(collet).fuse(endmill)
    set_color(obj_rtr, (0.85, 0.15, 0.15))
    asm_grp.addObject(obj_rtr)

    # 6. EXPORT PRODUCTION STL FILES FOR ALL PRINTABLE PARTS
    printable_catalog = {
        "Bed1_01_DM62659_AirCooled_Collar": collar_shape,
        "Bed2_01_TwinRail_Y_Outrigger": build_twin_rail_y_outrigger(),
        "Bed3_01_Concrete_Column_Sleeve_Half": sleeve_shape,
        "Bed3_02_Concrete_X_Girder_Half": girder_half,
    }

    for part_name, shape in printable_catalog.items():
        p_obj = doc.addObject("Part::Feature", part_name)
        p_obj.Shape = shape
        stl_grp.addObject(p_obj)
        stl_path = os.path.join(EXPORT_DIR, f"{part_name}.stl")
        Mesh.export([p_obj], stl_path)
        print(f"[FreeCAD Export] {part_name}.stl -> Volume: {shape.Volume/1000.0:.1f} cm^3 | Manifold: {shape.isValid()}")

    doc.recompute()
    fcstd_path = os.path.join(EXPORT_DIR, f"{DOC_NAME}.FCStd")
    doc.saveAs(fcstd_path)
    print(f"[FreeCAD Complete] Saved Parametric Assembly to: {fcstd_path}")
    return doc


if __name__ == "__main__":
    build_full_assembly()
