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
    "name": "Withe Water",
    "description": "Easy white water setup in blender",
    "author": "Jorge Hernandez - Melenedez",
    "version": (0, 0),
    "blender": (2, 77, 0),
    "location": "",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": ""
    }

class guiBotones(bpy.types.Panel):
    bl_label = "White Water"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "WhiteWater"    
    def draw(self, context):
        scn = context.scene
        layout = self.layout
        split = layout.split() 
        row1 = layout.row(align=True) 
        col1 = row1.column() 
        col1.alignment = 'EXPAND' 
        col1.operator("set.emiter", text='Set Emiter')
        col1.operator("set.domain", text='Set Domain')
        #col.operator("seleccionar.objetos", text='Select objects per name')  

emisor = []                  
dominio = []

class setEmiter(bpy.types.Operator):
    bl_idname = "set.emiter"
    bl_label = "Set as Emiter"
    bl_description = "Set selected object as emiter"    
    def execute(self, context):        
        scn = bpy.context.scene
        if bpy.context.selected_objects and len(bpy.context.selected_objects) == 1 :
            ob = bpy.context.selected_objects[0]
            if ob.type != 'MESH':
                self.report({'WARNING'}, 'This object is not a Mesh!')
            else:
                emisor.append(ob.name)
                if 'Fluidsim' not in ob.modifiers:
                    bpy.ops.object.modifier_add(type='FLUID_SIMULATION')
                bpy.context.object.modifiers["Fluidsim"].settings.type = 'FLUID'
        return{'FINISHED'}
    
    
class setDomain(bpy.types.Operator):
    bl_idname = "set.domain"
    bl_label = "Set as Domain"
    bl_description = "Set selected object as Domain"    
    def execute(self, context):        
        scn = bpy.context.scene
        if bpy.context.selected_objects and len(bpy.context.selected_objects) == 1 :
            ob = bpy.context.selected_objects[0]
            if ob.type != 'MESH':
                self.report({'WARNING'}, 'This object is not a Mesh!')
            else:
                dominio.append(ob.name)
                if 'Fluidsim' not in ob.modifiers:
                    bpy.ops.object.modifier_add(type='FLUID_SIMULATION')
                bpy.context.object.modifiers["Fluidsim"].settings.type = 'DOMAIN'
        return{'FINISHED'}
                    
def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
