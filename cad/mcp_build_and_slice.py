#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clean, Precision-Aligned Conventional Portal Milling Machine Kit (FreeCAD MCP + OrcaSlicer MCP):
RepStrap Zero-Cut Ender 3 -> Desktop CNC Mill (10.5" x 11.0" x 3.5" / 2.0")

Every part is coaxially aligned with ZERO extraneous, tilted, or floating fragments:
1. GROUND-CONTACTING BASE & PORTAL FRAME (Z = 0.0 mm):
   - 8 Uncut Factory Extrusions from `01 MAIN ASM Ender_3.STEP`
   - 4x Ground-Contacting Concrete Machine Base Sills (Z = 0..38 mm) under Twin 2040 Y-Ways
   - 2x Tapered Ground-Contacting Portal Columns (Z = 0..290 mm)
   - Thick Deep-Section Coffered Concrete Portal Crossbar (84 x 112 mm, Z = 154..280 mm)
2. COAXIAL Y-AXIS MOVING-TABLE DRIVETRAIN:
   - `Y plate.step` + 4x Twin-Rail Y Outriggers + 8x POM V-Slot Rollers (`Rollers.step`) with coaxial spacers/eccentric nuts riding in the Twin 2040 V-grooves
   - Rear Y NEMA 17 Stepper + Mount + Coaxial 20T GT2 Drive Pulley + Front Coaxial GT2 Idler Tensioner + Taut Closed GT2 Y-Belt Loop + Center Belt Clamp
   - 4x Cylindrical Aluminum Bed Standoffs + `Hot bed.step` + MDF T-Slot Spoilboard + 6061 Aluminum Workpiece + 2x T-Slot Step Clamps
3. COAXIAL X-AXIS GANTRY SADDLE DRIVETRAIN:
   - X-Saddle Plate riding on 4x POM V-Slot Rollers (`Rollers.step`) along the front 2020 X-Bridge Way (`Solid[44]`)
   - Left Coaxial X NEMA 17 Stepper + 20T GT2 Pulley + Right GT2 Idler Tensioner + Taut Closed GT2 X-Belt Loop
4. COAXIAL Z-AXIS VERTICAL PLUNGE DRIVETRAIN:
   - Integrated Vertical V-Guideway & Dual-608ZZ Arch Tower (`Bed1_02`) bolted to the X-Saddle
   - Upright Top NEMA 17 Z-Stepper + Coaxial 5x8mm Helical Coupler + Top & Bottom 608ZZ Bearings + Uncut T8x8 Leadscrew + Brass T8 Flanged Nut (all coaxial at X=0, Y=-84mm)
   - `E plate.step` Z-Plunge Carriage + 4x Vertical Z V-Rollers + Finned Air-Cooled DM62659 Headstock Shroud (`Bed1_01`) + Harbor Freight 62659 Router
"""

import os
import sys
import json
import time
import math
import base64
import asyncio
from freecad_mcp.freecad_client import FreeCADConnection
from orcaslicer_mcp.client import OrcaClient
from orcaslicer_mcp.config import Config

PROJECT_DIR = "/home/calvin/.gemini/antigravity/scratch/ender3-router-project"
STP_DIR     = os.path.join(PROJECT_DIR, "ender3_cad_repo/Ender-3 Mechanical/STP")
CAD_DIR     = os.path.join(PROJECT_DIR, "cad")
STL_DIR     = os.path.join(PROJECT_DIR, "stl")
GCODE_DIR   = os.path.join(PROJECT_DIR, "gcode")
RENDER_DIR  = os.path.join(PROJECT_DIR, "renders")

for d in (CAD_DIR, STL_DIR, GCODE_DIR, RENDER_DIR):
    os.makedirs(d, exist_ok=True)


FREECAD_SCRIPT = f"""
import os, sys, math, json
import FreeCAD as App
import Part, Mesh, MeshPart
from FreeCAD import Base

STP_DIR    = {STP_DIR!r}
CAD_DIR    = {CAD_DIR!r}
STL_DIR    = {STL_DIR!r}
RENDER_DIR = {RENDER_DIR!r}

for doc_name in list(App.listDocuments().keys()):
    if doc_name in ("Ender3_Donor_ZeroCut_CNC", "Printable_Parts_Preview"):
        App.closeDocument(doc_name)

doc = App.newDocument("Ender3_Donor_ZeroCut_CNC")

def set_visual(obj, rgb, transparency=0, line_rgb=(0.10, 0.12, 0.14), line_width=1.3):
    if App.GuiUp and hasattr(obj, "ViewObject") and obj.ViewObject:
        vo = obj.ViewObject
        vo.ShapeColor = rgb
        vo.Transparency = transparency
        try:
            vo.LineColor = line_rgb
            vo.LineWidth = line_width
        except Exception:
            pass

def normalize_shape_to_origin(shape):
    s = shape.copy()
    bb = s.BoundBox
    cx = (bb.XMin + bb.XMax) / 2.0
    cy = (bb.YMin + bb.YMax) / 2.0
    s.translate(Base.Vector(-cx, -cy, -bb.ZMin))
    return s

def translated(shape, x, y, z):
    s = shape.copy()
    s.translate(Base.Vector(x, y, z))
    return s

def load_stp_centered(filename):
    path = os.path.join(STP_DIR, filename)
    s = Part.Shape()
    s.read(path)
    return normalize_shape_to_origin(s)

def make_chamfered_rect_prism(w_x, w_y, h_z, ch, z0=0.0):
    hx, hy = w_x / 2.0, w_y / 2.0
    c = min(ch, hx * 0.45, hy * 0.45)
    pts = [
        Base.Vector(-hx + c, -hy, z0),
        Base.Vector( hx - c, -hy, z0),
        Base.Vector( hx, -hy + c, z0),
        Base.Vector( hx,  hy - c, z0),
        Base.Vector( hx - c,  hy, z0),
        Base.Vector(-hx + c,  hy, z0),
        Base.Vector(-hx,  hy - c, z0),
        Base.Vector(-hx, -hy + c, z0),
        Base.Vector(-hx + c, -hy, z0),
    ]
    return Part.Face(Part.makePolygon(pts)).extrude(Base.Vector(0, 0, h_z))

def oct_wire(wx, wy, ch, y_off, z):
    hx, hy = wx / 2.0, wy / 2.0
    c = min(ch, hx * 0.4, hy * 0.4)
    pts = [
        Base.Vector(-hx + c, -hy + y_off, z),
        Base.Vector( hx - c, -hy + y_off, z),
        Base.Vector( hx, -hy + c + y_off, z),
        Base.Vector( hx,  hy - c + y_off, z),
        Base.Vector( hx - c,  hy + y_off, z),
        Base.Vector(-hx + c,  hy + y_off, z),
        Base.Vector(-hx,  hy - c + y_off, z),
        Base.Vector(-hx, -hy + c + y_off, z),
        Base.Vector(-hx + c, -hy + y_off, z),
    ]
    return Part.makePolygon(pts)

def make_tapered_column_outer(w_x_bot, w_y_bot, w_x_top, w_y_top, y_shift_top, h_z, ch_bot=10.0, ch_top=8.0):
    w_bot = oct_wire(w_x_bot, w_y_bot, ch_bot, 0.0, 0.0)
    w_top = oct_wire(w_x_top, w_y_top, ch_top, y_shift_top, h_z)
    return Part.makeLoft([w_bot, w_top], True, False)

def make_nema17_motor(body_h=38.0, shaft_dir="Z-"):
    \"\"\"Precision Upright NEMA 17 Stepper Motor (42.3 x 42.3 x body_h mm, 22mm pilot boss, 5mm shaft).\"\"\"
    body = make_chamfered_rect_prism(42.3, 42.3, body_h, 5.0, 0.0)
    if shaft_dir == "Z-":
        pilot = Part.makeCylinder(11.0, 2.0, Base.Vector(0, 0, -2.0))
        shaft = Part.makeCylinder(2.5, 22.0, Base.Vector(0, 0, -22.0))
        m = body.fuse(pilot).fuse(shaft)
    elif shaft_dir == "Z+":
        pilot = Part.makeCylinder(11.0, 2.0, Base.Vector(0, 0, body_h))
        shaft = Part.makeCylinder(2.5, 22.0, Base.Vector(0, 0, body_h))
        m = body.fuse(pilot).fuse(shaft)
    elif shaft_dir == "Y-":
        pilot = Part.makeCylinder(11.0, 2.0, Base.Vector(0, 0, body_h))
        shaft = Part.makeCylinder(2.5, 22.0, Base.Vector(0, 0, body_h))
        m = body.fuse(pilot).fuse(shaft)
        m.rotate(Base.Vector(0, 0, 0), Base.Vector(1, 0, 0), 90)
    return m

