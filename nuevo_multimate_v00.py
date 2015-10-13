###################################
# testeado en blender 2.75a y 2.76
###################################

import bpy

def selectAll():
    bpy.ops.object.select_all(action='SELECT')

def deselectAll():
    bpy.ops.object.select_all(action='DESELECT')

def selectOnlyOneObjectByName(obn,scn = bpy.context.scene):
    ob = bpy.context.scene.objects[obn]
    bpy.ops.object.select_all(action='DESELECT')
    scn.objects.active = ob
    ob.select = True

def createNewScene(name, tipo='NEW', retornamos=False, motor='CYCLES'):
    scn_original = bpy.context.scene.name
    if tipo == 'NEW':
        bpy.ops.scene.new(type='NEW')
    if tipo == 'FULL_COPY':
        bpy.ops.scene.new(type='FULL_COPY')
    bpy.context.scene.name = name
    new_scn = bpy.context.scene.name
    if motor == 'CYCLES':
        bpy.context.scene.render.engine = motor
    if retornamos:
        bpy.context.screen.scene = bpy.data.scenes[scn_original]
    return [scn_original,new_scn]

# para hacer los materiales unicos y no vinculados (Make a single user copy):
def makeMaterialSingleUserCopy(ob,nombre):
    ob.active_material = bpy.data.materials[nombre].copy()

def cuantos_materiales_tiene(ob):
    return len(ob.material_slots)

def aplicar_shader(ob,nombre):
    ob.active_material = bpy.data.materials[nombre]

def crear_shader_shadeless(nombre,color):
    # solo lo creamos si no existe previamente:
    if buscador_posicion(bpy.data.materials, nombre) == '-1':
        bpy.data.materials.new(nombre)
        bpy.data.materials[nombre].use_nodes = True
        bpy.data.materials[nombre].node_tree.nodes.new(type='ShaderNodeEmission')
        outp = bpy.data.materials[nombre].node_tree.nodes['Emission'].outputs[0]
        # esta complicacion la creo por que en osx tuve problemas:
        materialoutput = buscador_posicion(bpy.data.materials[nombre].node_tree.nodes,'Material Output')
        moinput = buscador_posicion(bpy.data.materials[nombre].node_tree.nodes[materialoutput].inputs,'Surface')
        inp = bpy.data.materials[nombre].node_tree.nodes[materialoutput].inputs[moinput]
        if color == 'Rojo':
            color = 1,0,0,1
        if color == 'Verde':
            color = 0,1,0,1
        if color == 'Azul':
            color = 0,0,1,1
        ep = buscador_posicion(bpy.data.materials[nombre].node_tree.nodes,'Emission')
        bpy.data.materials[nombre].node_tree.nodes[ep].inputs[0].default_value = color
        # si sale muy mal el AA poner 1 en lugar de 1.25:
        bpy.data.materials[nombre].node_tree.nodes[ep].inputs[1].default_value = 1
        bpy.data.materials[nombre].node_tree.links.new(inp,outp)

def copyCurrentObjectToScene(ob, toscene):
    # Para evitar list index out of range:
    if len(bpy.context.selected_objects) != 0 and len(ob.material_slots) != 0:
        # duplico
        bpy.ops.object.duplicate(linked=False, mode='TRANSLATION')
        # guardo el nombre del nuevo duplicado
        duplicado = bpy.context.selected_objects[0]
        # renombro
        bpy.data.objects[duplicado.name].name = ob.name + "_copy"
        # copio el duplicado a su escena
        bpy.ops.object.make_links_scene(scene=toscene)
        # una vez copiado a la otra escena borro el duplicado de la escena actual
        bpy.ops.object.delete(use_global=False)
        # vuelvo a seleccionar al que corresponde por el bucle
        selectOnlyOneObjectByName(ob.name)
        # obtengo el nombre de su material
        mat = ob.material_slots[0].name
        # hago un material single user copy para que sea unico y no le afecte los cambios de las copias
        makeMaterialSingleUserCopy(duplicado, mat)

# para buscar los index:
def buscador_posicion(tupla,busqueda):
    for i in range(len(tupla)):
        if tupla[i].name == busqueda:
            return i
    return '-1'

