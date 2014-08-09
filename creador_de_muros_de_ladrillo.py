import bpy
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
bpy.context.scene.unit_settings.system = 'METRIC'

alto = 10
ancho = 8

# Ladrillo estandar en centimetros:            
# 40cm 6cm 11.5cm:
lancho=40
lato=6
llargo=11.5
# conversion a cm:
cm_lancho=lancho/2
cm_lalto=lato/2
cm_llargo=llargo/2

# offset de nacimiento vertical
# lo pongo en su sitio con el suelo Z:
nv_offset = cm_llargo
nh_offset = 0
# individual offsets (donde iria el cemento):
h_offset=lancho
v_offset=llargo

for v in range(alto):
    y=v
    for h in range(ancho):
        x=h
        bpy.ops.mesh.primitive_cube_add(radius=1, view_align=False, enter_editmode=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        bpy.context.object.name = "ladrillo"
        ob = bpy.context.object
        ob.scale.x = cm_lancho
        ob.scale.y = cm_lalto
        ob.scale.z = cm_llargo
        
        if y%2 == 0:
            ob.location.x += x*h_offset+nh_offset+cm_lancho
            ob.location.z = y*v_offset+nv_offset
        else:     
            ob.location.x = x*h_offset+nh_offset 
            ob.location.z = y*v_offset+nv_offset