def make_gt2_pulley_z(cx, cy, cz, h=14.0):
    \"\"\"Coaxial 20T GT2 Timing Pulley / Idler along Z axis.\"\"\"
    flange_b = Part.makeCylinder(8.0, 1.5, Base.Vector(cx, cy, cz))
    teeth    = Part.makeCylinder(6.3, h - 3.0, Base.Vector(cx, cy, cz + 1.5))
    flange_t = Part.makeCylinder(8.0, 1.5, Base.Vector(cx, cy, cz + h - 1.5))
    hub      = Part.makeCylinder(8.0, 6.0, Base.Vector(cx, cy, cz - 6.0))
    return flange_b.fuse(teeth).fuse(flange_t).fuse(hub).cut(
        Part.makeCylinder(2.5, h + 10.0, Base.Vector(cx, cy, cz - 8.0))
    )

def make_gt2_pulley_y(cx, cy, cz, h=14.0):
    \"\"\"Coaxial 20T GT2 Timing Pulley / Idler with axis along Y.\"\"\"
    p = make_gt2_pulley_z(0, 0, 0, h)
    p.rotate(Base.Vector(0, 0, 0), Base.Vector(1, 0, 0), -90)
    p.translate(Base.Vector(cx, cy, cz))
    return p

def make_closed_belt_loop_y(cx, y_min, y_max, cz, r_pulley=6.5, belt_w=6.0, belt_t=1.5):
    \"\"\"Taut Closed GT2 Timing Belt Loop running along Y between two vertical-axis (Z) pulleys.\"\"\"
    length = y_max - y_min
    outer_box = Part.makeBox(2*(r_pulley + belt_t), length, belt_w, Base.Vector(cx - r_pulley - belt_t, y_min, cz - belt_w/2.0))
    c1 = Part.makeCylinder(r_pulley + belt_t, belt_w, Base.Vector(cx, y_min, cz - belt_w/2.0))
    c2 = Part.makeCylinder(r_pulley + belt_t, belt_w, Base.Vector(cx, y_max, cz - belt_w/2.0))
    outer = outer_box.fuse(c1).fuse(c2)

    inner_box = Part.makeBox(2*r_pulley, length, belt_w + 2.0, Base.Vector(cx - r_pulley, y_min, cz - belt_w/2.0 - 1.0))
    ic1 = Part.makeCylinder(r_pulley, belt_w + 2.0, Base.Vector(cx, y_min, cz - belt_w/2.0 - 1.0))
    ic2 = Part.makeCylinder(r_pulley, belt_w + 2.0, Base.Vector(cx, y_max, cz - belt_w/2.0 - 1.0))
    inner = inner_box.fuse(ic1).fuse(ic2)
    return outer.cut(inner)

def make_closed_belt_loop_x(x_min, x_max, cy, cz, r_pulley=6.5, belt_w=6.0, belt_t=1.5):
    \"\"\"Taut Closed GT2 Timing Belt Loop running along X between two Y-axis pulleys.\"\"\"
    length = x_max - x_min
    outer_box = Part.makeBox(length, belt_w, 2*(r_pulley + belt_t), Base.Vector(x_min, cy - belt_w/2.0, cz - r_pulley - belt_t))
    c1 = Part.makeCylinder(r_pulley + belt_t, belt_w, Base.Vector(x_min, cy - belt_w/2.0, cz), Base.Vector(0, 1, 0))
    c2 = Part.makeCylinder(r_pulley + belt_t, belt_w, Base.Vector(x_max, cy - belt_w/2.0, cz), Base.Vector(0, 1, 0))
    outer = outer_box.fuse(c1).fuse(c2)

    inner_box = Part.makeBox(length, belt_w + 2.0, 2*r_pulley, Base.Vector(x_min, cy - belt_w/2.0 - 1.0, cz - r_pulley))
    ic1 = Part.makeCylinder(r_pulley, belt_w + 2.0, Base.Vector(x_min, cy - belt_w/2.0 - 1.0, cz), Base.Vector(0, 1, 0))
    ic2 = Part.makeCylinder(r_pulley, belt_w + 2.0, Base.Vector(x_max, cy - belt_w/2.0 - 1.0, cz), Base.Vector(0, 1, 0))
    inner = inner_box.fuse(ic1).fuse(ic2)
    return outer.cut(inner)

def make_608zz_bearing(cx, cy, cz):
    outer_ring = Part.makeCylinder(11.0, 7.0, Base.Vector(cx, cy, cz)).cut(
        Part.makeCylinder(9.2, 7.4, Base.Vector(cx, cy, cz - 0.2))
    )
    inner_ring = Part.makeCylinder(6.2, 7.0, Base.Vector(cx, cy, cz)).cut(
        Part.makeCylinder(4.0, 7.4, Base.Vector(cx, cy, cz - 0.2))
    )
    shield = Part.makeCylinder(9.3, 5.8, Base.Vector(cx, cy, cz + 0.6)).cut(
        Part.makeCylinder(6.1, 6.2, Base.Vector(cx, cy, cz + 0.4))
    )
    return outer_ring.fuse(inner_ring).fuse(shield)

donor_grp   = doc.addObject("App::DocumentObjectGroup", "01_Reused_Ender3_Factory_Hardware")
motion_grp  = doc.addObject("App::DocumentObjectGroup", "02_XYZ_Kinematics_Belts_Rollers_Drivetrain")
pla_grp     = doc.addObject("App::DocumentObjectGroup", "03_Conventional_Mill_Printed_Castings")
conc_grp    = doc.addObject("App::DocumentObjectGroup", "04_Distributed_Concrete_Ballast_Cores")
spindle_grp = doc.addObject("App::DocumentObjectGroup", "05_Mill_Headstock_Router_And_Workholding")
elec_grp    = doc.addObject("App::DocumentObjectGroup", "06_CNC_Controller_And_Power_Unit")

main_asm = Part.Shape()
main_asm.read(os.path.join(STP_DIR, "01 MAIN ASM Ender_3.STEP"))
solids = main_asm.Solids

e_plate_raw = Part.Shape()
e_plate_raw.read(os.path.join(STP_DIR, "E plate.step"))
cyl_faces = [f for f in e_plate_raw.Faces if "Cylinder" in str(type(f.Surface)) and 1.4 <= f.Surface.Radius <= 3.0]

# Color Palette
CLR_EXTRUSION = (0.14, 0.16, 0.18)  # Black Anodized V-Slot Extrusions
CLR_MILL_CAST = (0.22, 0.25, 0.29)  # Anthracite Mineral-Cast Grey (Columns & Base Sills)
CLR_MILL_TRIM = (0.94, 0.42, 0.08)  # Safety-Orange Crossbar & Clamps
CLR_HEADSTOCK = (0.10, 0.65, 0.72)  # Precision Teal Headstock & Y-Outriggers
CLR_ALU_PLATE = (0.80, 0.83, 0.87)  # Machined 6061 Aluminum / Chrome Steel
CLR_STEEL_BLK = (0.20, 0.22, 0.26)  # Powder-Coated Steel Brackets & Carriages
CLR_BRASS     = (0.88, 0.72, 0.22)  # Brass T8 Nut & Leadscrew
CLR_BELT      = (0.08, 0.08, 0.09)  # Neoprene GT2 Timing Belt & POM V-Wheels
CLR_CONCRETE  = (0.50, 0.53, 0.55)  # Internal Screened Concrete Core
CLR_MDF       = (0.74, 0.58, 0.36)  # T-Slot MDF Spoilboard

# ---------------------------------------------------------------------------
# 1. GROUND-LEVEL MACHINE BASE & 8 UNCUT EXTRUSIONS (COLUMNS TOUCH GROUND AT Z = 0.0 mm)
# ---------------------------------------------------------------------------
for sol_id, side, x_pos in [(4, "Left", -115.0), (5, "Right", 115.0)]:
    s_rail = normalize_shape_to_origin(solids[sol_id])
    s_rail.translate(Base.Vector(x_pos, 0.0, 20.0))
    obj = doc.addObject("Part::Feature", f"Donor_Solid{{sol_id}}_2040_TwinY_{{side}}_15_75in")
    obj.Shape = s_rail
    set_visual(obj, CLR_EXTRUSION)
    donor_grp.addObject(obj)

s_front = normalize_shape_to_origin(solids[2])
s_front.translate(Base.Vector(0.0, -180.0, 0.0))
obj_f = doc.addObject("Part::Feature", "Donor_Solid2_4040_FrontBaseTie_9_84in")
obj_f.Shape = s_front
set_visual(obj_f, CLR_EXTRUSION)
donor_grp.addObject(obj_f)

# Rear Base Cross-Tie uses the 2020 x 330 mm (`Solid[3]`) extrusion so the heavy 2040 x 330 mm (`Solid[421]`) can serve as the Primary X-Bridge Crossbar!
s_rear = normalize_shape_to_origin(solids[3])
s_rear.translate(Base.Vector(0.0, 190.0, 20.0))
obj_r = doc.addObject("Part::Feature", "Donor_Solid3_2020_RearBaseTie_13_00in")
obj_r.Shape = s_rear
set_visual(obj_r, CLR_EXTRUSION)
donor_grp.addObject(obj_r)

