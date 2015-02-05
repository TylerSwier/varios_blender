import bpy
bpy.ops.mesh.primitive_plane_add(radius=1, view_align=False, enter_editmode=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
bpy.ops.object.editmode_toggle()
bpy.ops.mesh.delete(type='VERT')

bpy.ops.object.editmode_toggle()
bpy.context.selected_objects[0].data.vertices.add(1)
bpy.context.selected_objects[0].data.update
bpy.ops.object.editmode_toggle()

longitud=5
cuantos_segmentos=40
calidad_de_colision=10
for i in range(cuantos_segmentos):
    bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(longitud/cuantos_segmentos, 0, 0), "constraint_axis":(True, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False})

bpy.ops.object.vertex_group_add()
#bpy.context.object.name = "pin"    
bpy.ops.object.vertex_group_assign()

# Group contiene los vertices del pin y Group.001 contiene la linea unica principal

bpy.ops.mesh.select_all(action='TOGGLE')
bpy.ops.mesh.select_all(action='TOGGLE') # sleccionamos todos los vertices y hacemos un nuevo grupo de vertices
bpy.ops.object.vertex_group_add()
bpy.ops.object.vertex_group_assign()

bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0, 0.005, 0), "constraint_axis":(False, True, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False})
bpy.ops.object.vertex_group_remove_from()


bpy.ops.mesh.select_all(action='TOGGLE')
bpy.ops.object.editmode_toggle()

bpy.ops.object.modifier_add(type='CLOTH')
bpy.context.object.modifiers["Cloth"].settings.use_pin_cloth = True
bpy.context.object.modifiers["Cloth"].settings.vertex_group_mass = "Group"
bpy.context.object.modifiers["Cloth"].collision_settings.collision_quality = calidad_de_colision

