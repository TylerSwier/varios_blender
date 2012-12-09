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

# After use the eliminat_todos_los_materiales.py you can run this other script:
# Despues de usar eliminat_todos_los_materiales.py puedes usar este script:

import bpy  
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
