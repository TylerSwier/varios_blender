# work well in blender 2.73a
import bpy

scn = bpy.context.scene
longitud=10
cuantos_segmentos=70
calidad_de_colision=20
substeps=50

def seleccionar_por_nombre(nombre):
    bpy.data.objects[nombre].select = True
    scn.objects.active = bpy.data.objects[nombre]

def deseleccionar_todo():
    bpy.ops.object.select_all(action='DESELECT')

def seleccionar_todo():
    bpy.ops.object.select_all(action='SELECT')
    
def crear_vertices(ob):
    ob.data.vertices.add(1)
    ob.data.update

def borrar_elementos_seleccionados(tipo):
    if tipo == "vertices":
        bpy.ops.mesh.delete(type='VERT')        

def tab_editmode():
    bpy.ops.object.editmode_toggle()
        
def obtener_coords_vertex_seleccionados():
    coordenadas_de_vertices = []
    for ob in bpy.context.selected_objects:
        print(ob.name)
        if ob.type == 'MESH':
            for v in ob.data.vertices:
                if v.select:
                    coordenadas_de_vertices.append([v.co[0],v.co[1],v.co[2]])
            print(coordenadas_de_vertices[0])
            return coordenadas_de_vertices[0]

def crear_locator(pos):
    bpy.ops.object.empty_add(type='PLAIN_AXES', radius=1, view_align=False, location=(pos[0],pos[1],pos[2]), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))

def extruir_vertices(longitud, cuantos_segmentos):    
    bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(longitud/cuantos_segmentos, 0, 0), "constraint_axis":(True, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False})
    
# creamos un plano y lo borramos
bpy.ops.mesh.primitive_plane_add(radius=1, view_align=False, enter_editmode=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
bpy.context.selected_objects[0].name = "cuerda"
tab_editmode()
#seleccionar_todo()
borrar_elementos_seleccionados("vertices")

tab_editmode()
ob = bpy.context.selected_objects[0]
crear_vertices(ob)
pos = obtener_coords_vertex_seleccionados()

tab_editmode()
bpy.ops.object.vertex_group_add()
bpy.ops.object.vertex_group_assign()
tab_editmode()


crear_locator(pos)
deseleccionar_todo()
seleccionar_por_nombre("cuerda")
tab_editmode()

for i in range(cuantos_segmentos):
    extruir_vertices(longitud, cuantos_segmentos)
    bpy.ops.object.vertex_group_remove_from()
    pos = obtener_coords_vertex_seleccionados()
    tab_editmode()
    crear_locator(pos)
    deseleccionar_todo()
    seleccionar_por_nombre("cuerda")
    tab_editmode()

# Group contiene los vertices del pin y Group.001 contiene la linea unica principal

bpy.ops.mesh.select_all(action='TOGGLE')
bpy.ops.mesh.select_all(action='TOGGLE') # sleccionamos todos los vertices y hacemos un nuevo grupo de vertices
bpy.ops.object.vertex_group_add()
bpy.ops.object.vertex_group_assign()

bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0, 0.005, 0), "constraint_axis":(False, True, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False})
bpy.ops.object.vertex_group_remove_from()


bpy.ops.mesh.select_all(action='TOGGLE')
bpy.ops.object.editmode_toggle()

bpy.ops.object.modifier_add(type='CLOTH')
bpy.context.object.modifiers["Cloth"].settings.use_pin_cloth = True
bpy.context.object.modifiers["Cloth"].settings.vertex_group_mass = "Group"
bpy.context.object.modifiers["Cloth"].collision_settings.collision_quality = calidad_de_colision
bpy.context.object.modifiers["Cloth"].settings.quality = substeps
