import math
import bpy

posiciones = []
# pongo activo el modo debug para ver el id de los vertex
bpy.app.debug = True

def deselectAll():
    bpy.ops.object.select_all(action='DESELECT')

def selectByName(name):
    scn = bpy.context.scene
    bpy.data.objects[name].select = True
    scn.objects.active = bpy.data.objects[name]

def createMeshes(name, vertex=[], edges=[], faces=[]):
    # Create mesh and object
    me = bpy.data.meshes.new(name+'_Mesh')
    ob = bpy.data.objects.new(name, me)
    ob.show_name = True
    ob.data.show_extra_indices = True
    me.from_pydata(vertex, edges, faces)
    # Update mesh with new data
    me.update()
    # Link object to scene
    bpy.context.scene.objects.link(ob)
    return ob


#Vector2 representa un vector 2D (en realidad solo es un punto(x,y), por lo que
#se usan 2 vectores, uno representa la posicion de la tortuga y el otro
# la direccion en la que mira)
class Vector2():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # self.step = 0
    # def getDistance(self, other):
    #     # math.sqrt es una raiz cuadrada en python (para el modulo de un vector)
    #     return math.sqrt((self.x - other.x)**2 + (self.y + other.y)**2)


class Turtle():
    def __init__(self, x, y):
        # vector que representa la posicion actual de la tortuga
        self.currentPosition = Vector2(x, y)
        # para darle mas distancia se usa el argumento steps de walk
        # el vector direccion esta normalizado (su modulo siempre es 1)
        self.direction = Vector2(1, 0)
    # funcion de rotacion
    def rotate(self, angle):
        # conversion de grados a radianes, tu le pasas por ejemplo
        # 90 grados, y antes del calculo se convierten a radianes, ya que
        # es el parametro de math.sin y math.cos
        # A = ( angle * math.pi ) / 180.0
        A = math.radians(angle)
        # se precalcula el cos y el sin para no hacerlo varias veces
        cos = math.cos(A)
        sin = math.sin(A)
        # esta formula proviene de la matriz de rotacion (para 2D)
        newx = self.direction.x * cos - self.direction.y * sin
        newy = self.direction.x * sin + self.direction.y * cos
        # se le asigna a la direccion el nuevo vector rotado
        self.direction.x = newx
        self.direction.y = newy
    # rotacion 90 izq
    def turnLeft(self):
        self.rotate(-90)
    # rotacion 90 dch
    def turnRight(self):
        self.rotate(90)
    # avanzar, simplemente se suma cada coordenada de la posicion a la
    # direccion que mira. recibe un parametro opcional que es la cantidad de pasos
    # por def. 1
    def walk(self, step=1):
        self.currentPosition.x += step * self.direction.x
        self.currentPosition.y += step * self.direction.y
    # pone un "huevo"
    def putEgg(self):
        print("Poniendo un huevo")
        #bpy.ops.mesh.primitive_cube_add(location=(self.currentPosition.x,self.currentPosition.y, 0), rotation=(0, 0, 0), radius=0.2)
        posiciones.append([self.currentPosition.x,self.currentPosition.y, 0])

    # Funcion que muestra posicion y direccion a la que apunta la tortuga
    def whereAreTheTurtle(obj):
        print ("Turtle Location: " + str(obj.currentPosition.x) + ".X ," + str(obj.currentPosition.y) + ".Y ")
        print ("Pointing Direction: " + str(obj.direction.x) + ".DirX ," + str(obj.direction.y) + ".DirY " )


# Funcion de ejemplo que hace girar en circulo a la tortuga.
# Lo correcto seria un Vec2 sobre el que rotara
def circle(turtle, rotation):
    steps = int(360 / rotation)
    for i in range(steps):
        turtle.walk()
        turtle.putEgg()
        turtle.rotate(rotation)
        print("Entro en pasada " + str(i))

# Funcion que dibuja linea horizontal
def horizontal(turtle, steps):
    turtle.direction.x = 1
    turtle.direction.y = 0
    for i in range(steps):
        turtle.putEgg()
        turtle.walk()

def vertical(turtle, steps):
    turtle.direction.x = 0
    turtle.direction.y = 1
    for i in range(steps):
        turtle.putEgg()
        turtle.walk()

def main():
    tortuga = Turtle(-8, 0)
    # H
    vertical(tortuga, 7)
    tortuga.currentPosition.y = 3
    horizontal(tortuga, 4)
    tortuga.currentPosition.y = 0
    vertical(tortuga, 7)
    # O
    tortuga.currentPosition.x += 5
    tortuga.currentPosition.y = 2
    circle(tortuga, 30)
    # L
    tortuga.currentPosition.x += 2
    tortuga.currentPosition.y = 0
    vertical(tortuga, 7)
    tortuga.currentPosition.y = 0
    horizontal(tortuga, 4)
    # A
    tortuga.currentPosition.x += 1
    tortuga.currentPosition.y = 0
    tortuga.rotate(70)
    for i in range(6):
        tortuga.putEgg()
        tortuga.walk()
    tortuga.rotate(-140)
    for i in range(7):
        tortuga.putEgg()
        tortuga.walk()
    tortuga.currentPosition.x -= 3
    tortuga.currentPosition.y = 2
    horizontal(tortuga, 3)
    #circulo
    tortuga.currentPosition.x = 1
    tortuga.currentPosition.y = -8
    circle(tortuga, 5)
    # las coordenadas de cada vertice:
    # vertices = [[-1,0,0],[-1,1,0],[0,1,-1],[0,0,0]]
    vertices = posiciones
    # de que vertice a que vertice hace el edge:
    # aristas = [[0,1],[1,2],[2,3],[3,0]] # el id de cada vertice para ese edge
    aristas = []
    for i in range(len(vertices)):
        if i != len(vertices):
            aristas.append([i,i+1])
        else:
            aristas.append([len(vertices),0])
    obName = 'objeto'
    ob = createMeshes(obName, vertices, aristas, [])
    deselectAll()
    selectByName(obName)
    bpy.data.objects[obName].modifiers.new('skinModifier',type='SKIN')
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="skinModifier")
    deselectAll()

main()
