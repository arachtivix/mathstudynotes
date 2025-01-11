import bpy

def print_cuda_devices():
    # Get preferences
    prefs = bpy.context.preferences
    
    # Get cycles compute device settings
    cycles_prefs = prefs.addons['cycles'].preferences
    
    print("\nAvailable Devices:")
    print("-----------------")
    
    # Force CUDA device type
    cycles_prefs.compute_device_type = 'CUDA'
    
    # Update devices
    cycles_prefs.get_devices()
    
    # Print all devices
    for device in cycles_prefs.devices:
        print(f"Device: {device.name}")
        print(f"Type: {device.type}")
        print(f"Use: {'Enabled' if device.use else 'Disabled'}")
        print("-----------------")

def enable_cuda_gpu(scene):
    """
    Configure scene to use CUDA GPU rendering
    Args:
        scene: bpy.types.Scene - Blender scene to configure
    """
    # Get preferences
    preferences = bpy.context.preferences
    cycles_preferences = preferences.addons['cycles'].preferences
    
    # Enable CUDA
    cycles_preferences.compute_device_type = 'CUDA'
    
    # Get and enable all CUDA devices
    cycles_preferences.get_devices()
    devices = cycles_preferences.devices
    
    # Enable all CUDA devices
    for device in devices:
        if device.type == 'CUDA':
            device.use = True
            
    # Set scene to use GPU rendering
    scene.cycles.device = 'GPU'
    scene.render.engine = 'CYCLES'
    
    # Force scene to update
    scene.update_render_engine()
    
    # Print confirmation of enabled devices
    print("Enabled CUDA devices:")
    for device in devices:
        if device.use:
            print(f"- {device.name}")


if __name__ == "__main__":
    print_cuda_devices()
