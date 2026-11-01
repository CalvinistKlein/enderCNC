#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clean Start — 3 Ways to Lay Out the 8 Uncut Ender 3 Aluminum Extrusions
for a 3" x 10" x 9" (76.2 mm x 254.0 mm x 228.6 mm) Build Volume.

Each layout uses ONLY the exact 8 uncut aluminum extrusions from `01 MAIN ASM Ender_3.STEP`:
  - 2x 4040 x 290 mm (`Solid[0]`, `Solid[1]`)  [Charcoal-Slate]
  - 1x 4040 x 250 mm (`Solid[2]`)              [Charcoal-Slate]
  - 2x 2040 x 400 mm (`Solid[4]`, `Solid[5]`)  [Steel-Blue]
  - 1x 2040 x 330 mm (`Solid[421]`)            [Steel-Blue]
  - 1x 2020 x 345 mm (`Solid[44]`)             [Amber-Gold]
  - 1x 2020 x 330 mm (`Solid[3]`)              [Amber-Gold]

Plus:
  - Translucent Worktable Reference Surface (where the spoilboard/workpiece sits)
  - Transparent 3" x 10" x 9" (76.2 x 254.0 x 228.6 mm) Predicted Build Volume Box
"""

import os
import json
from freecad_mcp.freecad_client import FreeCADConnection

PROJECT_DIR = "/home/calvin/.gemini/antigravity/scratch/ender3-router-project"
STP_PATH    = os.path.join(PROJECT_DIR, "ender3_cad_repo/Ender-3 Mechanical/STP/01 MAIN ASM Ender_3.STEP")
RENDER_DIR  = os.path.join(PROJECT_DIR, "renders")
CAD_DIR     = os.path.join(PROJECT_DIR, "cad")
os.makedirs(RENDER_DIR, exist_ok=True)
os.makedirs(CAD_DIR, exist_ok=True)

FREECAD_CODE = f"""
import os, json
import FreeCAD as App
import FreeCADGui as Gui
import Part
from FreeCAD import Base

STP_PATH   = {STP_PATH!r}
RENDER_DIR = {RENDER_DIR!r}
CAD_DIR    = {CAD_DIR!r}

for doc_name in list(App.listDocuments().keys()):
    App.closeDocument(doc_name)

main_asm = Part.Shape()
main_asm.read(STP_PATH)
solids = main_asm.Solids

def norm_origin(shape):
    s = shape.copy()
    bb = s.BoundBox
    cx = (bb.XMin + bb.XMax) / 2.0
    cy = (bb.YMin + bb.YMax) / 2.0
    s.translate(Base.Vector(-cx, -cy, -bb.ZMin))
    return s

# Canonicalized 8 Donor Extrusions (centered in X, Y with ZMin = 0.0):
# 1) 4040 x 290 mm (vertical Z = 0..290, X = -20..20, Y = -20..20)
ext_4040_290_A = norm_origin(solids[0])
ext_4040_290_B = norm_origin(solids[1])

# 2) 4040 x 250 mm (along X = -125..125, Y = -20..20, Z = 0..40)
ext_4040_250 = norm_origin(solids[2])

# 3) 2040 x 400 mm (along Y = -200..200, X = -20..20, Z = 0..20)
ext_2040_400_A = norm_origin(solids[4])
ext_2040_400_B = norm_origin(solids[5])

# 4) 2040 x 330 mm (native is vertical Z = 0..330, X = -10..10, Y = -20..20)
ext_2040_330_vert = norm_origin(solids[421])
# Also prepare horizontal-X version (X = -165..165, Y = -10..10, Z = 0..40):
ext_2040_330_horiz_x = ext_2040_330_vert.copy()
ext_2040_330_horiz_x.rotate(Base.Vector(0,0,0), Base.Vector(0,1,0), 90)
ext_2040_330_horiz_x.rotate(Base.Vector(0,0,0), Base.Vector(1,0,0), 90)
ext_2040_330_horiz_x = norm_origin(ext_2040_330_horiz_x)

