import bpy

# optener listado de materiales de objetos
def obtenermateriales(opcion1):
    mat_list = []
    if opcion1 == "local":
        tipo = bpy.context.selected_objects
    else:
        tipo = bpy.data.objects    
    if len(tipo) == 0:
        for m in bpy.context.scene.objects:
            for slot in m.material_slots:
                mat_list.append(slot)
    else:
        for m in tipo:
            for slot in m.material_slots:
                mat_list.append(slot)
    return mat_list
    
mat = obtenermateriales("local")
for i in mat:
    print(i.name)
