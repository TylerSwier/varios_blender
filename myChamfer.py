import bpy
import bmesh

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

bl_WARNING = {
    "name": "Chamfer",
    "description": "Similar to 3dmax WorkFlow: LowPoly -> smoothing groups + chamfer + turbosmooth = HightPoly",
    "author": "Jorge Hernandez - Melenedez",
    "version": (0, 9),
    "blender": (2, 78),
    "category": "User",
    #"location": "Left Toolbar > Tools"
    "location": "Left Toolbar > Chamfer"
}

class game_modeling(bpy.types.Panel):
    B = False
    S = False
    bl_label = "Chamfer"
    bl_category = "Chamfer"
    #bl_category = "Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    #bl_context = "mesh_edit"
    bl_label = "Game WorkFlow"
    def draw(self, context):
        layout = self.layout
        ob = bpy.context.active_object
        col = layout.column(align=True)
        col.label(text="Set / Unset bevels:")
        #
        col.operator("add.bevel", text="Add Bevel")
        #
        row = col.row(align=True)
        row.operator("set.edges", text="Edges")
        row.operator("set.faces", text="Faces")
        row.operator("unset.bevel", text="Unset")
        #
        col.operator("add.smooth", text="Add Subsurf")
        #
        col.label(text="Shading:")
        row = col.row(align=True)
        row.operator("object.shade_smooth", text="Smooth")
        row.operator("object.shade_flat", text="Flat")
        col.operator("grid.toggle", text="Hide/Show Grid")
        #
        col.label(text="Similar to EdgeSplit:")
        # este es mejor que edge split porque no separa los vertices:
        mesh = bpy.data.meshes[bpy.context.active_object.name]
        sub1 = col.column()
        sub1.prop(mesh, "use_auto_smooth")
        sub1.active = mesh.use_auto_smooth and not mesh.has_custom_normals
        sub1.prop(mesh, "auto_smooth_angle", text="Angle")

# este es el elemento que voy a incluir nuevo en mi ui:
def newElementMenu(self, context):
    ob = bpy.context.active_object
    mod = ob.modifiers["Bevel"]
    if self.B == False:
        self.layout.prop(mod, "width", text="Bevel width")
        self.layout.prop(mod, "segments", text="Bevel segments")
        self.layout.prop(mod, "profile", text="Bevel profile")
        self.B = True

def newElementMenuSmooth(self, context):
    ob = bpy.context.active_object
    try:
        mod = ob.modifiers["Subsurf"]
    except KeyError:
        pass
    if self.S == False:
        self.layout.prop(mod, "levels", text="Subsurf levels")
        #self.layout.prop(mod, "render_levels", text="Smooth Render levels")
        self.S = True

class addBevel(bpy.types.Operator):
    bl_idname = "add.bevel"
    bl_label = "Add Bevel"
    bl_description = "Add Bevel Modifier if not have"
    def execute(self, context):
        ob = bpy.context.active_object
        if "Bevel" not in ob.modifiers:
            bpy.ops.object.modifier_add(type='BEVEL')
            ob.modifiers["Bevel"].width = 0.05
            ob.modifiers["Bevel"].segments = 2
            ob.modifiers["Bevel"].profile = 1
            ob.modifiers["Bevel"].limit_method = 'WEIGHT'
            # Si le ponemos un bevel tambien externalizamos el width para mayor comodidad:
            # bpy.types.game_modeling.prepend(newElementMenu)
            bpy.types.game_modeling.append(newElementMenu)
        return {'FINISHED'}

class addSmooth(bpy.types.Operator):
    bl_idname = "add.smooth"
    bl_label = "Add Smooth"
    bl_description = "Add Smooth Modifier if not have"
    def execute(self, context):
        ob = bpy.context.active_object
        if "Bevel" not in ob.modifiers:
            self.report({'WARNING'}, "You need add Bevel first!")
            return {'FINISHED'}
        if "Subsurf" not in ob.modifiers:
            bpy.ops.object.modifier_add(type='SUBSURF')
            ob.modifiers["Subsurf"].levels = 3
            ob.modifiers["Subsurf"].render_levels = 3
            # ob.modifiers["Subsurf"].show_only_control_edges = True
            bpy.types.game_modeling.append(newElementMenuSmooth)
        return {'FINISHED'}

