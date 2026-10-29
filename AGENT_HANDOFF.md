# Downstream Agent Handoff Specification (`AGENT_HANDOFF.md`)

This document provides complete context, technical discoveries, FreeCAD execution rules, and the prioritized task backlog for any autonomous agent continuing the **RepStrap Zero-Cut Ender 3 CNC Mill** project.

---

## 1. Current State & Completed Milestones

1. **Official Donor CAD Decomposition (`cad/inspect_ender3_stp.py`):**
   - Cloned `https://github.com/Creality3DPrinting/Ender-3.git` and parsed `Ender-3 Mechanical/STP/01 MAIN ASM Ender_3.STEP` (655 solids) plus all individual STEP parts (`Y plate.step`, `E plate.step`, `Hot bed.step`, `42-34 motor.step`, `Z threaded rod.step`, `Rollers.step`, `24V15A power supply.step`).
   - Verified exact bounding boxes and coordinates of the **8 uncut aluminum extrusions** (`Solid[0]`, `Solid[1]`, `Solid[2]`, `Solid[3]`, `Solid[4]`, `Solid[5]`, `Solid[44]`, `Solid[421]`).
2. **Zero-Cut Assembly & Parametric Printable Kit (`cad/build_ender3_donor_cnc.py` & `cad/repstrap_zero_cut_freecad.py`):**
   - Generated `Ender3_Donor_ZeroCut_CNC.FCStd`, `Ender3_Donor_ZeroCut_CNC.step`, and `Ender3_Donor_ZeroCut_CNC_Assembly.stl`.
   - Generated initial printable STL components for the **Harbor Freight Drill Master 62659** air-cooled collar (`65.2 mm` bore + 8 cooling flutes), **Twin-Rail Y Outrigger**, **5-Wall Concrete Column Tower Sleeves**, and **Concrete X-Bridge Torsion Girder**.
3. **Interactive 3D Visualizers (`visuals/repstrap_3d_cad_viewer.html`):**
   - Built standalone zero-dependency HTML/Canvas 3D CAD visualizers showing the animated transition from Stock Ender 3 to the Zero-Cut CNC configuration, High-Deck (`3.5"`) vs. Low-Deck (`2.0"`) Z-clearance toggle, and concrete cutaway view.

---

## 2. Critical FreeCAD Headless Execution Gotchas (Read Before Running Commands)

When invoking FreeCAD in console/headless mode (`/snap/bin/freecad -c <script.py>`):

1. **`__name__` is NOT `"__main__"`:**
   - FreeCAD's `-c` loader imports the script by module name (`__name__ == "<script_stem>"`).
   - **Rule:** Either invoke your main function unconditionally at top-level or check `if __name__ in ("__main__", "<script_stem>"):`.
2. **Preventing Interactive `>>>` Prompt Hang:**
   - After executing a script passed to `-c`, FreeCAD drops into an interactive Python `>>>` REPL unless terminated explicitly.
   - **Rule:** Always call `import os; os._exit(0)` at the end of batch scripts so the process exits cleanly with code `0`.

---

## 3. Exact Donor Solid Coordinate Map (`01 MAIN ASM Ender_3.STEP`)

| Solid Index | Profile Type | Stock Bounding Box (`[XMin, XMax]`, `[YMin, YMax]`, `[ZMin, ZMax]` mm) | Dimensions (mm / in) | Assigned Zero-Cut CNC Component |
| :---: | :---: | :--- | :--- | :--- |
| `Solid[0]` | `4040` | `X:[125.0, 165.4] Y:[-0.4, 40.0] Z:[-135.0, 155.0]` | `40.4 x 40.4 x 290.0` (`11.42"`) | Right Heavy Vertical Gantry Column |
| `Solid[1]` | `4040` | `X:[-165.0, -124.6] Y:[-0.4, 40.0] Z:[-135.0, 155.0]` | `40.4 x 40.4 x 290.0` (`11.42"`) | Left Heavy Vertical Gantry Column |
| `Solid[2]` | `4040` | `X:[-125.0, 125.0] Y:[0.0, 40.0] Z:[-10.0, 30.0]` | `40.0 x 40.0 x 250.0` (`9.84"`) | Front Heavy Base Cross-Tie |
| `Solid[3]` | `2020` | `X:[-165.0, 165.0] Y:[440.0, 460.0] Z:[0.0, 20.0]` | `20.0 x 20.0 x 330.0` (`13.00"`) | Upper X-Bridge Torsion Rail |
| `Solid[4]` | `2040` | `X:[125.0, 165.0] Y:[40.0, 440.0] Z:[0.0, 20.0]` | `20.0 x 40.0 x 400.0` (`15.75"`) | Left Twin Y-Axis Bed Rail |
| `Solid[5]` | `2040` | `X:[-165.0, -125.0] Y:[40.0, 440.0] Z:[0.0, 20.0]` | `20.0 x 40.0 x 400.0` (`15.75"`) | Right Twin Y-Axis Bed Rail |
| `Solid[44]` | `2020` | `X:[-163.7, 181.3] Y:[179.3, 199.3] Z:[26.8, 46.8]` | `20.0 x 20.0 x 345.0` (`13.58"`) | Lower Primary X-Bridge Rail |
| `Solid[421]` | `2040` | `X:[-10.0, 10.0] Y:[33.0, 73.0] Z:[-110.0, 220.0]` | `20.0 x 40.0 x 330.0` (`13.00"`) | Rear Base Cross-Tie |
| `Solid[646]` | `PSU` | `X:[123.0, 173.0] Y:[87.5, 302.5] Z:[-113.0, 0.0]` | `50.0 x 113.0 x 215.0` | 24V 15A MeanWell/Creality Power Supply |

---

## 4. Next Tasks for Continuation Agent

### Priority 1: Exact Factory Hole-Pattern Registration in FreeCAD
- Inspect the factory M5 counterbores and tapped end-holes inside `Solid[0]`, `Solid[1]`, `Solid[2]`, `Solid[4]`, `Solid[5]`, and `E plate.step` so the printed PLA+ brackets and concrete sleeves align to `< 0.1 mm` with the existing factory holes—requiring **zero drilling** on the aluminum beams.

### Priority 2: Automated PrusaSlicer / OrcaSlicer CLI Toolpathing (`slicer_mcp`)
- Connect `slicer_mcp` to slice the 3 build plates (`Bed_01`, `Bed_02`, `Bed_03`) with:
  - Material: `PLA+` (`210°C` nozzle / `60°C` bed)
  - Layer Height: `0.28 mm`, Line Width: `0.45 mm`
  - Perimeters: `5` (`2.25 mm / 0.089"` solid shell wall) on concrete sleeves, `6` on the DM62659 spindle collar
  - Infill: `15% Gyroid` on hollow ballast sleeves, `30% Gyroid` on spindle collar & motor mounts
  - Verify total filament mass remains `<= 990 g` (`34.9 oz`, 1 spool).

### Priority 3: Phase 2 Self-Replication Toolpaths (1/4" 6061 Aluminum Upgrade Plates)
- Generate 2.5D DXF profiles and conservative G-code toolpaths (`DOC = 0.4 mm`, `WOC = 1.2 mm`, `Feed = 450 mm/min`, 1/8" single-flute upcut carbide endmill) so the completed V1-Heavy concrete-filled machine can mill its own replacement aluminum spindle carriage plate and gantry tie plates.
