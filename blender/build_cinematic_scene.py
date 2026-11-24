"""Create the final polished Star Dreamling diorama and animation."""
import bpy, math, os
from mathutils import Vector

ROOT = os.path.dirname(os.path.abspath(__file__))
bpy.ops.wm.read_factory_settings(use_empty=True)

def make_mat(name, color, rough=.45, metallic=0.0, emission=None):
    m = bpy.data.materials.new(name); m.use_nodes = True
    p = m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value = (*color, 1)
    p.inputs['Roughness'].default_value = rough
    p.inputs['Metallic'].default_value = metallic
    if emission:
        p.inputs['Emission Color'].default_value = (*emission[0], 1)
        p.inputs['Emission Strength'].default_value = emission[1]
    return m

def finish(o, material, bevel=0.0):
    o.data.materials.append(material)
    if hasattr(o.data, 'polygons'):
        for p in o.data.polygons: p.use_smooth = True
    if bevel:
        b=o.modifiers.new('Soft stylized edges','BEVEL'); b.width=bevel; b.segments=3
    return o

def sphere(name, loc, scale, material):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=20, location=loc)
    o=bpy.context.object; o.name=name; o.scale=scale; return finish(o, material)

def cone(name, loc, r1, r2, depth, material, rot=(0,0,0)):
    bpy.ops.mesh.primitive_cone_add(vertices=32, radius1=r1, radius2=r2, depth=depth, location=loc, rotation=rot)
    o=bpy.context.object; o.name=name; return finish(o, material, .025)

def cube(name, loc, scale, material, bevel=.08):
    bpy.ops.mesh.primitive_cube_add(location=loc); o=bpy.context.object; o.name=name; o.scale=scale
    return finish(o, material, bevel)

def torus(name, loc, major, minor, material, rot=(math.pi/2,0,0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor, major_segments=64, minor_segments=16, location=loc, rotation=rot)
    o=bpy.context.object; o.name=name; return finish(o, material)

plum=make_mat('Dreamling plum',(0.26,0.05,0.30),.28)
coat=make_mat('Dreamling velvet',(0.05,0.13,0.32),.3)
cream=make_mat('Moon cream',(0.96,0.72,0.35),.22,emission=((1,.2,.02),.8))
gold=make_mat('Lantern copper',(0.85,.22,.035),.22,.25,((1,.08,.01),1.5))
blue=make_mat('Portal blue',(.08,.22,.65),.3,.15,((.02,.08,.7),.8))
star=make_mat('Star glow',(1,.4,.03),.18,0,((1,.12,.01),5))
stone=make_mat('Night stone',(.06,.11,.25),.7)
ground=make_mat('Midnight ground',(.006,.012,.04),.9)

# Environment.
bpy.ops.mesh.primitive_plane_add(size=18, location=(0,0,0)); finish(bpy.context.object, ground)
cube('Raised moon platform',(0,0,.18),(3.25,2.5,.18),stone,.14)
torus('Platform light rim',(0,0,.4),2.65,.055,blue,(0,0,0))
torus('Dream portal',(0,1.15,3.1),2.15,.14,blue)
inner=torus('Dream portal inner light',(0,1.03,3.1),1.72,.055,star)
for i,x in enumerate((-2.35,2.35)):
    cube('Portal pillar %d'%i,(x,1.18,1.75),(.22,.3,1.45),stone,.1)
for i,(x,z) in enumerate(((-2.7,5.2),(-1.7,5.7),(1.8,5.5),(2.8,4.8),(0,5.9))):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=.11 if i<4 else .16,location=(x,.9,z))
    finish(bpy.context.object, star)

# Character, centered and connected as a single readable silhouette.
body=sphere('Dreamling body',(0,-.72,1.45),(.72,.55,.98),coat)
head=sphere('Dreamling head',(0,-.77,2.55),(.77,.6,.67),plum)
for side,x in [(-1,-.42),(1,.42)]:
    cone('Dreamling horn', (x,-.78,3.18), .2, .015, .72, plum, (0,-.3*side,-.12*side))
    sphere('Dreamling eye',(x*.57,-1.34,2.63),(.095,.035,.14),cream)
    sphere('Dreamling foot',(x*.42,-.75,.55),(.38,.34,.14),coat)
sphere('Dreamling cheek L',(-.38,-1.33,2.42),(.08,.025,.06),gold)
sphere('Dreamling cheek R',(.38,-1.33,2.42),(.08,.025,.06),gold)
torus('Dreamling tail',(-.66,-.42,1.42),.36,.075,plum,(math.pi/2,.3,0))
cone('Dream lantern',(.95,-.95,1.55),.28,.2,.58,gold)
sphere('Lantern flame',(.95,-1.0,1.78),(.14,.14,.18),cream)

# Cinematic lighting and camera.
scene=bpy.context.scene; scene.render.engine='BLENDER_EEVEE'; scene.render.resolution_x=1024; scene.render.resolution_y=768; scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'; scene.render.filepath=os.path.join(ROOT,'star_dreamling_preview.png')
scene.world=bpy.data.worlds.new('Deep blue dream world'); scene.world.use_nodes=True
scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.002,.004,.025,1); scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.16
bpy.ops.object.light_add(type='AREA', location=(1.8,-4.5,5.2)); key=bpy.context.object; key.name='Warm cinematic key'; key.data.energy=950; key.data.color=(1,.32,.1); key.data.size=3.2
bpy.ops.object.light_add(type='AREA', location=(-4,0,4.5)); rim=bpy.context.object; rim.name='Blue moon rim'; rim.data.energy=1200; rim.data.color=(.12,.3,1); rim.data.size=4
bpy.ops.object.light_add(type='POINT', location=(.95,-1.2,1.8)); glow=bpy.context.object; glow.name='Lantern glow'; glow.data.energy=130; glow.data.color=(1,.12,.02)
bpy.ops.object.camera_add(location=(5.5,-9.5,4.1)); cam=bpy.context.object; scene.camera=cam; cam.data.lens=58; cam.rotation_euler=(Vector((0,.2,2.05))-cam.location).to_track_quat('-Z','Y').to_euler()

# 120-frame idle loop: breathing, lantern pulse, portal rotation.
scene.frame_start=1; scene.frame_end=120
for z,frame in [(0,1),(.1,60),(0,120)]: body.location.z=z; body.keyframe_insert(data_path='location',index=2,frame=frame)
for energy,frame in [(90,1),(160,60),(90,120)]: glow.data.energy=energy; glow.data.keyframe_insert(data_path='energy',frame=frame)
inner.rotation_euler.z=0; inner.keyframe_insert(data_path='rotation_euler',index=2,frame=1); inner.rotation_euler.z=math.tau; inner.keyframe_insert(data_path='rotation_euler',index=2,frame=120)

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'star_dreamling.blend'))
bpy.ops.wm.obj_export(filepath=os.path.join(ROOT,'star_dreamling.obj'))
bpy.ops.export_scene.gltf(filepath=os.path.join(ROOT,'star_dreamling.glb'),export_format='GLB',export_animations=True)
bpy.ops.render.render(write_still=True)
