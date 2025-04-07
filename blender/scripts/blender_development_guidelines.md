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
- Organize imports and definitions carefully:
  - Import context managers separately from regular functions
  - Define context managers before functions that use them
  - Use explicit imports rather than importing *
  - Example:
    ```python
    # CORRECT - Clear separation of imports
    from utilities import editor_context  # Context manager first
    from utilities import operation1, operation2  # Regular functions
    
    # INCORRECT - May cause decorator confusion
    from utilities import *  # Don't use wildcard imports
    from utilities import operation1, editor_context  # Mixed import types
    ```
- Use context managers to handle editor state changes:
  - Implement proper context managers using @contextmanager decorator:
    - Define context managers before any functions that use them
    - Apply @contextmanager directly to the function definition
    - Do not reassign decorated functions as it breaks the context manager protocol
    - Ensure error handling in finally blocks
    - Catch and handle specific exceptions that may occur during cleanup
    - Avoid mixing context managers with functions that manage their own state:
      - Functions should either use a context manager OR manage state themselves, not both
      - When using context managers, keep functions focused on their core logic
      - Let the context manager handle all state management
      - Functions that use context managers should be wrapped by the caller, not internally:
      - Keep functions focused on core operations
      - Let the caller decide when to use context management
      - Group multiple operations under a single context manager when possible
      - Example:
        ```python
        # GOOD: Multiple operations under one context
        with editor_context(context):
            result1 = operation1()  # Clean operation
            result2 = operation2()  # Clean operation
            
        # BAD: Unnecessary context switching
        with editor_context(context):
            result1 = operation1()
        with editor_context(context):  # Avoid multiple contexts
            result2 = operation2()
        ```
      - Example of correct usage:
        ```python
        # CORRECT - Context manager applied by caller
        def modify_object(context, obj):
            # Just do the core operation
            obj.location.x += 1
            
        # Caller manages the context
        with editor_context(context):
            modify_object(context, my_obj)
            
        # INCORRECT - Function trying to manage its own context
        def modify_object(context, obj):
            # Don't mix core logic with context management
            with editor_context(context):
                obj.location.x += 1  # This should be a separate function
        ```
  - Example:
    ```python
    # CORRECT - direct decoration
    @contextmanager
    def editor_context(context):
        initial_state = save_state()
        try:
            yield context
        finally:
            try:
                restore_state(initial_state)
            except Exception:
                # Log or handle cleanup errors
                pass
                
    # INCORRECT - breaks context manager protocol
    @contextmanager
    def _editor_context(context):
        # ...
        
    editor_context = _editor_context  # Don't do this!
    ```
- Use context override instead of modifying global state when possible
- Clean up any temporary editor state changes
- Use context managers (`with` statements) for temporary state changes
- Handle Python module caching and reloading:
  - Be aware of Python's module caching behavior in Blender
  - Use importlib.reload() when testing module changes
  - Clear sys.modules entries for fully fresh imports
  - Restart Blender for clean state when debugging imports
  - Example module reloading:
    ```python
    import importlib
    import sys
    
    # When changing module code:
    if "my_module" in sys.modules:
        importlib.reload(sys.modules["my_module"])
    import my_module
    
    # For complete reset:
    if "my_module" in sys.modules:
        del sys.modules["my_module"]
    import my_module  # Fresh import
    ```
  - Test code changes immediately:
  - Create dedicated test scripts for each module
  - Run tests after every file modification
  - Verify file contents match expected code
  - Example test workflow:
    ```python
    # reload_test.py
    import bpy
    import dev_reload
    import my_module
    
    # Force reload
    my_module = dev_reload.clean_reload("my_module")
    
    # Clear scene
    for obj in bpy.data.objects:
        bpy.data.objects.remove(obj, do_unlink=True)
        
    # Run test
    my_module.test_function()
    ```
  - Check file contents during development:
    ```python
    # Quick file content check
    with open("my_module.py", "r") as f:
        print(f.read())  # Verify content matches expected
    ```
  - Always test context managers after changes:
    ```python
    # Test context manager directly
    with my_context_manager():
        pass  # Should work without errors
    ```

