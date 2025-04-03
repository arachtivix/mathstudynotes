"""
Demo script creating a tiled floor with multicolored glass balls.
Following Blender development guidelines for reusable code.
"""
import bpy
import random
from mathutils import Vector
from utilities import setup_render_defaults

def create_glass_material(name, color=(1, 1, 1, 1)):
    """Create a glass material with the specified color."""
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    
    # Clear default nodes
    nodes.clear()
    
    # Create glass shader nodes
    output = nodes.new('ShaderNodeOutputMaterial')
    glass = nodes.new('ShaderNodeBsdfGlass')
    glass.inputs['Color'].default_value = color
    glass.inputs['Roughness'].default_value = 0.0
    glass.inputs['IOR'].default_value = 1.45
    
    # Link nodes
    links.new(glass.outputs['BSDF'], output.inputs['Surface'])
    
    return material

def create_floor_material():
    """Create a diffuse material for the floor tiles."""
    material = bpy.data.materials.new(name="FloorTile")
    material.use_nodes = True
    nodes = material.node_tree.nodes
    
    # Use the default diffuse BSDF
    nodes["Principled BSDF"].inputs['Roughness'].default_value = 0.7
    return material

def create_floor(size=5, tile_size=1.0):
    """Create a tiled floor of the specified size."""
    bpy.ops.mesh.primitive_plane_add(size=size)
    floor = bpy.context.active_object
    
    # Add material
    floor_mat = create_floor_material()
    floor.data.materials.append(floor_mat)
    
    return floor

def create_glass_ball(location, color):
    """Create a glass ball at the specified location with given color."""
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.2, location=location)
    ball = bpy.context.active_object
    
    # Add material
    glass_mat = create_glass_material(f"Glass_{color[0]}_{color[1]}_{color[2]}", color)
    ball.data.materials.append(glass_mat)
    
    return ball

def setup_scene():
    """Set up the scene with lighting and camera."""
    # Add camera
    bpy.ops.object.camera_add(location=(5, -5, 3.5), rotation=(1.0, 0.0, 0.8))
    camera = bpy.context.active_object
    bpy.context.scene.camera = camera  # Set as active camera
    
    # Add sun lamp
    bpy.ops.object.light_add(type='SUN', location=(5, 5, 7), rotation=(0.5, 0.2, -0.3))
    lamp = bpy.context.active_object
    lamp.data.energy = 3.0
    
    return camera, lamp

def main():
    """Main function to create the scene."""
    # Clear existing objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    # Create floor
    floor = create_floor(size=6.0, tile_size=1.0)
    
    # Create glass balls with different colors
    colors = [
        (1.0, 0.2, 0.2, 1.0),  # Red
        (0.2, 1.0, 0.2, 1.0),  # Green
        (0.2, 0.2, 1.0, 1.0),  # Blue
        (1.0, 1.0, 0.2, 1.0),  # Yellow
        (1.0, 0.2, 1.0, 1.0),  # Purple
    ]
    
    # Place balls in a pattern
    for i in range(-2, 3):
        for j in range(-2, 3):
            if (i + j) % 2 == 0:  # Checker pattern
                color = random.choice(colors)
                location = Vector((i, j, 0.2))
                create_glass_ball(location, color)
    
    # Setup lighting and camera
    camera, lamp = setup_scene()
    
    # Set up render settings
    setup_render_defaults()
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 128

    # Render the current frame and save it
    bpy.ops.render.render(write_still=True)

if __name__ == "__main__":
    main()