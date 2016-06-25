import bpy, math

class Vector3D(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Turtle(object):
    def __init__(self, vectloc, vecrot):
        self.position = Vector3D(vectloc[0],vectloc[1],vectloc[2])
        self.direction = Vector3D(vecrot[0],vecrot[1],vecrot[2])
    def rotate(self, angle):
        angle = math.radians(angle)
        cos = math.cos(angle)
        sin = math.sin(angle)
        newx = self.direction.x*cos - self.direction.y*sin
        newy = self.direction.x*sin + self.direction.y*cos
        self.direction.x = newx
        self.direction.y = newy
    def turnLeft(self):
        self.rotate(-90)
    def turnRight(self):
        self.rotate(90)
    def walk(self, step=1):
        self.position.x += step*self.direction.x
        self.position.y += step*self.direction.y
    def putCube(self):
        print("Poniendo huevo en:")
        print("Location: " + str(self.position.x) + str(self.position.y) + str(self.position.z))
        print("Direction: " + str(self.direction.x) + str(self.direction.y) + str(self.direction.z))
        # para crear la piramide y que salga con los ejes correspondientes:
        bpy.ops.mesh.primitive_cone_add(vertices=4, view_align=False, enter_editmode=False, location=(self.position.x,self.position.y,self.position.z), rotation=(self.direction.x,self.direction.y,self.direction.z), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        #bpy.ops.mesh.primitive_cube_add(location=(self.position.x,self.position.y, 0), rotation=(0, 0, 0), radius=0.2)


############################
# Para probar como funciona
############################
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

# Funcion que dibuja un circulo
def circle(turtle, rotation):
    steps = int(360 / rotation)
    i = 0
    while i < steps:
        turtle.walk()
        turtle.putCube()
        turtle.rotate(rotation)
        i += 1
        # print("Entro en pasada " + str(i))

# Funcion que dibuja linea horizontal
def horizontal(turtle, steps):
    turtle.direction.x = 1
    turtle.direction.y = 0
    for i in range(steps):
        turtle.putCube()
        turtle.walk()

def vertical(turtle, steps):
    turtle.direction.x = 0
    turtle.direction.y = 1
    for i in range(steps):
        turtle.putCube()
        turtle.walk()


vecloc = [-8, 0, 0]
vecrot = [0, 0, math.radians(90)]
removeAllObjectsInScene()
tortuga = Turtle(vecloc, vecrot)
# H
vertical(tortuga, 7)
tortuga.position.y = 3
horizontal(tortuga, 4)
tortuga.position.y = 0
vertical(tortuga, 7)
# O
tortuga.position.x += 5
tortuga.position.y = 2
circle(tortuga, 30)
# L
tortuga.position.x += 2
tortuga.position.y = 0
vertical(tortuga, 7)
tortuga.position.y = 0
horizontal(tortuga, 4)
# A
tortuga.position.x += 1
tortuga.position.y = 0
tortuga.rotate(70)
for i in range(6):
    tortuga.putCube()
    tortuga.walk()

tortuga.rotate(-140)
for i in range(7):
    tortuga.putCube()
    tortuga.walk()

tortuga.position.x -= 3
tortuga.position.y = 2
horizontal(tortuga, 3)
#circulo
tortuga.position.x = 1
tortuga.position.y = -8
circle(tortuga, 5)