- Verify filesystem state:
  - Check actual file contents on disk match expected code
  - Look for duplicate files in different locations
  - Verify Python path and import locations
  - Use absolute paths during development
  - Example filesystem checks:
    ```python
    # Check file location and content
    import os
    import sys
    
    # Print actual file location
    print(f"Module location: {my_module.__file__}")
    
    # Check Python path
    print("\nPython path:")
    for path in sys.path:
        print(f"  {path}")
        
    # Verify file contents
    def check_file(path):
        try:
            with open(path, 'r') as f:
                print(f"\nFile contents of {path}:")
                print(f.read())
        except Exception as e:
            print(f"Error reading {path}: {e}")
            
    # Check both possible locations
    check_file("./my_module.py")
    check_file(my_module.__file__)
    ```
  - Common filesystem issues:
    - Files saved to wrong location
    - Multiple copies of same file
    - Incorrect Python path
    - File permissions issues
    - Hidden backup files
    - Case sensitivity mismatches

- Know when to restart Blender:
  - Some changes require a complete Blender restart
  - Particularly when working with decorators
  - Common scenarios requiring restart:
    - Context manager definition changes
    - Decorator application changes
    - Import order issues with decorated functions
    - Stubborn module caching issues
  - Signs you need a restart:
    - Reloading modules doesn't fix the issue
    - File content looks correct but error persists
    - Decorators not working as expected
    - Context managers showing wrong behavior
  - Example restart workflow:
    ```python
    # If you see unexpected decorator behavior:
    # 1. Save all files
    # 2. Exit Blender completely
    # 3. Delete __pycache__ directories
    # 4. Restart Blender
    # 5. Import modules fresh
    ```

- Troubleshoot context manager errors:
  - Common context manager error patterns:
    ```python
    # TypeError: 'generator' object does not support the context manager protocol
    # This usually means:
    # 1. A regular function is being used as a context manager
    # 2. A context manager is defined incorrectly
    # 3. Module reload hasn't picked up decorator changes
    ```
  - Quick context manager checks:
    ```python
    # Check if function is a context manager
    from inspect import isgenerator
    
    def is_context_manager(obj):
        """Check if object is properly decorated as context manager."""
        return hasattr(obj, '__enter__') and hasattr(obj, '__exit__')
        
    def check_context_manager(name, obj):
        print(f"\nChecking {name}:")
        print(f"Is generator? {isgenerator(obj)}")
        print(f"Is context manager? {is_context_manager(obj)}")
        print(f"Has __enter__? {hasattr(obj, '__enter__')}")
        print(f"Has __exit__? {hasattr(obj, '__exit__')}")
        
    # Usage:
    check_context_manager("editor_context", editor_context)
    ```
  - Debug context manager usage:
    ```python
    # Test context manager separately
    try:
        with suspect_function() as ctx:
            pass
    except Exception as e:
        print(f"Context manager error: {e}")
        print(f"Type: {type(suspect_function)}")
    ```
  - Common fixes:
    - Ensure @contextmanager decorator is applied
    - Check import path is correct
    - Verify function isn't reassigned
    - Force module reload
    - Clear __pycache__
    - Restart Blender

- Handle Blender-specific module reloading:
    - Be aware of both Python caching and Blender registration
    - Use dev_reload.py for Blender-safe module reloading
    - Place dev_reload.py in your scripts directory
    - Reload both Python modules and Blender registrations
    - Example Blender development workflow:
      ```python
      # In Blender text editor, create reload.py:
      import dev_reload
      import utilities
      
      # When editing code:
      utilities = dev_reload.clean_reload("utilities")
      
      # To force complete reload including Blender registration:
      bpy.ops.script.reload()
      
      # To prevent .pyc creation during development:
      import os
      os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
      ```
    - Example dev_reload.py for Blender:
      ```python
      # dev_reload.py
      import os
      import sys
      import importlib
      
      def clean_reload(module_name):
          """Force reload a module and its submodules."""
          # Remove .pyc files
          module = sys.modules.get(module_name)
          if module:
              module_dir = os.path.dirname(module.__file__)
              cache_dir = os.path.join(module_dir, "__pycache__")
              if os.path.exists(cache_dir):
                  for cache_file in os.listdir(cache_dir):
                      if cache_file.startswith(module_name):
                          os.remove(os.path.join(cache_dir, cache_file))
          
          # Clear from sys.modules
          to_reload = [
              m for m in sys.modules
              if m == module_name or m.startswith(module_name + ".")
          ]
          for m in to_reload:
              del sys.modules[m]
              
          # Fresh import
          return importlib.import_module(module_name)
      
      # Usage:
      # import dev_reload
      # my_module = dev_reload.clean_reload("my_module")
      ```
    - For quick testing, delete __pycache__:
      ```bash
      find . -type d -name "__pycache__" -exec rm -r {} +
      ```
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