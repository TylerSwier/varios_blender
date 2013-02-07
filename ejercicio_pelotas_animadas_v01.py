import bpy
import random

first_pos = [0,0,0]

for i in range(6):
    # creamos la esfera:
    bpy.ops.mesh.primitive_uv_sphere_add(segments=20, size=0.15, location=first_pos)
    bpy.ops.object.shade_smooth()
    
    ob = bpy.context.active_object
    scn = bpy.context.scene
    de_diez_en_diez = 0 #<- iterador de diez en diez
    
    if i == 0: #<- para la primera posicion
        scn.frame_set(de_diez_en_diez+1) #<- indicamos el frame
        ob.location = first_pos #<- lo movemos a su posicion
        ob.keyframe_insert(data_path="location", index=-1) #<- insertamos keyframe
    else: #<- si no es primera posicion:
        scn.frame_set(de_diez_en_diez+1) #<- indicamos el frame
        ob.location.x = i #<- lo movemos a su posicion
        ob.keyframe_insert(data_path="location", index=-1) #<- insertamos keyframe
    
    for p in range(25): #<- de diez en diez 25 veces son 250
        scn.frame_set(de_diez_en_diez) #<- indicamos el frame
        if p != 0: #<- para la primera posicion no hacemos nada, para el resto:
            ob.location.y = ob.location.y + 0.5 #<- lo movemos a su posicion
            ob.location.z = random.random() #<- lo movemos a su posicion
            ob.keyframe_insert(data_path="location", index=-1) #<- insertamos keyframe
        de_diez_en_diez = de_diez_en_diez+10 #<- iteramos de diez en diez
        
bpy.ops.screen.frame_jump() #<- rebobinamos hasta el frame 1
