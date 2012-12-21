import bpy

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
                        if ms.material.use_fake_user != True:
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

respeto = ""
#respeto = "respetando"
rm_material_by_name("verde",respeto)
