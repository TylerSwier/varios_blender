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
    "name": "Wall Creator",
    "description": "Wall Creator",
    "author": "Jorge Hernandez - Melenedez",
    "version": (0, 1),
    "blender": (2, 71, 0),
    "location": "Left Toolbar > WallCreator",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Add Mesh"}

def eliminarTodo():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def freezer():
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')

def creandoLadrillo(nombre):
    bpy.ops.mesh.primitive_cube_add(radius=1, view_align=False, enter_editmode=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    bpy.context.object.name = nombre

class DialogOperator(bpy.types.Operator):
    bl_idname = "object.zebus_dialog"
    bl_label = "Wall Bricks Creator v01"
    my_alto = IntProperty(name="alto", min=0, max=100, default=20)
    my_ancho = IntProperty(name="ancho", min=0, max=100, default=5)
    my_m_o_c = BoolProperty(name="Centimeters", default=False)
    #my_fillb = BoolProperty(name="Fill Boundaryes", default=True)
    #my_lancho = FloatProperty(name="lancho", min=0, max=100, default=24)
    #my_lalto = FloatProperty(name="lalto", min=0, max=100, default=11.2)
    #my_llargo = FloatProperty(name="llargo", min=0, max=100, default=5)
    #my_cemento = FloatProperty(name="cemento", min=0, max=1.8, default=1.6)
    
    my_fillb = BoolProperty(name="Fill Boundaryes", default=False)
    my_lancho = FloatProperty(name="lancho", min=0, max=100, default=0.5)
    my_lalto = FloatProperty(name="lalto", min=0, max=100, default=0.5)
    my_llargo = FloatProperty(name="llargo", min=0, max=100, default=0.5)
    my_cemento = FloatProperty(name="cemento", min=0, max=1.8, default=0.5)
    
    # en metros un cubo de escala 1 1 1 equivale a 2 metros x 2 metros x 2 metros...
    
    def execute(self,context):
        
        eliminarTodo()
        
        alto = self.my_alto
        ancho = self.my_ancho
        ladrillo_ancho = self.my_lancho
        ladrillo_alto = self.my_lalto
        ladrillo_largo = self.my_llargo
        en_cm = self.my_m_o_c
        fill_esquinas = self.my_fillb
        cemento = self.my_cemento
       
       
        bpy.context.scene.unit_settings.system = 'METRIC'
        ladrillo_ancho_cm=self.my_lancho
        ladrillo_alto_cm=self.my_lalto
        ladrillo_largo_cm=self.my_llargo
            
        #if self.my_m_o_c:
            ## conversion a cm:
            ## no se por que me los esta multiplicando por 2 asi que /2
            #bpy.context.scene.unit_settings.system = 'METRIC'
            #ladrillo_ancho_cm=self.my_lancho/2/100
            #ladrillo_alto_cm=self.my_lalto/2/100
            #ladrillo_largo_cm=self.my_llargo/2/100
        #else:
            #bpy.context.scene.unit_settings.system = 'METRIC'
            #ladrillo_ancho_cm=self.my_lancho/2
            #ladrillo_alto_cm=self.my_lalto/2
            #ladrillo_largo_cm=self.my_llargo/2
            
        # offset de nacimiento vertical
        # lo pongo en su sitio con el suelo Z:
        
        
        # individual offsets (donde iria el cemento):
        c_offset=cemento
        #if cemento != 0:
            #c_offset=cemento

        #else:
            #c_offset=ladrillo_ancho_cm
           
        
        for v in range(alto):
            y=v
            for h in range(ancho):
                x=h
                creandoLadrillo("ladrillo")
                ob = bpy.context.object
                ob.scale.x = ladrillo_ancho_cm
                ob.scale.y = ladrillo_alto_cm
                ob.scale.z = ladrillo_largo_cm
                
                # si son pares:
                if y%2 == 0:
                    anterior=ob.name
                    
                    # Boundaryes:
                    #if fill_esquinas:
                        #if h == 0:
                            #bpy.ops.object.select_all(action='DESELECT')
                            #creandoLadrillo("ladrillo_bordes")
                            #actual = bpy.context.selected_objects[0].name
                            
                            #ob = bpy.data.objects[str(actual)]
                            #ob.select = True            
                            #ob = bpy.context.object
                            #ob.scale.x = ladrillo_ancho_cm/2
                            #ob.scale.y = ladrillo_alto_cm
                            #ob.scale.z = ladrillo_largo_cm
                            #ob.location.x = x * c_offset + nh_offset + ladrillo_ancho_cm
                            #ob.location.z = y * c_offset + nv_offset
                            
                            #freezer()
                            
                        #if (h == ancho-1):
                            #bpy.ops.object.select_all(action='DESELECT')
                            #creandoLadrillo("ladrillo_bordes")
                            #actual = bpy.context.selected_objects[0].name

                            #ob = bpy.data.objects[str(actual)]
                            #ob.select = True            
                            #ob = bpy.context.object
                            #ob.scale.x = ladrillo_ancho_cm/2
                            #ob.scale.y = ladrillo_alto_cm
                            #ob.scale.z = ladrillo_largo_cm
                            #ob.location.x = x * c_offset + nh_offset + ladrillo_ancho_cm
                            #ob.location.z = y * c_offset + nv_offset + c_offset
                            
                            #freezer()
                            
                    bpy.ops.object.select_all(action='DESELECT')
                    ob = bpy.data.objects[str(anterior)]
                    ob.select = True            
                    ob.location.x = (x * (c_offset * 2)) + (ladrillo_ancho_cm * 2) + c_offset
                    ob.location.z = y * ((ladrillo_alto_cm * 2) + c_offset)
                    
                    freezer()
                    
                # si no son pares:
                else:     
                    ob.location.x = (x * (c_offset * 2)) + (ladrillo_ancho_cm * 2)
                    ob.location.z = y * ((ladrillo_alto_cm * 2) + c_offset)
                    
                    freezer()
            
                    
        return {'FINISHED'}   
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=200)

    def draw(self, context):
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
        col.label("Cement Settings:")
        col.prop(self, "my_cemento", text='Cemento')
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
        layout = self.layout
        context = bpy.context
        scn = context.scene
        row = layout.row(align=True)
        col = row.column()
        col.alignment = 'EXPAND'
        col.operator("object.zebus_dialog")
        
#	Registration
def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
