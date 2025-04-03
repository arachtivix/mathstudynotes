import bpy
import os
from datetime import datetime

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