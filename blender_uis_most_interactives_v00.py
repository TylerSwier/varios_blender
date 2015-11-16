import bpy

class interfaz(bpy.types.Panel):
    bl_label = "My Addon:"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Test"
    
    def draw(self, context):
        scn = context.scene
        layout = self.layout
        row = layout.row(align=True)
        col = row.column()
        col.alignment = 'EXPAND'
    
        col.label(text = "Interfaz")
        col.prop(scn, "MyBool")
    
        # show individuals checkboxs:
        col.label(text = "Individual:")    
        for obj in context.selected_objects:    
            col.prop(obj, "show_name", text="Name")
    
        col.operator("my.buton")

class MyButon(bpy.types.Operator):
    bl_idname = "my.buton" # <- el idname nunca con mayusculas
    bl_label = "Boton"
    bl_description = "tab"

    # Si hay objetos seleccionados se activa este item del addon, sino sale atenuado:
    @classmethod
    def poll(cls, context):
        return (len(context.selected_objects) > 0)

    # al clickar el boton:
    def execute(self, context):
        # en este caso no tiene sentido porque el propio bool ya lo hace
        # pero desde aqui podriamos decirle al boton que ejecute x funcion:
        #upd(self, context)
        self.report({'INFO'}, "MyButon executed.")
        return {'FINISHED'}
    
    
# action update:
def upd(self, context):
    for obj in context.selected_objects:    
        bpy.data.objects[obj.name].show_name = context.scene.MyBool

def register():
    bpy.utils.register_module(__name__)
    #bpy.utils.register_class(interfaz)
    bpy.types.Scene.MyBool = bpy.props.BoolProperty(update=upd)


def unregister():
    bpy.utils.register_module(__name__)
    #bpy.utils.unregister_class(interfaz)
    del bpy.types.Scene.MyBool


if __name__ == "__main__":
    register()
