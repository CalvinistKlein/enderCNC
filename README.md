# RepStrap Zero-Cut Ender 3 -> Desktop CNC Mill (`10.5" x 11.0" x 3.5" / 2.0"`)

> **Point-of-No-Return Invariant:** The stock Creality Ender 3 prints 100% of its own conversion brackets, 5-wall hollow concrete ballast sleeves, and air-cooled spindle collar using **a single 1 kg (2.2 lb) roll of PLA+** *before* a single bolt is loosened on the printer.

---

## 1. Locked-In Engineering Specifications (Imperial & Metric)

* **Working Cutting Envelope ($X \times Y \times Z$):**
  * **High-Deck Mode (Wood, $2\times 4$s, 3D Reliefs):** **$10.5\text{"} \times 11.0\text{"} \times 3.5\text{"}$** ($266.7 \times 279.4 \times 88.9\text{ mm}$)
  * **Low-Deck Mode ($1/4\text{"}$ 6061 Aluminum & Brass):** **$10.5\text{"} \times 11.0\text{"} \times 2.0\text{"}$** ($266.7 \times 279.4 \times 50.8\text{ mm}$) — achieved by dropping the X-bridge 4 bolts down the column sleeves.
* **Aluminum Extrusion Cuts Required:** **ZERO (`0`).** Every factory-milled square end on the donor Ender 3 is preserved.
* **Spindle:** Harbor Freight **Drill Master 2.4 Amp $1/4\text{"}$ Trim Router (SKU 62659)** ($\varnothing 2.56\text{"} / 65.0\text{ mm}$ motor barrel clamped in a 6-wall PLA+ split collar with 8 vertical $\varnothing 0.08\text{"}$ cooling air flutes).
* **Filament Budget:** **1 Single Roll of PLA+** ($34.9\text{ oz} / 2.18\text{ lbs} / 990\text{ g}$ across 3 sequential build plates; $\sim 21.5\text{ hours}$ total print time at $0.28\text{ mm}$ layer height, $0.45\text{ mm}$ line width, 5 perimeters = $0.089\text{"} / 2.25\text{ mm}$ solid hydrostatic shell walls).
* **Cast Ballast Core:** **$1/4\text{"}$-Screened Concrete** (standard bagged concrete sifted through $1/4\text{"}$ mesh, or Quikrete Sand/Topping Mix) mixed at **10 parts dry mix : 1.2 parts cold water + 3 drops dish soap surfactant**, poured through $\varnothing 1.00\text{"}$ ($25.4\text{ mm}$) top funnels with internal $0.25\text{"}$ sawtooth anti-shrinkage interlock fins.

---

## 2. The "Zero-Cut Beam Swap" Architecture (Mapped to Official Creality CAD)

Decomposing Creality's official [`01 MAIN ASM Ender_3.STEP`](https://github.com/Creality3DPrinting/Ender-3) (655 solids) reveals **8 uncut aluminum extrusions** that rearrange cleanly into a wide twin-rail moving-table CNC mill:

| Factory Solid ID (`01 MAIN ASM Ender_3.STEP`) | Uncut Extrusion Size | Original Ender 3 Role | **New Zero-Cut CNC Role** |
| :--- | :--- | :--- | :--- |
| **`Solid[4]` & `Solid[5]`** | $15.75\text{"}$ ($400\text{ mm}$) $\times 2040$ (Qty 2) | Left & Right Z-Uprights | **Twin Y-Axis Bed Rails** ($11.0\text{"}$ travel; eliminates single-rail bed seesawing) |
| **`Solid[0]` & `Solid[1]`** | $11.42\text{"}$ ($290\text{ mm}$) $\times 4040$ (Qty 2) | Left & Right Heavy Base Legs | **Heavy $4040$ Vertical Gantry Columns** (encased in 5-wall PLA+ concrete towers) |
| **`Solid[421]`** | $13.00\text{"}$ ($330\text{ mm}$) $\times 2040$ (Qty 1) | Y-Axis Center Spine | **Heavy $2040$ Primary X-Bridge Crossbar Way** ($6.6\times$ stiffer vertically than a $2020$, $40\text{ mm}$ V-roller stance) |
| **`Solid[44]`** | $13.58\text{"}$ ($345\text{ mm}$) $\times 2020$ (Qty 1) | X-Axis Carriage Rail | **Upper Rear X-Bridge Torsion Rebar** (cast into the concrete X-girder) |
| **`Solid[2]`** | $9.84\text{"}$ ($250\text{ mm}$) $\times 4040$ (Qty 1) | Center H-Frame Crossbar | **Front Heavy $4040$ Base Cross-Tie** |
| **`Solid[3]`** | $13.00\text{"}$ ($330\text{ mm}$) $\times 2020$ (Qty 1) | Top Frame Crossbar | **Rear $2020$ Base Cross-Tie** (base ways already supported along 90% of span by concrete sills) |
| **`Z threaded rod.step`** | $14.37\text{"}$ ($365\text{ mm}$) T8$\times$8 | Z-Axis Leadscrew | **Enclosed Z-Axis Leadscrew** (coaxial inside the dual-`608ZZ` Z-Arch Tower) |

---

## 3. Repository Structure

```text
repstrap-ender3-zerocut-cnc/
├── README.md                          # Project overview & locked-in engineering specs
├── AGENT_HANDOFF.md                   # Complete technical handoff & next-step roadmap for AI agents
├── cad/
│   ├── mcp_build_and_slice.py         # Full 62-object coaxial FreeCAD + OrcaSlicer MCP pipeline
│   ├── render_studio_parts.py         # High-resolution studio renderer for the 6 printable parts
│   ├── build_ender3_donor_cnc.py      # Extracts factory STEP solids & builds full FreeCAD CNC assembly
│   ├── repstrap_zero_cut_freecad.py   # Parametric printable STL generator (Beds 1, 2, 3)
│   ├── inspect_ender3_stp.py          # Diagnostic scanner for `01 MAIN ASM Ender_3.STEP`
│   ├── stl/                           # 6 watertight printable .stl meshes (Beds 1, 2, 3)
│   └── exports/                       # Generated .FCStd, .step, and full assembly .stl mesh
├── mcp/
│   └── freecad_mcp_bridge.py          # Live FreeCAD RPC/MCP server (`set_z_deck_mode`, `export_mesh`)
├── firmware/
│   └── Configuration_CNC_Patch.h      # Marlin 2.1.x patch for Creality V4.2.2 / V4.2.7 32-bit board
├── visuals/
│   ├── renders/                       # Orthographic, 3D close-up, studio part, and OrcaSlicer renders
│   ├── repstrap_3d_cad_viewer.html    # Full-screen interactive 3D CAD & Beam-Swap visualizer
│   └── repstrap_inline_viewer.html    # Compact inline 3D viewer
└── scripts/
    └── fetch_ender3_cad.sh            # Clones official Creality Ender-3 STEP repository if not present
```

---

## 4. Clean 62-Object Coaxial 3D CAD Assembly & Studio Showcase

![FreeCAD Isometric Assembly — Clean 62-Object Coaxial Portal Mill](visuals/renders/freecad_assembly_isometric.png)

| Close-Up: Headstock Shroud & Clamped Workpiece | Close-Up: Coaxial Z-Arch & Thick Concrete Crossbar | Close-Up: Ground-Contacting Portal Column & Y-Sill |
| :---: | :---: | :---: |
| ![Spindle Shroud](visuals/renders/freecad_closeup_spindle_shroud.png) | ![Z-Arch Bridge](visuals/renders/freecad_closeup_z_arch_bridge.png) | ![Portal Column](visuals/renders/freecad_closeup_exoskeleton_tower.png) |

| Front Elevation (3.5" High-Deck Mode) | Right Elevation (Compact Overhang) | Top Plan View (Twin-Rail Y & Closed Belt Loops) | Front Elevation (2.0" Low-Deck Mode) |
| :---: | :---: | :---: | :---: |
| ![Front](visuals/renders/freecad_assembly_front.png) | ![Right](visuals/renders/freecad_assembly_right.png) | ![Top](visuals/renders/freecad_assembly_top.png) | ![Low Deck](visuals/renders/freecad_assembly_front_low_deck_2in.png) |

### Printable Mineral-Cast Formwork & Motion Castings (`cad/stl/`)

| Part 1: Z-Guideway & Dual-608ZZ Arch (`Bed1_02`) | Part 2: Finned DM62659 Headstock Shroud (`Bed1_01`) | Part 3: Ground Concrete Base Sill (`Bed2_02`) |
| :---: | :---: | :---: |
| ![Z Arch](visuals/renders/studio_part2_z_stepper_arch.png) | ![Spindle Shroud](visuals/renders/studio_part1_spindle_shroud.png) | ![Base Sill](visuals/renders/studio_part6_ground_base_sill.png) |

| Part 4: Tapered Portal Column (`Bed3_01`) | Part 5: Thick Coffered X-Crossbar (`Bed3_02`) | Part 6: Twin-Rail Y Outrigger (`Bed2_01`) |
| :---: | :---: | :---: |
| ![Column](visuals/renders/studio_part4_exoskeleton_column.png) | ![X Girder](visuals/renders/studio_part5_x_bridge_girder.png) | ![Y Outrigger](visuals/renders/studio_part3_y_outrigger.png) |

### OrcaSlicer 5-Wall Hydrostatic Toolpath Previews ($220 \times 220\text{ mm}$ Ender 3 Bed)

| Bed 1 (`311.2 g` / `23h 57m`) | Bed 2 (`208.9 g` / `13h 25m`) | Bed 3 (`509.8 g` / `32h 12m`) |
| :---: | :---: | :---: |
| ![Orca Bed 1](visuals/renders/orca_Bed_01_Spindle_Collar_And_Z_Cap_preview.png) | ![Orca Bed 2](visuals/renders/orca_Bed_02_TwinRail_Y_Outriggers_preview.png) | ![Orca Bed 3](visuals/renders/orca_Bed_03_Concrete_Sleeves_And_X_Girder_preview.png) |

---

## 5. 2-Roll (`1.97 kg` PLA+) 5-Plate Full-Symmetry Production Schedule

| Spool # | Build Plate | Parts on Build Plate ($220 \times 220\text{ mm}$ Ender 3 Bed) | Filament Used ($\text{g}$ / $\text{m}$) | Est. Print Time | Printable STL Files |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **Spool 1** *(Roll 1: `947.4 g`)* | **Plate 1** | $1\times$ `DM62659_AirCooled_Collar` + $1\times$ `Z_Leadscrew_Top_Bearing_Cap` ($110\text{ mm}$ Integrated Z-Guideway Arch) | **$311.23\text{ g}$** ($104.35\text{ m}$) | `23h 57m` | `Bed1_01`, `Bed1_02` |
| **Spool 1** | **Plate 2 (Front Base)** | $1\times$ `Ground_Concrete_Base_Sill` (Front-Left) + $2\times$ `TwinRail_Y_Outrigger` (Left Pair) | **$208.89\text{ g}$** ($70.04\text{ m}$) | `13h 25m` | `Bed2_01`, `Bed2_02` |
| **Spool 1** | **Plate 3 (Rear Base)** | $3\times$ `Ground_Concrete_Base_Sill` (Front-Right, Rear-Left, Rear-Right) + $2\times$ `TwinRail_Y_Outrigger` (Right Pair) | **$427.30\text{ g}$** ($143.25\text{ m}$) | `24h 10m` | `Bed2_01`, `Bed2_02` |
| **Spool 2** *(Roll 2: `1,019.6 g`)* | **Plate 4 (Left Portal)** | $1\times$ `Concrete_Column_Sleeve_Half` (Left Pedestal) + $1\times$ `Concrete_X_Girder_Half` (Left Crossrail) | **$509.81\text{ g}$** ($170.93\text{ m}$) | `32h 12m` | `Bed3_01`, `Bed3_02` |
| **Spool 2** | **Plate 5 (Right Portal)** | $1\times$ `Concrete_Column_Sleeve_Half` (Right Pedestal) + $1\times$ `Concrete_X_Girder_Half` (Right Crossrail) | **$509.81\text{ g}$** ($170.93\text{ m}$) | `32h 12m` | `Bed3_01`, `Bed3_02` |
| **Total** | **5 Plates** | **Full Symmetrical Kit (12 Structural Castings + All Motion Brackets)** | **$1,967.04\text{ g}$ (`1.97 kg`)** | **2 Spools PLA+** | [`cad/stl/`](cad/stl) |

---

## 6. Quick Start

```bash
# 1. Fetch official Creality Ender-3 STEP donor files (if not already in ../ender3_cad_repo)
./scripts/fetch_ender3_cad.sh

# 2. Run the full FreeCAD + OrcaSlicer MCP build & slice pipeline
/home/calvin/.gemini/antigravity/scratch/cad-slicer-mcp/venv/bin/python cad/mcp_build_and_slice.py
```
