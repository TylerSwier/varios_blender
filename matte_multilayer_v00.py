# con este script intentare poner todos los objetos seleccionados en distintas layers para luego hacer
# un render layers para hacer mattes o mascaras de cada uno de los objetos y incluirlos luego en un .exr 
# multilayer...
# solo funciona con hasta 20 objetos seleccionados ya que solo existen 20 layers y 20 renderlayers en blender
import bpy
objetos = bpy.context.selected_objects
scn = bpy.context.scene
if len(objetos) <= 20:
    # creando el material:
    matName = 'shadeless_mt'
    bpy.data.materials.new(matName)
    bpy.data.materials[matName].use_nodes = True
    bpy.data.materials[matName].node_tree.nodes.new(type='ShaderNodeEmission')
    inp = bpy.data.materials[matName].node_tree.nodes['Material Output'].inputs['Surface']
    outp = bpy.data.materials[matName].node_tree.nodes['Emission'].outputs[0]
    bpy.data.materials[matName].node_tree.nodes['Emission'].inputs[1].default_value = 1.25
    bpy.data.materials[matName].node_tree.links.new(inp,outp)
    # en el area de view 3d:
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'VIEW_3D':
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
                    # aplicandole el material:
                    #ultimomat = bpy.data.materials[len(bpy.data.materials)-1]
                    #bpy.context.selected_objects[0].material_slots[0].material = ultimomat
                    objetos[i].active_material = bpy.data.materials[matName]
                    #objetos[i].material_slots[0].material =bpy.data.materials[matName]                
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
