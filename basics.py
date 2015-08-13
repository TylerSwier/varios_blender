import bpy
import bmesh

# version v00 tested in blender 2.75a
# for import this library in blender put this file in:
# blender-version/version/scripts/modules/zblibs
# from zblibs.basics import *

'''
Copyright (c) 2012 Jorge Hernandez - Melendez
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

bpy.app.debug = True

def obIsFirstObjectSelected():
    ob = bpy.context.selected_objects[0]
    return ob

def deselectAll():
    bpy.ops.object.select_all(action='DESELECT')

def selectAll():
    bpy.ops.object.select_all(action='SELECT')

def enterEditMode():
    if bpy.context.mode == "OBJECT":
        bpy.ops.object.mode_set(mode='EDIT')

def exitEditMode():
    if bpy.context.mode == "EDIT" or bpy.context.mode == "EDIT_CURVE" or bpy.context.mode == "EDIT_MESH":
        bpy.ops.object.mode_set(mode='OBJECT')

def deselectAllInEditMode(ob):
    if ob.mode != 'EDIT':
        enterEditMode()
    bpy.ops.mesh.select_all(action='DESELECT')

def selectAllInEditMode(ob):
    if ob.mode != 'EDIT':
        enterEditMode()
    deselectAllInEditMode(ob)
    bpy.ops.mesh.select_all(action='SELECT')

def whathVertexIsSelected(ob):
    current_mode = ob.mode
    if ob.mode != 'EDIT':
        enterEditMode()
    mesh = bmesh.from_edit_mesh(ob.data)
    for v in mesh.verts:
        if v.select:
            print("The vertex " + str(v.index) + " are selected.")
    # restore mode:
    bpy.ops.object.mode_set(mode=current_mode)

def hide(ob):
    ob.hide = True

def unhide(ob):
    ob.hide = False

def activeObjectLayerOnlyThisNumber(number):
    current_layer = bpy.context.scene.active_layer
    for scn in bpy.data.scenes:
        layers = scn.layers
        # first disable all layer
        for i in range(len(layers)):
            layers[i] = False
        # after active layer
        for i in range(len(layers)):
            if i == number:       
                layers[i] = True
        # disable first current layer:
        layers[current_layer] = False

# remove all objects in the current scene:
def removeAllObjectsInScene():
    # blender 2.75a have 20 layers
    for i in range(20):
        activeObjectLayerOnlyThisNumber(i)
        exitEditMode()
        deselectAll()
        for ob in bpy.data.objects:
            unhide(ob)
        selectAll()
        bpy.ops.object.delete(use_global=False)
    # return to 0 initial layer standar in blender:
    activeObjectLayerOnlyThisNumber(0)
