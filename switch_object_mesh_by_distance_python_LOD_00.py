import bpy
from math import sqrt # para calcular la distancia


cuboMotion = bpy.data.objects['Cube']
cubo2 = bpy.data.objects['Cube.001']
forma = bpy.data.objects['forma']

objetos = [cuboMotion, cubo2]

cubo2.data = cuboMotion.data


def get_distance():
    l = []  # we store the loacation vector of each object
    for item in objetos:
        l.append(item.location)
    distance = sqrt( (l[0][0] - l[1][0])**2 + (l[0][1] - l[1][1])**2 + (l[0][2] - l[1][2])**2)
    print(distance)  # print distance to console, DEBUG
    return distance



# main loop:
scene = bpy.context.scene
def my_handler(scene):
    
    print("Frame Change", scene.frame_current)
    dist = get_distance()
    if ( dist > 5 ):
        cubo2.data = forma.data
        print("se cambio la forma")
    
    
if not my_handler.__name__ in [funcion.__name__ for funcion in bpy.app.handlers.frame_change_pre]:
    print("no esta")
    bpy.app.handlers.frame_change_pre.append(my_handler)
