import bpy
bpy.app.debug = True

def createMeshes(name, vertex=[], edges=[], faces=[]):
    # Create mesh and object
    me = bpy.data.meshes.new(name+'_Mesh')
    ob = bpy.data.objects.new(name, me)
    ob.show_name = True
    ob.data.show_extra_indices = True
    me.from_pydata(vertex, edges, faces)
    # Update mesh with new data
    me.update()    
    # Link object to scene
    bpy.context.scene.objects.link(ob)
    return ob

# las coordenadas de cada vertice:  
vertices = [[-1,0,0],[-1,1,0],[0,1,-1],[0,0,0]]
# de que vertice a que vertice hace el edge:
aristas = [[0,1],[1,2],[2,3],[3,4]] # el id de cara vertice
caras = [[0,1,2,3]] # el id de los vertices para esa cara
# para hacer caras no hay que especificar tambien las aristas:
ob = createMeshes('test', vertices, [], caras)
#print(ob.name)
