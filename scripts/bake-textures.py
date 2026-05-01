"""
12cut GLB Texture Baking Script
- Import GLB → Identify parts by material
- UV unwrap all parts
- Assign PBR shaders per part (body, strap, button, lens, logo, internal)
- Bake AO + combined base color into texture maps
- Export as textured GLB

Usage: blender --background --python scripts/bake-textures.py
"""
import bpy
import os
import math

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "models")
INPUT_GLB = os.path.join(OUTPUT_DIR, "product-fixed.glb")
OUTPUT_GLB = os.path.join(OUTPUT_DIR, "product-textured.glb")
TEX_SIZE = 2048

# Part identification by material index (from GLB analysis)
# [0]=Material_8 front shell, [1]=Material_0 back shell,
# [2]=Material_1 back viewfinder, [3]=Material_2 internal plate,
# [4]=Material_3 lens ring, [5]=Material_4 logo emboss,
# [6]=Material_5 button cap, [7]=Material_6 button stem,
# [8]=Material_7 strap loop, [9]=Material_9 front lens
PART_CONFIG = {
    "BODY": {
        "mat_indices": [0, 1],
        "base_color": (0.96, 0.96, 0.96, 1.0),
        "roughness": 0.45,
        "metallic": 0.0,
        "sss_weight": 0.15,
        "sss_radius": (0.05, 0.02, 0.01),
        "sss_color": (1.0, 0.97, 0.95),
    },
    "LOGO": {
        "mat_indices": [5],
        "base_color": (0.93, 0.93, 0.93, 1.0),
        "roughness": 0.55,
        "metallic": 0.0,
        "sss_weight": 0.1,
        "sss_radius": (0.03, 0.01, 0.005),
        "sss_color": (1.0, 0.97, 0.95),
    },
    "STRAP": {
        "mat_indices": [8],
        "base_color": (0.91, 0.12, 0.12, 1.0),
        "roughness": 0.18,
        "metallic": 0.0,
        "transmission": 0.3,
        "ior": 1.45,
    },
    "BUTTON_CAP": {
        "mat_indices": [6],
        "base_color": (0.88, 0.10, 0.10, 1.0),
        "roughness": 0.12,
        "metallic": 0.0,
        "transmission": 0.35,
        "ior": 1.50,
    },
    "BUTTON_STEM": {
        "mat_indices": [7],
        "base_color": (0.85, 0.12, 0.12, 1.0),
        "roughness": 0.15,
        "metallic": 0.0,
        "transmission": 0.25,
        "ior": 1.45,
    },
    "LENS_RING": {
        "mat_indices": [4],
        "base_color": (0.45, 0.45, 0.45, 1.0),
        "roughness": 0.30,
        "metallic": 0.15,
    },
    "LENS_GLASS": {
        "mat_indices": [2, 9],
        "base_color": (0.08, 0.08, 0.08, 1.0),
        "roughness": 0.05,
        "metallic": 0.35,
    },
    "INTERNAL": {
        "mat_indices": [3],
        "base_color": (0.50, 0.50, 0.50, 1.0),
        "roughness": 0.60,
        "metallic": 0.0,
    },
}


def clean_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    for obj in bpy.data.objects:
        bpy.data.objects.remove(obj, do_unlink=True)
    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh, do_unlink=True)
    for mat in bpy.data.materials:
        bpy.data.materials.remove(mat, do_unlink=True)


def import_glb(path):
    bpy.ops.import_scene.gltf(filepath=path)
    obj = None
    for o in bpy.context.scene.objects:
        if o.type == 'MESH':
            obj = o
            break
    if obj:
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
    return obj


def smart_uv_unwrap(obj):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(
        angle_limit=math.radians(66),
        island_margin=0.005,
        area_weight=0.0,
        correct_aspect=True,
        scale_to_bounds=True
    )
    bpy.ops.object.mode_set(mode='OBJECT')


def create_bake_image(name, size=TEX_SIZE):
    img = bpy.data.images.new(name, width=size, height=size, alpha=True)
    img.colorspace_settings.name = 'sRGB'
    return img


