# 3 Ways to Lay Out the 8 Uncut Ender 3 Extrusions ($3"\times 10"\times 9"$ Build Volume)

Starting fresh with **only the 8 uncut aluminum extrusions** from the stock Creality Ender 3 assembly ([`01 MAIN ASM Ender_3.STEP`](file:///home/calvin/.gemini/antigravity/scratch/ender3-router-project/ender3_cad_repo/Ender-3%20Mechanical/STP/01%20MAIN%20ASM%20Ender_3.STEP)) in [`Ender3_3_Extrusion_Layouts_Comparison.FCStd`](file:///home/calvin/.gemini/antigravity/scratch/ender3-router-project/cad/Ender3_3_Extrusion_Layouts_Comparison.FCStd):

| Extrusion Profile | Qty | Stock Length | STEP Solid ID | Color in Renders | Original Ender 3 Role |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **`4040` Heavy V-Slot** | `2×` | $290.0\text{ mm}$ ($11.42"$) | `Solid[0]`, `Solid[1]` | **Charcoal-Slate** | Left & Right Base Frame Legs |
| **`4040` Heavy V-Slot** | `1×` | $250.0\text{ mm}$ ($9.84"$) | `Solid[2]` | **Charcoal-Slate** | Center Y-Axis Base Spine |
| **`2040` Medium V-Slot** | `2×` | $400.0\text{ mm}$ ($15.75"$) | `Solid[4]`, `Solid[5]` | **Steel-Blue** | Left & Right Vertical Z-Columns |
| **`2040` Medium V-Slot** | `1×` | $330.0\text{ mm}$ ($13.00"$) | `Solid[421]` | **Steel-Blue** | Power Supply / Upright Strut |
| **`2020` Light V-Slot** | `1×` | $345.0\text{ mm}$ ($13.58"$) | `Solid[44]` | **Amber-Gold** | Moving X-Axis Carriage Beam |
| **`2020` Light V-Slot** | `1×` | $330.0\text{ mm}$ ($13.00"$) | `Solid[3]` | **Amber-Gold** | Top Z-Frame Crossbar |

> [!IMPORTANT]
> **Target Build Volume Prediction ($3"\times 10"\times 9"$ = $76.2\text{ mm} \times 254.0\text{ mm} \times 228.6\text{ mm}$):**
> Every layout below includes a **translucent Cyan-Emerald box** showing the exact size and location of the $3"\times 10"\times 9"$ cutting envelope above the grey reference worktable surface.

---

## Side-by-Side Comparison of All 3 Layouts

````carousel
![All 3 Layouts — Isometric Comparison](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/layouts_all_3_side_by_side_iso.png)
<!-- slide -->
![All 3 Layouts — Top-Down Footprint & Build Area Comparison](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/layouts_all_3_side_by_side_top.png)
<!-- slide -->
![All 3 Layouts — Front Elevation & Z-Clearance Comparison](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/layouts_all_3_side_by_side_front.png)
````

---

## Layout 1: Fixed-Bridge Portal Mill (Moving-Y Table)

In **Layout 1**, the portal columns and compound X-bridge remain **completely stationary**, and the worktable travels along the twin `2040 × 400 mm` Y-ways. Because the spindle carriage rides across the full $330\text{ mm}$ front face of the `2040 × 330 mm` crossbar (in front of the `4040 × 290 mm` columns), the **entire $10.0"$ ($254.0\text{ mm}$) width** is achieved along X while $9.0"$ ($228.6\text{ mm}$) is achieved along Y.

````carousel
![Layout 1 — Isometric View](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/layout_1_iso.png)
<!-- slide -->
![Layout 1 — Front Elevation](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/layout_1_front.png)
<!-- slide -->
![Layout 1 — Right Side Elevation](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/layout_1_right.png)
<!-- slide -->
![Layout 1 — Top View](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/layout_1_top.png)
````

### Extrusion Mapping & Build Volume Location (Layout 1)
- **Base Front & Rear Ties:** `1× 2020×345 mm` ($Y = -190\text{ mm}$) + `1× 2020×330 mm` ($Y = +190\text{ mm}$) at $Z = [0, 20]\text{ mm}$.
- **Twin Y-Axis Bed Ways:** `2× 2040×400 mm` laid flat at $X = \pm 95\text{ mm}$ ($230\text{ mm}$ outer span), $Y = [-200, +200]\text{ mm}$, $Z = [20, 40]\text{ mm}$.
- **Fixed Portal Columns:** `2× 4040×290 mm` standing vertically at stock Ender 3 spacing $X = \pm 145\text{ mm}$ ($330\text{ mm}$ outer width, $250\text{ mm}$ inner gap), $Y = [0, 40]\text{ mm}$, $Z = [0, 290]\text{ mm}$.
- **Compound Fixed X-Crossbar:** `1× 4040×250 mm` inner core ($X = [-125, +125]\text{ mm}$, $Y = [0, 40]\text{ mm}$, $Z = [175, 215]\text{ mm}$) + `1× 2040×330 mm` front way ($X = [-165, +165]\text{ mm}$, $Y = [-20, 0]\text{ mm}$, $Z = [175, 215]\text{ mm}$) flush across the front of both columns.
- **Predicted Build Volume ($10.0"\text{ X} \times 9.0"\text{ Y} \times 3.0"\text{ Z}$):**
  - **Dimensions:** $254.0\text{ mm (X)} \times 228.6\text{ mm (Y)} \times 76.2\text{ mm (Z)}$
  - **Exact Coordinates:** $X \in [-127.0, +127.0]\text{ mm}$, $Y \in [-149.3, +79.3]\text{ mm}$ (centered under the front-mounted spindle axis at $Y = -35\text{ mm}$), $Z \in [50.0, 126.2]\text{ mm}$.

---

## Layout 2: Moving-Gantry Router Table (Stationary Bed, Moving Portal)

In **Layout 2**, the workpiece never moves. The `2× 2040 × 400 mm` extrusions form the left and right stationary Y-ways ($X = \pm 145\text{ mm}$), locked into a rigid stationary bed frame by the `4040 × 250 mm` central bed spine ($Z = [0, 40]\text{ mm}$, flush with the top of the Y-ways) and the `2020 × 345 mm` / `2020 × 330 mm` end ties. The `2× 4040 × 290 mm` columns and `2040 × 330 mm` X-crossbar form a **moving portal gantry** that travels along Y over the stationary bed.

````carousel
![Layout 2 — Isometric View](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/layout_2_iso.png)
<!-- slide -->
![Layout 2 — Front Elevation](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/layout_2_front.png)
<!-- slide -->
![Layout 2 — Right Side Elevation](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/layout_2_right.png)
<!-- slide -->
![Layout 2 — Top View](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/layout_2_top.png)
````

### Extrusion Mapping & Build Volume Location (Layout 2)
- **Stationary Base Ties:** `1× 2020×345 mm` ($Y = -190\text{ mm}$) + `1× 2020×330 mm` ($Y = +190\text{ mm}$) at $Z = [0, 20]\text{ mm}$.
- **Stationary Left & Right Y-Ways:** `2× 2040×400 mm` at $X = \pm 145\text{ mm}$ ($X \in [-165, -125]\text{ mm}$ and $[+125, +165]\text{ mm}$), $Y = [-200, +200]\text{ mm}$, $Z = [20, 40]\text{ mm}$.
- **Stationary Central Bed Spine:** `1× 4040×250 mm` bolted between the inner faces of the `2040×400` Y-ways ($X = [-125, +125]\text{ mm}$, $Z = [0, 40]\text{ mm}$).
- **Moving Portal Gantry Columns:** `2× 4040×290 mm` riding directly on top of the `2040×400` Y-ways ($X = \pm 145\text{ mm}$, $Z = [40, 330]\text{ mm}$).
- **Moving X-Gantry Crossbar:** `1× 2040×330 mm` bolted across the front face of the moving `4040×290` columns ($X = [-165, +165]\text{ mm}$, $Z = [175, 215]\text{ mm}$).
- **Predicted Build Volume ($9.0"\text{ X} \times 10.0"\text{ Y} \times 3.0"\text{ Z}$):**
  - **Dimensions:** $228.6\text{ mm (X)} \times 254.0\text{ mm (Y)} \times 76.2\text{ mm (Z)}$ (fits cleanly inside the $250\text{ mm}$ clear span between the moving gantry legs!)
  - **Exact Coordinates:** Centered on the stationary bed at $X \in [-114.3, +114.3]\text{ mm}$, $Y \in [-127.0, +127.0]\text{ mm}$, $Z \in [46.0, 122.2]\text{ mm}$.

---

## Layout 3: High-Rail "Box-Cage" Gantry Mill (Elevated Y-Ways, Zero-Riser `4040` X-Bridge)

In **Layout 3**, the `2× 2040 × 400 mm` Y-ways are raised to the top of the cutting envelope ($Z = [150, 190]\text{ mm}$) by bolting them to the inner faces ($X = \pm 125\text{ mm}$) of the fixed `2× 4040 × 290 mm` vertical columns, while the two `2020` extrusions lock the front and rear of the elevated Y-ways into a closed overhead halo. The heavy **`4040 × 250 mm`** extrusion rides directly on top of the elevated Y-rails ($X = [-125, +125]\text{ mm}$) as a **zero-riser moving X-bridge**, passing cleanly between the `4040 × 290 mm` columns across the full $10"$ Y-stroke.

````carousel
![Layout 3 — Isometric View](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/layout_3_iso.png)
<!-- slide -->
![Layout 3 — Front Elevation](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/layout_3_front.png)
<!-- slide -->
![Layout 3 — Right Side Elevation](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/layout_3_right.png)
<!-- slide -->
![Layout 3 — Top View](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/layout_3_top.png)
````

### Extrusion Mapping & Build Volume Location (Layout 3)
- **Fixed Vertical Columns:** `2× 4040×290 mm` at $X = \pm 145\text{ mm}$ ($X \in [-165, -125]\text{ mm}$ and $[+125, +165]\text{ mm}$, $250\text{ mm}$ clear inner gap), $Y = [-20, +20]\text{ mm}$, $Z = [0, 290]\text{ mm}$.
- **Lower Bed Crossbar:** `1× 2040×330 mm` bolted across the bottom front of the two `4040` columns ($X = [-165, +165]\text{ mm}$, $Y = [-40, -20]\text{ mm}$, $Z = [0, 40]\text{ mm}$).
- **Elevated High-Rail Y-Ways:** `2× 2040×400 mm` oriented $40\text{ mm}$ tall ($Z = [150, 190]\text{ mm}$) bolted to the inner faces of the `4040` columns ($X \in [-125, -105]\text{ mm}$ and $[+105, +125]\text{ mm}$, $Y = [-200, +200]\text{ mm}$).
- **Upper Box-Cage Halo Ties:** `1× 2020×345 mm` ($Y = -190\text{ mm}$) + `1× 2020×330 mm` ($Y = +190\text{ mm}$) at $Z = [190, 210]\text{ mm}$.
- **Zero-Riser Moving X-Bridge:** `1× 4040×250 mm` ($X = [-125, +125]\text{ mm}$, $Z = [190, 230]\text{ mm}$) riding directly on top of the elevated `2040×400` Y-ways with **zero tall gantry risers**!
- **Predicted Build Volume ($9.0"\text{ X} \times 10.0"\text{ Y} \times 3.0"\text{ Z}$):**
  - **Dimensions:** $228.6\text{ mm (X)} \times 254.0\text{ mm (Y)} \times 76.2\text{ mm (Z)}$
  - **Exact Coordinates:** Nested inside the stationary cage at $X \in [-114.3, +114.3]\text{ mm}$, $Y \in [-127.0, +127.0]\text{ mm}$, $Z \in [46.0, 122.2]\text{ mm}$.

---

## Quick Architectural Comparison

| Feature | **Layout 1: Fixed-Bridge Portal** | **Layout 2: Moving-Gantry Router** | **Layout 3: High-Rail Box-Cage** |
| :--- | :--- | :--- | :--- |
| **Build Volume ($X \times Y \times Z$)** | **$10.0" \times 9.0" \times 3.0"$** ($254 \times 228.6 \times 76.2\text{ mm}$) | **$9.0" \times 10.0" \times 3.0"$** ($228.6 \times 254 \times 76.2\text{ mm}$) | **$9.0" \times 10.0" \times 3.0"$** ($228.6 \times 254 \times 76.2\text{ mm}$) |
| **Workpiece / Table Motion** | Moving Y-Table | **Stationary Bed** | **Stationary Bed** |
| **X-Crossbar Profile** | Compound **`4040×250` + `2040×330`** ($60 \times 40\text{ mm}$) | Single **`2040×330`** ($20 \times 40\text{ mm}$) on moving `4040` columns | Heavy **`4040×250`** ($40 \times 40\text{ mm}$) riding directly on elevated Y-rails |
| **Gantry Riser Lever Arm** | **None** (Columns bolted to ground/base) | Tall moving `4040×290` gantry legs | **None** (Zero-riser bridge rides directly on elevated Y-rails) |
| **Best Suited For** | Highest X-bridge rigidity & easiest single-motor Y-table drive | Full-sheet/heavy clamping on a stationary table with open front/back access | Eliminating moving-gantry leg flex while keeping a stationary workpiece |
