import os, glob
import FreeCAD as App
import Part

stp_dir = "ender3_cad_repo/Ender-3 Mechanical/STP"
key_parts = [
    "2040 profile.step",
    "4040 profile.step",
    "2020 profile.step",
    "Y plate.step",
    "E plate.step",
    "Hot bed.step",
    "42-34 motor.step",
    "40-42 motor.step",
    "Z threaded rod.step",
    "Z coupler.step",
    "z nut.step",
    "Rollers.step",
    "24V15A power supply.step",
    "X motor bracket.step",
    "Y Motor holder.step",
    "Z motor bracket.step",
]

for name in key_parts:
    p = os.path.join(stp_dir, name)
    if os.path.exists(p):
        s = Part.Shape()
        s.read(p)
        bb = s.BoundBox
        print(f"{name:28s} | X:[{bb.XMin:6.1f},{bb.XMax:6.1f}] ({bb.XLength:5.1f}) | Y:[{bb.YMin:6.1f},{bb.YMax:6.1f}] ({bb.YLength:5.1f}) | Z:[{bb.ZMin:6.1f},{bb.ZMax:6.1f}] ({bb.ZLength:5.1f}) | Solids:{len(s.Solids)}")

# Also check solids inside 01 MAIN ASM Ender_3.STEP
asm_path = os.path.join(stp_dir, "01 MAIN ASM Ender_3.STEP")
if os.path.exists(asm_path):
    s_asm = Part.Shape()
    s_asm.read(asm_path)
    print(f"\n01 MAIN ASM Ender_3.STEP total solids: {len(s_asm.Solids)}, BoundBox: {s_asm.BoundBox}")
    # Find all extrusion-like solids (lengths >= 200mm)
    for idx, sol in enumerate(s_asm.Solids):
        bb = sol.BoundBox
        dims = sorted([round(bb.XLength, 1), round(bb.YLength, 1), round(bb.ZLength, 1)])
        if dims[2] >= 200.0 and dims[0] >= 18.0:
            print(f"  Solid[{idx:3d}]: dims={dims} | X:[{bb.XMin:6.1f},{bb.XMax:6.1f}] Y:[{bb.YMin:6.1f},{bb.YMax:6.1f}] Z:[{bb.ZMin:6.1f},{bb.ZMax:6.1f}]")
