# EnderCNC — Clean Coaxial 62-Object Conventional Portal Milling Machine Kit (`10.5" × 11.0" × 3.5" / 2.0"`)

> [!IMPORTANT]
> **Zero-Clutter Coaxial CAD Assembly + 2-Roll (`2.0 kg`) Full-Symmetry Kit:**
> 1. **Clean 62-Object Coaxial CAD Assembly ([`Ender3_Donor_ZeroCut_CNC.FCStd`](file:///home/calvin/.gemini/antigravity/scratch/ender3-router-project/cad/Ender3_Donor_ZeroCut_CNC.FCStd)):** All extraneous, tilted, dangling, or colliding 3D-printer sheetmetal/plastic brackets have been removed. Every part required for X, Y, and Z motion, spindle mounting, and workholding is coaxially aligned on its exact mechanical axis—including all **16 POM V-slot rollers** (`8×` Y-axis, `4×` X-axis, `4×` Z-axis), **coaxial stainless spacers & eccentric preload nuts**, **upright NEMA 17 stepper motors**, **coaxial 20T GT2 drive & idler pulleys**, **taut closed-loop X & Y GT2 timing belts**, **integrated vertical Z-guideway & dual-`608ZZ` bearing arch tower**, **coaxial $5\times 8\text{ mm}$ helical Z-coupler**, **enclosed $T8\times 8$ leadscrew & flanged brass T8 nut**, **cylindrical aluminum bed standoffs**, and **T-slot step clamps** centered directly under the $1/8\text{"}$ carbide endmill.
> 2. **Upgrading to 2 Rolls of Filament (`2.0 kg` / `2,000 g` PLA+):** Moving from 1 spool (`1,000 g`) to **2 spools (`1,967 g` total across 5 build plates)** prints **all 12 symmetrical mineral-cast formwork shells** (all $4\times$ Ground Base Sills, all $4\times$ Tapered Portal Column Halves, and both $2\times$ Thick X-Crossrail Halves) with thick **5-to-6-wall (`2.25–2.70 mm`) hydrostatic perimeters** plus a **Two-Tone Industrial Colorway** (Spool 1: Anthracite Cast-Grey; Spool 2: Safety Orange / Teal).

---

## 1. Clean 62-Object Coaxial CAD Assembly (FreeCAD MCP `127.0.0.1:9875`)

All CAD files and exports in [`/home/calvin/.gemini/antigravity/scratch/ender3-router-project/cad/`](file:///home/calvin/.gemini/antigravity/scratch/ender3-router-project/cad) are organized into 5 clean mechanical subsystems via [`mcp_build_and_slice.py`](file:///home/calvin/.gemini/antigravity/scratch/ender3-router-project/mcp_build_and_slice.py):
- **Parametric FreeCAD Native Assembly (62 Objects):** [`Ender3_Donor_ZeroCut_CNC.FCStd`](file:///home/calvin/.gemini/antigravity/scratch/ender3-router-project/cad/Ender3_Donor_ZeroCut_CNC.FCStd)
- **Full Assembly STEP Export:** [`Ender3_Donor_ZeroCut_CNC.step`](file:///home/calvin/.gemini/antigravity/scratch/ender3-router-project/cad/Ender3_Donor_ZeroCut_CNC.step)
- **Full Assembly STL Mesh:** [`Ender3_Donor_ZeroCut_CNC_Assembly.stl`](file:///home/calvin/.gemini/antigravity/scratch/ender3-router-project/cad/Ender3_Donor_ZeroCut_CNC_Assembly.stl)

````carousel
![FreeCAD Isometric Assembly — Clean 62-Object Coaxial Portal Mill with Zero Extraneous Fragments](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/freecad_assembly_isometric.png)
<!-- slide -->
![Close-Up: Finned Headstock Shroud, Harbor Freight 62659 Router, Carbide Endmill & Step-Clamped 6061 Aluminum Workpiece](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/freecad_closeup_spindle_shroud.png)
<!-- slide -->
![Close-Up: Coaxial Z-Stepper Arch Tower, 5x8mm Coupler, X-Axis GT2 Pulleys & Thick Concrete X-Crossbar](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/freecad_closeup_z_arch_bridge.png)
<!-- slide -->
![Close-Up: Ground-Contacting Portal Column (Z = 0.0 mm), Concrete Y-Base Sill, Twin-Rail Y Outriggers & Front Y-Belt Tensioner](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/freecad_closeup_exoskeleton_tower.png)
<!-- slide -->
![FreeCAD Front Elevation — High-Deck 3.5" Clearance Mode with Symmetrical Portal Frame & Taut X/Y Belt Loops](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/freecad_assembly_front.png)
<!-- slide -->
![FreeCAD Right Elevation — Compact Spindle Overhang Centered Directly Over the Clamped Workpiece](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/freecad_assembly_right.png)
<!-- slide -->
![FreeCAD Top Plan View — Twin-Rail Y-Ways, Closed Center Y-Belt Loop, Closed X-Belt Loop & T-Slot Step Clamps](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/freecad_assembly_top.png)
<!-- slide -->
![FreeCAD Front Elevation — Low-Deck 2.0" Aluminum Milling Mode](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/freecad_assembly_front_low_deck_2in.png)
````

---

## 2. Coaxial X, Y, Z Motion & Machine Subsystem Bill of Materials in CAD

Every mechanical link required to convert rotary stepper motion into rigid 3-axis CNC travel is coaxially modeled in [`Ender3_Donor_ZeroCut_CNC.FCStd`](file:///home/calvin/.gemini/antigravity/scratch/ender3-router-project/cad/Ender3_Donor_ZeroCut_CNC.FCStd):

| Subsystem Group | Modeled CAD Objects in `Ender3_Donor_ZeroCut_CNC.FCStd` | Donor STEP / Printed Source | Kinematic / Functional Role |
| :--- | :--- | :--- | :--- |
| **1. Base & Portal Frame (Stock `330.0 mm` Ender 3 X-Width, `Z = 0.0 mm`)** | `Donor_Solid0/1_4040_GantryCol`, `Donor_Solid4/5_2040_TwinY`, `Donor_Solid44_2020_FrontBaseTie`, `Donor_Solid3_2020_RearBaseTie`, `Donor_Solid421_2040_XBridgePrimary`, `Donor_Solid2_4040_XBridgeCore`, `4× PLA_Ground_Concrete_BaseSill`, `2× PLA_5Wall_Concrete_TowerSleeve`, `PLA_5Wall_XBridge_Concrete_Girder` | `01 MAIN ASM Ender_3.STEP` (8 uncut extrusions) + [`Bed2_02`](file:///home/calvin/.gemini/antigravity/scratch/ender3-router-project/stl/Bed2_02_Ground_Concrete_Base_Sill.stl), [`Bed3_01`](file:///home/calvin/.gemini/antigravity/scratch/ender3-router-project/stl/Bed3_01_Concrete_Column_Sleeve_Half.stl), [`Bed3_02`](file:///home/calvin/.gemini/antigravity/scratch/ender3-router-project/stl/Bed3_02_Concrete_X_Girder_Half.stl) | Exact stock Ender 3 X-width (`330.0 mm` / `13.00"` outer column width, `250.0 mm` / `9.84"` inner gap): **both** heavy extrusions—**`2040 × 330 mm` (`Solid[421]`)** across the front and **`4040 × 250 mm` (`Solid[2]`)** bolted between the columns—lock into a $60\times 40\text{ mm}$ compound aluminum X-crossbar! |
| **2. Coaxial Y-Axis Drivetrain (Moving Table)** | `Donor_Y_Carriage_Plate`, `4× PLA_TwinRail_Y_Outrigger`, `Motion_Y_8x_VSlot_POM_Rollers`, `Motion_Y_8x_Coaxial_Spacers_And_Eccentric_Nuts`, `Motion_Y_Rear_NEMA17_Stepper_Motor`, `Motion_Y_Rear_20T_GT2_Drive_Pulley`, `Motion_Y_Front_Belt_Tensioner_Clevis`, `Motion_Y_Front_GT2_Idler_Pulley`, `Motion_Y_GT2_Timing_Belt_Loop`, `Motion_Y_Carriage_Center_Belt_Clamp` | `Y plate.step`, `Rollers.step`, [`Bed2_01_TwinRail_Y_Outrigger.stl`](file:///home/calvin/.gemini/antigravity/scratch/ender3-router-project/stl/Bed2_01_TwinRail_Y_Outrigger.stl), coaxial NEMA 17 / GT2 drivetrain | 8 POM V-rollers with coaxial spacers/eccentric nuts carry the $235\text{ mm}$ moving table along the twin $400\text{ mm}$ $2040$ Y-ways (`X = ±80 mm`), passing cleanly through the $250\text{ mm}$ column throat (`X = ±121 mm`). |
| **3. Coaxial X-Axis Drivetrain (`2040` Gantry Saddle)** | `Motion_X_Saddle_Carriage_Plate`, `Motion_X_4x_VSlot_POM_Rollers`, `Motion_X_4x_Coaxial_Spacers_And_Eccentric_Nuts`, `Motion_X_Left_NEMA17_Stepper_Motor`, `Motion_X_Left_20T_GT2_Drive_Pulley`, `Motion_X_Right_GT2_Idler_Pulley`, `Motion_X_Right_Belt_Tensioner_Block`, `Motion_X_GT2_Timing_Belt_Loop` | `Rollers.step`, coaxial X-saddle & GT2 drivetrain | 4 POM V-rollers with coaxial spacers/eccentric nuts roll horizontally along the wide $40\text{ mm}$ vertical stance of the **$2040 \times 330\text{ mm}$ X-Crossbar (`Solid[421]`)**, driven by the coaxial left NEMA 17 X-motor & pulley (`X = -104 mm`) and right idler tensioner (`X = +104 mm`). |
| **4. Coaxial Z-Axis Vertical Plunge Drivetrain** | `PLA_Z_Stepper_And_608ZZ_Arch_Tower`, `Motion_Z_Top_And_Bottom_608ZZ_Radial_Bearings`, `Motion_Z_Top_NEMA17_Stepper_Motor`, `Motion_Z_5x8mm_Flexible_Shaft_Coupler`, `Donor_T8_Leadscrew_Uncut_14_37in`, `Motion_Z_Brass_T8x8_Leadscrew_Nut`, `Donor_X_Carriage_Steel_Plate`, `Motion_Z_4x_Vertical_Plunge_VSlot_Rollers` | [`Bed1_02_Z_Leadscrew_Top_Bearing_Cap.stl`](file:///home/calvin/.gemini/antigravity/scratch/ender3-router-project/stl/Bed1_02_Z_Leadscrew_Top_Bearing_Cap.stl), `E plate.step`, `Rollers.step` | All Z-axis components share the exact vertical axis (`X = 0.0 mm, Y = -72.0 mm`): upright top NEMA 17 motor, $5\times 8\text{ mm}$ helical coupler, top/bottom `608ZZ` bearings, enclosed $T8\times 8$ leadscrew, and brass T8 nut driving the 4-roller `E plate.step` Z-plunge slide. |
| **5. Worktable, Clamps & Router Spindle** | `Motion_Worktable_4x_Rigid_Aluminum_Standoffs`, `Donor_HeatedBed_Worktable_Plate`, `CNC_MDF_T_Slot_Spoilboard`, `Workpiece_6061_Aluminum_Plate`, `Workholding_2x_TSlot_Step_Clamps`, `PLA_6Wall_AirCooled_DM62659_Collar`, `HF62659_01..05` | `Hot bed.step`, [`Bed1_01_DM62659_AirCooled_Collar.stl`](file:///home/calvin/.gemini/antigravity/scratch/ender3-router-project/stl/Bed1_01_DM62659_AirCooled_Collar.stl) | 4 solid cylindrical aluminum standoffs support the subplate and T-slot MDF spoilboard; 2 M5 T-slot step clamps secure the 6061 aluminum stock at `X = 0.0, Y = -112.0 mm` directly beneath the Harbor Freight 62659 $1/4\text{"}$ router and $1/8\text{"}$ carbide endmill. |

---

## 3. What Going to 2 Rolls of Filament (`2.0 kg` PLA+) Unlocks

> [!TIP]
> **Why 2 Rolls (`2,000 g` / $\sim\$32$) Is the Sweet Spot for a Conventional Milling Machine Kit:**
> Squeezing into a single $1\text{ kg}$ spool (`1,000 g`) only prints **one set** of Bed 1 + Bed 2 + Bed 3 (`1,029.9 g`), meaning you either have to print thin 2-wall shells or leave half of the columns/base sills un-jacketed.
> Stepping up to **2 standard $1\text{ kg}$ spools (`1,967.0 g` total across 5 build plates)** gives you **100% full-symmetry concrete encapsulation** across the entire machine with **5-to-6-wall (`2.25–2.70 mm`) hydrostatic shells**:

| Feature | 1-Roll Budget (`~1,000 g` Minimalist Bootstrap) | **2-Roll Budget (`1,967 g` Full Conventional Mill Kit — Recommended)** |
| :--- | :--- | :--- |
| **Ground-Contacting Concrete Base Sills (`Z = 0..38 mm`)** | Only 1–2 short sills ($180\text{ mm}$ support under Y-ways) | **All $4\times$ Ground Base Sills ($720\text{ mm}$ total concrete way-cradle)** supporting 90% of both $400\text{ mm}$ $2040$ Y-ways on `Z = 0.0 mm` |
| **Tapered Ground-Contacting Portal Columns (`Z = 0..290 mm`)** | Half-height or thin 2-wall column sleeves | **All $4\times$ Heavy 5-Wall Tapered Column Castings** (Left Lower + Left Upper + Right Lower + Right Upper, $290\text{ mm}$ full height) |
| **Thick Deep-Section Portal X-Crossbar** | Thin $46 \times 56\text{ mm}$ bar (leaves $80\text{ mm}$ empty column chimneys) | **Massive $84 \times 112\text{ mm}$ Coffered Concrete Box-Beam (`Z = 154..280 mm`)** spanning flush to the column crowns for **$5.8\times$ higher torsional stiffness** |
| **Z-Axis Plunge Guideway & Headstock Shroud** | Compact 44 mm top bearing cap (`253 g` Bed 1) | **Full-Height $110\text{ mm}$ Integrated Vertical V-Guideway & Dual-`608ZZ` Arch Tower (`311.2 g` Bed 1)** |
| **Colorway & Aesthetics** | Monochrome single-spool color | **Two-Tone Industrial Colorway** (Spool 1: Anthracite Cast-Grey; Spool 2: Safety Orange / Precision Teal) |

### 2-Spool (`1,967 g`) 5-Plate Production Schedule (OrcaSlicer MCP Verified)

| Spool # | Build Plate | Parts on Build Plate ($220 \times 220\text{ mm}$ Ender 3 Bed) | Filament Used ($\text{g}$ / $\text{m}$) | Est. Print Time | G-Code / Reference Slice |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **Spool 1** *(Roll 1: `947.4 g`)* | **Plate 1** | $1\times$ `DM62659_AirCooled_Collar` + $1\times$ `Z_Leadscrew_Top_Bearing_Cap` ($110\text{ mm}$ Integrated Z-Guideway Arch) | **$311.23\text{ g}$** ($104.35\text{ m}$) | `23h 57m` | [`Bed_01_Spindle_Collar_And_Z_Cap.gcode`](file:///home/calvin/.gemini/antigravity/scratch/ender3-router-project/gcode/Bed_01_Spindle_Collar_And_Z_Cap.gcode) |
| **Spool 1** | **Plate 2 (Front Base)** | $1\times$ `Ground_Concrete_Base_Sill` (Front-Left) + $2\times$ `TwinRail_Y_Outrigger` (Left Pair) | **$208.89\text{ g}$** ($70.04\text{ m}$) | `13h 25m` | [`Bed_02_TwinRail_Y_Outriggers.gcode`](file:///home/calvin/.gemini/antigravity/scratch/ender3-router-project/gcode/Bed_02_TwinRail_Y_Outriggers.gcode) |
| **Spool 1** | **Plate 3 (Rear Base)** | $3\times$ `Ground_Concrete_Base_Sill` (Front-Right, Rear-Left, Rear-Right) + $2\times$ `TwinRail_Y_Outrigger` (Right Pair) | **$427.30\text{ g}$** ($143.25\text{ m}$) | `24h 10m` | Uses [`Bed_02_TwinRail_Y_Outriggers.gcode`](file:///home/calvin/.gemini/antigravity/scratch/ender3-router-project/gcode/Bed_02_TwinRail_Y_Outriggers.gcode) profile |
| **Spool 2** *(Roll 2: `1,019.6 g`)* | **Plate 4 (Left Portal)** | $1\times$ `Concrete_Column_Sleeve_Half` (Left Pedestal) + $1\times$ `Concrete_X_Girder_Half` (Left Crossrail) | **$509.81\text{ g}$** ($170.93\text{ m}$) | `32h 12m` | [`Bed_03_Concrete_Sleeves_And_X_Girder.gcode`](file:///home/calvin/.gemini/antigravity/scratch/ender3-router-project/gcode/Bed_03_Concrete_Sleeves_And_X_Girder.gcode) |
| **Spool 2** | **Plate 5 (Right Portal)** | $1\times$ `Concrete_Column_Sleeve_Half` (Right Pedestal) + $1\times$ `Concrete_X_Girder_Half` (Right Crossrail) | **$509.81\text{ g}$** ($170.93\text{ m}$) | `32h 12m` | Re-run [`Bed_03_Concrete_Sleeves_And_X_Girder.gcode`](file:///home/calvin/.gemini/antigravity/scratch/ender3-router-project/gcode/Bed_03_Concrete_Sleeves_And_X_Girder.gcode) |
| **Total** | **5 Plates** | **Full Symmetrical Kit (12 Structural Castings + All Motion Brackets)** | **$1,967.04\text{ g}$ (`1.97 kg`)** | **2 Spools PLA+** | All `.gcode` files in [`gcode/`](file:///home/calvin/.gemini/antigravity/scratch/ender3-router-project/gcode) |

---

## 4. Studio Showcase & OrcaSlicer Toolpath Previews

````carousel
![Part 1 — Integrated Z-Axis Vertical V-Guideway & Dual-608ZZ Stepper Arch Tower (88 x 54 x 110 mm)](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/studio_part2_z_stepper_arch.png)
<!-- slide -->
![Part 2 — Finned Air-Cooled DM62659 Vertical Mill Headstock Shroud (102 x 127 x 58 mm)](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/studio_part1_spindle_shroud.png)
<!-- slide -->
![Part 3 — Ground-Contacting Concrete Machine Base Sill (70 x 180 x 38 mm, Z = 0.0 mm)](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/studio_part6_ground_base_sill.png)
<!-- slide -->
![Part 4 — Tapered Ground-Contacting Mill Portal Column (104 x 136 x 150 mm, Z = 0.0 mm)](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/studio_part4_exoskeleton_column.png)
<!-- slide -->
![Part 5 — Thick Deep-Section Portal Box-Beam X-Crossbar Half (165 x 106 x 130 mm, 84x112mm Box Core)](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/studio_part5_x_bridge_girder.png)
<!-- slide -->
![Part 6 — Truss-Lightened Twin-Rail Y-Bed Outrigger & Way-Wiper Skirt (96 x 50 x 24 mm)](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/studio_part3_y_outrigger.png)
<!-- slide -->
![OrcaSlicer Bed 1 Preview — Headstock Spindle Shroud + 110mm Z-Guideway Arch Tower (311.2 g)](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/orca_Bed_01_Spindle_Collar_And_Z_Cap_preview.png)
<!-- slide -->
![OrcaSlicer Bed 2 Preview — Ground-Contacting Concrete Y-Base Sill + 2x Twin-Rail Y Outriggers (208.9 g)](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/orca_Bed_02_TwinRail_Y_Outriggers_preview.png)
<!-- slide -->
![OrcaSlicer Bed 3 Preview — Tapered Ground-Contacting Portal Column + Streamlined X-Crossrail (509.8 g)](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/orca_Bed_03_Concrete_Sleeves_And_X_Girder_preview.png)
````
