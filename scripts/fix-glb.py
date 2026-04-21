"""
Blender script to fix GLB axis/origin for web 3D viewer.
- Imports GLB
- Joins meshes
- Applies rotation via bmesh (guaranteed to bake into geometry)
- Centers at origin
- Normalizes scale
- Re-exports as clean GLB
Usage: blender --background --python scripts/fix-glb.py -- <rotation_x> <rotation_y> <rotation_z>
Example: blender --background --python scripts/fix-glb.py -- 0 -90 0
"""
import bpy
import bmesh
import sys
import math
from mathutils import Matrix, Vector
from pathlib import Path

argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
ROT_X = float(argv[0]) if len(argv) > 0 else 0
ROT_Y = float(argv[1]) if len(argv) > 1 else 0
ROT_Z = float(argv[2]) if len(argv) > 2 else 0

INPUT = "assets/models/product-viewer.glb"
OUTPUT = "assets/models/product-fixed.glb"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
input_path = PROJECT_ROOT / INPUT
output_path = PROJECT_ROOT / OUTPUT

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
for collection in bpy.data.collections:
    bpy.data.collections.remove(collection)
for mesh in bpy.data.meshes:
    bpy.data.meshes.remove(mesh)

bpy.ops.import_scene.gltf(filepath=str(input_path))

for obj in list(bpy.data.objects):
    if obj.type != "MESH":
        bpy.data.objects.remove(obj, do_unlink=True)

mesh_objects = [obj for obj in bpy.data.objects if obj.type == "MESH"]
print(f"[INFO] Imported {len(mesh_objects)} mesh objects")

if not mesh_objects:
    raise RuntimeError("No mesh found in GLB")

bpy.ops.object.select_all(action="DESELECT")
for obj in mesh_objects:
    obj.select_set(True)
bpy.context.view_layer.objects.active = mesh_objects[0]

if len(mesh_objects) > 1:
    bpy.ops.object.join()

obj = bpy.context.view_layer.objects.active
print(f"[INFO] Active object: {obj.name} (type: {obj.type})")
print(f"[INFO] Mesh vertex count: {len(obj.data.vertices)}")

rot_matrix = (
    Matrix.Rotation(math.radians(ROT_X), 4, "X")
    @ Matrix.Rotation(math.radians(ROT_Y), 4, "Y")
    @ Matrix.Rotation(math.radians(ROT_Z), 4, "Z")
)
print(f"[INFO] Applying rotation: X={ROT_X} Y={ROT_Y} Z={ROT_Z}")

mesh = obj.data
for v in mesh.vertices:
    v.co = rot_matrix @ v.co
mesh.update()

coords = [v.co for v in mesh.vertices]
min_x = min(c.x for c in coords)
max_x = max(c.x for c in coords)
min_y = min(c.y for c in coords)
max_y = max(c.y for c in coords)
min_z = min(c.z for c in coords)
max_z = max(c.z for c in coords)
size_x = max_x - min_x
size_y = max_y - min_y
size_z = max_z - min_z
print(f"[INFO] Dims after rotation: X={size_x:.2f} Y={size_y:.2f} Z={size_z:.2f}")

center_x = (min_x + max_x) / 2
center_y = (min_y + max_y) / 2
center_z = (min_z + max_z) / 2
for v in mesh.vertices:
    v.co.x -= center_x
    v.co.y -= center_y
    v.co.z -= center_z
mesh.update()

max_dim = max(size_x, size_y, size_z)
if max_dim > 0:
    scale_factor = 1.0 / max_dim
    for v in mesh.vertices:
        v.co *= scale_factor
    mesh.update()
    print(f"[INFO] Scale factor: {scale_factor:.4f}")

obj.location = (0, 0, 0)
obj.rotation_euler = (0, 0, 0)
obj.scale = (1, 1, 1)

bpy.ops.export_scene.gltf(
    filepath=str(output_path),
    export_format="GLB",
    export_apply=True,
    export_yup=True,
)

print(f"[SUCCESS] Exported to {output_path}")
