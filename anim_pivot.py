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
    "name": "Pivot Anim",
    "description": "Rig sistem for emulate a pivot animated",
    "author": "Jorge Hernandez - Melenedez",
    "version": (0,1),
    "blender": (2, 65, 0),
    "location": "",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": ""}
    
import bpy

def creandorig():
    #creando el rig:
    bpy.ops.object.add(type='EMPTY', view_align=False, enter_editmode=False, location=(0, 0, 0), rotation=(0, 0, 0), layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True))
    bpy.context.object.name = "e_pivot"
    bpy.context.object.empty_draw_type = 'SPHERE'
    bpy.data.objects['e_pivot'].scale = [0.5,0.5,0.5]

    bpy.ops.object.add(type='EMPTY', view_align=False, enter_editmode=False, location=(0, 0, 0), rotation=(0, 0, 0), layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True))
    bpy.context.object.name = "e_offset"
    bpy.data.objects['e_offset'].scale = [0.5,0.5,0.5]

    bpy.ops.object.armature_add(view_align=False, enter_editmode=False, location=(0, 0, 0), rotation=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    bpy.context.selected_objects[0].name = "mi_armature_g"
    bpy.context.selected_objects[0].data.name = "mi_armature"

    bpy.ops.object.editmode_toggle()
    bpy.ops.armature.select_all(action='DESELECT')
    bpy.ops.armature.select_all(action='SELECT')
    bpy.ops.armature.delete()

    bpy.ops.armature.bone_primitive_add(name="Offset")
    bpy.ops.armature.bone_primitive_add(name="Pivot")

    #bpy.ops.object.mode_set(mode='EDIT')
    #bpy.data.armatures['mi_armature'].edit_bones['Offset'].select = True #<-- en edit object
    bpy.ops.object.mode_set(mode='POSE')
    bpy.data.armatures['mi_armature'].bones['Offset'].select = True
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.data.armatures['mi_armature'].bones.active = bpy.data.armatures['mi_armature'].bones['Offset']
    #bpy.ops.object.mode_set(mode='EDIT')
    #bpy.data.armatures['mi_armature'].edit_bones['Pivot'].select = True
    bpy.ops.object.mode_set(mode='POSE')
    bpy.data.armatures['mi_armature'].bones['Pivot'].select = True        
    bpy.ops.object.mode_set(mode='OBJECT') 
    bpy.data.armatures['mi_armature'].bones.active = bpy.data.armatures['mi_armature'].bones['Pivot']
    #bpy.data.armatures[2].bones['Offset'].select = True #<-- en pose bone
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.armature.parent_set(type='OFFSET')
    bpy.ops.object.mode_set(mode='POSE')

    bpy.data.objects['mi_armature_g'].pose.bones['Pivot'].custom_shape = bpy.data.objects['e_pivot']
    bpy.data.objects['mi_armature_g'].pose.bones['Offset'].custom_shape = bpy.data.objects['e_offset']
    #bpy.ops.object.mode_set(mode='OBJECT')
    
def obtenercursor():
    #armature = bpy.context.active_object
    #pose_bone = bpy.context.active_pose_bone
    armature = bpy.data.objects['mi_armature_g']
    pose_bone1 = bpy.data.objects['mi_armature_g'].pose.bones["Pivot"]
    pose_bone2 = bpy.data.objects['mi_armature_g'].pose.bones["Offset"]
    cvec = bpy.context.scene.cursor_location
    ovec =  cvec - pose_bone2.vector
    # orden x        z        y
    #ovec = [-ovec[0],-ovec[1],-ovec[2]]
    pose_bone1.location = armature.matrix_world.inverted() * pose_bone1.bone.matrix_local.inverted() * cvec
    pose_bone2.location = ovec

def asignandorig():
    # emparentar mi rig al objeto seleccionado:
    # primero seleccionamos el objeto nuevo (al que aplicaremos el rig)
    if bpy.context.object:
        objeto = bpy.context.object.name
        #bpy.ops.object.mode_set(mode='OBJECT')
        bpy.context.scene.objects.active = bpy.data.objects['mi_armature_g']
        bpy.data.objects['mi_armature_g'].select = True
        bpy.ops.object.parent_set(type='BONE', xmirror=False, keep_transform=False)
        bpy.context.scene.objects.active = bpy.data.objects[objeto]
        bpy.data.objects[objeto].select = True
        bpy.context.object.parent_bone = "Offset"
        #bpy.context.selected_objects[0].parent = bpy.data.objects['mi_armature_g']

class BotonesPivotAnim(bpy.types.Panel):
    bl_label = "Pivot Anim"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"

    def draw(self, context):
        layout = self.layout
        scn = bpy.context.scene
        row = layout.row(align=True)
        col = row.column()
        col.alignment = 'EXPAND'        

        col.operator("grig.grig", text='Generate Rig')
        col.operator("arig.arig", text='Assign Rig')
        col.operator("ocursor.ocursor", text='Seteando pivote')

class accionb1(bpy.types.Operator):
    bl_idname = "grig.grig"
    bl_label = "Generate Rig"
    bl_description = "Generate a simple rig system"
    def execute(self, context):
        creandorig()
        return{'FINISHED'}

class accionb2(bpy.types.Operator):
    bl_idname = "arig.arig"
    bl_label = "Assign Rig"
    bl_description = "Assign Rig to object"
    def execute(self, context):
        asignandorig()
        return{'FINISHED'}

class accionb3(bpy.types.Operator):
    bl_idname = "ocursor.ocursor"
    bl_label = "Seteando pivote"
    bl_description = "Set pivot to cursor"
    def execute(self, context):
        obtenercursor()
        return{'FINISHED'}


def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
