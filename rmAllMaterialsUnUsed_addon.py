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
    "name": "Remove All UnUsed Materials",
    "description": "This script remove all materials unused.",
    "author": "Jorge Hernandez - Melenedez",
    "version": (0,1),
    "blender": (2, 65, 0),
    "location": "",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": ""}


import bpy

def rmMaterialsUnused():
    mat_list = []
    escenas = bpy.data.scenes
    # recorriendo todas las escenas en busca de materiales usados:
    for i in range(len(escenas)):
        for ob in escenas[i].objects:
            # si es de tipo objeto entonces
            if ob.type == 'MESH' or ob.type == 'SURFACE' or ob.type == 'META':
                if ob.data.materials == '' or len(ob.material_slots.items()) != 0:
                    # si no esta vacio o tiene mas de 0 slots entonces me lo recorro y 
                    # voy agregando los materiales al array
                    for ms in ob.material_slots:
                        mat_list.append(ms.material)
                        
    # limpiando lista de repetidos:
    def rmRepetidos(listado):
        listado = list(set(listado)) # elimina duplicados
        return listado
    
    # limpiando lista de repetidos:
    mat_list = rmRepetidos(mat_list)
    
    for m in bpy.data.materials:
        # si no estan en mi lista es que no estan siendo usados, por lo tanto los elimino:
        if m not in mat_list:
            if m.use_fake_user == False: # respetaremos los fake
                m.user_clear()
                bpy.data.materials.remove(m)


class rmAllUnUsedMaterials(bpy.types.Panel):
    bl_label = "Remove All unused Materials"
    bl_space_type = "VIEW_3D"
    #bl_region_type = "TOOL_PROPS"
    bl_region_type = "TOOLS"

    def draw(self, context):
        layout = self.layout
        scn = bpy.context.scene
        row = layout.row(align=True)
        col = row.column()
        col.alignment = 'EXPAND'

        col.operator("rmmat.rmmat", text='Remove materials unused')

class execbutonaction(bpy.types.Operator):
    bl_idname = "rmmat.rmmat"
    bl_label = "Remove materials unused"
    bl_description = "This script remove all materials unused."
    def execute(self, context):
        rmMaterialsUnused()
        return{'FINISHED'}

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
