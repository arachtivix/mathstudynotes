# generated entirely by Q except for this comment

import bpy

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Create a cube
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))

# Add a material to the cube
material = bpy.data.materials.new(name="Cube_Material")
material.use_nodes = True
material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.8, 0.1, 0.1, 1)  # Red color

# Assign material to cube
cube = bpy.context.active_object
cube.data.materials.append(material)

# Add a light
light_data = bpy.data.lights.new(name="Light", type='POINT')
light_data.energy = 1000
light_object = bpy.data.objects.new(name="Light", object_data=light_data)
bpy.context.scene.collection.objects.link(light_object)
light_object.location = (5, 5, 5)

# Add camera
camera_data = bpy.data.cameras.new(name="Camera")
camera_object = bpy.data.objects.new(name="Camera", object_data=camera_data)
bpy.context.scene.collection.objects.link(camera_object)
camera_object.location = (7, -7, 5)
camera_object.rotation_euler = (0.9, 0, 0.8)

# Make this the active camera
bpy.context.scene.camera = camera_object

# Set render engine and output settings
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.render.filepath = '//test_render.png'
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.resolution_x = 800
bpy.context.scene.render.resolution_y = 800

# Render the scene
bpy.ops.render.render(write_still=True)