class setBevelE(bpy.types.Operator):
    bl_idname = "set.edges"
    bl_label = "Set to Edges"
    bl_description = "Set to edges weight bevel and sharp"
    def execute(self, context):
        if bpy.context.mode == 'EDIT_MESH':
            ob = bpy.context.active_object
            if "Subsurf" in ob.modifiers:
                # determinar si solo es un edge loop o un edge o si son caras seleccionadas:
                me = bpy.context.object.data
                bm = bmesh.from_edit_mesh(me)
                edges = []
                for edge in bm.edges:
                    if edge.select:
                        edges.append(repr(edge.index))
                if len(edges) < 1 or bpy.context.tool_settings.mesh_select_mode[1] == False: # si son caras (y no son todas las caras del objeto):
                    self.report({'WARNING'}, "This option is only for Edges!")
                    return {'FINISHED'}
                bpy.ops.transform.edge_bevelweight(value=1)
                bpy.ops.mesh.mark_sharp()
                mesh = bpy.data.meshes[ob.name]
                mesh.use_auto_smooth = True
                ob.data.auto_smooth_angle = 180
            else:
                self.report({'WARNING'}, "You need add Subsurf first!")
                return {'FINISHED'}
        else:
            self.report({'WARNING'}, "This option only work in edit mode!")
        return {'FINISHED'}

class setBevelF(bpy.types.Operator):
    bl_idname = "set.faces"
    bl_label = "Set to Faces"
    bl_description = "Set to faces weight bevel and sharp"
    def execute(self, context):
        if bpy.context.mode == 'EDIT_MESH':
            ob = bpy.context.active_object
            if "Subsurf" in ob.modifiers:
                # determinar si solo es un edge loop o un edge o si son caras seleccionadas:
                me = bpy.context.object.data
                bm = bmesh.from_edit_mesh(me)
                faces = []
                for face in bm.faces:
                    if face.select:
                        faces.append(repr(face.index))
                if len(faces) < 1 or bpy.context.tool_settings.mesh_select_mode[2] == False: # si son caras (y no son todas las caras del objeto):
                    self.report({'WARNING'}, "This option is only for Faces!")
                    return {'FINISHED'}
                if len(faces) != len(bm.faces):
                    bpy.ops.mesh.region_to_loop() # si son caras con esto selecciono solo los contornos
                bpy.ops.transform.edge_bevelweight(value=1)
                bpy.ops.mesh.mark_sharp()
                mesh = bpy.data.meshes[ob.name]
                mesh.use_auto_smooth = True
                ob.data.auto_smooth_angle = 180
            else:
                self.report({'WARNING'}, "You need add Subsurf first!")
                return {'FINISHED'}
        else:
            self.report({'WARNING'}, "This option only work in edit mode!")
        return {'FINISHED'}

class UnsetBevel(bpy.types.Operator):
    bl_idname = "unset.bevel"
    bl_label = "UnSet"
    bl_description = "UnSet weight bevel"
    def execute(self, context):
        if bpy.context.mode == 'EDIT_MESH':
            bpy.ops.transform.edge_bevelweight(value=-1)
            bpy.ops.mesh.mark_sharp(clear=True)
        else:
            self.report({'WARNING'}, "This option only work in edit mode!")
        return {'FINISHED'}


class Grid(bpy.types.Operator):
    bl_idname = "grid.toggle"
    bl_label = "grid"
    bl_description = "Show/Hide grid"
    def execute(self, context):
        if bpy.context.space_data.show_floor:
            bpy.context.space_data.show_floor = False
            bpy.context.space_data.show_axis_x = False
            bpy.context.space_data.show_axis_y = False
        else:
            bpy.context.space_data.show_floor = True
            bpy.context.space_data.show_axis_x = True
            bpy.context.space_data.show_axis_y = True
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
