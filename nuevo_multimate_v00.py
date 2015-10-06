import bpy
# capturamos el nombre de la escena actual
scn_original = bpy.context.scene.name

def createNewScene(name):
    bpy.ops.scene.new(type='NEW')
    bpy.context.scene.name = name

# creamos una escena nueva
createNewScene("RGB_Pass")
# capturamos el nombre de la nueva escena
new_scn = bpy.context.scene.name

# seteamos el motor de render a cycles
bpy.context.scene.render.engine = 'CYCLES'

# volvemos a la escena oritinal
bpy.context.screen.scene = bpy.data.scenes[scn_original]

# seleccionamos todos los mesh y camaras
bpy.ops.object.select_all(action='DESELECT')
for ob in bpy.data.objects:
    if ob.type == 'MESH' or ob.type == 'CAMERA':
        ob.select = True
        
# enviamos los objetos seleccionados a la ultima nueva escena:
bpy.ops.object.make_links_scene(scene=new_scn)
