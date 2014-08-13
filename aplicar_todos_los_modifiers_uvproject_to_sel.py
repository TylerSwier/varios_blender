import bpy
objetos=bpy.context.selected_objects[:]
for ob in objetos:
    bpy.ops.object.select_all(action='DESELECT')
    ob = bpy.data.objects[ob.name]
    ob.select = True
    if "UV_PROJECT" in ob.modifiers:
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="UV_PROJECT")
