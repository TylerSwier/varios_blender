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
    bpy.types.Scene.ITextures = BoolProperty( name = "Include textures", description = "Include textures")
    scn['ITextures'] = False
    bpy.types.Scene.Respect = BoolProperty( name = "Respect Fake User", description = "Respect Fake User, for all remove actions")
    scn['Respect'] = True

mySceneProperties(bpy.context.scene)


# optener listado de texturas
def obtenertexturas(opcion1):
    text_list = []
    if opcion1 == "local":
        sel = bpy.context.selected_objects
        if len(sel) == 0:
            for os in bpy.context.scene.objects:
                for slot in os.material_slots:
                    for ts in slot.material.texture_slots:
                        text_list.append(ts)
        else:
            for os in sel:
                for slot in os.material_slots:
                    for ts in slot.material.texture_slots:
                        text_list.append(ts)
    else:
        sel = bpy.context.selected_objects
        for escena in bpy.data.scenes:
            for os in bpy.data.scenes[escena.name].objects:
                if len(sel) == 0:
                    for slot in os.material_slots:
                        for ts in slot.material.texture_slots:
                            text_list.append(ts)
                else:
                    for so in sel:
                        for slot in so.material_slots:
                            for ts in slot.material.texture_slots:
                                text_list.append(ts)
    # limpiando lista de repetidos:
    preparando = list(set(text_list))
    text_list = preparando
    return text_list
    
# optener listado de materiales de objetos
def obtenermateriales(opcion1):
    mat_list = []
    if opcion1 == "local":
        sel = bpy.context.selected_objects
        if len(sel) == 0:
            for os in bpy.context.scene.objects:
                for slot in os.material_slots:
                    mat_list.append(slot)
        else:
            for os in sel:
                for slot in os.material_slots:
                    mat_list.append(slot)
    else:
        sel = bpy.context.selected_objects
        for escena in bpy.data.scenes:
            for os in bpy.data.scenes[escena.name].objects:
                if len(sel) == 0:
                    for slot in os.material_slots:
                        mat_list.append(slot)
                else:
                    for so in sel:
                        for slot in so.material_slots:
                            mat_list.append(slot)
    # limpiando lista de repetidos:
    preparando = list(set(mat_list))
    mat_list = preparando
    return mat_list

# Nota: si no es en "local" y si es con algo seleccionado, evidentemente
# saldran solo los de los objetos deleccionados de la escena actual, ya
# que los full copy scene cambian de nombre los objetos y son "unicos"
#mat = obtenermateriales("local")
#for i in mat:
#    print(i.name)

def rm_texture_by_name(nombre,opcion1):
    if opcion1 == "rtexture":
        try:
            bpy.data.textures[nombre].user_clear()
            bpy.data.textures.remove(bpy.data.textures[nombre])
        except:
            pass
            
def rm_material_by_name(nombre,opcion1):
    scn = bpy.context.scene
    bpy.ops.object.select_all(action='DESELECT')
    objetos_c = [] # objetos que objeto contienen el material:

    for ob in bpy.data.scenes[scn.name].objects:
        if ob.type == 'MESH' or ob.type == 'SURFACE' or ob.type == 'META' or ob.type == 'CURVE' or ob.type == 'FONT':
            if len(bpy.context.selected_objects) == 0:
                scn.objects.active = bpy.data.objects[str(ob.name)]
                myobject = bpy.data.objects[str(ob.name)]
                myobject.select = True
                print(ob.name)
                for ms in ob.material_slots:
                    if ms.name == nombre:
                        if ms.material.use_fake_user != True or opcion1 != "respetando":
                            objetos_c.append(ob)
                ob.select = False
                bpy.ops.object.select_all(action='DESELECT')

    for x in objetos_c:
        scn.objects.active = bpy.data.objects[str(x.name)]
        sobject = bpy.data.objects[str(ob.name)]
        sobject.select = True
        # obteniendo posiciones de los slots que contengan el material:
        pos = []
        # buscamos en que slots esta:
        for i in range(len(x.material_slots)):
            if x.material_slots[i].name == nombre:
                pos.append(i)
        for mat in bpy.data.materials: # lo buscamos para desactivarle el fake user:
            if opcion1 != "respetando":
                if mat.name == nombre:
                    if mat.use_fake_user == True:
                        mat.use_fake_user = False
        for i in range(len(x.material_slots)): # por cada slot de materiales del objeto:
            # apuntar a que posicion de slot afectara el borrado:
            # bpy.data.objects['Cube.001'].active_material_index = 1
            if i < len(pos):
                x.active_material_index = pos[i]
                # y borandolo:
                bpy.ops.object.material_slot_remove() # esto borra el slot para dejarlo en users = 0
        x.user_clear()
        try:
            bpy.data.materials.remove(bpy.data.materials[nombre])
        except:
            pass
        ob.select = False
        bpy.ops.object.select_all(action='DESELECT')

#respeto = ""
#respeto = "respetando"
#rm_material_by_name("verde",respeto)


