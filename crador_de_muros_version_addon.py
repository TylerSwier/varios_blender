import bpy
from bpy.props import *

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
    "name": "Wall Creator",
    "description": "Wall Creator",
    "author": "Jorge Hernandez - Melenedez",
    "version": (0, 1),
    "blender": (2, 71, 0),
    "location": "Left Toolbar > WallCreator",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Add Mesh"
}

def renombrar(nombre, nuevonombre):
    ob = bpy.data.objects[str(nombre)]
    ob.name = nuevonombre
 
def mover(nombre, x, y):
    ob = bpy.data.objects[str(nombre)]
    # en cuanto a coordenadas
    # en metros un cubo de 1x1x1 equivale a 2x2x2 metros..
    # por lo tanto :
    x = x*2
    y = y*2
    ob.location.x = x
    ob.location.z = y
    
def escalar(nombre, x, y, z):
    ob = bpy.data.objects[str(nombre)]
    ob.scale.x = x
    ob.scale.y = y
    ob.scale.z = z

def selecccionarPorNombre(nombre):
    ob = bpy.data.objects[str(nombre)]
    ob.select = True

def desseleccionarTodo():
    bpy.ops.object.select_all(action='DESELECT')
    
def eliminarTodo():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def freezer():
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')

def creandoLadrillo(nombre, sizex, sizey, sizez):
    bpy.ops.mesh.primitive_cube_add(radius=1, view_align=False, enter_editmode=False, location=(0, 0, 0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    ob = bpy.context.object
    ob.name = nombre
    ob.scale.x = sizex
    ob.scale.y = sizey
    ob.scale.z = sizez

class DialogOperator(bpy.types.Operator):
    bl_idname = "object.zebus_dialog"
    bl_label = "Wall Bricks Creator v01"
    
    # Defaults:
    muro_alto = IntProperty(name="alto", min=0, max=100, default=4)
    muro_ancho = IntProperty(name="ancho", min=0, max=100, default=4)
       
    ladrillo_alto = FloatProperty(name="ladrillo_alto", min=0, max=100, default=5)
    ladrillo_ancho = FloatProperty(name="ladrillo_ancho", min=0, max=100, default=11.1)
    ladrillo_largo = FloatProperty(name="ladrillo_largo", min=0, max=100, default=24)
    cemento = FloatProperty(name="cemento", min=0, max=5, default=1.6)
    
    centimetros = BoolProperty(name="centimetros", default=False)
    fill_boundaryes = BoolProperty(name="fill_boundaryes", default=True)
    
    def execute(self,context):
        
        eliminarTodo()
        # pongo blender en metros:
        bpy.context.scene.unit_settings.system = 'METRIC'
                
        muro_alto = self.muro_alto
        muro_ancho = self.muro_ancho
        
        centimetros = self.centimetros
        # no se por que me multiplica el size *2 entonces: /2
        if centimetros:
            ladrillo_alto = self.ladrillo_alto/2/100
            ladrillo_ancho = self.ladrillo_ancho/2/100
            ladrillo_largo = self.ladrillo_largo/2/100
            cemento = self.cemento/2/100
        else:
            ladrillo_alto = self.ladrillo_alto/2
            ladrillo_ancho = self.ladrillo_ancho/2
            ladrillo_largo = self.ladrillo_largo/2
            cemento = self.cemento/2 
        
        fillb = self.fill_boundaryes
        
        ladrillo = ladrillo_largo
        medio = ladrillo_largo/2
        offset_nacimientov = ladrillo_alto/2
        offset_nacimientoh = medio
        
        # array 2 dimensiones
        for v in range(muro_alto):
            for h in range(muro_ancho):
                
                if v%2 == 0: # si es divisible por 2 entonces offset -->
                    
                    if fillb and h == 0: # bloque complejo --------------------------
                        desseleccionarTodo()
                        creandoLadrillo("primero", ladrillo_largo, ladrillo_ancho, ladrillo_alto)
                        ob = bpy.context.object
                        anterior = ob.name

                        escalar(ob.name, medio-cemento, ladrillo_ancho, ladrillo_alto)
                        x = ob.location.x - (ob.scale.x/2) - cemento + offset_nacimientoh
                        y = v * (ladrillo_alto + cemento) + offset_nacimientov
                        mover(ob.name, x ,y)
                        freezer()
                        desseleccionarTodo()
                    # fin bloque complejo --------------------------
                    
                    else: # el normal:
                        creandoLadrillo("ladrillo_ofset", ladrillo_largo, ladrillo_ancho, ladrillo_alto)
                        ob = bpy.context.object
                        #x = h * (ladrillo + medio + cemento) # <-- el normal con offset
                        x = h * (ladrillo + cemento) - cemento - medio  + offset_nacimientoh# <-- el normal con offset contando con fill
                        y = v * (ladrillo_alto + cemento) + offset_nacimientov
                        mover(ob.name, x ,y)
                        freezer()
                        
                else: # sin offset -->
                    if fillb and h == (muro_ancho-1): # bloque complejo --------------------------
                        desseleccionarTodo()
                        creandoLadrillo("final", ladrillo_largo, ladrillo_ancho, ladrillo_alto)
                        ob = bpy.context.object
                        anterior = ob.name

                        escalar(ob.name, medio-cemento, ladrillo_ancho, ladrillo_alto)
                        #x = h * (ladrillo + cemento) # <-- el normal sin offset
                        x = h * (ladrillo + cemento) - (ob.scale.x/2) - cemento + offset_nacimientoh# <-- el normal sin offset contando con fill
                        y = v * (ladrillo_alto + cemento) + offset_nacimientov
                        mover(ob.name, x ,y)
                        freezer()
                        desseleccionarTodo()
                        # fin bloque complejo --------------------------
                        
                    else: # el normal:
                        creandoLadrillo("ladrillo", ladrillo_largo, ladrillo_ancho, ladrillo_alto)
                        ob = bpy.context.object
                        x = h * (ladrillo + cemento) + offset_nacimientoh
                        y = v * (ladrillo_alto + cemento) + offset_nacimientov
                        mover(ob.name, x ,y)
                        freezer()
                
                                        
        return {'FINISHED'}   
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=200)

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        col = box.column()
        
        col.label("Wall Settings:")
        rowsub0 = col.row()
        rowsub0.prop(self, "muro_alto", text='M Alto')
        rowsub0.prop(self, "muro_ancho", text='M Ancho')
        
        col.label("Brick Settings:")
        col.prop(self, "ladrillo_alto", text='Alto')
        col.prop(self, "ladrillo_ancho", text='Ancho')
        col.prop(self, "ladrillo_largo", text='Largo')
        col.label("Cement Settings:")
        col.prop(self, "cemento", text='Cemento')
        
        col.label("Units Settings:")
        col = box.column()
        col.prop(self, "centimetros" )
        
        col.label("Fill Settings:")
        col.prop(self, "fill_boundaryes" )
            
bpy.utils.register_class(DialogOperator)

class DialogPanel(bpy.types.Panel):
    bl_label = "Dialog"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "WallCreator"
 
    def draw(self, context):
        layout = self.layout
        context = bpy.context
        scn = context.scene
        row = layout.row(align=True)
        col = row.column()
        col.alignment = 'EXPAND'
        col.operator("object.zebus_dialog")
        
#   Registration
def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
