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
    "name": "Material Manager",
    "description": "This script is a simple material Manager.",
    "author": "Jorge Hernandez - Melenedez",
    "version": (0,1),
    "blender": (2, 65, 0),
    "location": "",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": ""}


import bpy

def deleteallmaterials():
    scn = bpy.context.scene 
    bpy.ops.object.select_all(action='DESELECT')
    for ob in bpy.data.scenes[scn.name].objects: 
        if ob.type == 'MESH' or ob.type == 'SURFACE' or ob.type == 'META': 
            if len(bpy.context.selected_objects) == 0:
                scn.objects.active = bpy.data.objects[str(ob.name)]
                myobject = bpy.data.objects[str(ob.name)]
                myobject.select = True
#                scn.objects.active = ob
#                ob.select = True
                if len(bpy.context.selected_objects) != 0:
                    for i in range(len(bpy.context.selected_objects)):                
                        cuantos=len(bpy.context.selected_objects[i].material_slots)                    
                        for i in range(cuantos):
                            bpy.ops.object.material_slot_remove()
            ob.select = False
            bpy.ops.object.select_all(action='DESELECT')
            
    for m in bpy.data.materials: 
        if m.use_fake_user == True: 
            m.use_fake_user = False

    for m in bpy.data.materials: 
        if m.users == 0: 
            bpy.data.materials.remove(m)


def onematerialforall():
    scn = bpy.context.scene   
    bpy.ops.object.select_all(action='DESELECT')  

    if "Material" not in bpy.data.materials:  
        mat = bpy.data.materials.new("Material")  
    else: 
        mat = bpy.data.materials['Material'] 

    for ob in bpy.data.scenes[scn.name].objects:   
        if ob.type == 'MESH' or ob.type == 'SURFACE' or ob.type == 'META':   
            if len(bpy.context.selected_objects) == 0:  
                #scn.objects.active = bpy.data.objects[str(ob.name)]  
                #myobject = bpy.data.objects[str(ob.name)]  
                #myobject.select = True  
                scn.objects.active = ob  
                ob.select = True   
                  
                bpy.ops.object.material_slot_add()  
                ob.material_slots[0].material = mat  

                bpy.ops.object.select_all(action='DESELECT')
                

def rmmaterialsunused():
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
    def rmrepetidos(listado):
        listado = list(set(listado)) # elimina duplicados
        return listado
    
    # limpiando lista de repetidos:
    mat_list = rmrepetidos(mat_list)
    
    for m in bpy.data.materials:
        # si no estan en mi lista es que no estan siendo usados, por lo tanto los elimino:
        if m not in mat_list:
            if m.use_fake_user == False: # respetaremos los fake
                m.user_clear()
                bpy.data.materials.remove(m)


class rmAllUnUsedMaterials(bpy.types.Panel):
    bl_label = "Simple Material Manager"
    bl_space_type = "VIEW_3D"
    #bl_region_type = "TOOL_PROPS"
    bl_region_type = "TOOLS"

    def draw(self, context):
        layout = self.layout
        scn = bpy.context.scene
        row = layout.row(align=True)
        col = row.column()
        col.alignment = 'EXPAND'

        col.operator("rma.rma", text='Remove all materials')
        col.operator("smat.smat", text='Single material for all')
        col.operator("rmumat.rmumat", text='Remove unused materials')

class execButonAction1(bpy.types.Operator):
    bl_idname = "rma.rma"
    bl_label = "Remove materials"
    bl_description = "This remove all materials in current scene"
    def execute(self, context):
        deleteallmaterials()
        return{'FINISHED'}

class execButonAction2(bpy.types.Operator):
    bl_idname = "smat.smat"
    bl_label = "Single material for all"
    bl_description = "Assing single material for all in current scene"
    def execute(self, context):
        onematerialforall()
        return{'FINISHED'}

class execButonAction3(bpy.types.Operator):
    bl_idname = "rmumat.rmumat"
    bl_label = "Remove unused materials"
    bl_description = "This remove all unused materials"
    def execute(self, context):
        rmmaterialsunused()
        return{'FINISHED'}


def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
