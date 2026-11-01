# Router Research & Heavy-Duty 65mm Split-Clamp Mechanism

This document details the engineering research on CNC router spindles and the mechanical design of the **65mm heavy-duty split-collar clamp mechanism** modeled in [`Ender3_Router_Clamp_Mechanism.FCStd`](file:///home/calvin/.gemini/antigravity/scratch/ender3-router-project/cad/Ender3_Router_Clamp_Mechanism.FCStd).

---

## 1. Visual Verification & Renders

````carousel
![Router Clamp Mechanism — Isometric Close-Up (Makita RT0701C & Split Clamp)](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/router_clamp_closeup_iso.png)
<!-- slide -->
![Router Clamp Mechanism — Front Elevation (Dual M6 Pinch Bolts & Relief Flex Slit)](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/router_clamp_closeup_front.png)
<!-- slide -->
![Router Clamp Mechanism — Side View (Split-Weight Front-to-Back Balance)](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/router_clamp_closeup_side.png)
<!-- slide -->
![Full Assembly — Complete Mill with 65mm Router Clamp & Concrete Foundation](/home/calvin/.gemini/antigravity/brain/298df1bf-0561-4493-bd28-37704f60c3b5/router_clamp_full_machine_iso.png)
````

---

## 2. Router Selection Research

In desktop and small-format CNC milling, two primary spindle categories dominate DIY and light-industrial conversions:

| Metric | **Makita RT0701C / Compact Trim Router** | **500W Brushless Air-Cooled Spindle** |
| :--- | :--- | :--- |
| **Nominal Barrel Diameter** | **$65.0\text{ mm}$** ($64.85\text{ mm}$ measured) | **$52.0\text{ mm}$** |
| **Power Output** | **$1.25\text{ HP}$ ($\approx 930\text{ Watts}$)** | $500\text{ Watts}$ |
| **Speed Range** | $10,000\text{--}30,000\text{ RPM}$ (variable thumbwheel) | $12,000\text{--}24,000\text{ RPM}$ (PWM controlled) |
| **Collet System** | $1/4"$ standard ($1/8"$ & $3/8"$ precision adapters) | ER11 collet system ($1\text{ mm}$ to $7\text{ mm}$) |
| **Weight** | $3.9\text{ lbs}$ ($1.8\text{ kg}$) | $2.2\text{ lbs}$ ($1.0\text{ kg}$) |
| **Cutting Capability** | Aggressive roughing in hardwoods, plastics, and non-ferrous metals (6061 Aluminum) | Light engraving, PCB isolation, soft plastics, thin wood |
| **Noise Profile** | Louder (universal brushed AC motor) | Very quiet (brushless DC) |

> [!TIP]
> **Universal Dual-Format Solution:**
> The **Makita RT0701C (65mm)** is selected as the primary heavy-duty cutting tool due to its high torque and availability. However, to ensure maximum versatility, our clamp includes a precision **$65\text{ mm} \to 52\text{ mm}$ split reducing adapter sleeve**, allowing quick swapping to a quiet 500W ER11 brushless spindle with zero modifications!

---

## 3. Clamp Mechanism Engineering Details

A standard narrow clamp allows the router barrel to pivot or flex under side-milling cutting pressures ($20\text{--}40\text{ N}$). Our clamp incorporates several key design features:

### A. Heavy-Duty Split-Collar Geometry
- **Outer Footprint:** $92.0\text{ mm wide} \times 74.0\text{ mm deep} \times 48.0\text{ mm tall}$.
- **Clamping Band Height:** A full $48.0\text{ mm}$ tall contact cylinder that grips the cylindrical aluminum barrel of the router across a broad surface area, completely eliminating rocking or tilt.
- **Relief Flex Slit:** A $3.2\text{ mm}$ wide slit cuts through the front face into the $65.0\text{ mm}$ bore, providing uniform tangential clamping pressure without over-stressing the plastic/aluminum collar.

### B. Dual M6 Pinch-Bolt Clamping System
- **Fasteners:** Two $M6 \times 50\text{ mm}$ high-tensile black oxide socket head cap screws located at $Z = 215.0\text{ mm}$ (lower) and $Z = 243.0\text{ mm}$ (upper).
- **Recessed Counterbores:** Right clamping ear features deep counterbores to shield the screw heads.
- **Captive Hex Nut Pockets:** Left clamping ear features interlocking hex pockets ($11.5\text{ mm}$ across flats) so the clamp can be tightened from one side using a single $5\text{ mm}$ hex key.

### C. Z-Plunge Plate Interface & Tramming Registration
- The rear face of the clamp mates flush against the front of the Z-plunge slide plate ($Y = -54.0\text{ mm}$).
- **$4\times M5$ Mounting Pattern:** Spaced at $64\text{ mm (X)} \times 28\text{ mm (Z)}$ with precision dowel pin registration to allow micro-tramming (squaring the router axis perpendicular to the spoilboard).

### D. Interchangeable 65mm-to-52mm Split Adapter Sleeve
- Gold-anodized / brass split reduction bushing ($64.9\text{ mm OD} \times 52.1\text{ mm ID} \times 46.0\text{ mm tall}$).
- Slotted with a $3.0\text{ mm}$ slit that aligns with the main clamp gap, transferring pinch pressure directly into a 52mm spindle.

### E. Quick-Release Magnetic Dust Shoe Interface
- The underside of the clamp block features four $\varnothing 10.0\text{ mm} \times 3.5\text{ mm}$ neodymium magnet pockets and alignment dowel slots.
- Allows a snap-on vacuum dust boot to attach and detach instantly for tool changes without loosening any clamp bolts.
