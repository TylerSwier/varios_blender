import bpy
import math
from mathutils import Vector

# la manera mas sencilla que he encontrado de obtener el centroid de una figura irregular:
def getCentroid():
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            ctx = bpy.context.copy()
            ctx['area'] = area
            bpy.ops.view3d.snap_cursor_to_selected(ctx)
            return bpy.context.scene.cursor_location[:]

# para guardar las coordenadas originales de cada objeto:
originalCoords = []

def explodeObjects(centroid):
    centroid = Vector(centroid)    
    for ob in bpy.context.selected_objects:
        # guardo las coordenadas iniciales para luego poder restaurarlas:
        originalCoords.append([ob.name, ob.location.x, ob.location.y, ob.location.z ])
        # calculamos la direccion:
        direccion = ob.location - centroid
        # la normalizamos para que todas las piezas se desplacen lo mismo:
        direccion.normalize()
        # calculo la fuerza en funcion de las dimensiones del objeto:
        fuerza = (ob.dimensions.x + ob.dimensions.y + ob.dimensions.z)
        # trasladamos al objeto:
        ob.location = direccion * fuerza
    return originalCoords

# necesitamos el punto medio de todos los objetos para q sea el punto de partida
# de lo que seria la explosion:
centroid = getCentroid()

# restauramos las coordenadas como estaban:
coords = explodeObjects(centroid)
for i in coords:
    # parseo los datos para que sea mas sencillo:
    nombre = i[0]
    x = i[1]
    y = i[2]
    z = i[3]
    # reseteo a cada objeto a su posicion:
    bpy.data.objects[nombre].location = (x,y,z)
