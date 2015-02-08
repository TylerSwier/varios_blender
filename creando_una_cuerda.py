# work well in blender 2.73a
import bpy

scn = bpy.context.scene
longitud=10
cuantos_segmentos=70
calidad_de_colision=20
substeps=50
# para que desde el primer punto hasta el ultimo, entre 
# medias tenga x segmentos debo sumarle 1 a la cantidad:
cuantos_segmentos += 1

def deseleccionar_todo():
    bpy.ops.object.select_all(action='DESELECT')
        
def seleccionar_todo():
    bpy.ops.object.select_all(action='SELECT')

# Clear scene:
def reset_scene():
    seleccionar_todo()
    bpy.ops.object.delete(use_global=False)
    
reset_scene()

def entrar_en_editmode():
    bpy.ops.object.mode_set(mode='EDIT')
    
def salir_de_editmode():
    bpy.ops.object.mode_set(mode='OBJECT')

def select_all_in_edit_mode(ob):
    if ob.mode != 'EDIT':
        entrar_en_editmode()
    bpy.ops.mesh.select_all(action="DESELECT")
    bpy.context.tool_settings.mesh_select_mode = (True , False , False)
    salir_de_editmode()
    for v in ob.data.vertices:
        if not v.select:
            v.select = True
    entrar_en_editmode()
    #bpy.ops.mesh.select_all(action="SELECT")        

def deselect_all_in_edit_mode(ob):
    if ob.mode != 'EDIT':
        entrar_en_editmode()
    bpy.ops.mesh.select_all(action="DESELECT")
    bpy.context.tool_settings.mesh_select_mode = (True , False , False)
    salir_de_editmode()
    for v in ob.data.vertices:
        if not v.select:
            v.select = False
    entrar_en_editmode()
    #bpy.ops.mesh.select_all(action="DESELECT")

def which_vertex_are_selected(ob):
    for v in ob.data.vertices:
        if v.select:
            print(str(v.index))
            print("el vertice " + str(v.index) + " esta seleccionado")

def seleccionar_por_nombre(nombre):
    bpy.data.objects[nombre].select = True
    scn.objects.active = bpy.data.objects[nombre]
    
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
            #print(coordenadas_de_vertices[0])
            return coordenadas_de_vertices[0]

def crear_locator(pos):
    bpy.ops.object.empty_add(type='PLAIN_AXES', radius=1, view_align=False, location=(pos[0],pos[1],pos[2]), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))

def extruir_vertices(longitud, cuantos_segmentos):    
    bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(longitud/cuantos_segmentos, 0, 0), "constraint_axis":(True, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False})
    
# creamos un plano y lo borramos
bpy.ops.mesh.primitive_plane_add(radius=1, view_align=False, enter_editmode=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
ob = bpy.context.selected_objects[0]
# renombrar:
ob.name = "cuerda"
entrar_en_editmode() # entramos en edit mode
select_all_in_edit_mode(ob)
#seleccionar_todo() # ya viene por default seleccionado
borrar_elementos_seleccionados("vertices")
salir_de_editmode() # salimos de edit mode

crear_vertices(ob) # creamos un vertex

# creando el grupo Group para el PIN
# Group contiene los vertices del pin y Group.001 contiene la linea unica principal
entrar_en_editmode() # entramos en edit mode
bpy.ops.object.vertex_group_add() # creamos un grupo
select_all_in_edit_mode(ob)
bpy.ops.object.vertex_group_assign() # y lo asignamos
# los hooks van a la curva no a la guia poligonal...
# creo el primer hook sin necesidad de crear luego el locator a mano:
#bpy.ops.object.hook_add_newob()
salir_de_editmode() # salimos de edit mode
ob.vertex_groups[0].name = "Pin"

deseleccionar_todo()

seleccionar_por_nombre("cuerda")

# hago los extrudes del vertice:
for i in range(cuantos_segmentos):    
    entrar_en_editmode()
    extruir_vertices(longitud, cuantos_segmentos)
    # y los ELIMINO del grupo PIN
    bpy.ops.object.vertex_group_remove_from()
    # obtengo la direccion para lego crear el locator en su posicion
    pos = obtener_coords_vertex_seleccionados()
    # los hooks van a la curva no a la guia poligonal...
    # creo el hook sin necesidad de crear el locator a mano:
    #bpy.ops.object.hook_add_newob()
    salir_de_editmode() # salimos de edit mode
    # creo el locator en su sitio
    crear_locator(pos)
    deseleccionar_todo()
    seleccionar_por_nombre("cuerda")
    
deseleccionar_todo()
seleccionar_por_nombre("cuerda")    
# vuelvo a seleccionar la cuerda
entrar_en_editmode()
pos = obtener_coords_vertex_seleccionados() # y obtenemos su posicion
salir_de_editmode()
# creamos el ultimo locator
crear_locator(pos)

deseleccionar_todo()
seleccionar_por_nombre("cuerda")        
entrar_en_editmode() # entramos en edit mode
bpy.ops.object.vertex_group_add() # CREANDO GRUPO GUIA MAESTRA
select_all_in_edit_mode(ob)
bpy.ops.object.vertex_group_assign() # y lo asignamos
ob.vertex_groups[1].name = "Guide_rope"

# extruimos la curva para que tenga un minimo grosor para colisionar
bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"mirror":False}, TRANSFORM_OT_translate={"value":(0, 0.005, 0), "constraint_axis":(False, True, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False})
bpy.ops.object.vertex_group_remove_from()

