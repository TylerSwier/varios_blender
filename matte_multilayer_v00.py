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

def onlyselect(ob):
    bpy.ops.object.select_all(action='DESELECT')
    scn.objects.active = ob
    ob.select = True

def cuantos_materiales_tiene(ob):
    return len(ob.material_slots)

def crear_shader_shadeless(nombre,color):
    # solo lo creamos si no existe previamente:
    if buscador_posicion(bpy.data.materials, 'shaderless_mt') == '-1':
        bpy.data.materials.new(nombre)
        bpy.data.materials[nombre].use_nodes = True
        bpy.data.materials[nombre].node_tree.nodes.new(type='ShaderNodeEmission')
        outp = bpy.data.materials[nombre].node_tree.nodes['Emission'].outputs[0]
        # esta complicacion la creo por que en osx tuve problemas:
        materialoutput = buscador_posicion(bpy.data.materials[nombre].node_tree.nodes,'Material Output')
        moinput = buscador_posicion(bpy.data.materials[nombre].node_tree.nodes[materialoutput].inputs,'Surface')
        inp = bpy.data.materials[nombre].node_tree.nodes[materialoutput].inputs[moinput]
        if color == 'Rojo':
            color = 255,0,0,1
        if color == 'Verde':
            color = 0,255,0,1
        if color == 'Azul':
            color = 0,0,255,1
        if color == 'Blanco':
            color = 255,255,255,1
        ep = buscador_posicion(bpy.data.materials[nombre].node_tree.nodes,'Emission')
        bpy.data.materials[nombre].node_tree.nodes[ep].inputs[0].default_value = color
        # si sale muy mal el AA poner 1 en lugar de 1.25:
        bpy.data.materials[nombre].node_tree.nodes[ep].inputs[1].default_value = 1
        bpy.data.materials[nombre].node_tree.links.new(inp,outp)
        #
        # los contextos se ven asi: 
        # bpy.context.window_manager.windows[0].screen.areas[algo].type
        # ‘EMPTY’, ‘VIEW_3D’, ‘GRAPH_EDITOR’, ‘OUTLINER’, ‘PROPERTIES’, ‘FILE_BROWSER’, 
        # ‘IMAGE_EDITOR’, ‘INFO’, ‘SEQUENCE_EDITOR’, ‘TEXT_EDITOR’, ‘DOPESHEET_EDITOR’, 
        # ‘NLA_EDITOR’, ‘TIMELINE’, ‘NODE_EDITOR’, ‘LOGIC_EDITOR’, ‘CONSOLE’, ‘USER_PREFERENCES’, ‘CLIP_EDITOR’], default ‘EMPTY’
        #
        # intentando borrar el nodo sobrante:
        # deselecciono y borro el por default:
        #dn = buscador_posicion(bpy.data.materials[nombre].node_tree.nodes,'Diffuse BSDF')
        #contexto(bpy.ops.select_all(action='DESELECT'),'NODE_EDITOR')
        # luego selecciono el que quiero borrar y lo borro:
        #contexto(bpy.data.materials[nombre].node_tree.nodes[dn].select = True,'NODE_EDITOR')
        #contexto(bpy.ops.node.delete(),'NODE_EDITOR')

def aplicar_shader(ob,nombre):
    ob.active_material = bpy.data.materials[nombre]
    #objetos[i].material_slots[0].material =bpy.data.materials[nombre] 

def layers():
    # hago la accion de poner todos y cada uno de los objetos seleccionados en un layer distinto:
    posicion = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
    # creando y aplicando shader
    #nombre = 'shaderless_mt'
    #crear_shader_shadeless(nombre,'Rojo')
    #aplicar_shader(objetos[i],nombre)
    # de 3 en 3:
    todo = []
    c = 0
    while c <= len(objetos):
        grupo = []
        try:
            for g in range(3):
                ob = objetos[c]
                onlyselect(ob)
                ob.cycles_visibility.diffuse = False
                ob.cycles_visibility.transmission = False
                grupo.append(ob)
                c = c +1
        except:
            c = len(objetos)+1
        todo.append(grupo)
    for l in range(len(todo)):
        for ob in todo[l]:
            cuantos = cuantos_materiales_tiene(ob)
            if cuantos == 1:
                posicion[l] = True
                onlyselect(ob)
                bpy.ops.object.move_to_layer(layers=(posicion))
                posicion[l] = False

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
    renderlayers()

startmain()
