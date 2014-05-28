# con este script intentare poner todos los objetos seleccionados en distintas layers para luego hacer
# un render layers para hacer mattes o mascaras de cada uno de los objetos y incluirlos luego en un .exr 
# multilayer...
# solo funciona con hasta 20 objetos seleccionados ya que solo existen 20 layers y 20 renderlayers en blender
import bpy
objetos = bpy.context.selected_objects
scn = bpy.context.scene

def buscar_en_q_layer_esta_ob(ob): #<- tiene que recibir solo un objeto
    for l in range(len(ob.layers)):
        if ob.layers[l]:
            return l

# para buscar los index:
def buscador_posicion(tupla,busqueda):
    for i in range(len(tupla)):
        if tupla[i].name == busqueda:
            return i
    return '-1'

def select_only_by_name_ob(obn):
    ob = bpy.data.objects[obn]
    bpy.ops.object.select_all(action='DESELECT')
    scn.objects.active = ob
    ob.select = True

def cuantos_materiales_tiene(ob):
    return len(ob.material_slots)

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
        if color == 'Blanco':
            color = 1,1,1,1
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

def layers():
    # relleno de la representacion de las layers:    
    rlayers = []
    for rl in range(20):
        rlayers.append([])
    aopl = [] # creo un array con [] equivalente al numero de objetos que hay 
    for n in range(len(objetos)):
        aopl.append([])
    c = 0
    while c < len(objetos):
        ob = objetos[c]
        p = buscar_en_q_layer_esta_ob(ob)
        try:
            for g in range(len(objetos)):
                ob = objetos[c]
                aopl[g] = ob.name
                c = c +1
            rlayers[p] = aopl
        except:
            c = len(objetos)+5
    print(rlayers)
    posicion = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
    monomats = []
    for l in rlayers:
        for obn in l:
            if len(l) != 0:
                select_only_by_name_ob(obn)
                ob = scn.objects.active
                cuantos = cuantos_materiales_tiene(ob)
                if cuantos == 1:
                    monomats.append(obn)                
    rlordenadito = []
    canales = ['Rojo','Verde','Azul','Blanco']
    c = 0
    while c < len(monomats):
        grupo = []
        try:
            for g in range(3):
                obn = monomats[c]
                select_only_by_name_ob(obn)
                ob = scn.objects.active
                ob.cycles_visibility.diffuse = False
                ob.cycles_visibility.transmission = False
                crear_shader_shadeless('monomaterial'+str(g),canales[g])
                aplicar_shader(ob,'monomaterial'+str(g))
                grupo.append(ob.name)
                c = c +1
        except:
            c = len(objetos)+1        
        rlordenadito.append(grupo)
        for l in range(len(rlordenadito)):
            for obn in rlordenadito[l]:
                select_only_by_name_ob(obn)
                ob = scn.objects.active
                cuantos = cuantos_materiales_tiene(ob)
                if cuantos == 1:
                    posicion[l] = True
                    select_only_by_name_ob(ob.name)
                    bpy.ops.object.move_to_layer(layers=(posicion))
                    posicion[l] = False
    if len(rlordenadito) < 20:
        cuantos = 20 - len(rlordenadito)
        for i in range(cuantos):
            rlordenadito.append([])
    print(rlordenadito)
    return rlordenadito

def renderlayers(rlayerso):
    # por cada objeto creo un render layer
    c = 0
    for chkv in rlayerso:
        if len(chkv) != 0 and c != 0:    
            bpy.ops.scene.render_layer_add()
        c += 1
    # y configuro las render layers:
    for ln1 in range(len(bpy.context.scene.render.layers)):
        for li in range(len(bpy.context.scene.render.layers[ln1].layers)):
            bpy.context.scene.render.layers[ln1].layers[li] = False
        bpy.context.scene.render.layers[ln1].layers[ln1] = True
        bpy.context.scene.render.layers[ln1].layers[len(bpy.context.scene.render.layers[ln1].layers)-1] = False

rlayerso = layers()
renderlayers(rlayerso)

# seteo el clap para que luego me den valor de 1;
#scn.cycles.sample_clamp_direct = 0.3333
#scn.cycles.sample_clamp_indirect = 0.0001 #<-- este por si acaso lo elimino
scn.cycles.use_square_sample = True
scn.cycles.samples = 4
scn.cycles.aa_samples = 4
scn.render.image_settings.file_format = 'OPEN_EXR_MULTILAYER'

# pongo el fondo en negro:
#bpy.data.node_groups["Shader Nodetree"].nodes["Background"].inputs[0].default_value = (0, 0, 0, 1)
bpy.data.worlds['World'].node_tree.nodes['Background'].inputs['Color'].default_value = 0,0,0,1
