import bpy
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
bpy.context.scene.unit_settings.system = 'METRIC'

alto = 10
ancho = 8
def fabricarLadrillosHorizontal():
    # offset de nacimiento
    n_offset=0
    # individual offsets:
    h_offset=0.40
    v_offset=0.115
    for v in range(alto):
        y=v
        for h in range(ancho):
            x=h
            bpy.ops.mesh.primitive_cube_add(radius=1, view_align=False, enter_editmode=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
            bpy.context.object.name = "ladrillo"
            ob = bpy.context.object
            # Ladrillo estandar en centimetros:            
            # poniendo la escala correspondiente a los centimetro...
            # ob.dimensions.x = sx
            # 40cm 6cm 11.5cm:
            # son las cifras de arriba pero con: /2
            ob.scale.x = 0.2
            ob.scale.y = 0.03
            ob.scale.z = 0.0575
            # lo pongo en su sitio con el suelo Z:
            ob.location.z = 0.0575
            if y%2 == 0:
                ob.location.x += x*h_offset+n_offset+0.20
                ob.location.z = y*v_offset+n_offset
            else:     
                ob.location.x = x*h_offset+n_offset 
                ob.location.z = y*v_offset+n_offset
            
fabricarLadrillosHorizontal()
