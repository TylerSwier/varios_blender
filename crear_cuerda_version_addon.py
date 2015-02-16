# work well in blender 2.73a
import bpy
from bpy.props import *
'''
Copyright (c) 2012 Jorge Hernandez - Melendez
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''
bl_info = {
    "name": "Rope Creator",
    "description": "Dynamic rope (with cloth) creator",
    "author": "Jorge Hernandez - Melenedez",
    "version": (0, 0),
    "blender": (2, 73),
    "location": "Left Toolbar > ClothRope",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Add Mesh"
}

def deseleccionar_todo():
    bpy.ops.object.select_all(action='DESELECT')
        
def seleccionar_todo():
    bpy.ops.object.select_all(action='SELECT')

def salir_de_editmode():
    bpy.ops.object.mode_set(mode='OBJECT')

# Clear scene:
def reset_scene():
    try:
        salir_de_editmode()
    except:
        pass
    seleccionar_todo()
    bpy.ops.object.delete(use_global=False)
    
def entrar_en_editmode():
    bpy.ops.object.mode_set(mode='EDIT')    

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
    scn = bpy.context.scene
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

def select_all_vertex_in_curve_bezier(bc):
    for i in range(len(bc.data.splines[0].points)):
        bc.data.splines[0].points[i].select = True

def deselect_all_vertex_in_curve_bezier(bc):
    for i in range(len(bc.data.splines[0].points)):
        bc.data.splines[0].points[i].select = False

# addomizando:
class DialogOperator(bpy.types.Operator):
    bl_idname = "object.zebus_dialog"
    bl_label = "Rope Creator"
    # Defaults:
    #longitud=10
    #cuantos_segmentos=70
    #calidad_de_colision=20
    #substeps=50
    # para que desde el primer punto hasta el ultimo, entre 
    # medias tenga x segmentos debo sumarle 1 a la cantidad:
    #cuantos_segmentos += 1
    ropelenght = IntProperty(name="longitud", default=5)
    ropesegments = IntProperty(name="rsegments", default=5) 
    qcr = IntProperty(name="qualcolr", default=20)
    substeps = IntProperty(name="rsubsteps", default=50)
    resrope = IntProperty(name="resr", default=5)
    radiusrope =  FloatProperty(name="radius", min = 0.04, max = 1, default=0.04)
    hide_emptys = BoolProperty(name="hemptys", default=False)    
    def execute(self,context):        
        # chicha ###############################################################      
        reset_scene()
        longitud = self.ropelenght
        # para que desde el primer punto hasta el ultimo, entre 
        # medias tenga x segmentos debo sumarle 1 a la cantidad:
        #cuantos_segmentos += 1
        cuantos_segmentos = self.ropesegments + 1
        calidad_de_colision = self.qcr
        substeps = self.substeps
        deseleccionar_todo()
        # creamos el empty que sera el padre de todo
        bpy.ops.object.empty_add(type='SPHERE', radius=1, view_align=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        ob = bpy.context.selected_objects[0]
        ob.name = "Rope"
        deseleccionar_todo()
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
                if eo.name != "Rope":
                    emptys.append(eo)
        #print(emptys)
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
        ########################################################################
        # ocultar los emptys: ##################################################
        #for e in emptys:
            deseleccionar_todo()
        #    seleccionar_por_nombre(e.name)
        #    bpy.context.object.hide = True
        # emparentando todo al empty esferico:
        seleccionar_por_nombre("cuerda.001")
        seleccionar_por_nombre("cuerda")
        seleccionar_por_nombre("Rope")
        bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
        deseleccionar_todo()
        # display que no muestre las relaciones
        #bpy.context.space_data.show_relationship_lines = False
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                area.spaces[0].show_relationship_lines = False
        seleccionar_por_nombre("cuerda.001")
        # cuerda curva settings:
        bpy.context.object.data.fill_mode = 'FULL'
        bpy.context.object.data.bevel_depth = self.radiusrope
        bpy.context.object.data.bevel_resolution = self.resrope
        #################################################################################                                
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=310)

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        col = box.column()
        col.label("Rope settings:")
        rowsub0 = col.row()
        rowsub0.prop(self, "ropelenght", text='Length')
        rowsub0.prop(self, "ropesegments", text='Segments')
        rowsub0.prop(self, "radiusrope", text='Radius')
        
        col.label("Quality Settings:")
        col.prop(self, "resrope", text='Resolution curve')
        col.prop(self, "qcr", text='Quality Collision')
        col.prop(self, "substeps", text='Substeps')

bpy.utils.register_class(DialogOperator)

class DialogPanel(bpy.types.Panel):
    bl_label = "Rope Creator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "RopeCreator"
    def draw(self, context):
        layout = self.layout
        context = bpy.context
        scn = context.scene
        row = layout.row(align=True)
        col = row.column()
        col.alignment = 'EXPAND'
        col.operator("object.zebus_dialog")

#   Registration
def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
