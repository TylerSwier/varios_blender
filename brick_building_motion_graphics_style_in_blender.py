import bpy

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

def creandoLadrillo(nombre, sizex, sizey, sizez):
    bpy.ops.mesh.primitive_cube_add(radius=1, view_align=False, enter_editmode=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    ob = bpy.context.object
    ob.name = nombre
    ob.scale.x = sizex
    ob.scale.y = sizey
    ob.scale.z = sizez

def mover(nombre, x, y, z):
    ob = bpy.data.objects[str(nombre)]
    ob.location.x = x
    ob.location.z = y
    ob.location.y = z
    
def eliminarTodo():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
def escalar(nombre, x, y, z):
    ob = bpy.data.objects[str(nombre)]
    ob.scale.x = x
    ob.scale.y = y
    ob.scale.z = z

def insertarKeyframe(rot,trans,scale):
    if rot == "rotacion":
        ob.keyframe_insert(data_path="rotation_euler", index=-1)
    if trans == "translacion":
        ob.keyframe_insert(data_path="location", index=-1)
    if scale == "escala":
        ob.keyframe_insert(data_path="scale", index=-1)

def pivote(nombre):
    ob = bpy.data.objects[str(nombre)]
    bpy.context.scene.cursor_location  = [0, ob.scale.y, -ob.scale.z]
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

scn = bpy.context.scene

alto = 0.2
ancho = 1
largo = 1

start_frame = 0
end_frame = 10

cuantos_bricks = 5
de_cuanto_en_cuanto = 5
de_diez_en_diez = 0

eliminarTodo()

for i in range(cuantos_bricks):
    creandoLadrillo("ladrillo", ancho, alto, largo)        
    ob = bpy.context.selected_objects[0]
    pivote(ob.name)
    bpy.ops.object.modifier_add(type='BEVEL')
    bpy.context.object.modifiers["Bevel"].segments = 3
    bpy.context.object.modifiers["Bevel"].width = 0.07

    mover(ob.name, 0, 0, i*largo*2)

    escala_original = ob.scale 

    # un frame anterior lo escalo todo a 0 para que no se vea:
    scn.frame_set(de_diez_en_diez)
    escalar(ob.name, 0 ,0 , 0)
    insertarKeyframe("rotacion","translacion","escala")
    
    # ahora si lo escalo a la escala inicial
    scn.frame_set(de_diez_en_diez+1)
    escalar(ob.name, ancho , alto , 0)
    insertarKeyframe("rotacion","translacion","escala")

    de_diez_en_diez += de_cuanto_en_cuanto
    
    # y finalmente lo escalo a su escala real
    scn.frame_set(de_diez_en_diez+1)
    escalar(ob.name, ancho, alto, largo)
    # rotacion:
    #bpy.context.object.rotation_euler[0] = 1.5708
    bpy.ops.transform.rotate(value=-1.5708, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
    insertarKeyframe("rotacion","translacion","escala")
