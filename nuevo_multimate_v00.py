import bpy

def createNewScene(name, retornamos=True, motor='CYCLES'):
    scn_original = bpy.context.scene.name
    bpy.ops.scene.new(type='NEW')
    bpy.context.scene.name = name
    if retornamos:
        new_scn = bpy.context.scene.name
        bpy.context.screen.scene = bpy.data.scenes[scn_original]
        return new_scn
    else:
        # si no retornamos devolvemos el nombre de la nueva escena
        return bpy.context.scene.name
    # si no se especifica motor se usara cycles en la nueva escena
    if motor:
        bpy.context.scene.render.engine = motor

# creamos una escena nueva
name_scn = createNewScene("RGB_Pass")
#print(name_scn)

# seleccionamos todos los mesh y camaras
bpy.ops.object.select_all(action='DESELECT')
for ob in bpy.data.objects:
    if ob.type == 'MESH' or ob.type == 'CAMERA':
        ob.select = True
        
# enviamos los objetos seleccionados a la ultima nueva escena:
bpy.ops.object.make_links_scene(scene=name_scn)
