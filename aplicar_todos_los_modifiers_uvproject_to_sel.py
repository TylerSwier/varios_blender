import bpy
objetos=bpy.context.selected_objects[:]
for ob in objetos:
    ob = bpy.data.objects[ob.name]
    ob.select = True
    bpy.context.scene.objects.active = ob
    if "UV_PROJECT" in ob.modifiers:
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="UV_PROJECT")
