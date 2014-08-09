import bpy
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

alto = 20 # numero de ladrillos en vertical
ancho = 15 # numero de ladrillos en horizontal
en_cm = False # si lo quiero en metros o en centimetros los ladrillos
fill_esquinas=True

# Parece que un muro a escala real en cm las fisicas de blender es mas inestable el muro
# si luego lo queremos escalar podemos ir a la pestaña de Physics en el toolbar y le hacemos Bake To Keyframes
# creamos un empty y eparentamos los ladrillos al empty y escalamos el empty y listo! :)

# Ladrillo estandar en centimetros:            
# 24cm 11.5cm 6cm:
# no se por que me los esta multiplicando por 2 asi que /2
lancho=24 # x el numero mas alto
lalto=11.5 # z
llargo=6 # y <-- profundidad

def creandoLadrillo(nombre):
    bpy.ops.mesh.primitive_cube_add(radius=1, view_align=False, enter_editmode=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    bpy.context.object.name = nombre
        
if en_cm:
    # conversion a cm:
    # no se por que me los esta multiplicando por 2 asi que /2
    bpy.context.scene.unit_settings.system = 'METRIC'
    cm_lancho=lancho/2/100
    cm_lalto=lalto/2/100
    cm_llargo=llargo/2/100
else:
    bpy.context.scene.unit_settings.system = 'METRIC'
    cm_lancho=lancho/2
    cm_lalto=lalto/2
    cm_llargo=llargo/2

# offset de nacimiento vertical
# lo pongo en su sitio con el suelo Z:
nv_offset = cm_llargo
nh_offset = 0
# individual offsets (donde iria el cemento):
h_offset=cm_lancho*2 # los offset me esta dando la mitad del ladrillo por eso tengo q multipliarlos por 2
v_offset=cm_llargo*2 # los offset me esta dando la mitad del ladrillo por eso tengo q multipliarlos por 2

for v in range(alto):
    y=v
    for h in range(ancho):
        x=h
        creandoLadrillo("ladrillo")
        ob = bpy.context.object
        ob.scale.x = cm_lancho
        ob.scale.y = cm_lalto
        ob.scale.z = cm_llargo
        if y%2 == 0:
            #anterior = bpy.context.selected_objects[0].name
            anterior=ob.name

            if fill_esquinas:
                if h == 0:
                    bpy.ops.object.select_all(action='DESELECT')
                    creandoLadrillo("ladrillo_bordes")
                    actual = bpy.context.selected_objects[0].name
                    
                    ob = bpy.data.objects[str(actual)]
                    ob.select = True            
                    ob = bpy.context.object
                    ob.scale.x = cm_lancho/2
                    ob.scale.y = cm_lalto
                    ob.scale.z = cm_llargo
                    ob.location.x -= x*h_offset+nh_offset+cm_lancho/2
                    ob.location.z = y*v_offset+nv_offset
                    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
                    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
                if (h == ancho-1):
                    bpy.ops.object.select_all(action='DESELECT')
                    creandoLadrillo("ladrillo_bordes")
                    actual = bpy.context.selected_objects[0].name

                    ob = bpy.data.objects[str(actual)]
                    ob.select = True            
                    ob = bpy.context.object
                    ob.scale.x = cm_lancho/2
                    ob.scale.y = cm_lalto
                    ob.scale.z = cm_llargo
                    ob.location.x += x*h_offset+nh_offset+cm_lancho+cm_lancho/2
                    ob.location.z = y*v_offset+nv_offset+v_offset
                    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
                    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
            bpy.ops.object.select_all(action='DESELECT')
            ob = bpy.data.objects[str(anterior)]
            ob.select = True            
            ob.location.x += x*h_offset+nh_offset+cm_lancho
            ob.location.z = y*v_offset+nv_offset
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
        else:     
            ob.location.x = x*h_offset+nh_offset
            ob.location.z = y*v_offset+nv_offset
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
