# Blender Python Development Guidelines for Reusable Code
## THIS WAS WRITTEN BY AND _FOR_ Amazon Q to focus a little better on some stuff.


Based on analysis of existing Blender Python code and best practices, here are key guidelines for writing reusable Blender Python code:

## 1. Render Output Management
- Configure render output to use timestamped directories in /tmp
- Use the `utilities.setup_render_defaults()` function to:
  - Create output directory named "YYYY-MM-DD-HH-MM_render"
  - Set default render settings (1920x1080, PNG with alpha)
  - Enable GPU rendering when available

## 3. Clear Dependencies
- Explicitly import required Blender modules (bpy, bmesh, etc.)
- Use classes and functions that can work independently
- Avoid tight coupling between components

## 4. Error Handling
- Explicitly import required Blender modules (bpy, bmesh, etc.)
- Document any required Blender version dependencies
- Keep external dependencies minimal and document them

## 3. Configuration and Parameters  
- Use function parameters rather than hardcoded values
- Consider making key values configurable via Blender properties
- Provide sensible defaults while allowing customization

## 4. Error Handling
- Use try/except blocks around Blender operations that may fail
- Provide meaningful error messages
- Clean up resources and handle edge cases

## 5. Documentation
- Add docstrings explaining purpose and usage
- Document parameters and return values
- Include example usage
- Note any limitations or assumptions

## 6. Testing
- Write unit tests where possible
- Test with different Blender versions
- Include test files/scenes if needed

## 7. Code Organization
- Use consistent naming conventions
- Group related functionality
- Keep files focused and manageable size

## 8. Blender Integration
- Follow Blender Python API conventions
- Use Blender's built-in property system
- Consider add-on compatibility if relevant

## 9. Example Structure and Modular Design
- Break functionality into small, focused modules that do one thing well
- Use wrapper functions to handle common patterns like state management
- Keep functions simple and focused on a single task

```python
import bpy
from blender.scripts.transformations import transform_object

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

# Example usage:
# transform_object(bpy.context, "Cube", location=(1, 0, 0), rotation=(0, 0, 1.5708))
```

## 10. Editor State Management
- Always save and restore editor context when modifying it
- Use context override instead of modifying global state when possible
- Clean up any temporary editor state changes
- Use context managers (`with` statements) for temporary state changes
- Document any editor state dependencies or modifications
- Be aware of active object, mode, and selection state impacts
- Consider thread safety when dealing with editor state

Example:
```python
import bpy

def my_operation():
    # Save current state
    original_mode = bpy.context.object.mode
    original_selection = bpy.context.selected_objects[:]
    
    try:
        # Modify state temporarily
        bpy.ops.object.mode_set(mode='EDIT')
        # Perform operations...
    finally:
        # Restore original state
        bpy.ops.object.mode_set(mode=original_mode)
        # Restore selection
        for obj in bpy.context.selected_objects:
            obj.select_set(False)
        for obj in original_selection:
            obj.select_set(True)
```

## Resources
- Blender Python API Documentation
- Official Blender Add-on Guidelines
- Community Best Practices

Following these guidelines will help create more maintainable and reusable Blender Python code that can be shared and integrated into different projects.