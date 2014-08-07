import bpy
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

bpy.context.scene.unit_settings.system = 'METRIC'

for cl in range(5):
    bpy.ops.mesh.primitive_cube_add(radius=1, view_align=False, enter_editmode=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    bpy.context.object.name = "ladrillo"
    bpy.ops.object.select_all(action='DESELECT')

objetos = bpy.data.objects[:]

def fabricarLadrillosHorizontal():
    for i in range(len(objetos)):
        if "ladrillo" in objetos[i].name:
            bpy.ops.object.select_all(action='DESELECT')
            ob = bpy.data.objects[str(objetos[i].name)]
            ob.select = True

            # Ladrillo estandar en centimetros:
            
            # poniendo la escala correspondiente a los centimetro...
            # ob.dimensions.x = sx
            # 40cm 6cm 11.5cm:
            # son las cifras de arriba pero con: /2
            
            ob.scale.xyz = ((0.2,0.03,0.0575))

            # lo pongo en su sitio con el suelo Z:
            ob.location.z = 0.0575
            
            medio = ob.dimensions.x/2
            ox = i/2.5+medio+ob.dimensions.x
            ob.location.x += ox
            
fabricarLadrillosHorizontal()
