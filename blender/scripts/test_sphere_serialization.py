import bpy
import pytest
from utilities import export_mesh_data, import_mesh_data

class TestSphereImportExport:
    def setup_class(cls):
        # Delete the default cube if it exists
        if 'Cube' in bpy.data.objects:
            bpy.data.objects['Cube'].select_set(True)
            bpy.ops.object.delete()

    def test_sphere_serialization(self):
        # Create a UV sphere
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=(0, 0, 0))
        original_sphere = bpy.context.active_object
        
        expected_faces = len(original_sphere.data.polygons)
        expected_vertices = len(original_sphere.data.vertices)
        
        # Export the sphere to JSON
        json_data = export_mesh_data(original_sphere)
        
        # Delete the original sphere
        bpy.data.objects.remove(original_sphere, do_unlink=True)
        
        # Import the sphere from JSON
        restored_sphere = import_mesh_data(json_data, "RestoredSphere")
        
        # Verify the restored sphere
        assert restored_sphere is not None
        assert restored_sphere.type == 'MESH'
        
        assert len(restored_sphere.data.polygons) == expected_faces
        assert len(restored_sphere.data.vertices) == expected_vertices

    def teardown_class(cls):
        # Clean up any objects created during testing
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()