import bpy
scn = bpy.context.scene
inicio = bpy.data.scenes[scn.name].frame_start
final = bpy.data.scenes[scn.name].frame_end

def accion_insert_keyframe(f):
    for o in bpy.data.objects:
        scn.frame_set(f) #<- indicamos el frame
        o.keyframe_insert(data_path="scale", index=-1) #<- insertamos el keyframe
        o.keyframe_insert(data_path="location", index=-1) #<- insertamos el keyframe
        o.keyframe_insert(data_path="rotation_euler", index=-1) #<- insertamos el keyframe
for f in range(inicio, final):
    accion_insert_keyframe(f)
    
bpy.ops.screen.frame_jump() #<- vamos hasta el frame 1