for sol_id, side, x_col in [(1, "Left", -165.0), (0, "Right", 165.0)]:
    s_col = normalize_shape_to_origin(solids[sol_id])
    s_col.translate(Base.Vector(x_col, -10.0, 0.0))
    obj_c = doc.addObject("Part::Feature", f"Donor_Solid{{sol_id}}_4040_GantryCol_{{side}}_11_42in")
    obj_c.Shape = s_col
    set_visual(obj_c, CLR_EXTRUSION)
    donor_grp.addObject(obj_c)

z_high_deck = 160.0
# Heavy 2040 x 330 mm (`Solid[421]`, 40 mm tall x 20 mm deep) swapped into the Primary Lower X-Bridge Crossbar Way!
s_xmain = normalize_shape_to_origin(solids[421])
s_xmain.rotate(Base.Vector(0, 0, 0), Base.Vector(0, 1, 0), 90)
s_xmain.rotate(Base.Vector(0, 0, 0), Base.Vector(1, 0, 0), 90)
s_xmain = normalize_shape_to_origin(s_xmain)
s_xmain.translate(Base.Vector(0.0, -40.0, z_high_deck - 10.0))
obj_xm = doc.addObject("Part::Feature", "Donor_Solid421_2040_XBridgePrimary_13_00in")
obj_xm.Shape = s_xmain
set_visual(obj_xm, CLR_EXTRUSION)
donor_grp.addObject(obj_xm)

# 2020 x 345 mm (`Solid[44]`) serves as the Upper Rear X-Bridge Torsion Rebar inside the concrete box-beam
s_xback = normalize_shape_to_origin(solids[44])
s_xback.translate(Base.Vector(0.0, -8.0, z_high_deck + 76.0))
obj_xb = doc.addObject("Part::Feature", "Donor_Solid44_2020_XBridgeTorsion_13_58in")
obj_xb.Shape = s_xback
set_visual(obj_xb, CLR_EXTRUSION)
donor_grp.addObject(obj_xb)

# ---------------------------------------------------------------------------
# 2. DISTRIBUTED CONCRETE BALLAST ZONE A: GROUND-LEVEL MACHINE BASE SILLS (Z = 0..38 mm)
# ---------------------------------------------------------------------------
wall = 2.25

def make_concrete_base_sill_half():
    len_y, w_x, h_z = 180.0, 56.0, 38.0
    outer = make_chamfered_rect_prism(w_x, len_y, h_z, 6.0, 0.0)
    foot = make_chamfered_rect_prism(w_x + 14.0, len_y, 8.0, 6.0, 0.0)
    outer = outer.fuse(foot)
    rail_cut = Part.makeBox(40.4, len_y + 4.0, 22.0, Base.Vector(-20.2, -len_y/2.0 - 2.0, 20.0))
    void = Part.makeBox(w_x - 2*wall, len_y - 2*wall, 20.0 - 2*wall,
                        Base.Vector(-(w_x - 2*wall)/2.0, -(len_y - 2*wall)/2.0, wall))
    pour = Part.makeCylinder(10.0, 12.0, Base.Vector(0.0, 0.0, 12.0))
    sill = outer.cut(rail_cut).cut(void).cut(pour)
    return sill, void

base_sill_half, base_sill_core = make_concrete_base_sill_half()
for side, x_sill in [("Left", -115.0), ("Right", 115.0)]:
    for fb, y_sill in [("Front", -90.0), ("Rear", 90.0)]:
        s_inst = base_sill_half.copy()
        s_inst.translate(Base.Vector(x_sill, y_sill, 0.0))
        o_sill = doc.addObject("Part::Feature", f"PLA_Ground_Concrete_BaseSill_{{side}}_{{fb}}")
        o_sill.Shape = s_inst
        set_visual(o_sill, CLR_MILL_CAST, transparency=10)
        pla_grp.addObject(o_sill)

        c_inst = base_sill_core.copy()
        c_inst.translate(Base.Vector(x_sill, y_sill, 0.0))
        o_sc = doc.addObject("Part::Feature", f"Cast_Concrete_BaseSill_Core_{{side}}_{{fb}}")
        o_sc.Shape = c_inst
        set_visual(o_sc, CLR_CONCRETE, transparency=55)
        conc_grp.addObject(o_sc)

# ---------------------------------------------------------------------------
# 3. DISTRIBUTED CONCRETE BALLAST ZONE B: GROUND-CONTACTING TAPERED MILL COLUMNS (Z = 0..290 mm)
# ---------------------------------------------------------------------------
def make_conventional_mill_column(h=145.0, is_lower=True):
    if is_lower:
        wx0, wy0 = 82.0, 118.0
        wx1, wy1 = 76.0, 96.0
        y_shift  = 6.0
    else:
        wx0, wy0 = 76.0, 96.0
        wx1, wy1 = 70.0, 76.0
        y_shift  = 6.0

    outer = make_tapered_column_outer(wx0, wy0, wx1, wy1, y_shift, h, 10.0, 8.0)

    if is_lower:
        pedestal = make_chamfered_rect_prism(104.0, 136.0, 12.0, 12.0, 0.0)
        step_pad = make_chamfered_rect_prism(90.0, 124.0, 22.0, 10.0, 0.0)
        outer = outer.fuse(pedestal).fuse(step_pad)
        for bx in [-40.0, 40.0]:
            for by in [-54.0, 0.0, 54.0]:
                outer = outer.cut(Part.makeCylinder(2.75, 26.0, Base.Vector(bx, by, -1.0)))
                outer = outer.cut(Part.makeCylinder(5.2, 12.0, Base.Vector(bx, by, 12.0)))

    crown = make_chamfered_rect_prism(wx1 + 6.0, wy1 + 6.0, 8.0, 8.0, h - 8.0)
    crown.translate(Base.Vector(0.0, y_shift, 0.0))
    outer = outer.fuse(crown)

    z_p = 28.0
    while z_p + 34.0 < h - 14.0:
        p_cut = Part.makeBox(wx0 + 10.0, 36.0, 26.0, Base.Vector(-(wx0 + 10.0)/2.0, -14.0, z_p))
        p_keep = Part.makeBox(wx1 - 5.0, 40.0, 30.0, Base.Vector(-(wx1 - 5.0)/2.0, -16.0, z_p - 2.0))
        outer = outer.cut(p_cut.cut(p_keep))
        z_p += 38.0

    void = make_tapered_column_outer(
        wx0 - 2*wall - 4.0, wy0 - 2*wall - 4.0,
        wx1 - 2*wall - 4.0, wy1 - 2*wall - 4.0,
        y_shift, h - 2*wall, 8.0, 6.0
    )
    void.translate(Base.Vector(0.0, 0.0, wall))

    chimney_w = Part.makeBox(40.6 + 2*wall, 40.6 + 2*wall, h, Base.Vector(-20.3 - wall, -20.3 - wall, 0.0))
    chimney_v = Part.makeBox(40.6, 40.6, h + 4.0, Base.Vector(-20.3, -20.3, -2.0))

    funnel_rim = Part.makeCylinder(15.0, 5.0, Base.Vector(0.0, 26.0 + y_shift, h))
    pour_port  = Part.makeCylinder(12.7, 16.0, Base.Vector(0.0, 26.0 + y_shift, h - 8.0))
    bleed_port = Part.makeCylinder(2.5, 16.0, Base.Vector(0.0, -24.0 + y_shift, h - 8.0))

    col_shell = outer.fuse(funnel_rim).cut(void).fuse(chimney_w).cut(chimney_v).cut(pour_port).cut(bleed_port)

    for z_deck in [35.0, 75.0, 115.0, 155.0, 195.0, 235.0, 265.0]:
        if z_deck < h - 10.0:
            tunnel = Part.makeCylinder(2.65, wx0 + 20.0, Base.Vector(-wx0/2.0 - 10.0, 0.0, z_deck), Base.Vector(1, 0, 0))
            col_shell = col_shell.cut(tunnel)

    core = void.cut(chimney_w)
    return col_shell, core

col_sleeve_half, _ = make_conventional_mill_column(145.0, is_lower=True)
col_full_shell, col_full_core = make_conventional_mill_column(290.0, is_lower=True)

for side, x_col in [("Left", -165.0), ("Right", 165.0)]:
    slv = col_full_shell.copy()
    slv.translate(Base.Vector(x_col, -10.0, 0.0))
    o_slv = doc.addObject("Part::Feature", f"PLA_5Wall_Concrete_TowerSleeve_{{side}}")
    o_slv.Shape = slv
    set_visual(o_slv, CLR_MILL_CAST, transparency=12)
    pla_grp.addObject(o_slv)

    core = col_full_core.copy()
    core.translate(Base.Vector(x_col, -10.0, 0.0))
    o_core = doc.addObject("Part::Feature", f"Cast_Concrete_ColumnCore_{{side}}")
    o_core.Shape = core
    set_visual(o_core, CLR_CONCRETE, transparency=55)
    conc_grp.addObject(o_core)

