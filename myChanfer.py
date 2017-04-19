import bpy

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

bl_info = {
    "name": "Modeling for Games",
    "description": "Similar to 3dmax WorkFlow: LowPoly -> chanfer + turbosmooth = HightPoly",
    "author": "Jorge Hernandez - Melenedez",
    "version": (0, 1),
    "blender": (2, 78),
    "location": "Left Toolbar > Tools"
}

bpy.types.Scene.my_prop_1 = bpy.props.BoolProperty()
#bpy.types.Scene.my_prop_1 = bpy.context.selected_objects[0].data.use_auto_smooth

class game_modeling(bpy.types.Panel):
    bl_category = "Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "mesh_edit"
    bl_label = "Game WorkFlow"
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.label(text="Set / Unset bevels:")
        #
        col.operator("add.bevel", text="Add Bevel")
        #
        row = col.row(align=True)
        row.operator("set.bevel", text="Set")
        row.operator("unset.bevel", text="Unset")
        #
        col.operator("add.smooth", text="Add Smooth")
        #
        col.label(text="Similar to EdgeSplit:")
        mesh = bpy.data.meshes[bpy.context.active_object.name]
        sub1 = col.column()
        sub1.prop(mesh, "use_auto_smooth")
        sub1.active = mesh.use_auto_smooth and not mesh.has_custom_normals
        sub1.prop(mesh, "auto_smooth_angle", text="Angle")


class addBevel(bpy.types.Operator):
    bl_idname = "add.bevel"
    bl_label = "Add Bevel"
    bl_description = "Add Bevel Modifier if not have"
    def execute(self, context):
        ob = bpy.context.active_object
        if "Bevel" not in ob.modifiers:
            bpy.ops.object.modifier_add(type='BEVEL')
            ob.modifiers["Bevel"].limit_method = 'WEIGHT'
        return {'FINISHED'}

class addSmooth(bpy.types.Operator):
    bl_idname = "add.smooth"
    bl_label = "Add Smooth"
    bl_description = "Add Smooth Modifier if not have"
    def execute(self, context):
        ob = bpy.context.active_object
        if "Subsurf" not in ob.modifiers:
            bpy.ops.object.modifier_add(type='SUBSURF')
            ob.modifiers["Subsurf"].levels = 2
            ob.modifiers["Subsurf"].show_only_control_edges = True
        return {'FINISHED'}
    



class setBevel(bpy.types.Operator):
    bl_idname = "set.bevel"
    bl_label = "Set"
    bl_description = "Set to vertex/edges/faces one weight bevel"
    def execute(self, context):
        bpy.ops.transform.edge_bevelweight(value=1)
        return {'FINISHED'}

class UnsetBevel(bpy.types.Operator):
    bl_idname = "unset.bevel"
    bl_label = "UnSet"
    bl_description = "UnSet weight bevel"
    def execute(self, context):
        bpy.ops.transform.edge_bevelweight(value=-1)
        return {'FINISHED'}
        

# Registration
def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

# This allows you to run the script directly from blenders text editor
# to test the addon without having to install it.
if __name__ == "__main__":
    register()
