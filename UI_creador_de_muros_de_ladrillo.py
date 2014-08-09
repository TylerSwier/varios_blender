import bpy
from bpy.props import *
 
# default settings:
alto = 20 # numero de ladrillos en vertical
ancho = 15 # numero de ladrillos en horizontal
en_cm = False # si lo quiero en metros o en centimetros los ladrillos
fill_esquinas=True # si queremos que rellene los huecos de los cantos

class DialogOperator(bpy.types.Operator):
    bl_idname = "object.zebus_dialog"
    bl_label = "Creador de ladrillos v01"
    my_alto = IntProperty(name="alto", min=0, max=100, default=20)
    my_ancho = IntProperty(name="ancho", min=0, max=100, default=15)
    my_m_o_c = BoolProperty(name="Meters or Centimeters", default=False)
    my_fillb = BoolProperty(name="Fill Boundaryes", default=True)
    def execute(self,context):
        print("kk")
        return {'FINISHED'}     
    def invoke(self, context, event):
        global alto, ancho, fill_esquinas
        return context.window_manager.invoke_props_dialog(self, width=200)

    def draw(self, context):
        global alto, ancho, fill_esquinas
        layout = self.layout
        box = layout.box()
        col = box.column()
        rowsub = col.row()
        rowsub.prop(self, "my_alto")
        rowsub.prop(self, "my_ancho")

        col = box.column()
        rowsub = col.row()
        col.prop(self, "my_m_o_c")
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
