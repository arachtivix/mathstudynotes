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

if __name__ == "__main__":
    print_cuda_devices()
