import bpy  
ob = bpy.context.selected_objects[0]
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
    bpy.ops.mesh.primitive_cube_add(view_align=False, enter_editmode=False, location=(x, y, z), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    bpy.ops.transform.resize(value=(0.023373, 0.023373, 0.023373), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
