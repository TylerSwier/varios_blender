import bpy
bpy.app.debug = True

def createMeshes(name, vertex=[], edges=[], faces=[]):
    # Create mesh and object
    me = bpy.data.meshes.new(name+'_Mesh')
    ob = bpy.data.objects.new(name, me)
    ob.show_name = True
    ob.data.show_extra_indices = True
    # from_pydata( vertices aristas y caras)
    me.from_pydata(vertex, edges, faces)
    # Update mesh with new data
    me.update()    
    # Link object to scene
    bpy.context.scene.objects.link(ob)
    return ob

# las coordenadas de cada vertice:
vertices = [[0,0,0],[1,1,1],[2,2,2]]
# de que vertice a que vertice hace el edge:
aristas = [[0,1],[1,2]] # el id de cara vertice
ob = createMeshes('test', vertices, aristas )
#print(ob.name)