def deleteallmaterials():
    scn = bpy.context.scene
    if scn['Respect']:
        opcion1 = "respetando"
    else:
        opcion1 = ""
        
    if scn['ITextures']:
        opcion1 = "rtexture"
    else:
        opcion1 = ""
        
    texturas = obtenertexturas("local")
    for i in texturas:
        try:
            rm_texture_by_name(i.name,opcion1)
        except:
            pass
            
    materiales = obtenermateriales("local")
    for i in materiales:
        rm_material_by_name(i.name,opcion1)


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
        for i in ob:
            myobject = bpy.data.objects[str(i.name)]
            myobject.select = True
            scn.objects.active = i
            
            if len(i.material_slots) > 0:
                for sl in range(len(i.material_slots)):
                    i.user_clear()
                    bpy.ops.object.material_slot_remove()
                else:
                    for sl in i.material_slots:
                        i.user_clear()
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
    scn = bpy.context.scene
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
            # si es true se setea como respetando:
            if scn['Respect']:
                opcion1 = "respetando"
            else:
                opcion1 = ""
                
            if opcion1 != "respetando":
                if m.use_fake_user == True:
                    m.use_fake_user = False
                
            if m.use_fake_user == False: # respetaremos los fake
                m.user_clear()
                bpy.data.materials.remove(m)


def makefakeuser():
    scn = bpy.context.scene
    ob = bpy.context.selected_objects
    bpy.ops.object.select_all(action='DESELECT')
    if ob:
        for i in range(len(ob)):
            if ob[i].type == 'MESH' or ob[i].type == 'SURFACE' or ob[i].type == 'META' or ob[i].type == 'CURVE' or ob[i].type == 'FONT':
                myobject = bpy.data.objects[str(ob[i].name)]
                myobject.select = True
                scn.objects.active = ob[i]
                for mat in ob[i].material_slots:
                    bpy.data.materials[mat.name].use_fake_user = True
                myobject.select = False
            bpy.ops.object.select_all(action='DESELECT')

def demakefakeuser():
    scn = bpy.context.scene
    ob = bpy.context.selected_objects
    bpy.ops.object.select_all(action='DESELECT')
    if ob:
        for i in range(len(ob)):
            if ob[i].type == 'MESH' or ob[i].type == 'SURFACE' or ob[i].type == 'META' or ob[i].type == 'CURVE' or ob[i].type == 'FONT':
                myobject = bpy.data.objects[str(ob[i].name)]
                myobject.select = True
                scn.objects.active = ob[i]
                for mat in ob[i].material_slots:
                    bpy.data.materials[mat.name].use_fake_user = False
                myobject.select = False
            bpy.ops.object.select_all(action='DESELECT')

def selectfakeuser():
    scn = bpy.context.scene
    obs = bpy.data.scenes[scn.name].objects
    bpy.ops.object.select_all(action='DESELECT')
    for i in range(len(obs)):
        for mat in obs[i].material_slots:
            if bpy.data.materials[mat.name].use_fake_user == True:
                myobject = bpy.data.objects[str(obs[i].name)]
                myobject.select = True
                scn.objects.active = obs[i]


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

        col.prop(scn, 'ITextures')
        col.prop(scn, 'Respect')
        col.operator("rma.rma", text='Remove all materials')
        col.operator("smats.smats", text='Single material')
        col.operator("dsm.dsm", text='Untie mataterials slots')
        subrow = col.row(align=True)
        subrow.operator("mfu.mfu", text='Make Fake User')
        subrow.operator("umfu.umfu", text='Unmake Fake User')
        col.operator("sfu.sfu", text='Select Fake Users')
        col.operator("rmumat.rmumat", text='Remove unused materials')
        


class execButonAction1(bpy.types.Operator):
    bl_idname = "rma.rma"
    bl_label = "Remove materials" # el label que sale en el boton es el de col no este
    bl_description = "This remove all materials in current scene (all or selected objects)"
    def execute(self, context):
        if bpy.context.mode == 'OBJECT':
            deleteallmaterials()
        return{'FINISHED'}

class execButonAction2(bpy.types.Operator):
    bl_idname = "dsm.dsm"
    bl_label = "Untie mataterials slots"
    bl_description = "Untie materials from all objects (or selected objects)"
    def execute(self, context):
        if bpy.context.mode == 'OBJECT':
            desligar()
        return{'FINISHED'}

class execButonAction3(bpy.types.Operator):
    bl_idname = "mfu.mfu"
    bl_label = "Make Fake User" # el label que sale en el boton es el de col no este
    bl_description = "Make Fake User"
    def execute(self, context):
        if bpy.context.mode == 'OBJECT':
            makefakeuser()
        return{'FINISHED'}

class execButonAction4(bpy.types.Operator):
    bl_idname = "umfu.umfu"
    bl_label = "Unmake Fake User" # el label que sale en el boton es el de col no este
    bl_description = "Unmake Fake User"
    def execute(self, context):
        if bpy.context.mode == 'OBJECT':
            demakefakeuser()
        return{'FINISHED'}

class execButonAction5(bpy.types.Operator):
    bl_idname = "smats.smats"
    bl_label = "Single material"
    bl_description = "Single material for all objects (or selected objects)"
    def execute(self, context):
        if bpy.context.mode == 'OBJECT':
            onematerialforall()
        return{'FINISHED'}

class execButonAction6(bpy.types.Operator):
    bl_idname = "sfu.sfu"
    bl_label = "Select Fake Users"
    bl_description = "Select Fake Users"
    def execute(self, context):
        if bpy.context.mode == 'OBJECT':
            selectfakeuser()
        return{'FINISHED'}

class execButonAction7(bpy.types.Operator):
    bl_idname = "rmumat.rmumat"
    bl_label = "Remove unused materials"
    bl_description = "This remove all unused materials in all scenes"
    def execute(self, context):
        if bpy.context.mode == 'OBJECT':
            rmmaterialsunused()
        return{'FINISHED'}


def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
