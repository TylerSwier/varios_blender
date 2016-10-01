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
    "name": "regladetres", 
    "description": "Regla de tres simple", 
    "author": "Jorge Hernandez - Melenedez", 
    "version": (0,0), 
    "blender": (2, 64, 0), 
    "api": 31236, 
    "location": "", 
    "warning": "", 
    "wiki_url": "", 
    "tracker_url": "", 
    "category": ""} 

import bpy 
from bpy.props import * 

bpy.types.Scene.etxt1 = StringProperty(name="", description="Si A", maxlen= 1024, default="Si A (cantidad)") 
bpy.types.Scene.etxt2 = StringProperty(name="", description="Son B", maxlen= 1024, default="Son B (cantidad)") 
bpy.types.Scene.etxt3 = StringProperty(name="", description="Entonces C son", maxlen= 1024, default="Cuanto sera C?")
bpy.types.Scene.etxt4 = StringProperty(name="", attr="res", description="resultado", maxlen= 1024, default="") 

class reglaDeTres(bpy.types.Panel): 
    bl_label = "Regla de tres simple v00:" 
    bl_space_type = "VIEW_3D" 
    #bl_region_type = "TOOL_PROPS" 
    bl_region_type = "TOOLS" 

    def draw(self, context): 
        layout = self.layout 
        scn = bpy.context.scene 
        split = layout.split() 
        row1 = layout.row(align=True) 
        col1 = row1.column() 
        col1.alignment = 'EXPAND' 

        col1.prop(context.scene,"etxt1") 
        col1 = row1.column() 
        col1.prop(context.scene,"etxt2")  
        row2 = layout.row(align=True) 
        col2 = row2.column()
        col1 = row1.column() 
        col1.operator("calcular.calcular", text='Calcular')
        col2.prop(context.scene,"etxt3")
        col2.label(text=bpy.context.scene.etxt4)
        
        
        
        col1 = split.column() 

         
def calcular(): 
    resultado = str( float(bpy.context.scene.etxt3) * float(bpy.context.scene.etxt2) / float(bpy.context.scene.etxt1) ) 
    return resultado 

class botonAccion(bpy.types.Operator): 
    bl_idname = "calcular.calcular" 
    bl_label = "calcular" 
    bl_description = "Calculandora de regla de tres simple" 
    def execute(self, context): 
        try: 
            bpy.context.scene.etxt4 = "Resultado: " + calcular() 
        except: 
            bpy.context.scene.etxt3 = "Solo son validos valores numericos!!" 
        return{'FINISHED'} 

def register(): 
    bpy.utils.register_module(__name__) 

def unregister(): 
    bpy.utils.unregister_module(__name__) 


if __name__ == "__main__": 
    register()
