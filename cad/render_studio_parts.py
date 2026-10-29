#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
High-resolution Studio 3D Shaded Renderer for the Stylized Ender 3 CNC Printable Parts.
Generates crisp SVG -> PNG studio renders with dark engineering blueprint background,
specular/diffuse shading, and part callouts.
"""

import os
import math
import struct
import subprocess

PROJECT_DIR = "/home/calvin/.gemini/antigravity/scratch/ender3-router-project"
STL_DIR     = os.path.join(PROJECT_DIR, "stl")
RENDER_DIR  = os.path.join(PROJECT_DIR, "renders")


def parse_stl(path):
    triangles = []
    with open(path, "rb") as f:
        header = f.read(80)
        if header.startswith(b"solid ") and b"facet normal" in f.read(200):
            # ASCII STL fallback
            f.seek(0)
            verts = []
            norm = (0.0, 0.0, 1.0)
            for line in f.read().decode("utf-8", errors="ignore").splitlines():
                parts = line.strip().split()
                if len(parts) >= 4 and parts[0] == "facet" and parts[1] == "normal":
                    norm = (float(parts[2]), float(parts[3]), float(parts[4]))
                elif len(parts) == 4 and parts[0] == "vertex":
                    verts.append((float(parts[1]), float(parts[2]), float(parts[3])))
                    if len(verts) == 3:
                        triangles.append((norm, tuple(verts)))
                        verts = []
            return triangles
        f.seek(80)
        c_bytes = f.read(4)
        if len(c_bytes) < 4:
            return triangles
        n = struct.unpack("<I", c_bytes)[0]
        for _ in range(n):
            d = f.read(50)
            if len(d) < 50:
                break
            nx, ny, nz, x1, y1, z1, x2, y2, z2, x3, y3, z3, _ = struct.unpack("<12fH", d)
            triangles.append(((nx, ny, nz), ((x1, y1, z1), (x2, y2, z2), (x3, y3, z3))))
    return triangles


def render_stl_studio(stl_path, out_png, title, subtitle, base_rgb=(245, 112, 20), yaw=42, pitch=28, width=1200, height=900):
    triangles = parse_stl(stl_path)
    if not triangles:
        return
    all_v = [v for _, tri in triangles for v in tri]
    min_x, max_x = min(v[0] for v in all_v), max(v[0] for v in all_v)
    min_y, max_y = min(v[1] for v in all_v), max(v[1] for v in all_v)
    min_z, max_z = min(v[2] for v in all_v), max(v[2] for v in all_v)
    cx, cy, cz = (min_x + max_x) / 2.0, (min_y + max_y) / 2.0, (min_z + max_z) / 2.0
    extent = max(max_x - min_x, max_y - min_y, max_z - min_z) or 1.0
    scale = (min(width, height) * 0.62) / extent

    rad_y, rad_p = math.radians(yaw), math.radians(pitch)
    cos_y, sin_y = math.cos(rad_y), math.sin(rad_y)
    cos_p, sin_p = math.cos(rad_p), math.sin(rad_p)

    def transform(x, y, z):
        x -= cx; y -= cy; z -= cz
        x1 = x * cos_y - y * sin_y
        y1 = x * sin_y + y * cos_y
        z1 = z
        x2 = x1
        y2 = y1 * cos_p - z1 * sin_p
        z2 = y1 * sin_p + z1 * cos_p
        sx = width / 2.0 + x2 * scale
        sy = height / 2.0 - z2 * scale + 35.0
        return sx, sy, y2, x2, z2

    # Key light from top-front-left in camera space (x2 < 0, y2 < 0, z2 > 0)
    lx, ly, lz = -0.45, -0.65, 0.61
    projected = []
    for _, (v1, v2, v3) in triangles:
        p1, p2, p3 = transform(*v1), transform(*v2), transform(*v3)
        # In screen coords (X right, Y down), front-facing CCW 3D triangles have cp < 0
        cp = (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])
        if cp >= 0:
            continue
        avg_depth = (p1[2] + p2[2] + p3[2]) / 3.0
        # Camera-space normal
        ux, uy, uz = p2[3] - p1[3], p2[2] - p1[2], p2[4] - p1[4]
        vx, vy, vz = p3[3] - p1[3], p3[2] - p1[2], p3[4] - p1[4]
        nx = uy * vz - uz * vy
        ny = uz * vx - ux * vz
        nz = ux * vy - uy * vx
        n_mag = math.sqrt(nx*nx + ny*ny + nz*nz) or 1.0
        nx, ny, nz = nx / n_mag, ny / n_mag, nz / n_mag
        if ny > 0:
            nx, ny, nz = -nx, -ny, -nz
        dot = max(0.0, nx * lx + ny * ly + nz * lz)
        spec = math.pow(max(0.0, dot), 12) * 0.28
        rim = max(0.0, nz * 0.25)
        intensity = min(1.25, 0.38 + 0.62 * dot + rim)
        r = int(min(255, max(0, base_rgb[0] * intensity + 255 * spec)))
        g = int(min(255, max(0, base_rgb[1] * intensity + 255 * spec)))
        b = int(min(255, max(0, base_rgb[2] * intensity + 255 * spec)))
        fill_hex = f"#{r:02x}{g:02x}{b:02x}"
        stroke_hex = f"#{int(r*0.72):02x}{int(g*0.72):02x}{int(b*0.72):02x}"
        projected.append((avg_depth, p1, p2, p3, fill_hex, stroke_hex))

    projected.sort(key=lambda item: item[0], reverse=True)

    svg_path = out_png.replace(".png", ".svg")
    with open(svg_path, "w") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">\n')
        f.write('<defs><radialGradient id="bg" cx="50%" cy="48%" r="65%"><stop offset="0%" stop-color="#1e2530"/><stop offset="100%" stop-color="#0d1117"/></radialGradient></defs>\n')
        f.write(f'<rect width="{width}" height="{height}" fill="url(#bg)"/>\n')
        # Subtle CAD grid lines
        for gx in range(0, width, 60):
            f.write(f'<line x1="{gx}" y1="0" x2="{gx}" y2="{height}" stroke="#ffffff" stroke-opacity="0.03" stroke-width="1"/>\n')
        for gy in range(0, height, 60):
            f.write(f'<line x1="0" y1="{gy}" x2="{width}" y2="{gy}" stroke="#ffffff" stroke-opacity="0.03" stroke-width="1"/>\n')
        # Header HUD banner
        f.write(f'<rect x="32" y="24" width="{width-64}" height="68" rx="10" fill="#161b22" fill-opacity="0.85" stroke="#30363d" stroke-width="1.5"/>\n')
        f.write(f'<text x="54" y="54" fill="#f0f6fc" font-family="DejaVu Sans, sans-serif" font-size="22" font-weight="bold">{title.replace("&", "&amp;")}</text>\n')
        f.write(f'<text x="54" y="78" fill="#8b949e" font-family="DejaVu Sans Mono, monospace" font-size="14">{subtitle.replace("&", "&amp;")}  |  BBox: {max_x-min_x:.1f} x {max_y-min_y:.1f} x {max_z-min_z:.1f} mm</text>\n')
        for _, p1, p2, p3, fill_hex, stroke_hex in projected:
            pts = f"{p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f} {p3[0]:.1f},{p3[1]:.1f}"
            f.write(f'<polygon points="{pts}" fill="{fill_hex}" stroke="{stroke_hex}" stroke-width="0.45" stroke-linejoin="round"/>\n')
        f.write("</svg>\n")

    subprocess.run(["magick", svg_path, out_png], check=True)
    if os.path.exists(svg_path):
        os.remove(svg_path)
    print("Rendered studio showcase:", out_png)


if __name__ == "__main__":
    catalog = [
        (
            "Bed1_01_DM62659_AirCooled_Collar.stl",
            "studio_part1_spindle_shroud.png",
            "BED 1  //  HARBOR FREIGHT 62659 FINNED AIR-COOLED SPINDLE SHROUD",
            "6-Wall PLA+  |  65.2mm Bore  |  8 Venturi Flutes + 4 Heat-Sink Fins + Down-Draft Ring",
            (20, 184, 198),
        ),
        (
            "Bed1_02_Z_Leadscrew_Top_Bearing_Cap.stl",
            "studio_part2_z_stepper_arch.png",
            "BED 1  //  INTEGRATED Z-AXIS V-GUIDEWAY & DUAL-608ZZ ARCH TOWER",
            "6-Wall PLA+  |  Twin Vertical V-Guide Rails + Top & Bottom 608ZZ Pockets + Coupler Window",
            (95, 110, 128),
        ),
        (
            "Bed2_01_TwinRail_Y_Outrigger.stl",
            "studio_part3_y_outrigger.png",
            "BED 2  //  TWIN-RAIL Y-BED OUTRIGGER & GROUND CONCRETE BASE SILL",
            "5-Wall PLA+  |  V-Wheel Protective Skirt  |  Rides on Ground-Anchored Twin 2040 Ways",
            (26, 166, 184),
        ),
        (
            "Bed2_02_Ground_Concrete_Base_Sill.stl",
            "studio_part6_ground_base_sill.png",
            "BED 2  //  GROUND-CONTACTING CONCRETE MACHINE BASE SILL (Z = 0.0 mm)",
            "5-Wall Hydrostatic Shell  |  Cradles Twin 400mm 2040 Y-Ways  |  40% of Concrete Mass in Base",
            (92, 102, 115),
        ),
        (
            "Bed3_01_Concrete_Column_Sleeve_Half.stl",
            "studio_part4_exoskeleton_column.png",
            "BED 3  //  TAPERED GROUND-CONTACTING MILL PORTAL COLUMN (Z = 0.0 mm)",
            "5-Wall Hydrostatic Shell  |  118mm Base Foot -> 76mm Top  |  Touches Ground Flush at Z=0",
            (92, 102, 115),
        ),
        (
            "Bed3_02_Concrete_X_Girder_Half.stl",
            "studio_part5_x_bridge_girder.png",
            "BED 3  //  THICK DEEP-SECTION PORTAL BOX-BEAM X-CROSSBAR",
            "5-Wall Hydrostatic Shell  |  84x112mm Coffered Box Beam (5.8x Stiffness) + Column Saddle",
            (240, 108, 20),
        ),
    ]
    for stl_name, png_name, title, subtitle, rgb in catalog:
        stl_p = os.path.join(STL_DIR, stl_name)
        if os.path.exists(stl_p):
            render_stl_studio(stl_p, os.path.join(RENDER_DIR, png_name), title, subtitle, rgb)