# 5) 2020 x 345 mm (along X = -172.5..172.5, Y = -10..10, Z = 0..20)
ext_2020_345 = norm_origin(solids[44])

# 6) 2020 x 330 mm (along X = -165..165, Y = -10..10, Z = 0..20)
ext_2020_330 = norm_origin(solids[3])

# Distinct High-Contrast Colors by Extrusion Series + Transparent Build Volume:
CLR_4040     = (0.22, 0.26, 0.32)  # Heavy 4040 Extrusions (Charcoal-Slate)
CLR_2040     = (0.18, 0.52, 0.82)  # Medium 2040 Extrusions (Industrial Steel-Blue)
CLR_2020     = (0.90, 0.62, 0.14)  # Light 2020 Extrusions (Amber-Gold)
CLR_BED      = (0.75, 0.78, 0.82)  # Reference Worktable Surface
CLR_BUILDVOL = (0.00, 0.90, 0.76)  # Transparent 3" x 10" x 9" Build Volume Box (Cyan-Emerald)

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

def place(shape, x=0.0, y=0.0, z=0.0):
    s = shape.copy()
    s.translate(Base.Vector(x, y, z))
    return s

def make_build_vol_box(wx_mm, wy_mm, wz_mm, cx, cy, z0):
    return Part.makeBox(wx_mm, wy_mm, wz_mm, Base.Vector(cx - wx_mm/2.0, cy - wy_mm/2.0, z0))

# Target Build Area Dimensions in mm:
# 10.0 in = 254.0 mm, 9.0 in = 228.6 mm, 3.0 in = 76.2 mm
IN_10 = 254.0
IN_9  = 228.6
IN_3  = 76.2

# ===========================================================================
# BUILD ALL 3 LAYOUTS IN SEPARATE GROUPS SO WE CAN RENDER INDIVIDUAL & SIDE-BY-SIDE VIEWS
# ===========================================================================
doc = App.newDocument("Ender3_3_Extrusion_Layouts_Comparison")

# ---------------------------------------------------------------------------
# LAYOUT 1: FIXED-BRIDGE PORTAL MILL (Moving-Y Table on Twin 2040x400, 4040 Columns, 4040+2040 X-Bridge)
# Build Volume: 10.0" (X = 254.0 mm) x 9.0" (Y = 228.6 mm) x 3.0" (Z = 76.2 mm)
# ---------------------------------------------------------------------------
g1 = doc.addObject("App::DocumentObjectGroup", "Layout_1_Fixed_Portal_Moving_Table")

# 2x 2040x400 mm Twin Y-Ways (flat at Z = 20..40 mm, X = +/-95 mm)
add_part(doc, g1, "L1_2040x400_TwinY_Left",  place(ext_2040_400_A, -95.0, 0.0, 20.0), CLR_2040)
add_part(doc, g1, "L1_2040x400_TwinY_Right", place(ext_2040_400_B,  95.0, 0.0, 20.0), CLR_2040)

# 1x 2020x345 mm Front Base Tie + 1x 2020x330 mm Rear Base Tie (at Z = 0..20 mm)
add_part(doc, g1, "L1_2020x345_FrontBaseTie", place(ext_2020_345, 0.0, -190.0, 0.0), CLR_2020)
add_part(doc, g1, "L1_2020x330_RearBaseTie",  place(ext_2020_330, 0.0,  190.0, 0.0), CLR_2020)

# 2x 4040x290 mm Vertical Portal Columns (at stock Ender 3 X = +/-145 mm, Y = 20 mm, Z = 0..290 mm)
add_part(doc, g1, "L1_4040x290_Col_Left",  place(ext_4040_290_A, -145.0, 20.0, 0.0), CLR_4040)
add_part(doc, g1, "L1_4040x290_Col_Right", place(ext_4040_290_B,  145.0, 20.0, 0.0), CLR_4040)

