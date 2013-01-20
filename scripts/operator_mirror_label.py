bl_info = {
    "name": "Mirror Label",
    "description": "Mirror a decal or label node across the X axis.",
    "author": "John Bartholomew",
    "version": (1, 0),
    "blender": (2, 65, 0),
    "location": "Mirror Label",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"}

import bpy
import mathutils
import math

def get_rot(obj):
    mode = obj.rotation_mode
    if mode == 'QUATERNION':
        return obj.rotation_quaternion.to_matrix()
    else:
        return obj.rotation_euler.to_matrix()

def put_rot(obj, m):
    mode = obj.rotation_mode
    if mode == 'QUATERNION':
        obj.rotation_quaternion = m.to_quaternion()
    else:
        obj.rotation_euler = m.to_euler(mode)

def main(context):
    source = bpy.context.active_object
    target = [x for x in bpy.context.selected_objects if x != source]
    assert len(target) == 1
    target = target[0]

    loc = source.location.copy()
    loc.x *= -1.0

    m = get_rot(source)
    print('source rot:', m)
    yy = m.col[1]
    yy.x *= -1.0
    zz = m.col[2]
    zz.x *= -1.0
    xx = yy.cross(zz)
    m.col[0] = xx
    m.col[1] = yy
    m.col[2] = zz
    print('target rot:', m)

    target.location = loc
    target.scale = source.scale
    put_rot(target, m)
    bpy.context.scene.update()

class MirrorLabel(bpy.types.Operator):
    """Mirror label node"""
    bl_idname = "object.mirror_label"
    bl_label = "Mirror Label"

    @classmethod
    def poll(cls, context):
        return len(bpy.context.selected_objects) == 2 and context.active_object in bpy.context.selected_objects

    def execute(self, context):
        main(context)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(MirrorLabel)


def unregister():
    bpy.utils.unregister_class(MirrorLabel)


if __name__ == "__main__":
    register()
