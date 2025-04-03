import bpy

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Create a cube
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
cube = bpy.context.active_object

# Create a sphere
bpy.ops.mesh.primitive_uv_sphere_add(radius=1.2, location=(0.5, 0.5, 0))
sphere = bpy.context.active_object

# Create materials
cube_material = bpy.data.materials.new(name="Cube_Material")
cube_material.use_nodes = True
# Make cube blue and transparent
nodes = cube_material.node_tree.nodes
principled = nodes["Principled BSDF"]
principled.inputs[0].default_value = (0.1, 0.1, 0.8, 1)  # Blue color
principled.inputs[21].default_value = 0.8  # Transmission

sphere_material = bpy.data.materials.new(name="Sphere_Material")
sphere_material.use_nodes = True
# Make sphere red
nodes = sphere_material.node_tree.nodes
principled = nodes["Principled BSDF"]
principled.inputs[0].default_value = (0.8, 0.1, 0.1, 1)  # Red color

# Apply materials
cube.data.materials.append(cube_material)
sphere.data.materials.append(sphere_material)

# Create boolean difference modifier
bool_mod = cube.modifiers.new(name="Boolean", type='BOOLEAN')
bool_mod.object = sphere
bool_mod.operation = 'DIFFERENCE'

# Hide the sphere (optional - comment out if you want to see both objects)
sphere.hide_viewport = True
sphere.hide_render = True

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
bpy.context.scene.render.filepath = '//boolean_modifier_demo.png'
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.resolution_x = 800
bpy.context.scene.render.resolution_y = 800

# Enable transparency in render
bpy.context.scene.render.film_transparent = True

# Render the scene
bpy.ops.render.render(write_still=True)
