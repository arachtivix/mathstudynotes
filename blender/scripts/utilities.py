import bpy
import os
from datetime import datetime
from contextlib import contextmanager

def setup_render_defaults():
    """Sets up default render settings and output directory for Blender renders.
    
    Creates a timestamped directory in /tmp and configures it as the render output path.
    Also sets some sensible default render settings.
    
    Returns:
        str: The path to the created render directory
    """
    # Create timestamped directory name
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
    render_dir = f"/tmp/{timestamp}_render"
    
    # Create the directory if it doesn't exist
    os.makedirs(render_dir, exist_ok=True)
    
    # Set the render output path
    bpy.context.scene.render.filepath = render_dir
    
    # Set some default render settings
    scene = bpy.context.scene
    render = scene.render
    
    # Set output format to PNG with RGBA
    render.image_settings.file_format = 'PNG'
    render.image_settings.color_mode = 'RGBA'
    
    # Set resolution and quality
    render.resolution_x = 1920
    render.resolution_y = 1080
    render.resolution_percentage = 100
    
    # Enable GPU compute if available
    cycles_prefs = bpy.context.preferences.addons['cycles'].preferences
    cuda_devices = cycles_prefs.get_devices_for_type('CUDA')
    if cuda_devices:
        cycles_prefs.compute_device_type = 'CUDA'
        for device in cuda_devices:
            device.use = True
        scene.cycles.device = 'GPU'
    
    return render_dir


@contextmanager
def editor_context(context):
    '''A context manager for safely managing Blender editor state.
    
    This wrapper ensures that editor state is properly saved and restored
    when performing operations that might modify the global editor state.
    
    Args:
        context: The current Blender context
        
    Yields:
        context: The context object for use within the managed block
        
    Example:
        with editor_context(bpy.context) as ctx:
            # Perform operations that might modify editor state
            # State will be automatically restored after the block
    '''
    # Store initial state
    initial_mode = context.mode
    initial_active = context.active_object
    initial_selected = context.selected_objects.copy()
    
    try:
        yield context
    finally:
        # Restore selection state
        for obj in context.selected_objects:
            obj.select_set(False)
        for obj in initial_selected:
            if obj:
                obj.select_set(True)
        
        # Restore active object
        if initial_active:
            context.view_layer.objects.active = initial_active
            
        # Restore mode
        if initial_mode != context.mode:
            bpy.ops.object.mode_set(mode=initial_mode)