# con este script intentare poner todos los objetos seleccionados en distintas layers para luego hacer
# un render layers para hacer mattes o mascaras de cada uno de los objetos y incluirlos luego en un .exr 
# multilayer...
# solo funciona con hasta 20 objetos seleccionados ya que solo existen 20 layers y 20 renderlayers en blender
import bpy
objetos = bpy.context.selected_objects
scn = bpy.context.scene
# para buscar los index:
def buscador_posicion(tupla,busqueda):
    for i in range(len(tupla)):
        if tupla[i].name == busqueda:
            return i
    return '-1'

def contexto(accion, contexto):
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == contexto:
                accion                

def crear_shader_shadeless(nombre,color):
    matName = nombre
    bpy.data.materials.new(matName)
    bpy.data.materials[matName].use_nodes = True
    # solo lo creamos si no existe previamente:
    # -1 es si no existe:
    if buscador_posicion(bpy.data.materials[matName].node_tree.nodes,'Emission') == '-1':
        nole = True # es cierto q no existe
    else:
        nole = False
    # si no existe:
    if nole: 
        bpy.data.materials[matName].node_tree.nodes.new(type='ShaderNodeEmission')
        outp = bpy.data.materials[matName].node_tree.nodes['Emission'].outputs[0]
        # esta complicacion la creo por que en osx tuve problemas:
        materialoutput = buscador_posicion(bpy.data.materials[matName].node_tree.nodes,'Material Output')
        moinput = buscador_posicion(bpy.data.materials[matName].node_tree.nodes[materialoutput].inputs,'Surface')
        inp = bpy.data.materials[matName].node_tree.nodes[materialoutput].inputs[moinput]
        if color == 'Rojo':
            color = 255,0,0,1
        if color == 'Verde':
            color = 0,255,0,1
        if color == 'Azul':
            color = 0,0,255,1
        if color == 'Blanco':
            color = 255,255,255,1
        ep = buscador_posicion(bpy.data.materials[matName].node_tree.nodes,'Emission')
        bpy.data.materials[matName].node_tree.nodes[ep].inputs[0].default_value = color
        # si sale muy mal el AA poner 1 en lugar de 1.25:
        bpy.data.materials[matName].node_tree.nodes[ep].inputs[1].default_value = 1.25
        bpy.data.materials[matName].node_tree.links.new(inp,outp)
        # deselecciono y borro el por default:
        dn = buscador_posicion(bpy.data.materials[matName].node_tree.nodes,'Diffuse BSDF')
        # los contextos se ven asi: 
        # bpy.context.window_manager.windows[0].screen.areas[algo].type
        # ‘EMPTY’, ‘VIEW_3D’, ‘GRAPH_EDITOR’, ‘OUTLINER’, ‘PROPERTIES’, ‘FILE_BROWSER’, 
        # ‘IMAGE_EDITOR’, ‘INFO’, ‘SEQUENCE_EDITOR’, ‘TEXT_EDITOR’, ‘DOPESHEET_EDITOR’, 
        # ‘NLA_EDITOR’, ‘TIMELINE’, ‘NODE_EDITOR’, ‘LOGIC_EDITOR’, ‘CONSOLE’, ‘USER_PREFERENCES’, ‘CLIP_EDITOR’], default ‘EMPTY’
        contexto(bpy.ops.select_all(action='DESELECT'),'NODE_EDITOR')
        # luego selecciono el que quiero borrar y lo borro:
        bpy.data.materials[matName].node_tree.nodes[dn].select = True
        bpy.ops.node.delete()

def aplicar_shader():
    # aplicandole el material:
    #ultimomat = bpy.data.materials[len(bpy.data.materials)-1]
    #bpy.context.selected_objects[0].material_slots[0].material = ultimomat
    nombre = 'shaderless_mt'
    crear_shader_shadeless(nombre,'Rojo')
    for i in range(len(objetos)):
        objetos[i].active_material = bpy.data.materials[nombre]
    #objetos[i].material_slots[0].material =bpy.data.materials[matName]    

def cuantos_materiales_tiene(ob):
    return len(ob.material_slots)

def layers():
    # hago la accion de poner todos y cada uno de los objetos seleccionados en un layer distinto:
    posicion = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
    for i in range(len(objetos)):
        bpy.ops.object.select_all(action='DESELECT')
        scn.objects.active = objetos[i]
        objetos[i].select = True
        # desactivo un par de cosas para q los shaders emission no emitan luz y solo sean shadeless:
        objetos[i].cycles_visibility.diffuse = False
        objetos[i].cycles_visibility.transmission = False
        # poniendo cada objeto seleccionado en un layer:
        posicion[i] = True # indico el layer
        bpy.ops.object.move_to_layer(layers=(posicion)) # lo seteo
        posicion[i] = False # dejo el layer como estaba                

def renderlayers():
    # por cada objeto creo un render layer
    cuantos = len(objetos)
    for i in range(cuantos-1):
        bpy.ops.scene.render_layer_add()            
    # y configuro las render layers:
    for ln1 in range(len(bpy.context.scene.render.layers)):
        for li in range(len(bpy.context.scene.render.layers[ln1].layers)):
            bpy.context.scene.render.layers[ln1].layers[li] = False
        bpy.context.scene.render.layers[ln1].layers[ln1] = True
        bpy.context.scene.render.layers[ln1].layers[len(bpy.context.scene.render.layers[ln1].layers)-1] = False

# en el area de view 3d:
def startmain():
    contexto(layers(),'VIEW_3D')
    contexto(aplicar_shader(),'VIEW_3D')
    renderlayers()

startmain()
