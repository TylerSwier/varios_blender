import bpy, bmesh
 
bpy.ops.object.mode_set(mode = 'EDIT')   # Go to edit mode to create bmesh
ob = bpy.context.object                  # Reference to selected object
 
bm = bmesh.from_edit_mesh(ob.data)       # Create bmesh object from object mesh

bm.verts.ensure_lookup_table()           # <- para que no de error
bm.select_mode = {'FACE'}                # Go to face selection mode

# lista de nombres de los de materiales asignados a alguna cara:
materiales_aplicados = [] 
# por cada cara:
for face in bm.faces:
    material = ob.material_slots[face.material_index].name
    materiales_aplicados.append(material)

ob.data.update()                         # Update the mesh from the bmesh data
bpy.ops.object.mode_set(mode = 'OBJECT') # volvemos a object mode 

# comprobamos por cada slot del objeto si esta o no aplicado:
for i in range(len(ob.material_slots)):
    mat = ob.material_slots[i].name
    if mat in materiales_aplicados:
        print("El material " + str(mat) + " Si esta aplicado")
    else:
        print("El material " + str(mat) + " No esta aplicado")
