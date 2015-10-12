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
def aplicar_shader_copy(ob,nombre):
    ob.active_material = bpy.data.materials[nombre].copy()

def copyCurrentObjectToScene(ob, toscene):
    # duplico
    bpy.ops.object.duplicate(linked=False, mode='TRANSLATION')
    # renombro
    bpy.context.selected_objects[0].name = bpy.context.selected_objects[0].name + "_copy" 
    # copio el duplicado a su escena
    bpy.ops.object.make_links_scene(scene=toscene)
    # selecciono solo el seleccionado (el ultimo duplicado)
    #selectOnlyOneObjectByName(bpy.context.selected_objects[0].name)
    # borro el seleccionado
    bpy.ops.object.delete(use_global=False)
    # vuelvo a seleccionar al que corresponde por el bucle
    selectOnlyOneObjectByName(ob.name)
    # obtengo el nombre de su material
    mat = ob.material_slots[0].name
    # hago un material single user copy para que sea unico y no le afecte los cambios de las copias
    aplicar_shader_copy(ob, mat)    

if 'Backup_Original_Scene' not in bpy.data.scenes:
    createNewScene('Backup_Original_Scene','FULL_COPY', True)

createNewScene('test','NEW',True)
for ob in bpy.context.scene.objects:
    if ob.type == 'MESH': 
        deselectAll()
        selectOnlyOneObjectByName(ob.name)
        name_org = ob.name
        # copio el objeto actual a la escena indicada:
        copyCurrentObjectToScene(ob, 'test')
