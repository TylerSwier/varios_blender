import bpy

scn = bpy.context.scene

def seleccionar_por_nombre(nombre):
    bpy.ops.object.select_all(action='DESELECT')
    for ob in bpy.data.objects:
        if ob.name.find(nombre) >= 0:
            ob.select = True
            scn.objects.active = bpy.data.objects[str(ob.name)]

def backuper(ob):
    for i in range(len(ob.data.uv_layers)):
        ob.data.uv_textures[i].active = True
        if ob.data.uv_layers[i].name.find("backup_") != 0: # -1 no lo contiene, 0 si lo contiene:
            ob.data.uv_layers[i].name = str("backup_") + str(ob.data.uv_layers[i].name)

def crar_nuevo_uvmap(ob):
    if len(ob.data.uv_layers) != 0:
        backuper(ob)
    if "nuevo_mapa_uv" not in ob.data.uv_layers:
        bpy.ops.mesh.uv_texture_add()
        cuantos=len(ob.data.uv_textures)-1
        ob.data.uv_textures[cuantos].name = "nuevo_mapa_uv"
        ob.data.uv_textures[cuantos].active = True
        ob.data.uv_textures[cuantos].active_render = True    

def uv_chekeador(ob):
    seleccionar_por_nombre(ob.name)
    # backupeamos :
    if "backup_" not in ob.data.uv_layers and len(ob.data.uv_layers) != 0: # -1 no lo contiene, 0 si lo contiene:
        backuper(ob)
    # y creamos nuevas:       
    if "nuevo_mapa_uv" not in ob.data.uv_layers:
        crar_nuevo_uvmap(ob)

def nuevo_gestor(ob):
    cuantos = len(ob.data.uv_layers)
    if cuantos == 0:
        crar_nuevo_uvmap(ob)
    else:
        backuper(ob)

# cuantos materiales tiene (sin contar con 0):
total_mats = len(bpy.context.object.material_slots)
objetos = bpy.context.selected_objects
for a, ob in enumerate(objetos):
    #print(a)
    #print(ob)
    #uv_chekeador(ob)
    nuevo_gestor(ob)
    #creamos una nueva imagen por objeto donde ira el bakeo:
    #bpy.data.window_managers["WinMan"].(null) = "nuevo_map"
    nombre='nuevo_mapa_para_bakeo_0' + str(a)
    bpy.ops.image.new(name=nombre)
    for i in range(total_mats):
        if 'img_texture_automatic' not in bpy.context.object.material_slots[i].material.node_tree.nodes:
            bpy.context.object.material_slots[i].material.node_tree.nodes.new("ShaderNodeTexImage")
            bpy.context.object.material_slots[i].material.node_tree.nodes['Image Texture'].image = bpy.data.images[nombre]
            bpy.context.object.material_slots[i].material.node_tree.nodes['Image Texture'].name = 'img_texture_automatic'
