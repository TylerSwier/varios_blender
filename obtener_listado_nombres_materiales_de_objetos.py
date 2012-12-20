# optener listado de materiales de objetos
def obtenermateriales(opcion1):
    mat_list = []
    if opcion1 == "local":
        sel = bpy.context.selected_objects
        if len(sel) == 0:    
            for os in bpy.context.scene.objects:
                for slot in os.material_slots:
                    mat_list.append(slot)
        else:
            for os in sel:
                for slot in os.material_slots:
                    mat_list.append(slot)
    else:
        sel = bpy.context.selected_objects
        for escena in bpy.data.scenes:
            for os in bpy.data.scenes[escena.name].objects:
                if len(sel) == 0:
                    for slot in os.material_slots:
                        mat_list.append(slot)
                else:
                    for so in sel:
                        for slot in so.material_slots:
                            mat_list.append(slot)   
    # limpiando lista de repetidos:
    preparando = list(set(mat_list))
    mat_list = preparando
    return mat_list

# Nota: si no es en "local" y si es con algo seleccionado, evidentemente 
# saldran solo los de los objetos deleccionados de la escena actual, ya 
# que los full copy scene cambian de nombre los objetos y son "unicos"
mat = obtenermateriales("local")
for i in mat:
    print(i.name)
