"""Script for creating shell objects with holes using boolean modifiers."""


import bpy
import mathutils
from utilities import editor_context  # Import context manager first
from utilities import shell_object    # Import regular functions second
from utilities import setup_render_defaults

def create_shell_with_holes(context, object_name, shell_thickness, hole_radius=0.2, hole_positions=None):
    """Creates a shell object and cuts holes into it using boolean modifiers and cylinders.
    
    Args:
        context: The Blender context
        object_name: Name for the shell object
        shell_thickness: Thickness of the shell
        hole_radius: Radius of the holes (default: 0.2)
        hole_positions: List of (x, y, z) tuples for hole positions. If None, creates demo holes
    """
    # Create the shell object within editor context
    with editor_context(context):
        # Core operation call - no context management inside
        shell_object(context, object_name, shell_thickness)
    
    # If no hole positions provided, create some demo positions
    if hole_positions is None:
        hole_positions = [
            (1, 0, 0),
            (-1, 0, 0),
            (0, 1, 0),
            (0, -1, 0),
            (0, 0, 1),
            (0, 0, -1)
        ]
    
    # Create holes within editor context
    with editor_context(context):
        # Create cylinder template
        # Create cylinder with depth large enough to ensure full intersection
        shell = context.scene.objects[object_name]
        max_dimension = max(shell.dimensions)
        cylinder_depth = max_dimension * 2  # Make cylinder twice as long as largest object dimension
        bpy.ops.mesh.primitive_cylinder_add(radius=hole_radius, depth=cylinder_depth)
        hole_template = context.active_object
        hole_template.display_type = 'WIRE'
        
        # For each hole position, create a cylinder and set up boolean modifier
        for i, pos in enumerate(hole_positions):
            new_hole = hole_template.copy()
            new_hole.data = hole_template.data.copy()
            context.scene.collection.objects.link(new_hole)
            new_hole.location = pos
            # Calculate direction vector from origin to hole position
            direction = mathutils.Vector(pos)
            if direction.length > 0:  # Only rotate if not at origin
                # Calculate rotation to point cylinder along direction vector
                rot_quat = direction.to_track_quat('-Z', 'Y')
                new_hole.rotation_euler = rot_quat.to_euler()
            
            # Add boolean modifier to shell
            shell = context.scene.objects[object_name]
            bool_mod = shell.modifiers.new(name=f"Hole_{i}", type='BOOLEAN')
            bool_mod.object = new_hole
            bool_mod.operation = 'DIFFERENCE'
            
            # Apply the boolean modifier permanently before removing the hole object
            bpy.ops.object.select_all(action='DESELECT')
            shell.select_set(True)
            context.view_layer.objects.active = shell
            bpy.ops.object.modifier_apply(modifier=bool_mod.name)
            
            # Remove hole object after boolean operation
            bpy.data.objects.remove(new_hole, do_unlink=True)
        
        # Clean up template
        bpy.data.objects.remove(hole_template, do_unlink=True)

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
    """Main function to demonstrate shell with holes creation and render the scene."""
    context = bpy.context
    
    # Clear existing objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    # Create base cube within editor context
    with editor_context(context):
        bpy.ops.mesh.primitive_cube_add(size=2)
        cube = context.active_object
        cube.name = "holey_shell"
    
    # Create shell with holes
    create_shell_with_holes(context, "holey_shell", shell_thickness=0.1)
    
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