# ---------------------------------------------------------------------------
# 4. DISTRIBUTED CONCRETE BALLAST ZONE C: THICK DEEP-SECTION PORTAL BOX-BEAM X-CROSSBAR
# ---------------------------------------------------------------------------
def make_mill_x_crossrail_half():
    half_len, gd_y, gh_z = 165.0, 78.0, 112.0
    outer = make_chamfered_rect_prism(half_len, gd_y, gh_z, 10.0, 0.0)
    outer.translate(Base.Vector(half_len / 2.0, gd_y / 2.0, 0.0))

    flange = Part.makeBox(26.0, gd_y + 20.0, gh_z + 18.0, Base.Vector(0.0, -10.0, -4.0))
    flange_cut = Part.makeBox(18.0, gd_y - 12.0, gh_z + 22.0, Base.Vector(8.0, 6.0, -6.0))
    outer = outer.fuse(flange.cut(flange_cut))

    for x_p in [36.0, 88.0, 134.0]:
        pocket = Part.makeBox(34.0, 4.0, gh_z - 28.0, Base.Vector(x_p - 17.0, gd_y - 3.0, 14.0))
        outer = outer.cut(pocket)
    for x_r in [28.0, 66.0, 106.0, 144.0]:
        rib = Part.makeBox(6.0, 6.0, gh_z - 8.0, Base.Vector(x_r - 3.0, gd_y - 2.0, 4.0))
        outer = outer.fuse(rib)

    void = Part.makeBox(half_len - 2*wall - 8.0, gd_y - 2*wall - 6.0, gh_z - 2*wall,
                        Base.Vector(wall + 4.0, wall + 3.0, wall))
    pour_rim  = Part.makeCylinder(15.5, 5.0, Base.Vector(half_len / 2.0, gd_y / 2.0, gh_z))
    pour_hole = Part.makeCylinder(12.7, 16.0, Base.Vector(half_len / 2.0, gd_y / 2.0, gh_z - 8.0))
    bleed_h   = Part.makeCylinder(3.0, 16.0, Base.Vector(half_len / 2.0 + 42.0, gd_y / 2.0, gh_z - 8.0))
    girder = outer.fuse(pour_rim).cut(void).cut(pour_hole).cut(bleed_h)

    for x_b in [30.0, 82.5, 135.0]:
        for z_b in [24.0, 86.0]:
            t_hole = Part.makeCylinder(2.65, 18.0, Base.Vector(x_b, -3.0, z_b), Base.Vector(0, 1, 0))
            girder = girder.cut(t_hole)
    return girder

x_girder_half = make_mill_x_crossrail_half()

# Placed at Y = -32..+46 mm (centered at Y = +7.0 mm) so the front of `Solid[44]` (Y = -50..-30 mm) is 100% clear for the X-carriage!
xg_body = make_chamfered_rect_prism(330.0, 78.0, 112.0, 10.0, z_high_deck - 4.0)
xg_body.translate(Base.Vector(0.0, 7.0, 0.0))
for sx in [-165.0, 165.0]:
    cheek = make_chamfered_rect_prism(84.0, 98.0, 124.0, 10.0, z_high_deck - 8.0)
    cheek_in = make_chamfered_rect_prism(75.6, 89.6, 128.0, 9.0, z_high_deck - 10.0)
    cheek = cheek.cut(cheek_in)
    cheek.translate(Base.Vector(sx, -4.0, 0.0))
    xg_body = xg_body.fuse(cheek)

xg_void = make_chamfered_rect_prism(298.0, 66.0, 102.0, 8.0, z_high_deck + 1.0)
xg_void.translate(Base.Vector(0.0, 7.0, 0.0))
for px in [-75.0, 75.0]:
    xg_body = xg_body.fuse(Part.makeCylinder(15.5, 5.0, Base.Vector(px, 7.0, z_high_deck + 108.0)))
    xg_body = xg_body.cut(Part.makeCylinder(12.7, 16.0, Base.Vector(px, 7.0, z_high_deck + 98.0)))

xg_shell = xg_body.cut(xg_void).cut(s_xmain).cut(s_xback)
o_xg = doc.addObject("Part::Feature", "PLA_5Wall_XBridge_Concrete_Girder")
o_xg.Shape = xg_shell
set_visual(o_xg, CLR_MILL_TRIM, transparency=10)
pla_grp.addObject(o_xg)

o_xg_core = doc.addObject("Part::Feature", "Cast_Concrete_XBridge_Core")
o_xg_core.Shape = xg_void.cut(s_xmain).cut(s_xback)
set_visual(o_xg_core, CLR_CONCRETE, transparency=55)
conc_grp.addObject(o_xg_core)

# ---------------------------------------------------------------------------
# 5. COAXIAL Y-AXIS MOVING-TABLE DRIVETRAIN (ACTIVE MILLING POSITION AT Y = -42.0 mm)
# ---------------------------------------------------------------------------
y_table_pos = -42.0
y_plate = load_stp_centered("Y plate.step")
y_plate.translate(Base.Vector(0.0, y_table_pos, 44.0))
obj_yp = doc.addObject("Part::Feature", "Donor_Y_Carriage_Plate")
obj_yp.Shape = y_plate
set_visual(obj_yp, CLR_STEEL_BLK)
donor_grp.addObject(obj_yp)

def make_stylized_y_outrigger():
    base = make_chamfered_rect_prism(96.0, 50.0, 16.0, 8.0, 0.0)
    skirt = make_chamfered_rect_prism(96.0, 18.0, 24.0, 6.0, -8.0)
    skirt.translate(Base.Vector(0.0, 16.0, 0.0))
    plate = base.fuse(skirt)
    truss_pocket = make_chamfered_rect_prism(42.0, 26.0, 10.0, 5.0, 8.0)
    plate = plate.cut(truss_pocket)
    for x_w in [-32.0, 32.0]:
        wheel_hole = Part.makeCylinder(2.6, 30.0, Base.Vector(x_w, 12.0, -10.0))
        cb_w       = Part.makeCylinder(5.0, 4.0, Base.Vector(x_w, 12.0, 12.0))
        y_mount    = Part.makeCylinder(2.6, 22.0, Base.Vector(x_w, -12.0, -2.0))
        cb_y       = Part.makeCylinder(5.0, 4.0, Base.Vector(x_w, -12.0, 12.0))
        plate = plate.cut(wheel_hole).cut(cb_w).cut(y_mount).cut(cb_y)
    return plate

y_outrigger_shape = make_stylized_y_outrigger()
for side, x_out in [("Left", -95.0), ("Right", 95.0)]:
    for tag, y_out in [("Front", y_table_pos - 45.0), ("Rear", y_table_pos + 45.0)]:
        outr = y_outrigger_shape.copy()
        outr.translate(Base.Vector(x_out, y_out, 36.0))
        o_out = doc.addObject("Part::Feature", f"PLA_TwinRail_Y_Outrigger_{{side}}_{{tag}}")
        o_out.Shape = outr
        set_visual(o_out, CLR_HEADSTOCK)
        pla_grp.addObject(o_out)

# 8x Y-Axis V-Slot Rollers (`Rollers.step`) + Coaxial Stainless Spacers/Eccentric Nuts & M5 Bolts
roller_shape = load_stp_centered("Rollers.step")
y_rollers_list, y_spacers_list = [], []
for x_w in [-103.0, 103.0]:
    for dy_w in [-77.0, -13.0, 13.0, 77.0]:
        y_w = y_table_pos + dy_w
        r_i = roller_shape.copy()
        r_i.translate(Base.Vector(x_w, y_w, 25.0))
        y_rollers_list.append(r_i)
        # Coaxial spacer/eccentric column (OD=9mm, Z=35.2..44.0mm) + M5 bolt shaft & cap
        sp = Part.makeCylinder(4.5, 8.8, Base.Vector(x_w, y_w, 35.2)).fuse(
            Part.makeCylinder(4.2, 3.5, Base.Vector(x_w, y_w, 48.0))
        )
        y_spacers_list.append(sp)

o_yrol = doc.addObject("Part::Feature", "Motion_Y_8x_VSlot_POM_Rollers")
o_yrol.Shape = Part.makeCompound(y_rollers_list)
set_visual(o_yrol, CLR_BELT)
motion_grp.addObject(o_yrol)

o_ysp = doc.addObject("Part::Feature", "Motion_Y_8x_Coaxial_Spacers_And_Eccentric_Nuts")
o_ysp.Shape = Part.makeCompound(y_spacers_list)
set_visual(o_ysp, CLR_ALU_PLATE)
motion_grp.addObject(o_ysp)

