import bpy
def getCentroid():
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            ctx = bpy.context.copy()
            ctx['area'] = area
            bpy.ops.view3d.snap_cursor_to_selected(ctx)
            return bpy.context.scene.cursor_location[:]
        
cen = getCentroid()
print(str(cen))
