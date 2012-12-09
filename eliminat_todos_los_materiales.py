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

import bpy
scn = bpy.context.scene 
bpy.ops.object.select_all(action='DESELECT')
for ob in bpy.data.scenes[scn.name].objects: 
    if ob.type == 'MESH' or ob.type == 'SURFACE' or ob.type == 'META': 
        if len(bpy.context.selected_objects) == 0:
            scn.objects.active = bpy.data.objects[str(ob.name)]
            myobject = bpy.data.objects[str(ob.name)]
            myobject.select = True
#            scn.objects.active = ob
#            ob.select = True
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
