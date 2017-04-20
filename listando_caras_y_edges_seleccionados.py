import bpy
import bmesh

me = bpy.context.object.data

bm = bmesh.from_edit_mesh(me)

for elem in bm.select_history:
    print(repr(elem))

# Variant 1 - get the active edge
try:
    active_edge = filter(lambda elem: isinstance(elem, bmesh.types.BMEdge), 
        reversed(bm.select_history)).__next__()
except StopIteration:
    active_edge = None


# Variant 2 - same, but less geeky ;)

for elem in reversed(bm.select_history):
    if isinstance(elem, bmesh.types.BMEdge):
        active_edge = elem
        break
else:
    active_edge = None


# Get selected faces in order

for elem in bm.select_history:
    if isinstance(elem, bmesh.types.BMFace):
        print(repr(elem))


# Get all selected faces
# Note: bm.select_history lacks geometry selected via border select, lasso, etc.
#       (mass-selection operators)!

for face in bm.faces:
    if face.select:
        print(repr(face))
