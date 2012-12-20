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
from bpy.props import *

def mySceneProperties(scn):
    bpy.types.Scene.Respect = BoolProperty( name = "Respect Fake User", description = "Respect Fake User, for Remove all materials button")
    scn['Respect'] = True

mySceneProperties(bpy.context.scene)


def deleteallmaterials(opcion1,opcion2):
    scn = bpy.context.scene
    bpy.ops.object.select_all(action='DESELECT')
    for ob in bpy.data.scenes[scn.name].objects:
        if ob.type == 'MESH' or ob.type == 'SURFACE' or ob.type == 'META' or ob.type == 'CURVE' or ob.type == 'FONT':
            if len(bpy.context.selected_objects) == 0:
                scn.objects.active = bpy.data.objects[str(ob.name)]
                myobject = bpy.data.objects[str(ob.name)]
                myobject.select = True

                if len(bpy.context.selected_objects) != 0:
                    for i in range(len(bpy.context.selected_objects)):
                        cuantos=len(bpy.context.selected_objects[i].material_slots)
                        for i in range(cuantos):
                            bpy.ops.object.material_slot_remove()
            ob.select = False
            bpy.ops.object.select_all(action='DESELECT')

    if scn['Respect']:
        opcion2 = "respetando"

    if opcion2 != "respetando":
        for m in bpy.data.materials:
            if m.use_fake_user == True:
                m.use_fake_user = False

    if opcion1 == "borrando":
        for m in bpy.data.materials:
            if m.users == 0:
                bpy.data.materials.remove(m)


def onematerialforall():
    scn = bpy.context.scene
    objetos = bpy.context.selected_objects
    if len(objetos) != 0:
        seleccionados = True
    else:
        seleccionados = False

    mat = bpy.data.materials.new("Material")
    if seleccionados:

        for ob in objetos:
            if ob.type == 'MESH' or ob.type == 'SURFACE' or ob.type == 'META' or ob.type == 'CURVE' or ob.type == 'FONT':
                bpy.ops.object.select_all(action='DESELECT')
                if len(bpy.context.selected_objects) == 0:
                    scn.objects.active = ob
                    ob.select = True
                    
                    if len(ob.material_slots) == 0:
                        bpy.ops.object.material_slot_add()
                        ob.material_slots[0].material = mat
                    else:
                        for i in range(len(ob.material_slots)):
                            ob.material_slots[i].material = mat

                    bpy.ops.object.select_all(action='DESELECT')
    else:
        for ob in bpy.data.scenes[scn.name].objects:
            if ob.type == 'MESH' or ob.type == 'SURFACE' or ob.type == 'META' or ob.type == 'CURVE' or ob.type == 'FONT':
                if len(bpy.context.selected_objects) == 0:
                    scn.objects.active = ob
                    ob.select = True
           
                    if len(ob.material_slots) <= 0:
                        bpy.ops.object.material_slot_add()
                        ob.material_slots[0].material = mat
                    else:
                        for i in range(len(ob.material_slots)):
                            ob.material_slots[i].material = mat

                    bpy.ops.object.select_all(action='DESELECT')

def desligar():
    scn = bpy.context.scene
    ob = bpy.context.selected_objects
    bpy.ops.object.select_all(action='DESELECT')
    #if len(bpy.context.selected_objects) != 0:
    if ob: #<-- una manera mas elegante de hacer la misma comprobacion que arriba
        for i in range(len(ob)):
            if ob[i].type == 'MESH' or ob[i].type == 'SURFACE' or ob[i].type == 'META' or ob[i].type == 'CURVE' or ob[i].type == 'FONT':
                myobject = bpy.data.objects[str(ob[i].name)]
                myobject.select = True
                scn.objects.active = ob[i]
                
                cuantos=len(ob[i].material_slots)
                for i in range(cuantos):
                    bpy.ops.object.material_slot_remove()
                myobject.select = False

            bpy.ops.object.select_all(action='DESELECT')
    else:
        for ob in bpy.data.scenes[scn.name].objects:
            if ob.type == 'MESH' or ob.type == 'SURFACE' or ob.type == 'META' or ob.type == 'CURVE' or ob.type == 'FONT':
                myobject = bpy.data.objects[str(ob.name)]
                myobject.select = True
                scn.objects.active = ob
                
                cuantos=len(ob.material_slots)
                for i in range(cuantos):
                    bpy.ops.object.material_slot_remove()
                myobject.select = False

            bpy.ops.object.select_all(action='DESELECT')


def rmmaterialsunused():
    mat_list = []
    escenas = bpy.data.scenes
    # recorriendo todas las escenas en busca de materiales usados:
    for i in range(len(escenas)):
        for ob in escenas[i].objects:
            # si es de tipo objeto entonces
            if ob.type == 'MESH' or ob.type == 'SURFACE' or ob.type == 'META' or ob.type == 'CURVE' or ob.type == 'FONT':
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

        col.prop(scn, 'Respect')
        col.operator("rma.rma", text='Remove all materials')
        col.operator("dsm.dsm", text='Untie mataterials slots')
        col.operator("smats.smats", text='Single material')
        col.operator("rmumat.rmumat", text='Remove unused materials')


class execButonAction1(bpy.types.Operator):
    bl_idname = "rma.rma"
    bl_label = "Remove materials" # el label que sale en el boton es el de col no este
    bl_description = "This remove all materials in current scene"
    def execute(self, context):
        deleteallmaterials("borrando","")
        return{'FINISHED'}

class execButonAction2(bpy.types.Operator):
    bl_idname = "dsm.dsm"
    bl_label = "Untie mataterials slots"
    bl_description = "Untie materials from all objects (or selected objects)"
    def execute(self, context):
        desligar()
        return{'FINISHED'}

class execButonAction3(bpy.types.Operator):
    bl_idname = "smats.smats"
    bl_label = "Single material"
    bl_description = "Single material for all objects (or selected objects)"
    def execute(self, context):
        onematerialforall()
        return{'FINISHED'}

class execButonAction4(bpy.types.Operator):
    bl_idname = "rmumat.rmumat"
    bl_label = "Remove unused materials"
    bl_description = "This remove all unused materials in all scenes"
    def execute(self, context):
        rmmaterialsunused()
        return{'FINISHED'}


def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
