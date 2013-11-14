import bpy

# selecciono todo y lo borro:
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

diametro = 8
# si el diametro es mayor que la altura 
# en la cima quedara una base muy amplia
x = diametro
y = diametro
# si el diametro es bajo por mas que tegamos 
# mas altura, el maximo de altura sera lo que permita las restas del diametro
altura = 8

def laminas2D(x,y,z):
    for v in range(-x,x): # -x es un -8,-7,-6,etc... y x es 8,7,6,etc...
        for h in range(-y,y):
            # a las posiciones h,v les resto de offset x,y para que se centren sobre si mismas
            bpy.ops.mesh.primitive_cube_add(view_align=False,location=(v*2, h*2, z*2))
        
# para darle la profundidad en z:
for i in range(altura):
    laminas2D(x,y,i)
    x -= 1  # le voy restando para que cada pasada al subir de altura las laminas sean de menor size
    y -= 1  # le voy restando para que cada pasada al subir de altura las laminas sean de menor size