def setup_principled_material(mat, config):
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (600, 0)

    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (200, 0)
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    bc = config["base_color"]
    bsdf.inputs['Base Color'].default_value = bc
    bsdf.inputs['Roughness'].default_value = config["roughness"]
    bsdf.inputs['Metallic'].default_value = config["metallic"]

    if config.get("sss_weight"):
        bsdf.inputs['Subsurface Weight'].default_value = config["sss_weight"]
        bsdf.inputs['Subsurface Radius'].default_value = config["sss_radius"]
        bsdf.inputs['Subsurface Scale'].default_value = 0.01

    if config.get("transmission"):
        bsdf.inputs['Transmission Weight'].default_value = config["transmission"]
        bsdf.inputs['IOR'].default_value = config.get("ior", 1.45)

    return bsdf


def add_bake_image_node(mat, img):
    nodes = mat.node_tree.nodes
    tex_node = nodes.new('ShaderNodeTexImage')
    tex_node.image = img
    tex_node.location = (-400, 0)
    tex_node.select = True
    nodes.active = tex_node
    return tex_node


def setup_ao_bake_environment():
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'CPU'
    scene.cycles.samples = 128
    scene.cycles.bake_type = 'AO'
    scene.render.bake.use_pass_direct = False
    scene.render.bake.use_pass_indirect = False
    scene.render.bake.margin = 4
    scene.render.bake.margin_type = 'EXTEND'


def bake_combined(obj):
    scene = bpy.context.scene
    scene.cycles.bake_type = 'COMBINED'
    scene.render.bake.use_pass_direct = True
    scene.render.bake.use_pass_indirect = True
    scene.render.bake.use_pass_color = True
    scene.render.bake.margin = 4

    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    bpy.ops.object.bake(type='COMBINED')


def setup_world_lighting():
    world = bpy.data.worlds.new("BakeWorld")
    bpy.context.scene.world = world
    world.use_nodes = True
    nodes = world.node_tree.nodes
    links = world.node_tree.links
    nodes.clear()

    bg = nodes.new('ShaderNodeBackground')
    bg.inputs['Color'].default_value = (1.0, 1.0, 1.0, 1.0)
    bg.inputs['Strength'].default_value = 1.5

    output = nodes.new('ShaderNodeOutputWorld')
    links.new(bg.outputs['Background'], output.inputs['Surface'])

    sun = bpy.data.lights.new(name="KeyLight", type='SUN')
    sun.energy = 3.0
    sun.color = (1.0, 0.98, 0.95)
    sun_obj = bpy.data.objects.new("KeyLight", sun)
    bpy.context.scene.collection.objects.link(sun_obj)
    sun_obj.rotation_euler = (math.radians(45), math.radians(15), math.radians(30))

    fill = bpy.data.lights.new(name="FillLight", type='SUN')
    fill.energy = 1.2
    fill.color = (0.95, 0.97, 1.0)
    fill_obj = bpy.data.objects.new("FillLight", fill)
    bpy.context.scene.collection.objects.link(fill_obj)
    fill_obj.rotation_euler = (math.radians(60), math.radians(-30), math.radians(-45))

    rim = bpy.data.lights.new(name="RimLight", type='SUN')
    rim.energy = 1.8
    rim.color = (1.0, 1.0, 1.0)
    rim_obj = bpy.data.objects.new("RimLight", rim)
    bpy.context.scene.collection.objects.link(rim_obj)
    rim_obj.rotation_euler = (math.radians(30), math.radians(160), 0)


