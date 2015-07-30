import bpy  

ob = bpy.context.selected_objects[0]

bpy.ops.object.empty_add(type='PLAIN_AXES', radius=1, view_align=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
bpy.context.object.name = "target_lights"

vectores=[]
for vertex in ob.data.vertices:
    vco = vertex.co
    mat = ob.matrix_world
    loc = mat * vco
    #print(loc)
    vectores.append(loc)

for c in vectores:
    x = c[0]
    y = c[1]
    z = c[2]
    if z >= 0:    
        bpy.ops.object.lamp_add(type='SPOT', radius=1, view_align=False, location=(x, y, z), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        bpy.ops.object.constraint_add(type='TRACK_TO')
        bpy.context.object.constraints["Track To"].target = bpy.data.objects["target_lights"]
        bpy.context.object.constraints["Track To"].track_axis = 'TRACK_NEGATIVE_Z'
        bpy.context.object.constraints["Track To"].up_axis = 'UP_Y'
        #bpy.ops.mesh.primitive_cube_add(view_align=False, enter_editmode=False, location=(x, y, z), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        #bpy.ops.transform.resize(value=(0.023373, 0.023373, 0.023373), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
