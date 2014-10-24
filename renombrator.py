# License:
''' Copyright (c) 2012 Jorge Hernandez - Melendez

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''
bl_info = {
    "name": "Renombrator",
    "description": "Rename all objects selected",
    "author": "Jorge Hernandez - Melenedez",
    "version": (0, 1),
    "blender": (2, 72, 0),
    "location": "",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": ""
    }
    
import bpy
from bpy.props import *

def mySceneProperties():
    bpy.types.Scene.Nombre = bpy.props.StringProperty( name = "Name: ", default = "", description = "New Name for selected objects")
mySceneProperties()


class Botones_Renombrator(bpy.types.Panel):
    bl_label = "Renombrator"
    bl_space_type = "VIEW_3D"
    #bl_region_type = "TOOL_PROPS"
    bl_region_type = "TOOLS"
    bl_category = "Renombrator"
    
    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        col = row.column()
        col.alignment = 'EXPAND'
        scn = context.scene
    
        subrow0 = col.row(align=True)
        subrow0.prop(scn, "Nombre")
        subrow0.operator("seleccionar.semejantes", text='<-')
        col.operator("renombrar.objetos", text='Rename objects selected')  
        col.operator("seleccionar.objetos", text='Select objects per name')  

def desseleccionarTodo():
    bpy.ops.object.select_all(action='DESELECT')
    
def deseleccionarTodoEditmode():
    bpy.ops.mesh.select_all(action='DESELECT')
    
def seleccionarTodoEditmode():
    bpy.ops.mesh.select_all(action='SELECT')

def subdividir(cuantas):
    for i in range(cuantas):
        bpy.ops.mesh.subdivide(smoothness=0)


class Seleccionar(bpy.types.Operator):
    bl_idname = "seleccionar.objetos"
    bl_label = "Select"
    bl_description = "Select objects per name"
    
    def execute(self, context):        
        scn = bpy.context.scene
        for ob in bpy.data.objects:
            if ob.name.find(scn.Nombre) >= 0:
                ob.select = True
                scn.objects.active = bpy.data.objects[str(ob.name)]
        return{'FINISHED'}


class SeleccionarSemejantes(bpy.types.Operator):
    bl_idname = "seleccionar.semejantes"
    bl_label = "Select"
    bl_description = "Select objects by similar name to the current object selected"

    def execute(self, context):
        patron = bpy.context.selected_objects[0].name
        try:
            nombre = patron.split(".")
            nombre = nombre[0]
        except:
            nombre = patron
        
        scn = bpy.context.scene            
        scn.Nombre = nombre
        for ob in bpy.data.objects:
            if ob.name.find(nombre) >= 0:
                ob.select = True
                scn.objects.active = bpy.data.objects[str(ob.name)]
        return{'FINISHED'}

class Renombrar(bpy.types.Operator):
    bl_idname = "renombrar.objetos"
    bl_label = "Rename"
    bl_description = "Rename objects selected"
    
    def execute(self, context):        
        scn = bpy.context.scene
        nuevonombre = str(bpy.context.scene.Nombre)
        n = 0
        if bpy.context.selected_objects:
            for ob in bpy.context.selected_objects:
                scn.objects.active = bpy.data.objects[str(ob.name)]
                if nuevonombre:
                    if n == 0:
                        ob.name = nuevonombre + str(".000")
                    else:
                        ob.name = str(nuevonombre)
        return{'FINISHED'}
                    
def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
