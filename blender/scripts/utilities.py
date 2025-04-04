"""Utility functions for Blender scripts.

Notes:
    If you see unexpected behavior:
    1. Check actual file location with __file__
    2. Verify file contents match expected
    3. Clear __pycache__ directory
    4. Restart Blender if needed
"""

import bpy
import os
import sys
from datetime import datetime
from contextlib import contextmanager
import mathutils

# Define all context managers first
@contextmanager 
def editor_context(context):
    """A context manager for safely managing Blender editor state.
    
    Args:
        context: The current Blender context
        
    Yields:
        context: The context object for use within the managed block
    """
    initial_mode = context.mode
    initial_active = context.active_object
    initial_selected = list(context.selected_objects)
    
    try:
        yield context
    finally:
        try:
            for obj in context.selected_objects:
                obj.select_set(False)
            for obj in initial_selected:
                if obj:
                    obj.select_set(True)
            if initial_active:
                context.view_layer.objects.active = initial_active
            if initial_mode != context.mode:
                bpy.ops.object.mode_set(mode=initial_mode)
        except Exception:
            pass

def _verify_location():
    """Print information about this module's location.
    
    Call this if you suspect filesystem/import issues.
    """
    print(f"Module location: {__file__}")
    print("\nPython path:")
    for path in sys.path:
        print(f"  {path}")
    
    try:
        with open(__file__, 'r') as f:
            print(f"\nActual file contents:")
            print(f.read())
    except Exception as e:
        print(f"Error reading file: {e}")

def shell_object(context, object_name, thickness):
    """Creates a hollow shell from a solid object.
    
    Args:
        context: The current Blender context
        object_name: Name of the object to create a shell from
        thickness: Thickness of the shell to create
        
    Returns:
        str: The name of the shell object
        
    Raises:
        ValueError: If thickness is not positive or object not found
        
    Note:
        This function performs core operations only - use with editor_context
        from the caller if state management is needed.
    """
    if thickness <= 0:
        raise ValueError("Shell thickness must be positive")
        
    original = context.scene.objects.get(object_name)
    if not original:
        raise ValueError(f"Object {object_name} not found")
        
    inner = original.copy()
    inner.data = original.data.copy()
    context.scene.collection.objects.link(inner)
    
    scale_factor = 1 - (thickness / min(original.dimensions))
    inner.scale = mathutils.Vector((scale_factor,) * 3)
    
    bool_mod = original.modifiers.new(name="Shell", type='BOOLEAN')
    bool_mod.object = inner
    bool_mod.operation = 'DIFFERENCE'
    
    # Apply the boolean modifier permanently before removing the hole object
    bpy.ops.object.select_all(action='DESELECT')
    original.select_set(True)
    context.view_layer.objects.active = original
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)
            
    # Remove hole object after boolean operation
    bpy.data.objects.remove(inner, do_unlink=True)
    
    return object_name

def setup_render_defaults():
    """Sets up default render settings and output directory for Blender renders."""
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
    render_dir = f"/mnt/c/Users/danie/Desktop/{timestamp}_render"
    os.makedirs(render_dir, exist_ok=True)
    bpy.context.scene.render.filepath = render_dir
    
    scene = bpy.context.scene
    render = scene.render
    render.image_settings.file_format = 'PNG'
    render.image_settings.color_mode = 'RGBA'
    render.resolution_x = 1920
    render.resolution_y = 1080
    render.resolution_percentage = 100
    return render_dir