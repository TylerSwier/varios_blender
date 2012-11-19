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
######################################### 
# Nuevo material id: 
######################################### 
import bpy, random 
escenas = bpy.data.scenes 
#materiales=bpy.data.materials 
if "Material_ID" not in escenas: 
    bpy.ops.scene.new(type='FULL_COPY') 
    bpy.context.scene.name = "Material_ID" 
    bpy.ops.object.select_all(action='DESELECT') 
    scn = bpy.context.scene 
    cntxt = bpy.context 
    def chequeoEscena(): 
        if scn.name == "Material_ID": 
            return True 
        else: 
            return False 
    if chequeoEscena():         
        def getMateriales(): 
            # obteniendo todos los nombres de los materiales de todos los objetos de la escena actual:
            mat_list = [] 
            for ob in bpy.data.scenes[scn.name].objects: 
                if ob.type == 'MESH' or ob.type == 'SURFACE' or ob.type == 'META':  
                    if ob.data.materials == '' or len(ob.material_slots.items()) != 0: 
                        for ms in ob.material_slots: 
                            mat_list.append(ms.material) 
            # limpiando lista de repetidos:                 
            def rmRepetidos(listado): 
                listado = list(set(listado)) # elimina duplicados 
                return listado 
            # limpiando lista de repetidos: 
            mat_list = rmRepetidos(mat_list) 
            return mat_list 
        mat_list = getMateriales() 
        # numero de nuevos material ids: 
        NM=len(mat_list) 
        def deslinkar(): 
            # deslinkando todos los materiales de la escena actual 
            for mat in mat_list: 
                mat.user_clear() # unlink 
                bpy.data.materials.remove(mat) # remove "mat" from materials slot 
        deslinkar() 
        # Crenado libreria de materiales id: 
        def fabricaMaterialsID(cuantos): 
            materiales = [] 
            for i in range(0,cuantos): 
                m=bpy.data.materials.new("Material_ID_"+str(i)) 
                m.diffuse_color=(random.random(),random.random(),random.random()) 
                m.specular_intensity = 0 
                m.use_shadeless = True 
                materiales.append(m) 
            return materiales 
        # libreria de materiales: 
        materialesID = fabricaMaterialsID(NM) 
        #mat_list = getMateriales() 
        # para todos los objetos validos de la ecena: 
        for ob in bpy.data.scenes[scn.name].objects: 
            if ob.type == 'MESH' or ob.type == 'SURFACE' or ob.type == 'META': 
                scn.objects.active = ob # lo hacemos objeto activo                     
                # al primer slot le asignamos un material id de mi libreria 
                for mat in ob.material_slots: 
                    #mat=materialesID[random.randrange(0,NM-1)] <-- get me this error: empty range for randrange() (0,0, 0)
                    mat=materialesID[random.randint(0,NM-1)] 
                    mat.use_fake_user = True # linkear     
        # borrar materiales que tienen el prefijo 0: 
        for m in bpy.data.materials: 
            if m.users == 0: 
                bpy.data.materials.remove(m) 
        # indico el motor de render a usar: 
        scn.render.engine = 'BLENDER_RENDER'
