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

bl_info = {
    "name": "Chamfer",
    "description": "Similar to 3dmax WorkFlow: LowPoly -> smoothing groups + chamfer + turbosmooth = HightPoly",
    "author": "Jorge Hernandez - Melenedez",
    "version": (0, 2),
    "blender": (2, 78),
    "category": "User",
    #"location": "Left Toolbar > Tools"
    "location": "Left Toolbar > Chamfer"
}

# los elementos nuevos de mi ui al externalizarlos a veces hacia
# varias veces el append. Para prevenir esto hice estas variables:
elemento1 = False
elemento2 = False

class game_modeling(bpy.types.Panel):
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
        row.operator("set.bevel", text="Set")
        row.operator("unset.bevel", text="Unset")
        #
        col.operator("add.smooth", text="Add Smooth")
        #
        col.label(text="Shading:")
        row = col.row(align=True)
        row.operator("object.shade_smooth", text="Smooth")
        row.operator("object.shade_flat", text="Flat")
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
    self.layout.prop(mod, "width", text="Bevel width")
    self.layout.prop(mod, "segments", text="Bevel segments")
    self.layout.prop(mod, "profile", text="Bevel profile")
    elemento1 = True

def newElementMenuSmooth(self, context):
    ob = bpy.context.active_object
    mod = ob.modifiers["Subsurf"]
    self.layout.prop(mod, "levels", text="Smooth levels")
    #self.layout.prop(mod, "render_levels", text="Smooth Render levels")
    elemento2 = True

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
            if elemento1 == False:
                bpy.types.game_modeling.append(newElementMenu)
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
            if elemento2 == False:
                bpy.types.game_modeling.append(newElementMenuSmooth)
        return {'FINISHED'}


class setBevel(bpy.types.Operator):
    bl_idname = "set.bevel"
    bl_label = "Set"
    bl_description = "Set to (edges or faces) one weight bevel and sharp"
    def execute(self, context):
        if bpy.context.mode == 'EDIT_MESH':
            # determinar si solo es un edge loop o un edge o si son caras seleccionadas:
            me = bpy.context.object.data
            bm = bmesh.from_edit_mesh(me)
            faces = []
            for face in bm.faces:
                if face.select:
                    faces.append(repr(face.index))
            if (len(faces) > 0 and len(faces) < len(bm.faces) ): # si son caras (y no son todas las caras del objeto):
                bpy.ops.mesh.region_to_loop() # si son caras con esto selecciono solo los contornos
            bpy.ops.transform.edge_bevelweight(value=1)
            bpy.ops.mesh.mark_sharp()
            ob = bpy.context.active_object
            mesh = bpy.data.meshes[ob.name]
            mesh.use_auto_smooth = True
            ob.data.auto_smooth_angle = 180
        else:
            self.report({'INFO'}, "This option only work in edit mode!")
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
            self.report({'INFO'}, "This option only work in edit mode!")
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
