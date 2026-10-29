#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
Decompose Official Creality Ender 3 STEP Assembly & Rebuild as Zero-Cut CNC
-------------------------------------------------------------------------------
Reads `ender3_cad_repo/Ender-3 Mechanical/STP/01 MAIN ASM Ender_3.STEP` and
individual factory STEP files, breaks apart the 8 uncut aluminum extrusions
and motion hardware, and reassembles them with the 1-Roll PLA+ & Concrete
Ballast kit + Harbor Freight 62659 1/4" Trim Router.
===============================================================================
"""

import os
import sys
import math
import FreeCAD as App
import Part
import Mesh
from FreeCAD import Base

STP_DIR = "ender3_cad_repo/Ender-3 Mechanical/STP"
OUT_DIR = "stl_exports_zerocut"
os.makedirs(OUT_DIR, exist_ok=True)


def normalize_shape_to_origin(shape):
    """Centers X and Y at 0, and puts ZMin at 0 for clean parametric placement."""
    s = shape.copy()
    bb = s.BoundBox
    cx = (bb.XMin + bb.XMax) / 2.0
    cy = (bb.YMin + bb.YMax) / 2.0
    s.translate(Base.Vector(-cx, -cy, -bb.ZMin))
    return s


def load_stp_centered(filename):
    path = os.path.join(STP_DIR, filename)
    s = Part.Shape()
    s.read(path)
    return normalize_shape_to_origin(s)


def build_donor_cnc():
    doc = App.newDocument("Ender3_Donor_ZeroCut_CNC")

    donor_grp = doc.addObject("App::DocumentObjectGroup", "01_Reused_Ender3_Factory_Parts")
    pla_grp   = doc.addObject("App::DocumentObjectGroup", "02_Printable_PLA_Plus_Parts")
    conc_grp  = doc.addObject("App::DocumentObjectGroup", "03_Cast_Concrete_Cores_5_8lbs")
    spindle_grp = doc.addObject("App::DocumentObjectGroup", "04_HarborFreight_62659_Spindle")

    print("[1/5] Breaking apart `01 MAIN ASM Ender_3.STEP` (655 factory solids)...")
    main_asm = Part.Shape()
    main_asm.read(os.path.join(STP_DIR, "01 MAIN ASM Ender_3.STEP"))
    solids = main_asm.Solids

    # Extract genuine factory extrusions from 01 MAIN ASM Ender_3.STEP:
    # Solid[4], Solid[5] : 2x 400mm (15.75") 2040 Z-uprights -> Now Twin Y-Bed Rails!
    # Solid[0], Solid[1] : 2x 290mm (11.42") 4040 Base Rails -> Now Heavy Vertical Gantry Columns!
    # Solid[2]           : 1x 250mm ( 9.84") 4040 Crossbar   -> Now Front Heavy Base Cross-Tie!
    # Solid[421]         : 1x 330mm (13.00") 2040 Y-Spine    -> Now Rear Base Cross-Tie!
    # Solid[44]          : 1x 345mm (13.58") 2020 X-Gantry   -> Now Primary X-Bridge Rail!
    # Solid[3]           : 1x 330mm (13.00") 2020 Top Bar    -> Now Secondary X-Bridge Torsion Rail!
    # Solid[646]         : 24V 15A Power Supply

    # 1. TWIN 15.75" (400mm) 2040 Y-AXIS BED RAILS (Extracted from Solid[4] & Solid[5])
    for idx, (sol_id, side, x_pos) in enumerate([(4, "Left", -135.0), (5, "Right", 135.0)]):
        s_rail = normalize_shape_to_origin(solids[sol_id])
        # In main asm, Solid[4/5] is X=40, Y=400, Z=20 -> already aligned along Y (400mm)!
        s_rail.translate(Base.Vector(x_pos, 0.0, 20.0))
        obj = doc.addObject("Part::Feature", f"Donor_Solid{sol_id}_2040_TwinY_{side}_15_75in")
        obj.Shape = s_rail
        donor_grp.addObject(obj)

    # 2. FRONT 4040 CROSS-TIE (Solid[2], 250mm / 9.84") & REAR 2040 CROSS-TIE (Solid[421], 330mm / 13.00")
    s_front = normalize_shape_to_origin(solids[2]) # X=250, Y=40, Z=40
    s_front.translate(Base.Vector(0.0, -180.0, 0.0))
    obj_f = doc.addObject("Part::Feature", "Donor_Solid2_4040_FrontBaseTie_9_84in")
    obj_f.Shape = s_front
    donor_grp.addObject(obj_f)

    s_rear = normalize_shape_to_origin(solids[421]) # X=20, Y=40, Z=330 -> rotate to lie along X
    s_rear.rotate(Base.Vector(0, 0, 0), Base.Vector(0, 1, 0), 90)
    s_rear = normalize_shape_to_origin(s_rear)
    s_rear.translate(Base.Vector(0.0, 180.0, 0.0))
    obj_r = doc.addObject("Part::Feature", "Donor_Solid421_2040_RearBaseTie_13_00in")
    obj_r.Shape = s_rear
    donor_grp.addObject(obj_r)

    # 3. TWO HEAVY 4040 VERTICAL GANTRY COLUMNS (Extracted from Solid[0] & Solid[1], 290mm / 11.42")
    # In main asm, Solid[0/1] is X=40.4, Y=40.4, Z=290.0 -> already standing vertically along Z (290mm)!
    for sol_id, side, x_col in [(1, "Left", -155.0), (0, "Right", 155.0)]:
        s_col = normalize_shape_to_origin(solids[sol_id])
        s_col.translate(Base.Vector(x_col, -10.0, 40.0))
        obj_c = doc.addObject("Part::Feature", f"Donor_Solid{sol_id}_4040_GantryCol_{side}_11_42in")
        obj_c.Shape = s_col
        donor_grp.addObject(obj_c)

    # 4. DUAL-BEAM X-BRIDGE: Solid[44] (345mm / 13.58" 2020 X-Rail) + Solid[3] (330mm / 13.00" 2020 Top Bar)
    z_high_deck = 40.0 + 88.9 + 35.0  # 3.5" (88.9mm) Z-clearance above spoilboard
    s_xmain = normalize_shape_to_origin(solids[44]) # X=345, Y=20, Z=20
    s_xmain.translate(Base.Vector(0.0, -42.0, z_high_deck))
    obj_xm = doc.addObject("Part::Feature", "Donor_Solid44_2020_XBridgePrimary_13_58in")
    obj_xm.Shape = s_xmain
    donor_grp.addObject(obj_xm)

    s_xback = normalize_shape_to_origin(solids[3]) # X=330, Y=20, Z=20
    s_xback.translate(Base.Vector(0.0, -2.0, z_high_deck + 22.0))
    obj_xb = doc.addObject("Part::Feature", "Donor_Solid3_2020_XBridgeTorsion_13_00in")
    obj_xb.Shape = s_xback
    donor_grp.addObject(obj_xb)

    # 5. REUSED ENDER 3 MOTION HARDWARE (Bed, Y-Plate, X-Carriage E-Plate, Steppers, Leadscrew, Rollers, PSU)
    print("[2/5] Placing genuine Ender 3 motion plates, NEMA 17 steppers, V-rollers & leadscrew...")
    y_plate = load_stp_centered("Y plate.step")
    y_plate.translate(Base.Vector(0.0, 0.0, 42.0))
    obj_yp = doc.addObject("Part::Feature", "Donor_Y_Carriage_Plate")
    obj_yp.Shape = y_plate
    donor_grp.addObject(obj_yp)

    hotbed = load_stp_centered("Hot bed.step")
    hotbed.translate(Base.Vector(0.0, 0.0, 50.0))
    obj_hb = doc.addObject("Part::Feature", "Donor_HeatedBed_Worktable_Plate")
    obj_hb.Shape = hotbed
    donor_grp.addObject(obj_hb)

    e_plate = load_stp_centered("E plate.step")
    e_plate.rotate(Base.Vector(0, 0, 0), Base.Vector(1, 0, 0), 90)
    e_plate = normalize_shape_to_origin(e_plate)
    e_plate.translate(Base.Vector(0.0, -56.0, z_high_deck - 18.0))
    obj_ep = doc.addObject("Part::Feature", "Donor_X_Carriage_Steel_Plate")
    obj_ep.Shape = e_plate
    donor_grp.addObject(obj_ep)

    leadscrew = load_stp_centered("Z threaded rod.step")
    leadscrew.translate(Base.Vector(0.0, -52.0, z_high_deck - 45.0))
    obj_ls = doc.addObject("Part::Feature", "Donor_T8_Leadscrew_Uncut_14_37in")
    obj_ls.Shape = leadscrew
    donor_grp.addObject(obj_ls)

    motor_shape = load_stp_centered("42-34 motor.step")
    for m_name, pos in [
        ("Donor_NEMA17_X_Motor", Base.Vector(-185.0, -42.0, z_high_deck - 10.0)),
        ("Donor_NEMA17_Y_Motor", Base.Vector(0.0, -210.0, 10.0)),
        ("Donor_NEMA17_Z_Motor", Base.Vector(0.0, -52.0, 315.0)),
        ("Donor_NEMA17_DualY_Sync_FromExtruder", Base.Vector(0.0, 210.0, 10.0)),
    ]:
        m_inst = motor_shape.copy()
        m_inst.translate(pos)
        obj_m = doc.addObject("Part::Feature", m_name)
        obj_m.Shape = m_inst
        donor_grp.addObject(obj_m)

    psu = normalize_shape_to_origin(solids[646])
    psu.translate(Base.Vector(215.0, 40.0, 0.0))
    obj_psu = doc.addObject("Part::Feature", "Donor_Solid646_24V15A_PSU")
    obj_psu.Shape = psu
    donor_grp.addObject(obj_psu)

    # 6. GENERATE CUSTOM PLA+ SLEEVES, CONCRETE CORES & AIR-COOLED ROUTER COLLAR
    print("[3/5] Generating 5-wall PLA+ Concrete Sleeves, X-Girder & Air-Cooled Router Collar...")
    wall = 2.25  # 0.089" (5 perimeters)
    # Column Concrete Sleeves enclosing the 4040 columns (40.4 x 40.4mm inner chimney, 84 x 84mm outer)
    col_outer = Part.makeBox(84.0, 84.0, 280.0, Base.Vector(-42.0, -42.0, 0))
    col_void  = Part.makeBox(84.0 - 2*wall, 84.0 - 2*wall, 280.0 - 2*wall,
                             Base.Vector(-42.0 + wall, -42.0 + wall, wall))
    col_chimney_w = Part.makeBox(40.6 + 2*wall, 40.6 + 2*wall, 280.0,
                                 Base.Vector(-20.3 - wall, -20.3 - wall, 0))
    col_chimney_v = Part.makeBox(40.6, 40.6, 282.0, Base.Vector(-20.3, -20.3, -1.0))
    pour_port = Part.makeCylinder(12.7, 10.0, Base.Vector(0, 28.0, 275.0)) # 1.00" pour funnel
    col_sleeve = col_outer.cut(col_void).fuse(col_chimney_w).cut(col_chimney_v).cut(pour_port)
    col_concrete_core = col_void.cut(col_chimney_w)

    for side, x_col in [("Left", -155.0), ("Right", 155.0)]:
        slv = col_sleeve.copy()
        slv.translate(Base.Vector(x_col, -10.0, 40.0))
        o_slv = doc.addObject("Part::Feature", f"PLA_5Wall_Concrete_TowerSleeve_{side}")
        o_slv.Shape = slv
        pla_grp.addObject(o_slv)

        core = col_concrete_core.copy()
        core.translate(Base.Vector(x_col, -10.0, 40.0))
        o_core = doc.addObject("Part::Feature", f"Cast_Concrete_ColumnCore_{side}")
        o_core.Shape = core
        conc_grp.addObject(o_core)

    # X-Bridge Concrete Torsion Girder tying Solid[44] (Primary 2020) and Solid[3] (Upper Torsion 2020)
    xg_outer = Part.makeBox(320.0, 52.0, 62.0, Base.Vector(-160.0, -32.0, z_high_deck - 8.0))
    xg_void  = Part.makeBox(320.0 - 2*wall, 52.0 - 2*wall, 62.0 - 2*wall,
                            Base.Vector(-160.0 + wall, -32.0 + wall, z_high_deck - 8.0 + wall))
    xg_pour  = Part.makeCylinder(12.7, 10.0, Base.Vector(-75.0, -6.0, z_high_deck + 48.0))
    xg_shell = xg_outer.cut(xg_void).cut(xg_pour).cut(s_xmain).cut(s_xback)
    o_xg = doc.addObject("Part::Feature", "PLA_5Wall_XBridge_Concrete_Girder")
    o_xg.Shape = xg_shell
    pla_grp.addObject(o_xg)

    o_xg_core = doc.addObject("Part::Feature", "Cast_Concrete_XBridge_Core")
    o_xg_core.Shape = xg_void.cut(s_xmain).cut(s_xback)
    conc_grp.addObject(o_xg_core)

    # Air-Cooled Harbor Freight Drill Master 62659 Collar + Router Spindle
    r_in, r_out, h_col = 32.6, 44.0, 50.0
    c_body = Part.makeCylinder(r_out, h_col).fuse(
        Part.makeBox(88.0, 26.0, h_col, Base.Vector(-44.0, -r_out - 8.0, 0))
    )
    c_bore = Part.makeCylinder(r_in, h_col + 2.0, Base.Vector(0, 0, -1.0))
    c_slot = Part.makeBox(3.0, 30.0, h_col + 2.0, Base.Vector(-1.5, r_in - 2.0, -1.0))
    c_collar = c_body.cut(c_bore).cut(c_slot)
    for i in range(8):
        ang = math.radians(i * 45.0 + 22.5)
        flute = Part.makeCylinder(2.5, h_col + 2.0,
                                  Base.Vector((r_in + 0.5)*math.cos(ang), (r_in + 0.5)*math.sin(ang), -1.0))
        c_collar = c_collar.cut(flute)
    c_collar.translate(Base.Vector(0.0, -102.0, z_high_deck - 18.0))
    o_col = doc.addObject("Part::Feature", "PLA_6Wall_AirCooled_DM62659_Collar")
    o_col.Shape = c_collar
    pla_grp.addObject(o_col)

    rtr = Part.makeCylinder(32.5, 140.0, Base.Vector(0.0, -102.0, z_high_deck - 25.0)).fuse(
        Part.makeCylinder(9.5, 26.0, Base.Vector(0.0, -102.0, z_high_deck - 51.0))
    ).fuse(
        Part.makeCylinder(3.175, 25.0, Base.Vector(0.0, -102.0, z_high_deck - 76.0))
    )
    o_rtr = doc.addObject("Part::Feature", "HarborFreight_62659_TrimRouter_1_4in")
    o_rtr.Shape = rtr
    spindle_grp.addObject(o_rtr)

    print("[4/5] Recomputing FreeCAD Document & Calculating Concrete + PLA+ Volumes...")
    doc.recompute()

    total_pla_cm3 = sum(o.Shape.Volume / 1000.0 for o in pla_grp.Group)
    total_conc_cm3 = sum(o.Shape.Volume / 1000.0 for o in conc_grp.Group)
    print(f"  -> Total PLA+ Shell & Structural Volume: {total_pla_cm3:.1f} cm^3")
    print(f"  -> Total Internal Concrete Cavity Volume: {total_conc_cm3:.1f} cm^3 ({total_conc_cm3/16.387:.1f} in^3)")
    print(f"  -> Cast Screened Concrete Weight (@ 2.25 g/cm^3): {(total_conc_cm3 * 2.25)/453.592:.2f} lbs")

    fcstd_out = os.path.join(OUT_DIR, "Ender3_Donor_ZeroCut_CNC.FCStd")
    step_out  = os.path.join(OUT_DIR, "Ender3_Donor_ZeroCut_CNC.step")
    stl_out   = os.path.join(OUT_DIR, "Ender3_Donor_ZeroCut_CNC_Assembly.stl")
    doc.saveAs(fcstd_out)

    all_objs = donor_grp.Group + pla_grp.Group + conc_grp.Group + spindle_grp.Group
    Part.export(all_objs, step_out)
    Mesh.export(all_objs, stl_out)
    print(f"[5/5] Saved FreeCAD Assembly: {fcstd_out}")
    print(f"      Saved STEP Assembly:    {step_out}")
    print(f"      Saved STL Assembly:     {stl_out}")


if __name__ == "__main__":
    build_donor_cnc()
    os._exit(0)
