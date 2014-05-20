# con este script intentare poner todos los objetos seleccionados en distintas layers para luego hacer
# un render layers para hacer mattes o mascaras de cada uno de los objetos y incluirlos luego en un .exr 
# multilayer...
import bpy
objetos = bpy.context.selected_objects
scn = bpy.context.scene
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
                posicion[i] = True # indico el layer
                bpy.ops.object.move_to_layer(layers=(posicion)) # lo seteo
                posicion[i] = False # dejo el layer como estaba
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
