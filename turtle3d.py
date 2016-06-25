import bpy, math

'''
Agradecimientos en especial a Carlos, Sin el este desarrollo hubiera sido
mas costoso o incluso imposible... Y tambien agradecimientos a Antonio, el
creador de la primera implementacion de la tortuga para blender. Antonio me dio
a conocer el maravilloso (y complejo) mundo de la tortuga 3D de logo.

LICENSE GPL2:

Copyright (c) 2016 Jorge Hernandez - Melendez

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

For the complete terms of the GNU General Public License, please see this URL:
http://www.gnu.org/licenses/gpl-2.0.html
'''

class Vector3D(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Turtle3D(object):
    def __init__(self, initloc, initdir):
        self.position = Vector3D(initloc[0], initloc[1], initloc[2])
        self.direction = Vector3D(initdir[0], initdir[1], initdir[2])
    def rotateX(self, angle=90): # si no se especifica un angulo por defecto seran 90 grados <-(puramente vagueria)
        # convirtiendo grados a radianes ( lo mismo que math.radians(angle) ):
        angle = angle / 180 * math.pi
        # precalculamos cos y sin ya que se utilizaran varias veces:
        cos, sin = math.cos(angle), math.sin(angle) # <-- esta en una sola linea pero se puede en 2 tambien
        # formula de rotacion de matrices en el eje X:
        newy = self.direction.y * cos - self.direction.z * sin
        newz = self.direction.y * sin + self.direction.z * cos
        # actualizamos la nueva direccion a donde apunta la cabeza de la tortuga:
        self.direction.y = newy
        self.direction.z = newz
    def rotateY(self, angle=90): # si no se especifica un angulo por defecto seran 90 grados <-(puramente vagueria)
        # convirtiendo grados a radianes ( lo mismo que math.radians(angle) ):
        angle = angle / 180 * math.pi
        # precalculamos cos y sin ya que se utilizaran varias veces:
        cos, sin = math.cos(angle), math.sin(angle) # <-- esta en una sola linea pero se puede en 2 tambien
        # formula de rotacion de matrices en el eje Y:
        newx = self.direction.x * cos + self.direction.z * sin
        newz = self.direction.z * cos - self.direction.x * sin
        # actualizamos la nueva direccion a donde apunta la cabeza de la tortuga:
        self.direction.x = newx
        self.direction.z = newz
    # si quisieramos hacer la tortuga en 2D solo tendriamos que omitir el eje z de los vectore
    # y utilizar la formula de rotacion de matrices del eje Z:
    def rotateZ(self, angle=90): # si no se especifica un angulo por defecto seran 90 grados <-(puramente vagueria)
        # convirtiendo grados a radianes ( lo mismo que math.radians(angle) ):
        angle = angle / 180 * math.pi
        # precalculamos cos y sin ya que se utilizaran varias veces:
        cos, sin = math.cos(angle), math.sin(angle) # <-- esta en una sola linea pero se puede en 2 tambien
        # formula de rotacion de matrices en el eje Z:
        newx = self.direction.x * cos - self.direction.y * sin
        newy = self.direction.x * sin + self.direction.y * cos
        # actualizamos la nueva direccion a donde apunta la cabeza de la tortuga:
        self.direction.x = newx
        self.direction.y = newy
    # para que se mas facil usar la tortuga aqui creamos una serie de
    # atajos, de este modo no tenemos que tener tan presente en  que eje roramos:
    def turnLeft(self):
        self.rotateZ(90)
    def turnRight(self):
        self.rotateZ(-90)
    def turnUp(self):
        self.rotateX(90)
    def turnDown(self):
        self.rotateX(-90)
    # caminar en la direccion en la que este mirando la tortuga:
    def walk(self, strength=1):
        self.position.x += strength * self.direction.x
        self.position.y += strength * self.direction.y
        self.position.z += strength * self.direction.z
    # caminar en la direccion en la que este mirando la tortuga y poniendo huevos primero
    # en x numero de pasos:
    def walkStep(self, strength=1, steps=10):
        for i in range(steps):
            self.putEgg()
            self.position.x += strength * self.direction.x
            self.position.y += strength * self.direction.y
            self.position.z += strength * self.direction.z
    # aqui la tortua pone los huevos:
    def putEgg(self):
        print("Poniendo huevo en:")
        print("Location: " + str(self.position.x) + str(self.position.y) + str(self.position.z))
        print("Direction: " + str(self.direction.x) + str(self.direction.y) + str(self.direction.z))
        bpy.ops.mesh.primitive_cube_add(location=(self.position.x,self.position.y, self.position.z), rotation=(self.direction.x, self.direction.y, self.direction.z), radius=0.2)
        posiciones.append([self.position.x, self.position.y, self.position.z])
        return posiciones

# fin de la tortuga

###############################
### PARA PROBAR LA TORTUGA: ###
###############################
###################################################################################
# Con todo esto lo unico que hago es probar que funciona correctamente la tortuga:
# si estas en otro script tendras que importar la tortuga primero:
# for import this library in blender put this file in:
# /path/to/your/blender-version/version/scripts/modules/turtle
# from turtle.turtle3d import *
###################################################################################
###################################################################################
def hide(ob):
    ob.hide = True

def unhide(ob):
    ob.hide = False

def selectAll():
    bpy.ops.object.select_all(action='SELECT')

def deselectAll():
    bpy.ops.object.select_all(action='DESELECT')

def exitEditMode():
    if bpy.context.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

def activeObjectLayerOnlyThisNumber(layer):
    for l in range(len(bpy.context.scene.layers)):
        if l ==  layer:
            bpy.context.scene.layers[1] = True
        else:
            bpy.context.scene.layers[1] = False

# Las funciones anteriores son dependencias de la funcion removeAllObjectsInScene.
# Con esta funcion elimino todos los objetos de la escena:
def removeAllObjectsInScene():
    # blender 2.75a have 20 layers
    for i in range(20):
        activeObjectLayerOnlyThisNumber(i)
        exitEditMode()
        deselectAll()
        for ob in bpy.data.objects:
            unhide(ob)
        selectAll()
        bpy.ops.object.delete(use_global=False)
    # return to 0 initial layer standar in blender:
    activeObjectLayerOnlyThisNumber(0)

removeAllObjectsInScene()

def createMeshes(name, vertex=[], edges=[], faces=[]):
    profile_mesh = bpy.data.meshes.new(name+'_Mesh')
    ob = bpy.data.objects.new(name, profile_mesh)
    ob.show_name = True
    ob.data.show_extra_indices = True
    profile_mesh.from_pydata(vertex, edges, faces)
    # Update mesh with new data
    profile_mesh.update()
    profile_object = bpy.data.objects.new(name, profile_mesh)
    profile_object.data = profile_mesh
    scene = bpy.context.scene
    scene.objects.link(profile_object)
    # Link object to scene
    # bpy.context.scene.objects.link(ob)
    return ob

# probando que la tortuga funciona perfectamente.
# mi tortuga empieza con la cabeza apuntando a Y
posiciones = [] # <--- en este array voy guardando las coordenadas de cada huevo
# pongo activo el modo debug para ver el id de los vertex
bpy.app.debug = True
#########################################################
initloc = [0,0,0]
direct = math.radians(90)
initdir = [0,direct,0]
tortuga = Turtle3D(initloc,initdir)
posiciones = tortuga.putEgg()
tortuga.walk(0.5)
posiciones = tortuga.putEgg()
tortuga.turnUp()
tortuga.walk(0.5)
posiciones = tortuga.putEgg()
tortuga.turnDown()
tortuga.walk(0.5)
posiciones = tortuga.putEgg()
tortuga.turnLeft()
tortuga.walk(0.5)
posiciones = tortuga.putEgg()
tortuga.turnRight()
tortuga.walk(0.5)
posiciones = tortuga.putEgg()
tortuga.walk(0.5)
posiciones = tortuga.putEgg()
#######################
# creando la geometria:
#######################
### las coordenadas de cada vertice:
### vertices = [[-1,0,0],[-1,1,0],[0,1,-1],[0,0,0]]
vertices = posiciones
### de que vertice a que vertice hace el edge:
### aristas = [[0,1],[1,2],[2,3],[3,0]] # el id de cada vertice para ese edge
aristas = []
def getEdges(como='open'):
    if (como == 'open'):
        for i in range(len(vertices)-1):
            aristas.append([i,i+1])
    # no consigo que no pete al hacerlos closed:
    # elif (como == 'close'):
    #     for i in range(len(vertices)):
    #         if (i < len(vertices)):
    #             aristas.append([i,i+1])
    #         else:
    #             aristas.append([len(vertices),0])

getEdges()
obName = 'objeto'
# si hacemos caras no le pasamos aristas y si hacemos aristas no le pasamos caras:
ob = createMeshes(obName, vertices, aristas, [])
deselectAll()
