# Option 1 Fixed-Bridge Mill: Motion Systems & Undercarriage Architecture

This document presents the detailed design, motion mechanisms, and undercarriage electronics packaging for the **Option 1 Fixed-Bridge Portal Mill**, modeled in [`Ender3_Option1_Full_CNC.FCStd`](file:///home/calvin/.gemini/antigravity/scratch/ender3-router-project/cad/Ender3_Option1_Full_CNC.FCStd) and rendered below.

---

## 1. Visual Assembly & Renders

````carousel
![Option 1 — Isometric Assembly View](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/opt1_full_iso.png)
<!-- slide -->
![Option 1 — Front Elevation (Basement Clearance & Z-Plunge)](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/opt1_full_front.png)
<!-- slide -->
![Option 1 — Undercarriage View (PSU, Mainboard & Central Leadscrew)](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/opt1_undercarriage_bottom.png)
<!-- slide -->
![Option 1 — Right Side Elevation (Column Support & Y-Travel)](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/opt1_full_right.png)
````

---

## 2. Undercarriage Electronics & Ground Support Feet

To ensure the machine has high stability while keeping all high-voltage power wiring and driver boards completely shielded from falling aluminum and wood chips, the entire machine is elevated $75\text{ mm}$ ($3"$) above the bench:

### A. Ground-Support Riser Feet ($6\times$ System)
- **4 Corner Riser Feet:** Positioned at the 4 frame corners ($X = \pm 145\text{ mm}$, $Y = \pm 190\text{ mm}$), bolting into the lower `2020 × 345 mm` (front) and `2020 × 330 mm` (rear) base ties. Each foot features a wide $52 \times 52\text{ mm}$ rubber vibration-isolation bench pad and a $44 \times 44\text{ mm}$ rigid riser body.
- **2 Direct Column Riser Feet:** Positioned directly under the base of the two vertical `4040 × 290 mm` columns ($X = \pm 145\text{ mm}$, $Y = +20\text{ mm}$). This ensures all vertical cutting forces from the X-bridge and spindle transfer directly into the workbench with zero frame cantilever or sag.

### B. Undercarriage Basement Electronics Cavity
- **Clearance:** $250\text{ mm}$ wide $\times 380\text{ mm}$ deep $\times 75\text{ mm}$ high open basement beneath the bed ways.
- **Left Side ($X = -72\text{ mm}$):** Stock Creality 24V 15A Power Supply ($215 \times 113 \times 50\text{ mm}$), oriented longitudinally along Y. Its AC inlet and rocker switch face the rear/side for clean cable routing.
- **Right Side ($X = +78\text{ mm}$):** Stock Creality Mainboard & TMC Stepper Driver Enclosure ($145 \times 153 \times 40\text{ mm}$), lying flat with cooling vents facing down and SD card / USB programming ports accessible from the front/side.
- **Central Corridor ($X \in [-15, +15]\text{ mm}$):** A clear central channel isolating the rotating Y-axis leadscrew from all electrical wiring.

---

## 3. Motion System Mechanisms (X, Y, and Z)

### A. Y-Axis Motion System (Moving Worktable)
*Why a Leadscrew for Y?* Unlike 3D printers that use lightweight rubber belts, a milling machine experiences continuous cutting forces ($15\text{--}40\text{ N}$) in the direction of feed. A leadscrew provides high mechanical advantage, zero belt stretch, and positive locking against tool push-back.

- **Guidance:**
  - Twin `2040 × 400 mm` extrusions spaced at $X = \pm 95\text{ mm}$ (Ender 3 standard wheel span).
  - Dual MGN12H linear guide rails ($400\text{ mm}$) or dual 4-wheel V-slot roller clusters riding top and bottom channels.
  - Ender 3 aluminum bed carriage plate ($190 \times 190\text{ mm}$) tying both rails together with zero racking.
- **Drive:**
  - Rear-mounted NEMA 17 stepper motor ($42 \times 42 \times 34\text{ mm}$) mounted on the rear base tie ($Y = +210\text{ mm}$).
  - $5\text{ mm} \to 8\text{ mm}$ flexible helical coupler.
  - $370\text{ mm}$ T8 leadscrew ($8\text{ mm}$ pitch per revolution, 4-start) running along $X = 0$, $Z = 105\text{ mm}$.
  - Brass/POM anti-backlash spring-loaded nut block bolted to the underside of the bed carriage plate.
- **Worktable Surface:** $264\text{ mm (X)} \times 240\text{ mm (Y)} \times 12\text{ mm}$ MDF/aluminum spoilboard with threaded inserts for workpiece clamping.
- **Travel Stroke:** $228.6\text{ mm}$ ($9.0"$) cutting travel with $25\text{ mm}$ overtravel margin.

---

### B. X-Axis Motion System (Moving Toolhead Carriage)
- **Guidance:**
  - Compound X-Bridge: `4040 × 250 mm` inner girder bolted between columns ($X = \pm 145\text{ mm}$) + `2040 × 330 mm` front beam bolted across column faces.
  - Linear way: MGN12H linear guide rail ($330\text{ mm}$) or dual V-slot track mounted horizontally on the front face of the `2040 × 330 mm` extrusion ($Z = 265\text{--}275\text{ mm}$).
  - Rigid aluminum/printed X-carriage plate ($90\text{ mm wide} \times 110\text{ mm tall} \times 8\text{ mm thick}$).
- **Drive:**
  - NEMA 17 stepper motor mounted on an outrigger bracket on the left column ($X = -185\text{ mm}$).
  - Steel-core GT2 timing belt ($6\text{ mm}$ width, non-stretch fiberglass/steel reinforcement) running across the front face.
  - Adjustable bearing idler pulley on the right column ($X = +180\text{ mm}$) with tensioning screw.
- **Travel Stroke:** $254.0\text{ mm}$ ($10.0"$) cutting travel across the $330\text{ mm}$ bridge span.

---

### C. Z-Axis Motion System (Vertical Plunge Toolhead)
- **Guidance:**
  - Twin vertical precision linear rails / $8\text{ mm}$ induction-hardened ground rods ($140\text{ mm}$ tall) spaced at $X = \pm 28\text{ mm}$ on the front of the X-carriage plate.
  - Linear carriage blocks supporting the vertical Z-plunge plate ($75 \times 90 \times 8\text{ mm}$).
- **Drive:**
  - Top-mounted NEMA 17 stepper motor sitting on the Z arch ($Z = 327\text{ mm}$).
  - $5\text{ mm} \to 8\text{ mm}$ coupler driving a vertical T8 stainless steel leadscrew ($130\text{ mm}$ long).
  - Anti-backlash brass nut bolted directly to the Z-plunge plate.
- **Spindle Mount:**
  - High-rigidity 52mm aluminum clamp collar (Safety Orange) bolted directly to the Z-plunge plate.
  - 500W ER11 brushless DC milling spindle ($12,000\text{--}24,000\text{ RPM}$) with ER11 collet system capable of clamping $1/8"$ and $1/4"$ end mills.
- **Plunge Stroke:** $76.2\text{ mm}$ ($3.0"$) vertical cutting plunge plus $15\text{ mm}$ tool clearance retract height.

---

## 4. Predicted Build Volume Coordinate Verification

| Axis | Specified Envelope | Machine Stroke | Travel Margins | Coordinate Range in CAD |
| :--- | :---: | :---: | :---: | :---: |
| **X-Axis** | **$10.0"$ ($254.0\text{ mm}$)** | $260.0\text{ mm}$ | $+6.0\text{ mm}$ | $X \in [-127.0, +127.0]\text{ mm}$ |
| **Y-Axis** | **$9.0"$ ($228.6\text{ mm}$)** | $250.0\text{ mm}$ | $+21.4\text{ mm}$ | $Y \in [-191.3, +37.3]\text{ mm}$ (centered at $Y = -77.0\text{ mm}$) |
| **Z-Axis** | **$3.0"$ ($76.2\text{ mm}$)** | $90.0\text{ mm}$ | $+13.8\text{ mm}$ | $Z \in [149.0, 225.2]\text{ mm}$ (above table top at $Z = 149.0\text{ mm}$) |

The translucent Cyan-Emerald box verifies that the cutting volume sits entirely within the spindle travel envelope and clears all structural extrusions.
