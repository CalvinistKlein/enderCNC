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
| **`Solid[44]`** | $13.58\text{"}$ ($345\text{ mm}$) $\times 2020$ (Qty 1) | X-Axis Carriage Rail | **Primary Lower X-Bridge Rail** ($10.5\text{"}$ X-travel) |
| **`Solid[3]`** | $13.00\text{"}$ ($330\text{ mm}$) $\times 2020$ (Qty 1) | Top Frame Crossbar | **Secondary Upper X-Bridge Torsion Rail** (cast into the concrete X-girder) |
| **`Solid[2]`** | $9.84\text{"}$ ($250\text{ mm}$) $\times 4040$ (Qty 1) | Center H-Frame Crossbar | **Front Heavy $4040$ Base Cross-Tie** |
| **`Solid[421]`** | $13.00\text{"}$ ($330\text{ mm}$) $\times 2040$ (Qty 1) | Y-Axis Center Spine | **Rear $2040$ Base Cross-Tie** |
| **`Z threaded rod.step`** | $14.37\text{"}$ ($365\text{ mm}$) T8$\times$8 | Z-Axis Leadscrew | **Uncut Z-Axis Leadscrew** (passes through top 608ZZ bearing cap; cutting optional) |

---

## 3. Repository Structure

```text
repstrap-ender3-zerocut-cnc/
├── README.md                          # Project overview & locked-in engineering specs
├── AGENT_HANDOFF.md                   # Complete technical handoff & next-step roadmap for AI agents
├── cad/
│   ├── build_ender3_donor_cnc.py      # Extracts factory STEP solids & builds full FreeCAD CNC assembly
│   ├── repstrap_zero_cut_freecad.py   # Parametric printable STL generator (Beds 1, 2, 3)
│   ├── inspect_ender3_stp.py          # Diagnostic scanner for `01 MAIN ASM Ender_3.STEP`
│   └── exports/                       # Generated .FCStd, .step, and printable .stl meshes
├── mcp/
│   └── freecad_mcp_bridge.py          # Live FreeCAD RPC/MCP server (`set_z_deck_mode`, `export_mesh`)
├── firmware/
│   └── Configuration_CNC_Patch.h      # Marlin 2.1.x patch for Creality V4.2.2 / V4.2.7 32-bit board
├── visuals/
│   ├── repstrap_3d_cad_viewer.html    # Full-screen interactive 3D CAD & Beam-Swap visualizer
│   └── repstrap_inline_viewer.html    # Compact inline 3D viewer
└── scripts/
    └── fetch_ender3_cad.sh            # Clones official Creality Ender-3 STEP repository if not present
```

---

## 4. Quick Start

```bash
# 1. Fetch official Creality Ender-3 STEP donor files (if not already in ../ender3_cad_repo)
./scripts/fetch_ender3_cad.sh

# 2. Generate printable STL files and full FreeCAD / STEP assemblies
/snap/bin/freecad -c cad/build_ender3_donor_cnc.py
```
