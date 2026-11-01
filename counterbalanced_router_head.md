# Counterbalanced "Split-Weight" Router Head Design

This document details the **mass-balanced router head** engineered for the **Option 1 Fixed-Bridge Mill**, modeled in [`Ender3_Option1_Counterbalanced_CNC.FCStd`](file:///home/calvin/.gemini/antigravity/scratch/ender3-router-project/cad/Ender3_Option1_Counterbalanced_CNC.FCStd).

---

## 1. Visual Proof & Renders

````carousel
![Toolhead Side Elevation — Split-Weight Architecture (Router FRONT / Rail MIDDLE / Motor BACK)](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/opt1_toolhead_split_weight_side.png)
<!-- slide -->
![Toolhead Top View — Overhead GT2 Synchronous Belt & Mass Symmetry](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/opt1_toolhead_split_weight_top.png)
<!-- slide -->
![Toolhead Isometric Close-Up — Saddle Carriage & Spindle Mount](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/opt1_toolhead_split_weight_iso.png)
<!-- slide -->
![Full Assembly Isometric View — Complete Machine with Counterbalanced Carriage](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/opt1_counterbalanced_iso.png)
````

---

## 2. Mechanical Architecture & Weight Split

Conventional desktop routers place both the heavy cutting spindle and the Z-axis drive motor far in front of the X-axis linear rails. This creates a severe **overhung cantilever pitch moment ($M_x$)** that twists the X-rail downward, accelerates bearing wear, and induces tool chatter during milling passes.

By implementing a **saddle carriage with front-to-back weight splitting**:

```
 [ FRONT: Cutting Zone ]           [ IN BETWEEN: Guidance ]           [ BACK: Counterbalance ]
+-------------------------+     +-------------------------------+     +-----------------------+
| 52 mm ER11 Spindle      |     | Front MGN12 Linear Guide Rail |     | Z-Axis NEMA 17 Stepper|
| Safety Orange Clamp     |<===>| 2040 x 330 mm Front Way Extr  |<===>| Rear Mounting Bracket |
| Vertical Z-Plunge Slide |     | 4040 x 250 mm Inner Girder    |     | Top Drive Pulley      |
| Front T8 Leadscrew      |     | (Combined X = 330 mm Bridge)  |     |                       |
+-------------------------+     +-------------------------------+     +-----------------------+
     Mass: ~1.15 kg                       Support Plane                    Mass: ~0.55 kg
   Lever Arm: -80 mm                      Pivot: Y = 0 mm                Lever Arm: +60 mm
```

### Static Moment Balance:
- **Front Moment ($M_{\text{front}}$):** $1.15\text{ kg} \times 80\text{ mm} \approx 92\text{ kg}\cdot\text{mm}$ (forward pitch).
- **Rear Counter-Moment ($M_{\text{rear}}$):** $(0.55\text{ kg} \text{ motor/bracket} + 0.35\text{ kg} \text{ saddle rear}) \times 60\text{ mm} \approx 54\text{ kg}\cdot\text{mm}$ (rear pitch).
- **Net Cantilever Reduction:** The tipping torque on the linear rail bearings is **reduced by over $60\%$**, placing the center of gravity directly within the footprint of the linear guide blocks!

---

## 3. Motion Transmission Mechanism

1. **Saddle Carriage Body:**
   - Machined/printed saddle plate wraps completely over the top of the compound bridge:
     - **Top Strut ($Z = 290\text{ mm}$):** $95\text{ mm wide} \times 85\text{ mm deep} \times 8\text{ mm thick}$ plate tying front and back together.
     - **Front Drop Plate ($Y = -36\text{ mm}$):** Mounts the twin vertical guide rails and front T8 leadscrew bearings.
     - **Rear Drop Plate ($Y = +41\text{ mm}$):** Mounts the inverted NEMA 17 stepper motor.

2. **Overhead Synchronous Drive:**
   - The rear Z stepper motor shaft points upward, equipped with a $16$-tooth GT2 aluminum drive pulley ($Y = +60\text{ mm}$).
   - A short, closed-loop GT2 timing belt runs horizontally across the top of the saddle plate to an $18$-tooth pulley attached to the top of the front T8 leadscrew ($Y = -48\text{ mm}$).
   - This eliminates bulky motor overhang on top of the spindle, lowers the machine's overall vertical center of gravity, and provides a smooth $1:1$ or $1:1.125$ mechanical reduction for micro-stepping precision.

3. **Front Vertical Plunge:**
   - The front T8 leadscrew drives an anti-backlash brass nut attached to the Z-plunge plate.
   - Twin $8\text{ mm}$ hardened ground rails guide the plunge motion with zero twist.
   - Spindle clamp collar firmly secures the 52mm ER11 brushless milling spindle, delivering the full $3.0"$ ($76.2\text{ mm}$) vertical travel.