# 1x 4040x250 mm Inner X-Bridge Core (bolted between columns at X = -125..125, Y = 20, Z = 175..215 mm)
add_part(doc, g1, "L1_4040x250_XBridge_InnerCore", place(ext_4040_250, 0.0, 20.0, 175.0), CLR_4040)

# 1x 2040x330 mm Primary Front X-Bridge Way (bolted across front of columns at X = -165..165, Y = -10, Z = 175..215 mm)
add_part(doc, g1, "L1_2040x330_XBridge_FrontWay", place(ext_2040_330_horiz_x, 0.0, -10.0, 175.0), CLR_2040)

# Worktable Reference Plane (260 x 240 x 6 mm at Z = 44..50 mm, centered under spindle at Y = -35 mm)
add_part(doc, g1, "L1_Ref_Worktable_Surface", make_build_vol_box(260.0, 240.0, 6.0, 0.0, -35.0, 44.0), CLR_BED, transparency=50)

# Transparent Predicted Build Volume: 10.0" (X = 254.0 mm) x 9.0" (Y = 228.6 mm) x 3.0" (Z = 76.2 mm)
# Location: X = [-127.0, +127.0], Y = [-149.3, +79.3] (centered under front-mounted spindle nose at Y = -35 mm), Z = [50.0, 126.2]
add_part(doc, g1, "L1_Predicted_Build_Volume_10x9x3in",
         make_build_vol_box(IN_10, IN_9, IN_3, 0.0, -35.0, 50.0),
         CLR_BUILDVOL, transparency=65, line_rgb=(0.0, 1.0, 0.85), line_width=2.8)


# ---------------------------------------------------------------------------
# LAYOUT 2: MOVING-GANTRY ROUTER TABLE (Stationary Bed Frame, Moving 4040 Portal Gantry + 2040 X-Bridge)
# Build Volume: 9.0" (X = 228.6 mm) x 10.0" (Y = 254.0 mm) x 3.0" (Z = 76.2 mm)
# ---------------------------------------------------------------------------
g2 = doc.addObject("App::DocumentObjectGroup", "Layout_2_Moving_Gantry_Stationary_Bed")

# 1x 2020x345 mm Front Stationary Base Tie + 1x 2020x330 mm Rear Stationary Base Tie (at Z = 0..20 mm, Y = +/-190 mm)
add_part(doc, g2, "L2_2020x345_FrontBaseTie", place(ext_2020_345, 0.0, -190.0, 0.0), CLR_2020)
add_part(doc, g2, "L2_2020x330_RearBaseTie",  place(ext_2020_330, 0.0,  190.0, 0.0), CLR_2020)

# 2x 2040x400 mm Stationary Left & Right Y-Axis Side Ways (flat at Z = 20..40 mm, X = +/-145 mm, outer width = 330 mm, inner bed span = 250 mm)
add_part(doc, g2, "L2_2040x400_Left_YWay",  place(ext_2040_400_A, -145.0, 0.0, 20.0), CLR_2040)
add_part(doc, g2, "L2_2040x400_Right_YWay", place(ext_2040_400_B,  145.0, 0.0, 20.0), CLR_2040)

# 1x 4040x250 mm Central Stationary Worktable Spine bolted between the 2040x400 Y-ways (X = -125..125, Y = -60, Z = 0..40 mm, flush at Z = 40 mm!)
add_part(doc, g2, "L2_4040x250_CenterBedSpine", place(ext_4040_250, 0.0, -60.0, 0.0), CLR_4040)

# 2x 4040x290 mm Moving Gantry Vertical Columns riding on top of the stationary 2040x400 Y-ways (X = +/-145 mm, Y = 30 mm, Z = 40..330 mm)
add_part(doc, g2, "L2_4040x290_MovingGantryCol_Left",  place(ext_4040_290_A, -145.0, 30.0, 40.0), CLR_4040)
add_part(doc, g2, "L2_4040x290_MovingGantryCol_Right", place(ext_4040_290_B,  145.0, 30.0, 40.0), CLR_4040)

