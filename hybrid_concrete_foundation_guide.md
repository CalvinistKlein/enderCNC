# Hybrid Concrete-Filled Plastic Shell Foundation & CNC Assembly

This document presents the detailed design and CAD implementation of the **stay-in-place 3D-printed plastic formwork shells filled with concrete**, complete with precision extrusion alignment sockets, ground-contact mounting, and full motion systems, modeled in [`Ender3_Concrete_Hybrid_CNC.FCStd`](file:///home/calvin/.gemini/antigravity/scratch/ender3-router-project/cad/Ender3_Concrete_Hybrid_CNC.FCStd).

---

## 1. Visual Verification & Multi-View Renders

````carousel
![Hybrid Concrete Foundation — Full Isometric Assembly](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/hybrid_concrete_iso.png)
<!-- slide -->
![Front Elevation — Ground-Contact Concrete Sills & Extrusion Seating](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/hybrid_concrete_front.png)
<!-- slide -->
![Right Side Elevation — 420mm Concrete Foundation Beam & Bench Bolt Lugs](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/hybrid_concrete_right.png)
<!-- slide -->
![Top View — Pour Funnels, Extrusion Sockets & Electronics Bay](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/hybrid_concrete_top.png)
````

---

## 2. Key Architecture & User Requirements Addressed

### A. T8 Leadscrew Utilized for Z-Axis Motion
- The stock Ender 3 stainless steel **T8 leadscrew** ($8\text{ mm}$ diameter, 4-start, $2\text{ mm}$ pitch / $8\text{ mm}$ lead) is utilized as the primary vertical plunge drive on the Z-axis.
- It is mounted in front of the crossbar at $Y = -48\text{ mm}$, driven via an overhead GT2 synchronous timing belt from the rear-mounted NEMA 17 stepper motor, delivering a smooth, zero-backlash $3.0"$ ($76.2\text{ mm}$) vertical milling plunge.

### B. Complete Removal of Sheet Metal
- All donor sheet metal parts (`Sheetmetal enclosure bottom.step`, `Sheetmetal enclosure top.step`) have been removed from the CAD model.
- Replaced by a dedicated **3D-printed undercarriage electronics slide tray** ($220 \times 180 \times 4\text{ mm}$) with integrated cable routing passages, supporting:
  - Creality 24V 15A Power Supply ($X = -65\text{ mm}$).
  - 32-bit silent controller board with four blue anodized TMC driver heatsinks ($X = +55\text{ mm}$).
  - Fully sheltered from falling chips and coolant under the worktable.

### C. Stay-In-Place 3D-Printed Plastic Shells Filled with Concrete
The foundation consists of **two massive longitudinal foundation sills** ($420\text{ mm long} \times 100\text{ mm wide} \times 115\text{ mm tall}$) that sit directly on the ground/workbench ($Z = 0$):

1. **Precision Extrusion Pockets & Alignment Sockets:**
   - **Column Anchor Socket:** A deep $40.8 \times 40.8\text{ mm}$ vertical pocket embeds the bottom $60\text{ mm}$ of each `4040 × 290 mm` column directly into concrete ($Z = 55\text{--}115\text{ mm}$), creating an ultra-rigid cantilever-free column root.
   - **Twin Y-Way Bed Saddles:** Step-recessed shelves with alignment ribs that seat the two `2040 × 400 mm` Y-ways at $X = \pm 95\text{ mm}$, $Z = 95\text{--}115\text{ mm}$.
   - **Front & Rear Base Crossbar Sockets:** Transverse keyways that lock the `2020 × 345 mm` front tie ($Y = -190\text{ mm}$) and `2020 × 330 mm` rear tie ($Y = +190\text{ mm}$) squarely at $90^\circ$.

2. **Cast Concrete Internal Cores:**
   - The shell has a $4.5\text{ mm}$ wall thickness printed in PETG/PLA.
   - The interior forms a continuous cavity filled with high-density cast concrete / non-shrink grout (rendered in stone grey inside the semi-transparent orange shell).
   - Concrete volume: $\approx 5.2\text{ liters}$ total ($\approx 12\text{--}13\text{ kg}$ / $26\text{--}28\text{ lbs}$ of ballast), providing massive inertial damping against tool chatter and vibrations.

3. **Pour Funnels & Ground Anchoring:**
   - Three $\varnothing 32\text{ mm}$ conical pour funnels per side on the top surface allow easy pouring of grout slurry with no air pockets.
   - Four heavy bolt-down lugs per side ($8\times$ total) touch the bench at $Z = 0$ with $M8$ through-holes to bolt the mill solidly to your workbench.

---

## 3. Split-Weight Counterbalanced Router Head Summary

```
 [ FRONT: Cutting Zone ]           [ IN BETWEEN: Guidance ]           [ BACK: Counterbalance ]
+-------------------------+     +-------------------------------+     +-----------------------+
| 52 mm ER11 Spindle      |     | Front MGN12 Linear Guide Rail |     | Z-Axis NEMA 17 Stepper|
| Safety Orange Clamp     |<===>| 2040 x 330 mm Front Way Extr  |<===>| Rear Mounting Bracket |
| Vertical Z-Plunge Slide |     | 4040 x 250 mm Inner Girder    |     | Top GT2 Drive Pulley  |
| Front T8 Leadscrew      |     | (Combined X = 330 mm Bridge)  |     |                       |
+-------------------------+     +-------------------------------+     +-----------------------+
```

- **Router in Front:** 52mm ER11 milling spindle centered at $Y = -80\text{ mm}$.
- **Rail in Middle:** Compound X-crossbar and MGN12 guide rail at $Y \in [-20, +40]\text{ mm}$.
- **Motor in Back:** Z stepper motor hanging at $Y = +60\text{ mm}$, driving the front leadscrew via the top GT2 synchronous timing belt.
- **Tipping moment on the linear guide blocks is eliminated**, providing maximum cutting stiffness and extended bearing life.

---

## 4. Build Volume & Motion Envelopes

- **Cutting Volume:** $10.0" \text{ (X)} \times 9.0" \text{ (Y)} \times 3.0" \text{ (Z)}$ ($254.0 \times 228.6 \times 76.2\text{ mm}$) verified by the translucent Cyan-Emerald box.
- **Worktable:** $264 \times 240\text{ mm}$ spoilboard surface at $Z = 137\text{ mm}$.
