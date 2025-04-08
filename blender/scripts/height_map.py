"""Script for creating height maps using stacked cubes."""

from utilities import setup_render_defaults

import bpy
from contextlib import contextmanager
import numpy as np
from utilities import editor_context, setup_render_defaults

def create_height_map(context, array_2d, cube_size=1.0, spacing=0.0):
    """Creates a height map from a 2D array using stacked cubes.
    
    Args:
        context: The Blender context
        array_2d: 2D numpy array or list of lists containing height values
        cube_size: Size of each cube (default: 1.0)
        spacing: Additional space between cubes (default: 0.0)
    
    Returns:
        The created height map object
    """
    if not isinstance(array_2d, np.ndarray):
        array_2d = np.array(array_2d)
    
    # Create an empty mesh and object
    mesh = bpy.data.meshes.new('HeightMap')
    obj = bpy.data.objects.new('HeightMap', mesh)
    
    # Link the object to the scene
    context.scene.collection.objects.link(obj)
    
    grid_size = array_2d.shape
    total_size = cube_size + spacing
    
    # Create cubes for each position in the grid
    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            height = array_2d[i, j]
            if height > 0:
                # Create cube
                with editor_context(context):
                    bpy.ops.mesh.primitive_cube_add(
                        size=cube_size,
                        location=(
                            i * total_size,
                            j * total_size,
                            (height * total_size) / 2
                        )
                    )
                    cube = context.active_object
                    # Scale the cube to match the height
                    cube.scale.z = height
                    # Parent the cube to our height map object
                    cube.parent = obj
    
    return obj

def create_basic_material(name, color):
    """Creates a basic material using Cycles nodes.
    
    Args:
        name: Name for the material
        color: Tuple of (R, G, B, A) values
    
    Returns:
        The created material
    """
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    # Create principled BSDF shader (standard in Cycles)
    principled = nodes.new('ShaderNodeBsdfPrincipled')
    principled.inputs['Base Color'].default_value = color
    principled.inputs['Roughness'].default_value = 0.7
    
    # Create material output
    material_output = nodes.new('ShaderNodeOutputMaterial')
    
    # Link nodes
    mat.node_tree.links.new(principled.outputs[0], material_output.inputs[0])
    
    return mat

def setup_scene():
    """Sets up the scene with camera and lighting."""
    # Clear existing objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    # Setup rendering defaults
    render_dir = setup_render_defaults()
    
    # Set render engine to Cycles
    bpy.context.scene.render.engine = 'CYCLES'
    
    # Add camera
    bpy.ops.object.camera_add(location=(15, -15, 10))
    camera = bpy.context.active_object
    camera.rotation_euler = (0.9, 0.0, 0.8)
    
    # Add light
    bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
    light = bpy.context.active_object
    light.data.energy = 5
    
    # Set camera as active
    bpy.context.scene.camera = camera

def main():
    """Main function demonstrating height map creation and rendering."""
    context = bpy.context
    
    # Example height map data
    height_data = np.array([
        [1, 2, 1, 3],
        [2, 4, 2, 1],
        [1, 3, 3, 2],
        [2, 1, 2, 1]
    ])
    
    # Setup the scene
    setup_scene()
    
    # Create height map
    height_map = create_height_map(context, height_data, cube_size=1.0, spacing=0.1)
    
    # Create and apply material
    mat = create_basic_material("HeightMapMaterial", (0.2, 0.5, 0.8, 1.0))
    for child in height_map.children:
        child.data.materials.append(mat)
    
    # Render from different angles
    angles = [
        ((15, -15, 10), (0.9, 0.0, 0.8)),  # Diagonal view
        ((0, -20, 15), (1.0, 0.0, 0.0)),   # Front view
        ((20, 0, 15), (1.0, 0.0, 1.57))    # Side view
    ]
    
    # Render each angle
    for i, (location, rotation) in enumerate(angles):
        context.scene.camera.location = location
        context.scene.camera.rotation_euler = rotation
        bpy.context.scene.render.filepath = f"//height_map_view_{i}.png"
        bpy.ops.render.render(write_still=True)

if __name__ == "__main__":
    main()