import bpy
from .utilities import editor_context

def transform_object(context, object_name, location=None, rotation=None, scale=None):
    """Transforms a Blender object with proper context management.
    
    Args:
        context: The current Blender context
        object_name: Name of the object to transform
        location: Optional new location (x, y, z)
        rotation: Optional new rotation in radians (x, y, z)
        scale: Optional new scale (x, y, z)
        
    Returns:
        True if transformation was successful
        
    Raises:
        ValueError: If object is not found or transformation fails
    """
    with editor_context(context) as ctx:
        try:
            # Access the object safely within the context
            obj = ctx.scene.objects.get(object_name)
            if not obj:
                raise ValueError(f"Object {object_name} not found")
            
            if location:
                obj.location = location
            if rotation:
                obj.rotation_euler = rotation
            if scale:
                obj.scale = scale
                
            return True
        except Exception as e:
            raise ValueError(f"Transform operation failed: {str(e)}")