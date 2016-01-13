import bpy, os

def deselectAll():
    bpy.ops.object.select_all(action='DESELECT')

def selectAll():
    bpy.ops.object.select_all(action='SELECT')

def selectByName(name):
    scn = bpy.context.scene
    bpy.data.objects[name].select = True
    scn.objects.active = bpy.data.objects[name]

# guardando la seleccion:
seleccion_actual = bpy.context.selected_objects

# aplicando la escala a todos:
for ob in bpy.data.objects:
    deselectAll()
    if ob.type == 'MESH' or ob.type == 'SURFACE' or ob.type == 'META':
        selectByName(ob.name)
        # aplicando escala si hay animaciones cuidado con esto:
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        # todos con el pivot en su geometry:
        #bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
        # activar sombras
    try:
        if ob.name != 'cuerpo':
            ob.b4w_shadow_cast = True
            ob.b4w_shadow_receive = True
    except:
        pass

# recuperando la seleccion
deselectAll()
for ob in seleccion_actual:
    selectByName(ob.name)

# hacer todos los path relative:
bpy.ops.file.make_paths_relative()

# ir al frame 0
#bpy.context.scene.frame_current = 300
#bpy.context.scene.frame_current = 0

# save all images:
#bpy.ops.image.save_dirty()

#bpy.context.screen.scene = bpy.data.scenes['Scene']
#bpy.ops.render.render(scene='Scene')

# guardo mi escena:
bpy.ops.wm.save_as_mainfile()


ruta=bpy.data.filepath.split("/")
ruta = ruta[:-2]
nombre_json="first-person.json"
nombre_bin="first-person.bin"
ruta = ','.join(ruta).replace(',','/')+"/"+nombre_json
bin = ','.join(ruta).replace(',','/')+"/"+nombre_bin

# eliminamos el .bin:
file_target = bin
if os.path.isfile(file_target):
    os.remove(file_target)

# exportar a json:
bpy.ops.export_scene.b4w_json(filepath=ruta, do_autosave=True, strict_mode=False, run_in_viewer=False, override_filepath=ruta, save_export_path=False, is_html_export=False)
# exportar el html tambien:
#bpy.ops.export_scene.b4w_html(filepath=bpy.data.filepath)

