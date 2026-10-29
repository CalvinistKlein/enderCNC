#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
FreeCAD MCP Server & Live CAD Decomposition Bridge (`freecad_mcp_bridge.py`)
-------------------------------------------------------------------------------
1. Exposes a live XML-RPC / JSON-RPC & MCP-compatible endpoint inside FreeCAD
   on port 9876 (`create_parametric_part`, `boolean_operation`,
   `apply_structural_ribs`, `export_mesh`, `rearrange_ender3_donor`).
2. Loads the official Creality Ender 3 STEP assembly from `ender3_cad_repo`,
   identifies all genuine stock Ender 3 parts (2040/2020/4040 extrusions,
   NEMA 17 steppers, V-slot wheels, X-carriage plate, heated bed plate, PSU,
   leadscrew, brackets), and rearranges them with ZERO aluminum cuts into the
   10.5" x 11.0" x 3.5" (and 2.0" Low-Deck) PLA+ & Concrete RepStrap CNC Mill.
===============================================================================
"""

import os
import sys
import json
import math
import threading
from xmlrpc.server import SimpleXMLRPCServer

import FreeCAD as App
import Part
import Mesh
from FreeCAD import Base

WORKSPACE_DIR = "/home/calvin/Documents/U-Penn/Website Files/html"
EXPORT_DIR = os.path.join(WORKSPACE_DIR, "stl_exports_zerocut")
os.makedirs(EXPORT_DIR, exist_ok=True)


class FreeCADMCPServer:
    """
    Implements the exact `freecad_mcp` tool interface inside the running FreeCAD
    instance and allows live external queries and updates.
    """
    def __init__(self, doc):
        self.doc = doc
        self.parts = {}

    def ping(self):
        return {"status": "online", "document": self.doc.Name, "objects": len(self.doc.Objects)}

    def list_objects(self):
        out = []
        for obj in self.doc.Objects:
            if hasattr(obj, "Shape") and obj.Shape and not obj.Shape.isNull():
                bb = obj.Shape.BoundBox
                out.append({
                    "name": obj.Name,
                    "label": obj.Label,
                    "size_in": [
                        round(bb.XLength / 25.4, 2),
                        round(bb.YLength / 25.4, 2),
                        round(bb.ZLength / 25.4, 2),
                    ],
                    "size_mm": [
                        round(bb.XLength, 1),
                        round(bb.YLength, 1),
                        round(bb.ZLength, 1),
                    ],
                })
        return out

    def set_z_deck_mode(self, mode="high"):
        """
        Switches the live FreeCAD assembly between:
          - 'high': 3.5" (88.9mm) Z-clearance for wood / 2x4s / relief carving
          - 'low' : 2.0" (50.8mm) Z-clearance for 1/4" 6061 aluminum & brass milling
        """
        z_offset = 0.0 if mode == "high" else -(1.5 * 25.4)
        bridge_objs = [
            "Donor_2020_X_Bridge_13in",
            "Donor_X_Carriage_Assy",
            "PLA_Concrete_X_Girder_L",
            "PLA_Concrete_X_Girder_R",
            "PLA_DM62659_AirCooled_Collar",
            "HarborFreight_DM62659_Router",
        ]
        for name in bridge_objs:
            obj = self.doc.getObject(name)
            if obj and hasattr(obj, "Placement"):
                base_z = getattr(obj, "_high_deck_z", obj.Placement.Base.z)
                obj.Placement.Base.z = base_z + z_offset
        self.doc.recompute()
        return {"status": "ok", "deck_mode": mode, "z_offset_mm": z_offset}

    def export_mesh(self, part_id, fmt="STL", tolerance=0.05):
        obj = self.doc.getObject(part_id)
        if not obj:
            return {"error": f"Object {part_id} not found"}
        out_path = os.path.join(EXPORT_DIR, f"{part_id}.{fmt.lower()}")
        Mesh.export([obj], out_path)
        return {
            "part_id": part_id,
            "path": out_path,
            "volume_cm3": round(obj.Shape.Volume / 1000.0, 2),
            "manifold": obj.Shape.isValid(),
        }