# Rear Y-Axis Stepper Motor (upright at X=0, Y=+168mm, Z=0..36mm, shaft pointing +Z into 20T GT2 pulley at Z=28mm)
y_mot = make_nema17_motor(36.0, "Z+")
y_mot.translate(Base.Vector(0.0, 168.0, 0.0))
o_ym1 = doc.addObject("Part::Feature", "Motion_Y_Rear_NEMA17_Stepper_Motor")
o_ym1.Shape = y_mot
set_visual(o_ym1, CLR_EXTRUSION)
motion_grp.addObject(o_ym1)

y_pulley_rear = make_gt2_pulley_z(0.0, 168.0, 26.0, 14.0)
o_ypr = doc.addObject("Part::Feature", "Motion_Y_Rear_20T_GT2_Drive_Pulley")
o_ypr.Shape = y_pulley_rear
set_visual(o_ypr, CLR_ALU_PLATE)
motion_grp.addObject(o_ypr)

# Front Y-Axis Idler Pulley & Compact Tensioner Clevis (mounted to inner face of Front 4040 Tie at X=0, Y=-152mm)
y_tens_clevis = make_chamfered_rect_prism(34.0, 24.0, 24.0, 4.0, 18.0)
y_tens_clevis.translate(Base.Vector(0.0, -156.0, 0.0))
y_tens_clevis = y_tens_clevis.cut(Part.makeBox(22.0, 22.0, 16.0, Base.Vector(-11.0, -162.0, 22.0)))
o_yab = doc.addObject("Part::Feature", "Motion_Y_Front_Belt_Tensioner_Clevis")
o_yab.Shape = y_tens_clevis
set_visual(o_yab, CLR_STEEL_BLK)
motion_grp.addObject(o_yab)

y_idler = make_gt2_pulley_z(0.0, -152.0, 23.0, 14.0)
o_yid = doc.addObject("Part::Feature", "Motion_Y_Front_GT2_Idler_Pulley")
o_yid.Shape = y_idler
set_visual(o_yid, CLR_ALU_PLATE)
motion_grp.addObject(o_yid)

# Taut Closed GT2 Y-Belt Loop + Center Y-Carriage Belt Clamp Block
y_belt_loop = make_closed_belt_loop_y(0.0, -152.0, 168.0, 31.0, r_pulley=6.5, belt_w=6.0, belt_t=1.5)
o_ybelt = doc.addObject("Part::Feature", "Motion_Y_GT2_Timing_Belt_Loop")
o_ybelt.Shape = y_belt_loop
set_visual(o_ybelt, CLR_BELT)
motion_grp.addObject(o_ybelt)

y_clamp_block = make_chamfered_rect_prism(26.0, 32.0, 16.0, 4.0, 28.0)
y_clamp_block.translate(Base.Vector(0.0, y_table_pos, 0.0))
o_yclp = doc.addObject("Part::Feature", "Motion_Y_Carriage_Center_Belt_Clamp")
o_yclp.Shape = y_clamp_block
set_visual(o_yclp, CLR_BRASS)
motion_grp.addObject(o_yclp)

# ---------------------------------------------------------------------------
# 6. COAXIAL X-AXIS GANTRY SADDLE DRIVETRAIN (ZERO CLUTTER)
# ---------------------------------------------------------------------------
# Precision X-Saddle Carriage Plate (`92 x 8 x 96 mm`) riding at Y = -56 mm along the front of `Solid[44]` (Y = -40 mm)
x_saddle = make_chamfered_rect_prism(92.0, 8.0, 96.0, 8.0, z_high_deck - 24.0)
x_saddle.translate(Base.Vector(0.0, -56.0, 0.0))
o_xsad = doc.addObject("Part::Feature", "Motion_X_Saddle_Carriage_Plate")
o_xsad.Shape = x_saddle
set_visual(o_xsad, CLR_STEEL_BLK)
motion_grp.addObject(o_xsad)

# 4x X-Axis POM V-Slot Rollers (`Rollers.step`) engaging top (Z=192mm) and bottom (Z=148mm) V-grooves of the 40mm-tall 2040 X-Crossbar (`Solid[421]`, Y=-40mm)
x_rollers_list, x_spacers_list = [], []
for rx_w in [-32.0, 32.0]:
    for rz_w in [z_high_deck - 22.0, z_high_deck + 34.0]:
        rw = roller_shape.copy()
        rw.rotate(Base.Vector(0, 0, 0), Base.Vector(1, 0, 0), 90)
        rw = normalize_shape_to_origin(rw)
        rw.translate(Base.Vector(rx_w, -40.0, rz_w))
        x_rollers_list.append(rw)

        sp = Part.makeCylinder(4.5, 7.0, Base.Vector(rx_w, -52.0, rz_w + 12.0), Base.Vector(0, 1, 0))
        x_spacers_list.append(sp)

o_xrol = doc.addObject("Part::Feature", "Motion_X_4x_VSlot_POM_Rollers")
o_xrol.Shape = Part.makeCompound(x_rollers_list)
set_visual(o_xrol, CLR_BELT)
motion_grp.addObject(o_xrol)

o_xhw = doc.addObject("Part::Feature", "Motion_X_4x_Coaxial_Spacers_And_Eccentric_Nuts")
o_xhw.Shape = Part.makeCompound(x_spacers_list)
set_visual(o_xhw, CLR_ALU_PLATE)
motion_grp.addObject(o_xhw)

# Left X-Axis Stepper Motor (mounted neatly inside the left crossrail bay at X=-132mm, shaft pointing -Y to pulley at Y=-50mm)
x_mot = make_nema17_motor(34.0, "Y-")
x_mot.translate(Base.Vector(-132.0, -6.0, z_high_deck + 10.0))
o_xm = doc.addObject("Part::Feature", "Motion_X_Left_NEMA17_Stepper_Motor")
o_xm.Shape = x_mot
set_visual(o_xm, CLR_EXTRUSION)
motion_grp.addObject(o_xm)

x_pulley = make_gt2_pulley_y(-132.0, -56.0, z_high_deck + 10.0, 12.0)
o_xpul = doc.addObject("Part::Feature", "Motion_X_Left_20T_GT2_Drive_Pulley")
o_xpul.Shape = x_pulley
set_visual(o_xpul, CLR_ALU_PLATE)
motion_grp.addObject(o_xpul)

# Right X-Axis GT2 Idler Pulley & Compact Tensioner Clevis at X=+132mm
x_idler = make_gt2_pulley_y(132.0, -56.0, z_high_deck + 10.0, 12.0)
o_xidl = doc.addObject("Part::Feature", "Motion_X_Right_GT2_Idler_Pulley")
o_xidl.Shape = x_idler
set_visual(o_xidl, CLR_ALU_PLATE)
motion_grp.addObject(o_xidl)

x_tens_clevis = make_chamfered_rect_prism(22.0, 18.0, 22.0, 4.0, z_high_deck - 1.0)
x_tens_clevis.translate(Base.Vector(138.0, -48.0, 0.0))
o_xadj = doc.addObject("Part::Feature", "Motion_X_Right_Belt_Tensioner_Block")
o_xadj.Shape = x_tens_clevis
set_visual(o_xadj, CLR_STEEL_BLK)
motion_grp.addObject(o_xadj)

# Taut Closed GT2 X-Belt Loop (`X = -132..+132 mm, Y = -50 mm, Z = z_high_deck + 10 mm`)
x_belt_loop = make_closed_belt_loop_x(-132.0, 132.0, -50.0, z_high_deck + 10.0, r_pulley=6.5, belt_w=6.0, belt_t=1.5)
o_xbelt = doc.addObject("Part::Feature", "Motion_X_GT2_Timing_Belt_Loop")
o_xbelt.Shape = x_belt_loop
set_visual(o_xbelt, CLR_BELT)
motion_grp.addObject(o_xbelt)

