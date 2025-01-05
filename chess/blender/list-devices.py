import bpy

def list_available_gpus():
    """List all available GPUs that Blender can use for rendering."""
    
    # Get preferences and addon
    preferences = bpy.context.preferences
    cycles_preferences = preferences.addons['cycles'].preferences
    
    if cycles_preferences.get_devices() is None:
        print("No devices found.")
        return False

    # Print available devices
    print("\nAvailable Devices:")
    for device_type in cycles_preferences.get_devices():
        print(f"\nDevice Type: {device_type.type}")
        for device in device_type.devices:
            print(f"   {device.name} {'(CUDA)' if device.use_cuda else '(OpenCL)'}")
            print(f"      - Type: {device.type}")
            print(f"      - Active: {'Yes' if device.use else 'No'}")

    return True

def enable_gpu_rendering():
    """Configure Blender to use GPU rendering with available devices."""
    
    # Get scene and preferences
    scene = bpy.context.scene
    preferences = bpy.context.preferences
    cycles_preferences = preferences.addons['cycles'].preferences
    
    # Enable CUDA/OptiX
    cycles_preferences.compute_device_type = 'CUDA'  # or 'OPTIX' for RTX cards
    
    # Enable all GPU devices
    for device_type in cycles_preferences.get_devices():
        for device in device_type.devices:
            device.use = True
    
    # Set render engine to Cycles and device to GPU
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'GPU'
    
    # Print confirmation
    print("\nGPU rendering enabled:")
    print(f"Render Engine: {scene.render.engine}")
    print(f"Compute Device: {scene.cycles.device}")

def main():
    # List available GPUs
    print("\n=== Listing Available GPUs ===")
    found = list_available_gpus()
    
    if not found:
        print("No GPUs found. Exiting.")
        return
    
    # Enable GPU rendering
    print("\n=== Enabling GPU Rendering ===")
    enable_gpu_rendering()

if __name__ == "__main__":
    main()
