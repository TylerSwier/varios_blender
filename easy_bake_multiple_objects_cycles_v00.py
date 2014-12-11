import bpy



# cuantos materiales tiene (sin contar con 0):
total_mats = len(bpy.context.object.material_slots)
objetos = len(bpy.context.selected_objects)

for a in range(objetos):
    #creamos una nueva imagen por objeto donde ira el bakeo:
    #bpy.data.window_managers["WinMan"].(null) = "nuevo_map"
    nombre='nuevo_mapa_para_bakeo_0' + str(a)
    bpy.ops.image.new(name=nombre)

    # si no tiene uvs se las creamos y si tene las backupeamos y creamos nuevas:
	if len(bpy.context.object.data.uv_layers) == 0:
		# agregamos un nuevo mapa de uvs:
		bpy.ops.mesh.uv_texture_add()
	else:
		if len(bpy.context.object.data.uv_layers) == 1:
			# -1 no lo contiene, 0 si lo contiene:
			if bpy.context.object.data.uv_textures[0].name.find("backup_") != 0:
				# lo seleccionamos y lo renombramos
				#bpy.context.object.data.active_index = 0
				bpy.context.object.data.uv_textures[0].active = True
				bpy.context.object.data.uv_textures[0].name = str("backup_") + str(bpy.context.object.data.uv_textures[0].name)
			# agregamos un nuevo mapa de uvs:
			bpy.ops.mesh.uv_texture_add()
			#bpy.context.object.data.active_index = 1 # <-- esto es así:
			bpy.context.object.data.uv_textures[1].active = True
			bpy.context.object.data.uv_textures[1].active_render = True
			bpy.context.object.data.uv_textures[1].name = "nuevo_mapa_uv"

    for i in range(total_mats):
        if 'img_texture_automatic' not in bpy.context.object.material_slots[i].material.node_tree.nodes:
            bpy.context.object.material_slots[i].material.node_tree.nodes.new("ShaderNodeTexImage")
            bpy.context.object.material_slots[i].material.node_tree.nodes['Image Texture'].image = bpy.data.images[nombre]
            bpy.context.object.material_slots[i].material.node_tree.nodes['Image Texture'].name = 'img_texture_automatic'

    #bpy.ops.node.add_node(type="ShaderNodeTexImage", use_transform=False)