# 1x 2040x330 mm Moving X-Gantry Crossbar bolted across the front face of the moving 4040x290 columns (X = -165..165, Y = 0 mm, Z = 175..215 mm)
add_part(doc, g2, "L2_2040x330_MovingXBridge", place(ext_2040_330_horiz_x, 0.0, 0.0, 175.0), CLR_2040)

# Stationary Worktable Reference Plane (246 x 270 x 6 mm at Z = 40..46 mm)
add_part(doc, g2, "L2_Ref_Stationary_Worktable", make_build_vol_box(246.0, 270.0, 6.0, 0.0, 0.0, 40.0), CLR_BED, transparency=50)

# Transparent Predicted Build Volume: 9.0" (X = 228.6 mm) x 10.0" (Y = 254.0 mm) x 3.0" (Z = 76.2 mm)
# Location: Stationary in the center of the bed between the 4040 gantry legs! X = [-114.3, +114.3], Y = [-127.0, +127.0], Z = [46.0, 122.2]
add_part(doc, g2, "L2_Predicted_Build_Volume_9x10x3in",
         make_build_vol_box(IN_9, IN_10, IN_3, 0.0, 0.0, 46.0),
         CLR_BUILDVOL, transparency=65, line_rgb=(0.0, 1.0, 0.85), line_width=2.8)


# ---------------------------------------------------------------------------
# LAYOUT 3: HIGH-RAIL "BOX-CAGE" GANTRY MILL (Elevated Twin 2040x400 Y-Rails on 4040 Columns, Zero-Riser 4040x250 Moving X-Bridge)
# Build Volume: 9.0" (X = 228.6 mm) x 10.0" (Y = 254.0 mm) x 3.0" (Z = 76.2 mm)
# ---------------------------------------------------------------------------
g3 = doc.addObject("App::DocumentObjectGroup", "Layout_3_HighRail_BoxCage_Mill")

# 2x 4040x290 mm Vertical Side Columns at X = +/-145 mm (X = -165..-125 and +125..+165, clear inner gap = 250 mm!), Y = 0 mm, Z = 0..290 mm
add_part(doc, g3, "L3_4040x290_MidColumn_Left",  place(ext_4040_290_A, -145.0, 0.0, 0.0), CLR_4040)
add_part(doc, g3, "L3_4040x290_MidColumn_Right", place(ext_4040_290_B,  145.0, 0.0, 0.0), CLR_4040)

# 1x 2040x330 mm Lower Bed Crossbar bolted across the bottom front face of the two 4040 columns at Z = 0..40 mm (X = -165..165, Y = -30 mm)
add_part(doc, g3, "L3_2040x330_LowerBedCrossbar", place(ext_2040_330_horiz_x, 0.0, -30.0, 0.0), CLR_2040)

# 2x 2040x400 mm ELEVATED Top Y-Ways (oriented 40 mm vertical Z = 150..190 mm, X = +/-115 mm [spanning X = -125..-105 and +105..+125], Y = -200..+200 mm)
# Bolted directly against the inner faces (X = +/-125 mm) of the two 4040x290 columns!
s_2040_400_tall = ext_2040_400_A.copy()
s_2040_400_tall.rotate(Base.Vector(0,0,0), Base.Vector(0,1,0), 90)
s_2040_400_tall = norm_origin(s_2040_400_tall)
add_part(doc, g3, "L3_2040x400_Elevated_YWay_Left",  place(s_2040_400_tall, -115.0, 0.0, 150.0), CLR_2040)
add_part(doc, g3, "L3_2040x400_Elevated_YWay_Right", place(s_2040_400_tall,  115.0, 0.0, 150.0), CLR_2040)