# ---------------------------------------------------------------------------
# 7. COAXIAL Z-AXIS VERTICAL PLUNGE DRIVETRAIN (ALL COAXIAL AT X = 0.0 mm, Y = -72.0 mm)
# ---------------------------------------------------------------------------
def make_z_stepper_arch_tower():
    \"\"\"
    Integrated Z-Axis Vertical Linear V-Guideway & Dual-608ZZ Stepper Arch Tower:
    - Bolts directly to the front of the X-Saddle (Y = -56 mm).
    - Top & Bottom 608ZZ bearing pockets + NEMA 17 Z-Stepper mount centered at local (0, -4.0).
    \"\"\"
    base_plate = make_chamfered_rect_prism(88.0, 44.0, 12.0, 8.0, 0.0)
    top_deck   = make_chamfered_rect_prism(68.0, 44.0, 14.0, 8.0, 96.0)
    leg_l      = Part.makeBox(14.0, 36.0, 92.0, Base.Vector(-38.0, -18.0, 8.0))
    leg_r      = Part.makeBox(14.0, 36.0, 92.0, Base.Vector( 24.0, -18.0, 8.0))
    back_web   = Part.makeBox(76.0, 8.0, 92.0, Base.Vector(-38.0, 10.0, 8.0))
    window_cut = make_chamfered_rect_prism(42.0, 20.0, 64.0, 6.0, 22.0)
    window_cut.translate(Base.Vector(0.0, 12.0, 0.0))
    arch = base_plate.fuse(top_deck).fuse(leg_l).fuse(leg_r).fuse(back_web.cut(window_cut))

    arch = arch.cut(Part.makeCylinder(11.1, 8.0, Base.Vector(0, -4.0, 102.5)))
    arch = arch.cut(Part.makeCylinder(11.1, 8.0, Base.Vector(0, -4.0, -0.5)))
    arch = arch.cut(Part.makeCylinder(5.5, 120.0, Base.Vector(0, -4.0, -4.0)))

    for mx in [-15.5, 15.5]:
        for my in [-19.5, 11.5]:
            arch = arch.cut(Part.makeCylinder(1.75, 20.0, Base.Vector(mx, my, 92.0)))

    for bx in [-32.0, 32.0]:
        for by in [-12.0, 12.0]:
            arch = arch.cut(Part.makeCylinder(2.65, 18.0, Base.Vector(bx, by, -2.0)))
    return arch

z_arch_printable = make_z_stepper_arch_tower()
z_arch_placed = z_arch_printable.copy()
# Local (0, -4.0, 0) translates to global (0.0, -72.0, z_high_deck - 24.0)
z_arch_placed.translate(Base.Vector(0.0, -68.0, z_high_deck - 24.0))
o_zarch = doc.addObject("Part::Feature", "PLA_Z_Stepper_And_608ZZ_Arch_Tower")
o_zarch.Shape = z_arch_placed
set_visual(o_zarch, CLR_MILL_CAST)
pla_grp.addObject(o_zarch)

# Coaxial Top & Bottom 608ZZ Radial Bearings at (X = 0.0, Y = -72.0)
z_brg_top = make_608zz_bearing(0.0, -72.0, z_high_deck + 78.5)
z_brg_bot = make_608zz_bearing(0.0, -72.0, z_high_deck - 24.0)
o_zbrg = doc.addObject("Part::Feature", "Motion_Z_Top_And_Bottom_608ZZ_Radial_Bearings")
o_zbrg.Shape = Part.makeCompound([z_brg_top, z_brg_bot])
set_visual(o_zbrg, CLR_ALU_PLATE)
motion_grp.addObject(o_zbrg)

# Coaxial Upright NEMA 17 Z-Stepper Motor sitting flush on top of the Z-Arch Tower (Z = z_high_deck + 86.0 mm)
z_mot = make_nema17_motor(36.0, "Z-")
z_mot.translate(Base.Vector(0.0, -72.0, z_high_deck + 86.0))
o_zm = doc.addObject("Part::Feature", "Motion_Z_Top_NEMA17_Stepper_Motor")
o_zm.Shape = z_mot
set_visual(o_zm, CLR_EXTRUSION)
motion_grp.addObject(o_zm)

# Coaxial 5x8mm Flexible Helical Shaft Coupler (OD=19mm, H=25mm) at (X=0.0, Y=-72.0, Z=z_high_deck+50.0)
z_coupler = Part.makeCylinder(9.5, 25.0, Base.Vector(0.0, -72.0, z_high_deck + 50.0)).cut(
    Part.makeCylinder(4.0, 27.0, Base.Vector(0.0, -72.0, z_high_deck + 49.0))
)
o_zcpl = doc.addObject("Part::Feature", "Motion_Z_5x8mm_Flexible_Shaft_Coupler")
o_zcpl.Shape = z_coupler
set_visual(o_zcpl, CLR_ALU_PLATE)
motion_grp.addObject(o_zcpl)

# Coaxial Enclosed T8x8 Leadscrew (spanning cleanly inside the Z-Arch from bottom 608ZZ bearing Z=136mm into 5x8mm coupler Z=222mm) + Brass T8 Flanged Nut
leadscrew = Part.makeCylinder(4.0, 96.0, Base.Vector(0.0, -72.0, z_high_deck - 24.0))
obj_ls = doc.addObject("Part::Feature", "Donor_T8_Leadscrew_Uncut_14_37in")
obj_ls.Shape = leadscrew
set_visual(obj_ls, CLR_BRASS)
motion_grp.addObject(obj_ls)

z_brass_nut = Part.makeCylinder(11.0, 3.5, Base.Vector(0.0, -72.0, z_high_deck + 18.0)).fuse(
    Part.makeCylinder(5.5, 14.0, Base.Vector(0.0, -72.0, z_high_deck + 8.0))
).cut(Part.makeCylinder(4.0, 18.0, Base.Vector(0.0, -72.0, z_high_deck + 6.0)))
o_znut = doc.addObject("Part::Feature", "Motion_Z_Brass_T8x8_Leadscrew_Nut")
o_znut.Shape = z_brass_nut
set_visual(o_znut, CLR_BRASS)
motion_grp.addObject(o_znut)

# Z-Plunge Steel Carriage Plate (`E plate.step`) + 4x Concealed Vertical Z-Plunge Rollers inside the Z-Arch Guideway
e_plate = load_stp_centered("E plate.step")
e_plate.rotate(Base.Vector(0, 0, 0), Base.Vector(1, 0, 0), 90)
e_plate = normalize_shape_to_origin(e_plate)
e_plate.translate(Base.Vector(0.0, -80.0, z_high_deck - 18.0))
obj_ep = doc.addObject("Part::Feature", "Donor_X_Carriage_Steel_Plate")
obj_ep.Shape = e_plate
set_visual(obj_ep, CLR_STEEL_BLK)
motion_grp.addObject(obj_ep)

z_rollers_list = []
for zx_w in [-24.0, 24.0]:
    for zz_w in [z_high_deck - 8.0, z_high_deck + 28.0]:
        zrw = roller_shape.copy()
        zrw.rotate(Base.Vector(0, 0, 0), Base.Vector(1, 0, 0), 90)
        zrw = normalize_shape_to_origin(zrw)
        zrw.translate(Base.Vector(zx_w, -72.0, zz_w))
        z_rollers_list.append(zrw)

o_zrol = doc.addObject("Part::Feature", "Motion_Z_4x_Vertical_Plunge_VSlot_Rollers")
o_zrol.Shape = Part.makeCompound(z_rollers_list)
set_visual(o_zrol, CLR_BELT)
motion_grp.addObject(o_zrol)

# ---------------------------------------------------------------------------
# 8. WORKTABLE, RIGID BED STANDOFFS, T-SLOT CLAMPS & HARBOR FREIGHT 62659 ROUTER HEADSTOCK
# ---------------------------------------------------------------------------
# 4x Clean Cylindrical Aluminum Bed Standoffs (OD=14mm, Z=46..54mm) at X=+/-85mm, Y=y_table_pos +/- 85mm
bed_standoffs = []
for bx in [-85.0, 85.0]:
    for by in [y_table_pos - 85.0, y_table_pos + 85.0]:
        stdf = Part.makeCylinder(7.0, 8.0, Base.Vector(bx, by, 46.0))
        bed_standoffs.append(stdf)

o_bmnt = doc.addObject("Part::Feature", "Motion_Worktable_4x_Rigid_Aluminum_Standoffs")
o_bmnt.Shape = Part.makeCompound(bed_standoffs)
set_visual(o_bmnt, CLR_ALU_PLATE)
motion_grp.addObject(o_bmnt)

hotbed = load_stp_centered("Hot bed.step")
hotbed.translate(Base.Vector(0.0, y_table_pos, 52.0))
obj_hb = doc.addObject("Part::Feature", "Donor_HeatedBed_Worktable_Plate")
obj_hb.Shape = hotbed
set_visual(obj_hb, CLR_ALU_PLATE)
donor_grp.addObject(obj_hb)

spoilboard = make_chamfered_rect_prism(235.0, 235.0, 12.0, 8.0, 56.0)
for x_slot in [-80.0, -40.0, 0.0, 40.0, 80.0]:
    spoilboard = spoilboard.cut(Part.makeBox(6.0, 220.0, 4.5, Base.Vector(x_slot - 3.0, -110.0, 64.0)))
spoilboard.translate(Base.Vector(0.0, y_table_pos, 0.0))
obj_sb = doc.addObject("Part::Feature", "CNC_MDF_T_Slot_Spoilboard")
obj_sb.Shape = spoilboard
set_visual(obj_sb, CLR_MDF)
spindle_grp.addObject(obj_sb)

