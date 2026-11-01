#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
from freecad_mcp.freecad_client import FreeCADConnection
import mcp_build_and_slice as m

def main():
    fc = FreeCADConnection(host="127.0.0.1", port=9875)
    print("[FreeCAD MCP] Connected:", fc.ping())
    res = fc.execute_code(m.FREECAD_SCRIPT, timeout=240)
    msg = res.get("message", "")
    print("[FreeCAD MCP] Rebuilt CAD assembly:", res.get("success"))
    for line in msg.splitlines():
        if line.startswith("FREECAD_SUMMARY_JSON:"):
            print(line)

    for view_name in ("Isometric", "Front", "Right", "Top"):
        b64 = fc.get_active_screenshot(view_name=view_name, width=1400, height=1050)
        out_png = os.path.join(m.RENDER_DIR, f"freecad_assembly_{view_name.lower()}.png")
        if m.save_b64_png(b64, out_png):
            print(f"[FreeCAD MCP] Saved screenshot: {out_png}")

    closeup_code = f"""
import os
import FreeCAD as App
import FreeCADGui as Gui

RENDER_DIR = {m.RENDER_DIR!r}
doc = App.getDocument("Ender3_Donor_ZeroCut_CNC")
view = Gui.ActiveDocument.ActiveView

def snap_selection_iso(obj_names, filename):
    Gui.Selection.clearSelection()
    for name in obj_names:
        o = doc.getObject(name)
        if o:
            Gui.Selection.addSelection(o)
    view.viewIsometric()
    Gui.SendMsgToActiveView("ViewSelection")
    Gui.Selection.clearSelection()
    Gui.updateGui()
    view.saveImage(os.path.join(RENDER_DIR, filename), 1400, 1050, "Current")

snap_selection_iso([
    "PLA_5Wall_Concrete_TowerSleeve_Left",
    "PLA_Ground_Concrete_BaseSill_Left_Front",
    "PLA_TwinRail_Y_Outrigger_Left_-45",
    "Motion_Y_Front_Belt_Tensioner_Bracket",
    "Motion_Y_Front_Tensioner_Knob",
    "Donor_Solid2_4040_FrontBaseTie_9_84in",
], "freecad_closeup_exoskeleton_tower.png")

snap_selection_iso([
    "PLA_Z_Stepper_And_608ZZ_Arch_Tower",
    "Donor_NEMA17_Z_Motor",
    "Motion_Z_5x8mm_Flexible_Shaft_Coupler",
    "Motion_Z_Top_And_Bottom_608ZZ_Radial_Bearings",
    "Motion_Z_Brass_T8x8_Leadscrew_Nut",
    "Motion_Z_Homing_Limit_Switch_Assembly",
    "Motion_X_Right_Belt_Tensioner_Bracket",
    "Motion_X_Homing_Limit_Switch_Assembly",
    "PLA_5Wall_XBridge_Concrete_Girder",
], "freecad_closeup_z_arch_bridge.png")

snap_selection_iso([
    "PLA_6Wall_AirCooled_DM62659_Collar",
    "HF62659_01_Machined_Aluminum_Barrel",
    "HF62659_02_Crimson_Motor_Housing",
    "HF62659_04_Collet_Nut",
    "HF62659_05_Carbide_Endmill_1_8in",
    "Workpiece_6061_Aluminum_Plate",
    "Workholding_2x_TSlot_Step_Clamps_And_M5_Hardware",
    "Motion_Z_3x_Vertical_Plunge_VSlot_Rollers",
], "freecad_closeup_spindle_shroud.png")

view.viewIsometric()
view.fitAll()
Gui.updateGui()
"""
    fc.execute_code(closeup_code, timeout=60)
    print("[FreeCAD MCP] Saved 3 closeup views.")

if __name__ == "__main__":
    main()