# 1x 2020x345 mm Front Top Halo Tie + 1x 2020x330 mm Rear Top Halo Tie (tying the ends of the elevated 2040x400 Y-rails at Z = 190..210 mm!)
add_part(doc, g3, "L3_2020x345_FrontTopHaloTie", place(ext_2020_345, 0.0, -190.0, 190.0), CLR_2020)
add_part(doc, g3, "L3_2020x330_RearTopHaloTie",  place(ext_2020_330, 0.0,  190.0, 190.0), CLR_2020)

# 1x 4040x250 mm Zero-Riser Moving X-Bridge riding directly on top of the elevated 2040x400 Y-rails (X = -125..+125 mm, Z = 190..230 mm, Y = -40 mm)
# Passes cleanly between the inner faces (X = +/-125 mm) of the 4040x290 columns across the entire Y stroke!
add_part(doc, g3, "L3_4040x250_ZeroRiser_MovingXBridge", place(ext_4040_250, 0.0, -40.0, 190.0), CLR_4040)

# Stationary Worktable Reference Plane (240 x 280 x 6 mm at Z = 40..46 mm)
add_part(doc, g3, "L3_Ref_Stationary_Worktable", make_build_vol_box(240.0, 280.0, 6.0, 0.0, 0.0, 40.0), CLR_BED, transparency=50)

# Transparent Predicted Build Volume: 9.0" (X = 228.6 mm) x 10.0" (Y = 254.0 mm) x 3.0" (Z = 76.2 mm)
# Location: Nested inside the High-Rail Box Cage at X = [-114.3, +114.3], Y = [-127.0, +127.0], Z = [46.0, 122.2]
add_part(doc, g3, "L3_Predicted_Build_Volume_9x10x3in",
         make_build_vol_box(IN_9, IN_10, IN_3, 0.0, 0.0, 46.0),
         CLR_BUILDVOL, transparency=65, line_rgb=(0.0, 1.0, 0.85), line_width=2.8)

doc.recompute()

view = Gui.ActiveDocument.ActiveView
view.setAnimationEnabled(False)

def set_group_vis(g, vis):
    for o in g.Group:
        if o.ViewObject:
            o.ViewObject.Visibility = vis

# Render each layout individually (Isometric + Front + Top)
for idx, grp in [(1, g1), (2, g2), (3, g3)]:
    set_group_vis(g1, grp == g1)
    set_group_vis(g2, grp == g2)
    set_group_vis(g3, grp == g3)
    Gui.updateGui()

    for vname, vfn in [("iso", "viewIsometric"), ("front", "viewFront"), ("right", "viewRight"), ("top", "viewTop")]:
        getattr(view, vfn)()
        view.fitAll()
        Gui.updateGui()
        view.saveImage(os.path.join(RENDER_DIR, f"layout_{{idx}}_{{vname}}.png"), 1400, 1050, "Current")

# Now translate Layout 1 to X = -480 mm and Layout 3 to X = +480 mm for a Side-by-Side 3-Way Comparison!
for o in g1.Group:
    o.Placement.Base.x -= 480.0
for o in g3.Group:
    o.Placement.Base.x += 480.0
set_group_vis(g1, True)
set_group_vis(g2, True)
set_group_vis(g3, True)
doc.recompute()
Gui.updateGui()

for vname, vfn in [("iso", "viewIsometric"), ("front", "viewFront"), ("top", "viewTop")]:
    getattr(view, vfn)()
    view.fitAll()
    Gui.updateGui()
    view.saveImage(os.path.join(RENDER_DIR, f"layouts_all_3_side_by_side_{{vname}}.png"), 1800, 950, "Current")

fcstd_path = os.path.join(CAD_DIR, "Ender3_3_Extrusion_Layouts_Comparison.FCStd")
doc.saveAs(fcstd_path)
print("SAVED_3_LAYOUTS:" + fcstd_path)
"""

def main():
    fc = FreeCADConnection(host="127.0.0.1", port=9875)
    res = fc.execute_code(FREECAD_CODE, timeout=120)
    print(res)

if __name__ == "__main__":
    main()