deselect_all_in_edit_mode(ob)

salir_de_editmode()

bpy.ops.object.modifier_add(type='CLOTH')
bpy.context.object.modifiers["Cloth"].settings.use_pin_cloth = True
bpy.context.object.modifiers["Cloth"].settings.vertex_group_mass = "Pin"
bpy.context.object.modifiers["Cloth"].collision_settings.collision_quality = calidad_de_colision
bpy.context.object.modifiers["Cloth"].settings.quality = substeps

# DUPLICAMOS para convertir a curva:
# selecciono los vertices que forman parte del grupo Group.001
seleccionar_por_nombre("cuerda")
entrar_en_editmode()
bpy.ops.mesh.select_all(action="DESELECT")
bpy.context.tool_settings.mesh_select_mode = (True , False , False)
salir_de_editmode()
gi = ob.vertex_groups["Guide_rope"].index # get group index
for v in ob.data.vertices:
  for g in v.groups:
    if g.group == gi: # compare with index in VertexGroupElement
      v.select = True
      
entrar_en_editmode()

# ya tenemos la guia seleccionada:      
# la duplicamos:
bpy.ops.mesh.duplicate_move(MESH_OT_duplicate={"mode":1}, TRANSFORM_OT_translate={"value":(0, 0, 0), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False})
# separamos por seleccion:
bpy.ops.mesh.separate(type='SELECTED')
salir_de_editmode()

deseleccionar_todo()
seleccionar_por_nombre("cuerda.001")
# a la nueva curva copiada le quitamos el cloth:
bpy.ops.object.modifier_remove(modifier="Cloth")
# la convertimos en curva:
bpy.ops.object.convert(target='CURVE')

# todos los emptys:
emptys = []
for eo in bpy.data.objects:
    if eo.type == 'EMPTY':
        emptys.append(eo)
        
#print(emptys)

def select_all_vertex_in_curve_bezier(bc):
    for i in range(len(bc.data.splines[0].points)):
        bc.data.splines[0].points[i].select = True

def deselect_all_vertex_in_curve_bezier(bc):
    for i in range(len(bc.data.splines[0].points)):
        bc.data.splines[0].points[i].select = False
        
# cuantos puntos tiene la becier:
#len(bpy.data.objects['cuerda.001'].data.splines[0].points)
# seleccionar y deseleccionar:
#bpy.data.objects['cuerda.001'].data.splines[0].points[0].select = True

bc = bpy.data.objects['cuerda.001']
n = 0 
for e in emptys:
    deseleccionar_todo()
    seleccionar_por_nombre(e.name)
    seleccionar_por_nombre(bc.name)
    entrar_en_editmode()
    deselect_all_vertex_in_curve_bezier(bc)
    bc.data.splines[0].points[n].select = True
    bpy.ops.object.hook_add_selob(use_bone=False)
    salir_de_editmode()
    n = n + 1
#entrar_en_editmode()
        

ob = bpy.data.objects['cuerda']
n = 0 
for e in emptys:
    deseleccionar_todo()
    seleccionar_por_nombre(e.name)
    seleccionar_por_nombre(ob.name)
    entrar_en_editmode()
    bpy.ops.mesh.select_all(action="DESELECT")
    bpy.context.tool_settings.mesh_select_mode = (True , False , False)
    salir_de_editmode()
    for v in ob.data.vertices:
        if v.select:
            v.select = False
    ob.data.vertices[n].select = True
    entrar_en_editmode()
    bpy.ops.object.vertex_parent_set()
    #deselect_all_in_edit_mode(ob)
    salir_de_editmode()
    n = n + 1

# display que no muestre las relaciones
#bpy.context.space_data.show_relationship_lines = False
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        area.spaces[0].show_relationship_lines = False

seleccionar_por_nombre("cuerda.001")
# cuerda curva settings:
bpy.context.object.data.fill_mode = 'FULL'
bpy.context.object.data.bevel_depth = 0.04
bpy.context.object.data.bevel_resolution = 6