# Obteniendo settings de la escena original
current_scene = bpy.context.scene.name
cycles_samples = bpy.data.scenes[current_scene].cycles.samples
file_format = bpy.data.scenes[current_scene].render.image_settings.file_format
color_depth = bpy.data.scenes[current_scene].render.image_settings.color_depth
img_compression = bpy.data.scenes[current_scene].render.image_settings.compression
filter_type = bpy.data.scenes[current_scene].cycles.filter_type
filter_width = bpy.data.scenes[current_scene].cycles.filter_width
exr_codec = bpy.data.scenes[current_scene].render.image_settings.exr_codec
color_mode = bpy.data.scenes[current_scene].render.image_settings.color_mode
# copio las mismas layers activas de la original:
layers = []
for li in range(20):
    layers.append(bpy.data.scenes[current_scene].layers[li])

#if 'Backup_Original_Scene' not in bpy.data.scenes:
#    createNewScene('Backup_Original_Scene','FULL_COPY', True)

monomaterials = []
multimaterials =  []
canales = ['Rojo','Verde','Azul']

bpy.ops.object.select_all(action='DESELECT')
for ob in bpy.data.objects:
    if ob.type == 'MESH':
        cuantos = cuantos_materiales_tiene(ob)
        if cuantos <= 1: # si son mono material lo seleccionamos
            ob.select = True
            monomaterials.append( ob.name )
        else:
            multimaterials.append( ob.name )


# de 3 en 3:
todo = monomaterials
detresentres = [] # <-- el array contenedor tendra los grupos de 3 en 3 dentro
i = 0
while i <= len(todo):
    grupo = [] # creando los subgrupos de 3 en 3
    try: # <-- puede dar error si no hay suficientes para completar otro grupo de tres
        for j in range(3): # realizo 3 veces una accion
            grupo.append(todo[i]) # se va rellenando con el iterador externo de 3 en 3 tandas
            i = i +1 # al terminar las 3 tandas se sigue iterando otras 3 mas y asi
    except: # <-- si no hay suficientes no importa continuamos y salimos del while
        i = len(todo)+1
    detresentres.append(grupo) # agregando al grupo principal

n = 0
#print(detresentres)
#print(len(detresentres))
for group3 in detresentres:
    #print(n)
    if len(group3) != 0:
        # creamos una escena nueva
        scn_name = 'RGB_Pass.00' + str(n)
        name_scn = createNewScene(scn_name,'NEW',True)
        # Copiando settings de la escena original a la nueva
        current_scene = name_scn[1]
        bpy.data.scenes[current_scene].cycles.samples = cycles_samples
        bpy.data.scenes[current_scene].render.image_settings.file_format = file_format
        bpy.data.scenes[current_scene].render.image_settings.color_depth = color_depth
        bpy.data.scenes[current_scene].render.image_settings.compression = img_compression
        bpy.data.scenes[current_scene].cycles.filter_type = filter_type
        bpy.data.scenes[current_scene].cycles.filter_width = filter_width
        bpy.data.scenes[current_scene].render.image_settings.exr_codec = exr_codec
        bpy.data.scenes[current_scene].render.image_settings.color_mode = color_mode
        # copio las mismas layers activas de la original:
        bpy.data.scenes[current_scene].layers = layers
        #print(group3)
        for i in range(len(group3)):
            # Para evitar list index out of range:
            # como len empieza desde 1 y el for desde 0 le tengo que restar 1:
            if i <= (len(group3)-1) and i <= (len(canales)-1):
                selectOnlyOneObjectByName(group3[i])
                ob = bpy.context.selected_objects[0]
                # si esta oculto el ojo de para el render no nos interesa ese objeto:
                if not ob.hide_render:
                    copyCurrentObjectToScene(ob, scn_name)
                    crear_shader_shadeless(canales[i],canales[i])
                    aplicar_shader(bpy.data.objects[group3[i]+'_copy'],canales[i])
    # si esta vacia la elimino (este apartado puede tardar bastante...):
    if len(bpy.data.scenes[scn_name].objects) == '0':
        # current suele ser el main scene y la scn_name son las copias
        current_scn = bpy.context.scene.name
        bpy.context.screen.scene = bpy.data.scenes[scn_name]
        bpy.ops.scene.delete()
        bpy.context.screen.scene = bpy.data.scenes[current_scn]
    n += 1

#bpy.ops.outliner.orphans_purge()
