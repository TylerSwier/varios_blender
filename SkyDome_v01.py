import bpy  

scn = bpy.context.scene

def ocultar_relationships():
    #bpy.context.space_data.show_relationship_lines = False
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            area.spaces[0].show_relationship_lines = False

def deseleccionar_todo():
    bpy.ops.object.select_all(action='DESELECT')

def seleccionar_por_nombre(nombre):
    bpy.data.objects[nombre].select = True
    scn.objects.active = bpy.data.objects[nombre]
    
deseleccionar_todo()

sizesky=100
# con icosphere con 5 es mucho y con esfera normal valores mas altos
resolution=4
difusion=0.2

bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=resolution, size=1, view_align=False, enter_editmode=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
#bpy.ops.mesh.primitive_uv_sphere_add(segments=resolution, size=1, view_align=False, enter_editmode=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
#bpy.ops.mesh.primitive_uv_sphere_add(view_align=False, enter_editmode=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
bpy.context.object.scale = [sizesky, sizesky, sizesky]
bpy.context.object.name = "skydome_base"

ob = bpy.context.selected_objects[0]

bpy.ops.object.empty_add(type='PLAIN_AXES', radius=1, view_align=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
bpy.context.object.name = "target_lights"

vectores=[]
for vertex in ob.data.vertices:
    vco = vertex.co
    mat = ob.matrix_world
    loc = mat * vco
    #print(loc)
    vectores.append(loc)

for c in vectores:
    x = c[0]
    y = c[1]
    z = c[2]
    #if z >= 0:
    if z >= -1: # con icosphere para que funcione bien tiene que ser -1    
        #bpy.ops.object.lamp_add(type='SPOT', radius=1, view_align=False, location=(x, y, z), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        bpy.ops.object.lamp_add(type='AREA', view_align=False, location=(x, y, z), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        bpy.context.object.data.size = difusion
        bpy.ops.object.constraint_add(type='TRACK_TO')
        bpy.context.object.constraints["Track To"].target = bpy.data.objects["target_lights"]
        bpy.context.object.constraints["Track To"].track_axis = 'TRACK_NEGATIVE_Z'
        bpy.context.object.constraints["Track To"].up_axis = 'UP_Y'
        #bpy.ops.mesh.primitive_cube_add(view_align=False, enter_editmode=False, location=(x, y, z), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        #bpy.ops.transform.resize(value=(0.023373, 0.023373, 0.023373), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

deseleccionar_todo()
seleccionar_por_nombre("skydome_base")
bpy.ops.object.delete(use_global=False)
ocultar_relationships()
#bpy.context.space_data.show_relationship_lines = False
