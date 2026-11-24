"""Polish the original dreamling scene with a cinematic 3D environment and looped animation."""
import bpy
import math
import os
from mathutils import Vector

ROOT = os.path.dirname(os.path.abspath(__file__))
bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT, "star_dreamling.blend"))


def mat(name, color, metallic=0.0, roughness=0.45, emission=None):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1.0)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    if emission:
        bsdf.inputs["Emission Color"].default_value = (*emission[0], 1.0)
        bsdf.inputs["Emission Strength"].default_value = emission[1]
    return m


def smooth(obj, bevel=0.0):
    if obj.type == "MESH":
        for poly in obj.data.polygons:
            poly.use_smooth = True
    if bevel and obj.type == "MESH":
        mod = obj.modifiers.new("Cinematic soft edges", "BEVEL")
        mod.width = bevel
        mod.segments = 3
    return obj


def sphere(name, loc, scale, material):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=20, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    obj.data.materials.append(material)
    return smooth(obj)


def add_star(name, loc, size, material):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=size, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.scale = (1.0, 1.0, 1.5)
    obj.data.materials.append(material)
    return obj


def add_torus(name, loc, major, minor, material, rotation=(math.pi / 2, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor, major_segments=64, minor_segments=16, location=loc, rotation=rotation)
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(material)
    return smooth(obj)


plum = mat("Dreamling plum", (0.24, 0.055, 0.28), roughness=0.3)
coat = mat("Dreamling velvet coat", (0.045, 0.12, 0.30), roughness=0.26)
gold = mat("Lantern gold", (0.95, 0.32, 0.04), metallic=0.25, roughness=0.2, emission=((1.0, 0.12, 0.01), 1.5))
star_mat = mat("Star emission", (1.0, 0.48, 0.05), roughness=0.15, emission=((1.0, 0.18, 0.01), 5.0))
stone = mat("Dream portal stone", (0.06, 0.11, 0.25), roughness=0.62)
stone_edge = mat("Dream portal edge", (0.20, 0.35, 0.70), metallic=0.2, roughness=0.3, emission=((0.03, 0.08, 0.4), 0.6))

# Upgrade existing materials and soften every mesh for a coherent stylized render.
for obj in bpy.context.scene.objects:
    if obj.type == "MESH":
        smooth(obj, 0.025)

# A luminous portal and a few floating stars make the environment readable.
portal = add_torus("Dream gate halo", (0, 0.7, 2.75), 2.15, 0.12, stone_edge)
inner = add_torus("Dream gate inner glow", (0, 0.62, 2.75), 1.74, 0.045, star_mat)
for idx, pos in enumerate(((-2.7, 0.45, 4.75), (-1.75, 0.1, 5.45), (2.1, 0.4, 5.1), (3.0, 0.8, 4.3), (0.0, 0.2, 5.6))):
    add_star("Portal star %02d" % idx, pos, 0.11 if idx != 4 else 0.16, star_mat)

# Layered platform and side stones.
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0.05), scale=(3.5, 2.7, 0.16))
platform = bpy.context.object
platform.name = "Moonlit stone platform"
platform.data.materials.append(stone)
smooth(platform, 0.12)
add_torus("Platform rim", (0, 0, 0.25), 2.8, 0.055, stone_edge, rotation=(0, 0, 0))

# Animate the character, lantern and halo for a seamless idle loop.
body = bpy.data.objects.get("Body") or bpy.data.objects.get("Dreamling body")
if body:
    body.location.z = 0
    body.keyframe_insert(data_path="location", index=2, frame=1)
    body.location.z = 0.10
    body.keyframe_insert(data_path="location", index=2, frame=60)
    body.location.z = 0
    body.keyframe_insert(data_path="location", index=2, frame=120)
light = bpy.data.objects.get("Lantern glow") or bpy.data.objects.get("Area")
if light and light.type == "LIGHT":
    light.data.energy = 100
    light.data.keyframe_insert(data_path="energy", frame=1)
    light.data.energy = 170
    light.data.keyframe_insert(data_path="energy", frame=60)
    light.data.energy = 100
    light.data.keyframe_insert(data_path="energy", frame=120)
inner.rotation_euler.z = 0
inner.keyframe_insert(data_path="rotation_euler", index=2, frame=1)
inner.rotation_euler.z = math.tau
inner.keyframe_insert(data_path="rotation_euler", index=2, frame=120)

scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = 120
scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x = 1024
scene.render.resolution_y = 768
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = os.path.join(ROOT, "star_dreamling_preview.png")
if scene.world is None:
    scene.world = bpy.data.worlds.new("Dream night world")
scene.world.use_nodes = True
scene.world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.003, 0.006, 0.03, 1)
scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.14

# Cinematic warm key, cool rim and soft fill.
bpy.ops.object.light_add(type="AREA", location=(1.6, -4.5, 5.0))
key = bpy.context.object
key.name = "Cinematic warm key"
key.data.energy = 900
key.data.color = (1.0, 0.36, 0.12)
key.data.size = 3.2
key.rotation_euler = (math.radians(24), 0, math.radians(18))
bpy.ops.object.light_add(type="AREA", location=(-4, 1, 4.8))
rim = bpy.context.object
rim.name = "Cinematic blue rim"
rim.data.energy = 1200
rim.data.color = (0.12, 0.32, 1.0)
rim.data.size = 4.0
rim.rotation_euler = (math.radians(62), 0, math.radians(-55))

camera = scene.camera
camera.location = (5.8, -9.2, 4.2)
camera.data.lens = 58
camera.rotation_euler = (Vector((0, 0.35, 2.0)) - camera.location).to_track_quat("-Z", "Y").to_euler()

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT, "star_dreamling.blend"))
bpy.ops.wm.obj_export(filepath=os.path.join(ROOT, "star_dreamling.obj"))
try:
    bpy.ops.export_scene.gltf(filepath=os.path.join(ROOT, "star_dreamling.glb"), export_format="GLB", export_animations=True)
except Exception as exc:
    print("GLB export warning:", exc)
bpy.ops.render.render(write_still=True)
