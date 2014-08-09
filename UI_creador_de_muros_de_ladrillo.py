import bpy
from bpy.props import *
 
# default settings:
#alto = 20 # numero de ladrillos en vertical
#ancho = 15 # numero de ladrillos en horizontal
#en_cm = False # si lo quiero en metros o en centimetros los ladrillos
#fill_esquinas=True # si queremos que rellene los huecos de los cantos

# ladrillo estandar:
#lancho = 24
#lalto = 11.5
#llargo = 6 # <- profundidad

# funciones varias:
def creandoLadrillo(nombre):
    bpy.ops.mesh.primitive_cube_add(radius=1, view_align=False, enter_editmode=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    bpy.context.object.name = nombre

class DialogOperator(bpy.types.Operator):
    bl_idname = "object.zebus_dialog"
    bl_label = "Creador de ladrillos v01"
    my_alto = IntProperty(name="alto", min=0, max=100, default=20)
    my_ancho = IntProperty(name="ancho", min=0, max=100, default=15)
    my_m_o_c = BoolProperty(name="Centimeters", default=False)
    my_fillb = BoolProperty(name="Fill Boundaryes", default=True)
    my_lancho = FloatProperty(name="lancho", min=0, max=100, default=24)
    my_lalto = FloatProperty(name="lalto", min=0, max=100, default=11.5)
    my_llargo = FloatProperty(name="llargo", min=0, max=100, default=6)
    
    def execute(self,context):
        alto = self.my_alto
        ancho = self.my_ancho
        lancho = self.my_lancho
        lalto = self.my_lalto
        llargo = self.my_llargo
        en_cm = self.my_m_o_c
        fill_esquinas = self.my_fillb
       
        if self.my_m_o_c:
            # conversion a cm:
            # no se por que me los esta multiplicando por 2 asi que /2
            bpy.context.scene.unit_settings.system = 'METRIC'
            cm_lancho=self.my_lancho/2/100
            cm_lalto=self.my_lalto/2/100
            cm_llargo=self.my_llargo/2/100
        else:
            bpy.context.scene.unit_settings.system = 'METRIC'
            cm_lancho=self.my_lancho/2
            cm_lalto=self.my_lalto/2
            cm_llargo=self.my_llargo/2
            
        # offset de nacimiento vertical
        # lo pongo en su sitio con el suelo Z:
        nv_offset = cm_llargo
        nh_offset = 0
        # individual offsets (donde iria el cemento):
        h_offset=cm_lancho*2 # los offset me esta dando la mitad del ladrillo por eso tengo q multipliarlos por 2
        v_offset=cm_llargo*2 # los offset me esta dando la mitad del ladrillo por eso tengo q multipliarlos por 2
        
        for v in range(alto):
            y=v
            for h in range(ancho):
                x=h
                creandoLadrillo("ladrillo")
                ob = bpy.context.object
                ob.scale.x = cm_lancho
                ob.scale.y = cm_lalto
                ob.scale.z = cm_llargo
                if y%2 == 0:
                    #anterior = bpy.context.selected_objects[0].name
                    anterior=ob.name

                    if fill_esquinas:
                        if h == 0:
                            bpy.ops.object.select_all(action='DESELECT')
                            creandoLadrillo("ladrillo_bordes")
                            actual = bpy.context.selected_objects[0].name
                            
                            ob = bpy.data.objects[str(actual)]
                            ob.select = True            
                            ob = bpy.context.object
                            ob.scale.x = cm_lancho/2
                            ob.scale.y = cm_lalto
                            ob.scale.z = cm_llargo
                            ob.location.x -= x*h_offset+nh_offset+cm_lancho/2
                            ob.location.z = y*v_offset+nv_offset
                            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
                            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
                        if (h == ancho-1):
                            bpy.ops.object.select_all(action='DESELECT')
                            creandoLadrillo("ladrillo_bordes")
                            actual = bpy.context.selected_objects[0].name

                            ob = bpy.data.objects[str(actual)]
                            ob.select = True            
                            ob = bpy.context.object
                            ob.scale.x = cm_lancho/2
                            ob.scale.y = cm_lalto
                            ob.scale.z = cm_llargo
                            ob.location.x += x*h_offset+nh_offset+cm_lancho+cm_lancho/2
                            ob.location.z = y*v_offset+nv_offset+v_offset
                            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
                            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
                    bpy.ops.object.select_all(action='DESELECT')
                    ob = bpy.data.objects[str(anterior)]
                    ob.select = True            
                    ob.location.x += x*h_offset+nh_offset+cm_lancho
                    ob.location.z = y*v_offset+nv_offset
                    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
                    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
                else:     
                    ob.location.x = x*h_offset+nh_offset
                    ob.location.z = y*v_offset+nv_offset
                    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
                    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            
                    
        return {'FINISHED'}     
    def invoke(self, context, event):
        global alto, ancho, fill_esquinas
        return context.window_manager.invoke_props_dialog(self, width=200)

    def draw(self, context):
        global alto, ancho, fill_esquinas
        layout = self.layout
        box = layout.box()
        col = box.column()
        col.label("Wall Settings:")
        rowsub0 = col.row()
        rowsub0.prop(self, "my_alto", text='Alto')
        rowsub0.prop(self, "my_ancho", text='Ancho')
        col.label("Brick Settings:")
        col.prop(self, "my_lancho", text='Alto')
        col.prop(self, "my_lalto", text='Ancho')
        col.prop(self, "my_llargo", text='Largo')
        col.label("Units Settings:")
        col = box.column()
        col.prop(self, "my_m_o_c")
        col.label("Fill Settings:")
        col.prop(self, "my_fillb")
            
bpy.utils.register_class(DialogOperator)

class DialogPanel(bpy.types.Panel):
    bl_label = "Dialog"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "WallCreator"
 
    def draw(self, context):
        #global alto, ancho, fill_esquinas
        layout = self.layout
        context = bpy.context
        scn = context.scene
        row = layout.row(align=True)
        col = row.column()
        col.alignment = 'EXPAND'
        col.operator("object.zebus_dialog")
        
#
#	Registration
bpy.utils.register_module(__name__)
