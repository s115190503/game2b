"""Create an original low-poly Star Dreamling asset for Blender 5.x."""
import bpy, os
from mathutils import Vector
bpy.ops.wm.read_factory_settings(use_empty=True)
def mat(name,color,metallic=0,rough=.55):
    m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.metallic=metallic;m.roughness=rough;return m
violet=mat('Dreamling plum',(.27,.12,.22));bodymat=mat('Dreamling coat',(.16,.23,.34));cream=mat('Moon cream',(.95,.73,.42),0,.3);gold=mat('Star gold',(.92,.49,.18),.25,.3);dark=mat('Night ground',(.025,.05,.08))
def sphere(name,loc,scale,material):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,location=loc);o=bpy.context.object;o.name=name;o.scale=scale;o.data.materials.append(material);bpy.ops.object.shade_smooth();return o
def cone(name,loc,r1,r2,depth,material,rot=(0,0,0)):
    bpy.ops.mesh.primitive_cone_add(vertices=16,radius1=r1,radius2=r2,depth=depth,location=loc,rotation=rot);o=bpy.context.object;o.name=name;o.data.materials.append(material);return o
sphere('Body',(0,0,1.15),(.62,.43,.82),bodymat);sphere('Head',(0,0,2.2),(.67,.5,.62),violet)
cone('Horn.L',(-.38,0,2.72),.19,0,.65,violet,(0,-.35,-.18));cone('Horn.R',(.38,0,2.72),.19,0,.65,violet,(0,.35,.18));sphere('Eye.L',(-.23,-.46,2.27),(.07,.035,.1),cream);sphere('Eye.R',(.23,-.46,2.27),(.07,.035,.1),cream);sphere('Foot.L',(-.32,-.04,.38),(.34,.3,.13),bodymat);sphere('Foot.R',(.32,-.04,.38),(.34,.3,.13),bodymat);sphere('LanternGlow',(.8,-.35,1.55),(.23,.23,.3),cream);cone('Lantern',(.8,-.35,1.5),.27,.22,.55,gold)
bpy.ops.mesh.primitive_plane_add(size=12,location=(0,0,.2));bpy.context.object.name='Night Ground';bpy.context.object.data.materials.append(dark)
bpy.ops.object.light_add(type='AREA',location=(1,-3,3));bpy.context.object.data.energy=550;bpy.context.object.data.color=(1,.65,.3);bpy.context.object.data.size=3
bpy.ops.object.light_add(type='AREA',location=(-3,1,3));bpy.context.object.data.energy=350;bpy.context.object.data.color=(.2,.55,1);bpy.context.object.data.size=4
bpy.ops.object.camera_add(location=(4,-7,3.1));cam=bpy.context.object;bpy.context.scene.camera=cam;direction=Vector((0,0,1.45))-cam.location;cam.rotation_euler=direction.to_track_quat('-Z','Y').to_euler();cam.data.lens=52
scene=bpy.context.scene;scene.render.engine='BLENDER_EEVEE';scene.render.resolution_x=700;scene.render.resolution_y=700;scene.render.resolution_percentage=100;scene.render.filepath=os.path.join(os.path.dirname(__file__),'star_dreamling_preview.png');base=os.path.dirname(__file__);bpy.ops.wm.save_as_mainfile(filepath=os.path.join(base,'star_dreamling.blend'));bpy.ops.wm.obj_export(filepath=os.path.join(base,'star_dreamling.obj'));bpy.ops.render.render(write_still=True)