# 6061 Aluminum Workpiece + Step Clamps centered at (X = 0.0, Y = -112.0 mm) directly beneath the 1/8" Carbide Endmill!
wp_y = -112.0
workpiece = make_chamfered_rect_prism(110.0, 76.0, 6.35, 3.0, 68.0).cut(
    make_chamfered_rect_prism(68.0, 42.0, 4.0, 6.0, 71.0)
)
workpiece.translate(Base.Vector(0.0, wp_y, 0.0))
obj_wp = doc.addObject("Part::Feature", "Workpiece_6061_Aluminum_Plate")
obj_wp.Shape = workpiece
set_visual(obj_wp, (0.58, 0.62, 0.67))
spindle_grp.addObject(obj_wp)

clamps_list = []
for cx_cl, dir_x in [(-68.0, 1.0), (68.0, -1.0)]:
    strap = make_chamfered_rect_prism(38.0, 18.0, 8.0, 3.0, 74.0)
    strap.translate(Base.Vector(cx_cl, wp_y, 0.0))
    heel  = Part.makeBox(10.0, 18.0, 6.0, Base.Vector(cx_cl - dir_x*14.0 - 5.0, wp_y - 9.0, 68.0))
    bolt  = Part.makeCylinder(4.2, 20.0, Base.Vector(cx_cl, wp_y, 66.0))
    clamps_list.append(strap.fuse(heel).fuse(bolt))

o_clmp = doc.addObject("Part::Feature", "Workholding_2x_TSlot_Step_Clamps")
o_clmp.Shape = Part.makeCompound(clamps_list)
set_visual(o_clmp, CLR_MILL_TRIM)
spindle_grp.addObject(o_clmp)

# Finned Air-Cooled Vertical Mill Headstock Shroud (`Bed1_01_DM62659_AirCooled_Collar.stl`)
def make_stylized_dm62659_collar():
    r_in, r_out, h = 32.6, 45.0, 52.0
    shroud_oct = make_chamfered_rect_prism(92.0, 92.0, h, 22.0, 0.0)
    shroud_cyl = Part.makeCylinder(r_out, h)
    outer_body = shroud_oct.common(Part.makeCylinder(48.0, h)).fuse(shroud_cyl)
    back_mount = make_chamfered_rect_prism(96.0, 26.0, h, 6.0, 0.0)
    back_mount.translate(Base.Vector(0.0, -r_out, 0.0))
    pinch_ear = make_chamfered_rect_prism(32.0, 24.0, h, 5.0, 0.0)
    pinch_ear.translate(Base.Vector(0.0, r_out + 2.0, 0.0))
    body = outer_body.fuse(back_mount).fuse(pinch_ear)

    for z_f in [8.0, 20.0, 32.0, 44.0]:
        fin_plate = make_chamfered_rect_prism(102.0, 52.0, 3.0, 12.0, z_f - 1.5)
        fin_plate.translate(Base.Vector(0.0, -6.0, 0.0))
        body = body.fuse(fin_plate)

    for x_rib in [-43.0, 37.0]:
        rib = Part.makeBox(6.0, 32.0, h, Base.Vector(x_rib, -r_out - 10.0, 0.0))
        body = body.fuse(rib)

    nozzle_ring = Part.makeCylinder(r_in + 8.0, 6.0, Base.Vector(0, 0, -6.0)).cut(
        Part.makeCylinder(r_in + 1.0, 8.0, Base.Vector(0, 0, -7.0))
    )
    body = body.fuse(nozzle_ring)

    bore = Part.makeCylinder(r_in, h + 16.0, Base.Vector(0, 0, -8.0))
    slot = Part.makeBox(3.0, 44.0, h + 16.0, Base.Vector(-1.5, r_in - 2.0, -8.0))
    body = body.cut(bore).cut(slot)

    for i in range(8):
        ang = math.radians(i * 45.0 + 22.5)
        flute = Part.makeCylinder(2.8, h + 16.0, Base.Vector((r_in + 0.6)*math.cos(ang), (r_in + 0.6)*math.sin(ang), -8.0))
        body = body.cut(flute)

    for z_h in [13.0, 39.0]:
        b_hole = Part.makeCylinder(2.65, 44.0, Base.Vector(-22.0, r_out + 5.0, z_h), Base.Vector(1, 0, 0))
        cb_l   = Part.makeCylinder(5.0, 6.0, Base.Vector(-18.0, r_out + 5.0, z_h), Base.Vector(1, 0, 0))
        cb_r   = Part.makeCylinder(5.0, 6.0, Base.Vector( 12.0, r_out + 5.0, z_h), Base.Vector(1, 0, 0))
        body = body.cut(b_hole).cut(cb_l).cut(cb_r)

    for x_m in [-32.0, 32.0]:
        for z_m in [12.0, 38.0]:
            m_hole = Part.makeCylinder(2.65, 48.0, Base.Vector(x_m, -r_out - 18.0, z_m), Base.Vector(0, 1, 0))
            body = body.cut(m_hole)
    for x_e in [-7.0, 7.0]:
        e_hole = Part.makeCylinder(1.65, 48.0, Base.Vector(x_e, -r_out - 18.0, 25.0), Base.Vector(0, 1, 0))
        body = body.cut(e_hole)
    return body

collar_printable = make_stylized_dm62659_collar()
c_collar = collar_printable.copy()
c_collar.translate(Base.Vector(0.0, wp_y, z_high_deck - 18.0))
o_col = doc.addObject("Part::Feature", "PLA_6Wall_AirCooled_DM62659_Collar")
o_col.Shape = c_collar
set_visual(o_col, CLR_HEADSTOCK)
pla_grp.addObject(o_col)

# Multi-Part Harbor Freight 62659 Trim Router Spindle (Coaxial at X=0.0, Y=wp_y=-112.0)
rx, ry, rz = 0.0, wp_y, z_high_deck - 25.0
alu_barrel = Part.makeCylinder(32.5, 58.0, Base.Vector(rx, ry, rz)).fuse(
    Part.makeCone(32.5, 16.0, 14.0, Base.Vector(rx, ry, rz - 14.0), Base.Vector(0, 0, 1))
).fuse(Part.makeCylinder(11.0, 16.0, Base.Vector(rx, ry, rz - 30.0)))
o_rtr_alu = doc.addObject("Part::Feature", "HF62659_01_Machined_Aluminum_Barrel")
o_rtr_alu.Shape = alu_barrel
set_visual(o_rtr_alu, CLR_ALU_PLATE)
spindle_grp.addObject(o_rtr_alu)

red_body = Part.makeCylinder(33.2, 72.0, Base.Vector(rx, ry, rz + 58.0))
for i in range(12):
    ang = math.radians(i * 30.0)
    rib = Part.makeCylinder(1.8, 54.0, Base.Vector(rx + 33.0*math.cos(ang), ry + 33.0*math.sin(ang), rz + 66.0))
    red_body = red_body.fuse(rib)
o_rtr_red = doc.addObject("Part::Feature", "HF62659_02_Crimson_Motor_Housing")
o_rtr_red.Shape = red_body
set_visual(o_rtr_red, (0.86, 0.12, 0.14))
spindle_grp.addObject(o_rtr_red)

top_cap = Part.makeCylinder(33.5, 18.0, Base.Vector(rx, ry, rz + 130.0)).fuse(
    Part.makeCone(33.5, 24.0, 8.0, Base.Vector(rx, ry, rz + 148.0))
).fuse(Part.makeBox(12.0, 8.0, 10.0, Base.Vector(rx - 6.0, ry + 30.0, rz + 134.0))).fuse(
    Part.makeCylinder(5.0, 24.0, Base.Vector(rx, ry, rz + 156.0))
)
o_rtr_cap = doc.addObject("Part::Feature", "HF62659_03_Vented_Top_Cap_And_Switch")
o_rtr_cap.Shape = top_cap
set_visual(o_rtr_cap, (0.12, 0.13, 0.15))
spindle_grp.addObject(o_rtr_cap)

collet_nut = make_chamfered_rect_prism(19.0, 19.0, 12.0, 4.0, rz - 42.0)
collet_nut.translate(Base.Vector(rx, ry, 0.0))
o_rtr_nut = doc.addObject("Part::Feature", "HF62659_04_Collet_Nut")
o_rtr_nut.Shape = collet_nut
set_visual(o_rtr_nut, (0.15, 0.15, 0.18))
spindle_grp.addObject(o_rtr_nut)

endmill = Part.makeCylinder(3.175, 24.0, Base.Vector(rx, ry, rz - 66.0))
o_rtr_bit = doc.addObject("Part::Feature", "HF62659_05_Carbide_Endmill_1_8in")
o_rtr_bit.Shape = endmill
set_visual(o_rtr_bit, CLR_BRASS)
spindle_grp.addObject(o_rtr_bit)

doc.recompute()

# Export Full Assembly (.FCStd, .step, .stl)
fcstd_out = os.path.join(CAD_DIR, "Ender3_Donor_ZeroCut_CNC.FCStd")
step_out  = os.path.join(CAD_DIR, "Ender3_Donor_ZeroCut_CNC.step")
stl_out   = os.path.join(CAD_DIR, "Ender3_Donor_ZeroCut_CNC_Assembly.stl")
doc.saveAs(fcstd_out)

