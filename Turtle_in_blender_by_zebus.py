import bpy, math, mathutils

'''
Turtle for blender 2.77 v0.5
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

posiciones = []
bpy.app.debug = True

class Turtle(object):
    def __init__(self, startpos, startdir):
        self.currentPosition = mathutils.Vector(startpos) # vector de posicion (donde esta)
        self.direction = mathutils.Vector(startdir)
    def rotTurtleFromX(self, angle):
        A = math.radians(angle)
        self.direction.x = A
        eulrot = mathutils.Euler((self.direction.x, self.direction.y, self.direction.z), 'XYZ')
        self.direction.rotate(eulrot)
    def rotTurtleFromY(self, angle):
        A = math.radians(angle)
        self.direction.y = A
        eulrot = mathutils.Euler((self.direction.x, self.direction.y, self.direction.z), 'XYZ')
        self.direction.rotate(eulrot)
    def rotTurtleFromZ(self, angle):
        A = math.radians(angle)
        self.direction.z = A
        eulrot = mathutils.Euler((self.direction.x, self.direction.y, self.direction.z), 'XYZ')
        self.direction.rotate(eulrot)
    def putEgg(self):
        print("Poniendo un huevo en: " + str(self.currentPosition))
        print("Con una rotacion de: " + str(self.direction))
        # el tipo de huevo:
        bpy.ops.mesh.primitive_cube_add(location=(self.currentPosition), rotation=(self.direction), radius=0.2)
        #posiciones.append([self.currentPosition.x,self.currentPosition.y, self.currentPosition.z])
    def walk(self, whenput=False, steps=0.51):
        if whenput:
            self.putEgg()
        self.currentPosition.x += steps * self.direction.x
        self.currentPosition.y += steps * self.direction.y
        self.currentPosition.z += steps * self.direction.z
        if not whenput:
            self.putEgg()

# Funcion que muestra posicion y direction a la que apunta la tortuga
def whereAreTheTurtle(obj):
    print ("Turtle Location: " + str(obj.currentPosition))
    print ("Pointing Direction: " + str(obj.direction))

# fin de la tortuga


# Para probar como funciona puedes descomentar esto:
# def hide(ob):
#     ob.hide = True
#
# def unhide(ob):
#     ob.hide = False
#
# def selectAll():
#     bpy.ops.object.select_all(action='SELECT')
#
# def deselectAll():
#     bpy.ops.object.select_all(action='DESELECT')
#
# def exitEditMode():
#     if bpy.context.mode != 'OBJECT':
#         bpy.ops.object.mode_set(mode='OBJECT')
#
# def activeObjectLayerOnlyThisNumber(layer):
#     for l in range(len(bpy.context.scene.layers)):
#         if l ==  layer:
#             bpy.context.scene.layers[1] = True
#         else:
#             bpy.context.scene.layers[1] = False
#
# def removeAllObjectsInScene():
#     # blender 2.75a have 20 layers
#     for i in range(20):
#         activeObjectLayerOnlyThisNumber(i)
#         exitEditMode()
#         deselectAll()
#         for ob in bpy.data.objects:
#             unhide(ob)
#         selectAll()
#         bpy.ops.object.delete(use_global=False)
#     # return to 0 initial layer standar in blender:
#     activeObjectLayerOnlyThisNumber(0)
#
# removeAllObjectsInScene()
# startpos = [0,0,0]
# startdir = [0,math.radians(90),0]
# tortuga = Turtle(startpos, startdir)
# tortuga.walk()
# tortuga.walk()
# tortuga.rotTurtleFromZ(90)
# tortuga.rotTurtleFromX(90)
# tortuga.walk()