def main():
    print("\n=== 12cut GLB Texture Bake ===\n")

    print("[1/7] Cleaning scene...")
    clean_scene()

    print("[2/7] Importing GLB...")
    obj = import_glb(INPUT_GLB)
    if not obj:
        print("ERROR: No mesh found in GLB")
        return

    mat_names = [slot.material.name if slot.material else "None" for slot in obj.material_slots]
    print(f"  Found {len(mat_names)} materials: {mat_names}")

    print("[3/7] UV Unwrapping...")
    smart_uv_unwrap(obj)

    print("[4/7] Setting up materials...")
    mat_index_to_part = {}
    for part_name, config in PART_CONFIG.items():
        for mi in config["mat_indices"]:
            mat_index_to_part[mi] = part_name

    for slot_idx, slot in enumerate(obj.material_slots):
        part_name = mat_index_to_part.get(slot_idx)
        if not part_name:
            continue
        config = PART_CONFIG[part_name]
        mat = slot.material
        if not mat:
            continue
        setup_principled_material(mat, config)
        print(f"  [{slot_idx}] {mat.name} → {part_name}")

    print("[5/7] Setting up lighting for bake...")
    setup_world_lighting()
    setup_ao_bake_environment()

    print("[6/7] Baking textures...")
    bake_img = create_bake_image("12cut_baked", TEX_SIZE)

    for slot in obj.material_slots:
        if slot.material:
            add_bake_image_node(slot.material, bake_img)

    bpy.context.scene.cycles.bake_type = 'COMBINED'
    bpy.context.scene.render.bake.use_pass_direct = True
    bpy.context.scene.render.bake.use_pass_indirect = True
    bpy.context.scene.render.bake.use_pass_color = True

    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.bake(type='COMBINED')

    bake_path = os.path.join(OUTPUT_DIR, "12cut_baked.png")
    bake_img.filepath_raw = bake_path
    bake_img.file_format = 'PNG'
    bake_img.save()
    print(f"  Saved baked texture: {bake_path}")

    print("[6b/7] Baking AO...")
    ao_img = create_bake_image("12cut_ao", TEX_SIZE)
    for slot in obj.material_slots:
        if slot.material:
            nodes = slot.material.node_tree.nodes
            for n in nodes:
                if n.type == 'TEX_IMAGE':
                    n.image = ao_img
                    nodes.active = n

    bpy.ops.object.bake(type='AO')
    ao_path = os.path.join(OUTPUT_DIR, "12cut_ao.png")
    ao_img.filepath_raw = ao_path
    ao_img.file_format = 'PNG'
    ao_img.save()
    print(f"  Saved AO texture: {ao_path}")

    print("[6c/7] Compositing final materials...")
    for slot_idx, slot in enumerate(obj.material_slots):
        mat = slot.material
        if not mat:
            continue
        part_name = mat_index_to_part.get(slot_idx)
        if not part_name:
            continue
        config = PART_CONFIG[part_name]

        nodes = mat.node_tree.nodes
        links = mat.node_tree.links

        for n in list(nodes):
            if n.type == 'TEX_IMAGE':
                nodes.remove(n)

        bsdf = None
        for n in nodes:
            if n.type == 'BSDF_PRINCIPLED':
                bsdf = n
                break
        if not bsdf:
            continue

        baked_tex = nodes.new('ShaderNodeTexImage')
        baked_tex.image = bake_img
        baked_tex.location = (-600, 200)

        ao_tex = nodes.new('ShaderNodeTexImage')
        ao_tex.image = ao_img
        ao_tex.location = (-600, -100)

        mix = nodes.new('ShaderNodeMix')
        mix.data_type = 'RGBA'
        mix.blend_type = 'MULTIPLY'
        mix.location = (-200, 100)
        mix.inputs['Factor'].default_value = 0.6

        links.new(baked_tex.outputs['Color'], mix.inputs[6])
        links.new(ao_tex.outputs['Color'], mix.inputs[7])
        links.new(mix.outputs[2], bsdf.inputs['Base Color'])

    print("[7/7] Exporting textured GLB...")
    bpy.ops.export_scene.gltf(
        filepath=OUTPUT_GLB,
        export_format='GLB',
        export_image_format='JPEG',
        export_jpeg_quality=85,
        export_materials='EXPORT',
        export_cameras=False,
        export_lights=False,
        export_apply=True,
    )
    print(f"  Exported: {OUTPUT_GLB}")

    file_size = os.path.getsize(OUTPUT_GLB)
    print(f"  File size: {file_size / 1024 / 1024:.2f} MB")
    print("\n=== Done ===\n")


if __name__ == "__main__":
    main()