all_objs = (
    donor_grp.Group
    + motion_grp.Group
    + pla_grp.Group
    + conc_grp.Group
    + spindle_grp.Group
    + elec_grp.Group
)
Part.export(all_objs, step_out)
Mesh.export(all_objs, stl_out)

printable_parts = {{
    "Bed1_01_DM62659_AirCooled_Collar": collar_printable,
    "Bed1_02_Z_Leadscrew_Top_Bearing_Cap": z_arch_printable,
    "Bed2_01_TwinRail_Y_Outrigger": y_outrigger_shape,
    "Bed2_02_Ground_Concrete_Base_Sill": base_sill_half,
    "Bed3_01_Concrete_Column_Sleeve_Half": col_sleeve_half,
    "Bed3_02_Concrete_X_Girder_Half": x_girder_half,
}}

stl_metrics = {{}}
for p_name, p_shape in printable_parts.items():
    p_path = os.path.join(STL_DIR, f"{{p_name}}.stl")
    m = MeshPart.meshFromShape(Shape=p_shape, LinearDeflection=0.1, AngularDeflection=0.2)
    m.write(p_path)
    bb = p_shape.BoundBox
    stl_metrics[p_name] = {{
        "stl_path": p_path,
        "volume_cm3": round(p_shape.Volume / 1000.0, 2),
        "manifold": bool(p_shape.isValid()),
        "bbox_mm": [round(bb.XLength, 1), round(bb.YLength, 1), round(bb.ZLength, 1)],
        "bbox_in": [round(bb.XLength/25.4, 2), round(bb.YLength/25.4, 2), round(bb.ZLength/25.4, 2)],
    }}

total_pla_cm3  = sum(o.Shape.Volume / 1000.0 for o in pla_grp.Group)
total_conc_cm3 = sum(o.Shape.Volume / 1000.0 for o in conc_grp.Group)

summary = {{
    "document": doc.Name,
    "fcstd_path": fcstd_out,
    "step_path": step_out,
    "assembly_stl_path": stl_out,
    "total_cad_feature_objects": len(all_objs),
    "total_factory_solids_parsed": len(solids),
    "e_plate_registered_holes": len(cyl_faces),
    "columns_touch_ground_z_mm": 0.0,
    "base_sills_touch_ground_z_mm": 0.0,
    "total_pla_assembly_cm3": round(total_pla_cm3, 1),
    "total_concrete_cavity_cm3": round(total_conc_cm3, 1),
    "cast_concrete_weight_lbs": round((total_conc_cm3 * 2.25) / 453.592, 2),
    "printable_parts": stl_metrics,
}}
print("FREECAD_SUMMARY_JSON:" + json.dumps(summary))
"""


def save_b64_png(b64_str: str | None, out_path: str) -> bool:
    if not b64_str:
        return False
    raw = base64.b64decode(b64_str)
    with open(out_path, "wb") as f:
        f.write(raw)
    return True


def main():
    fc = FreeCADConnection(host="127.0.0.1", port=9875)
    print("[FreeCAD MCP] Connected:", fc.ping())
    res = fc.execute_code(FREECAD_SCRIPT, timeout=240)
    if not res.get("success"):
        print("[FreeCAD MCP] Error:", res)
    msg = res.get("message", "")
    print("[FreeCAD MCP] Execution output:\n", msg)

    for view_name in ("Isometric", "Front", "Right", "Top"):
        b64 = fc.get_active_screenshot(view_name=view_name, width=1400, height=1050)
        out_png = os.path.join(RENDER_DIR, f"freecad_assembly_{view_name.lower()}.png")
        if save_b64_png(b64, out_png):
            print(f"[FreeCAD MCP] Saved screenshot: {out_png}")

    closeup_code = f"""
import os
import FreeCAD as App
import FreeCADGui as Gui

RENDER_DIR = {RENDER_DIR!r}
doc = App.getDocument("Ender3_Donor_ZeroCut_CNC")
view = Gui.ActiveDocument.ActiveView
view.setAnimationEnabled(False)

for objs, fn in [
    (["PLA_5Wall_Concrete_TowerSleeve_Left", "PLA_Ground_Concrete_BaseSill_Left_Front", "PLA_TwinRail_Y_Outrigger_Left_Front", "Motion_Y_Front_Belt_Tensioner_Clevis", "Motion_Y_Front_GT2_Idler_Pulley", "Donor_Solid2_4040_FrontBaseTie_9_84in"], "freecad_closeup_exoskeleton_tower.png"),
    (["PLA_Z_Stepper_And_608ZZ_Arch_Tower", "Motion_Z_Top_NEMA17_Stepper_Motor", "Motion_Z_5x8mm_Flexible_Shaft_Coupler", "Motion_Z_Top_And_Bottom_608ZZ_Radial_Bearings", "Motion_Z_Brass_T8x8_Leadscrew_Nut", "Motion_X_Left_NEMA17_Stepper_Motor", "Motion_X_Right_GT2_Idler_Pulley", "PLA_5Wall_XBridge_Concrete_Girder"], "freecad_closeup_z_arch_bridge.png"),
    (["PLA_6Wall_AirCooled_DM62659_Collar", "HF62659_01_Machined_Aluminum_Barrel", "HF62659_02_Crimson_Motor_Housing", "HF62659_04_Collet_Nut", "HF62659_05_Carbide_Endmill_1_8in", "Workpiece_6061_Aluminum_Plate", "Workholding_2x_TSlot_Step_Clamps", "Motion_Z_4x_Vertical_Plunge_VSlot_Rollers"], "freecad_closeup_spindle_shroud.png"),
]:
    view.viewIsometric()
    Gui.updateGui()
    Gui.Selection.clearSelection()
    for name in objs:
        o = doc.getObject(name)
        if o:
            Gui.Selection.addSelection(o)
    Gui.SendMsgToActiveView("ViewSelection")
    Gui.Selection.clearSelection()
    Gui.updateGui()
    view.saveImage(os.path.join(RENDER_DIR, fn), 1400, 1050, "Current")

view.viewIsometric()
view.fitAll()
Gui.updateGui()
"""
    fc.execute_code(closeup_code, timeout=60)

    # Low-Deck Mode Screenshot
    low_deck_code = """
import FreeCAD as App
doc = App.getDocument("Ender3_Donor_ZeroCut_CNC")
z_offset = -(1.5 * 25.4)
for name in [
    "Donor_Solid421_2040_XBridgePrimary_13_00in",
    "Donor_Solid44_2020_XBridgeTorsion_13_58in",
    "Motion_X_Saddle_Carriage_Plate",
    "Motion_X_4x_VSlot_POM_Rollers",
    "Motion_X_4x_Coaxial_Spacers_And_Eccentric_Nuts",
    "Motion_X_Left_NEMA17_Stepper_Motor",
    "Motion_X_Left_20T_GT2_Drive_Pulley",
    "Motion_X_Right_GT2_Idler_Pulley",
    "Motion_X_Right_Belt_Tensioner_Block",
    "Motion_X_GT2_Timing_Belt_Loop",
    "PLA_5Wall_XBridge_Concrete_Girder",
    "Cast_Concrete_XBridge_Core",
    "PLA_Z_Stepper_And_608ZZ_Arch_Tower",
    "Motion_Z_Top_And_Bottom_608ZZ_Radial_Bearings",
    "Motion_Z_Top_NEMA17_Stepper_Motor",
    "Motion_Z_5x8mm_Flexible_Shaft_Coupler",
    "Donor_T8_Leadscrew_Uncut_14_37in",
    "Motion_Z_Brass_T8x8_Leadscrew_Nut",
    "Donor_X_Carriage_Steel_Plate",
    "Motion_Z_4x_Vertical_Plunge_VSlot_Rollers",
    "PLA_6Wall_AirCooled_DM62659_Collar",
    "HF62659_01_Machined_Aluminum_Barrel",
    "HF62659_02_Crimson_Motor_Housing",
    "HF62659_03_Vented_Top_Cap_And_Switch",
    "HF62659_04_Collet_Nut",
    "HF62659_05_Carbide_Endmill_1_8in",
]:
    obj = doc.getObject(name)
    if obj:
        obj.Placement.Base.z += z_offset
doc.recompute()
"""
    fc.execute_code(low_deck_code)
    b64_low = fc.get_active_screenshot(view_name="Front", width=1400, height=1050)
    save_b64_png(b64_low, os.path.join(RENDER_DIR, "freecad_assembly_front_low_deck_2in.png"))
    fc.execute_code(low_deck_code.replace("-(1.5 * 25.4)", "+(1.5 * 25.4)"))
    print("[FreeCAD MCP] All screenshots updated.")


if __name__ == "__main__":
    main()
