import bpy
import bmesh
import json
from mathutils import Vector
from utilities import export_mesh_data, import_mesh_data, setup_render_defaults

def main():
    # Clear existing mesh objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Create the original sphere
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=(-2, 0, 0))
    original_sphere = bpy.context.active_object

    # Export the sphere data to JSON string
    sphere_data = export_mesh_data(original_sphere)
    
    # Import the sphere data to create a new object
    imported_sphere = import_mesh_data(sphere_data, "ImportedSphere")
    imported_sphere.location = Vector((2, 0, 0))  # Move it to the right
    
    # Set up materials for surface and edges
    surface_material = bpy.data.materials.new(name="SurfaceMaterial")
    surface_material.use_nodes = True
    surface_nodes = surface_material.node_tree.nodes
    surface_nodes["Principled BSDF"].inputs[0].default_value = (0.5, 0.5, 0.5, 1)  # Grey color

    edge_material = bpy.data.materials.new(name="EdgeMaterial")
    edge_material.use_nodes = True
    edge_nodes = edge_material.node_tree.nodes
    edge_nodes["Principled BSDF"].inputs[0].default_value = (1, 0, 0, 1)  # Red color
    
    # Apply materials and enable edge display
    for obj in [original_sphere, imported_sphere]:
        obj.data.materials.append(surface_material)  # Add grey surface material
        obj.show_wire = True  # Show wireframe
    
    # Set up camera and lighting
    bpy.ops.object.camera_add(location=(0, -10, 0), rotation=(1.5708, 0, 0))
    camera = bpy.context.active_object
    
    bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
    
    # Set up render settings
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.render.film_transparent = True
    render_dir = setup_render_defaults()
    
    # Set active camera
    bpy.context.scene.camera = camera
    
    # Render the current frame and save it
    bpy.ops.render.render(write_still=True)

if __name__ == "__main__":
    main()