import bpy
import pytest
import math
import bmesh
from mathutils import Vector
from shell_with_holes import create_shell_with_holes

class TestShellWithHoles:
    @classmethod
    def setup_class(cls):
        # Setup - create a shell with default holes
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        
        # Create base sphere
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 0))
        base_obj = bpy.context.active_object
        base_obj.name = "test_shell"
        
        # Create shell with holes
        create_shell_with_holes(bpy.context, "test_shell", shell_thickness=0.1)
        cls.shell_obj = bpy.data.objects["test_shell"]

    def test_basic_mesh_statistics(self):
        """Test if the mesh has expected number of vertices, edges, and faces"""
        mesh = self.shell_obj.data
        
        # Basic checks
        assert len(mesh.vertices) > 0, "Mesh should have vertices"
        assert len(mesh.edges) > 0, "Mesh should have edges"
        assert len(mesh.polygons) > 0, "Mesh should have faces"
        
        # Check if holes affected topology (should have more elements than base sphere)
        base_sphere_verts = 482  # Standard UV sphere default
        assert len(mesh.vertices) > base_sphere_verts, "Should have more vertices than base sphere"

    def test_shell_thickness(self):
        """Test if the shell thickness is approximately correct"""
        mesh = self.shell_obj.data
        bm = bmesh.new()
        bm.from_mesh(mesh)
        
        # Sample some vertices and measure thickness
        thickness_measurements = []
        for v in bm.verts:
            # Cast ray from vertex along normal to find opposite surface
            hit, loc, norm, _ = self.shell_obj.ray_cast(v.co, v.normal)
            if hit:
                thickness = (Vector(loc) - Vector(v.co)).length
                thickness_measurements.append(thickness)
        
        avg_thickness = sum(thickness_measurements) / len(thickness_measurements)
        # Allow for some deviation due to surface curvature
        assert 0.09 < avg_thickness < 0.11, f"Shell thickness {avg_thickness} not within expected range"
        
        bm.free()

    def test_hole_positions(self):
        """Test if holes are present at expected positions"""
        default_hole_positions = [
            (1, 0, 0), (-1, 0, 0),
            (0, 1, 0), (0, -1, 0),
            (0, 0, 1), (0, 0, -1)
        ]
        
        mesh = self.shell_obj.data
        
        for pos in default_hole_positions:
            # Test if there are edges near each hole position
            found_hole = False
            for edge in mesh.edges:
                # Get edge center
                center = (mesh.vertices[edge.vertices[0]].co + 
                         mesh.vertices[edge.vertices[1]].co) / 2
                # Check if edge is near hole position
                distance = (Vector(pos) - center).length
                if distance < 0.3:  # Tolerance for hole edge detection
                    found_hole = True
                    break
            assert found_hole, f"No hole found at position {pos}"

    def test_mesh_integrity(self):
        """Test for mesh integrity and manifold properties"""
        bm = bmesh.new()
        bm.from_mesh(self.shell_obj.data)
        
        # Check for non-manifold elements
        non_manifold_verts = [v for v in bm.verts if not v.is_manifold]
        non_manifold_edges = [e for e in bm.edges if not e.is_manifold]
        
        assert len(non_manifold_verts) == 0, "Found non-manifold vertices"
        assert len(non_manifold_edges) == 0, "Found non-manifold edges"
        
        bm.free()

    def test_volume_and_surface_area(self):
        """Test if volume and surface area are within expected ranges"""
        # Calculate volume using bmesh
        bm = bmesh.new()
        bm.from_mesh(self.shell_obj.data)
        volume = bm.calc_volume()
        
        # Calculate surface area
        surface_area = sum(f.calc_area() for f in bm.faces)
        
        # Expected ranges for a sphere with r=1 and thickness=0.1
        # Volume should be less than solid sphere but more than hollow sphere
        max_volume = 4/3 * math.pi  # Volume of solid sphere with r=1
        min_volume = 4/3 * math.pi * 0.8  # Approximate for hollow sphere
        
        assert min_volume < volume < max_volume, f"Volume {volume} outside expected range"
        
        # Surface area should be greater than original sphere due to holes
        min_surface_area = 4 * math.pi  # Surface area of unit sphere
        assert surface_area > min_surface_area, f"Surface area {surface_area} too small"
        
        bm.free()

    def test_normal_consistency(self):
        """Test if mesh normals are consistent"""
        mesh = self.shell_obj.data
        
        # Check if all face normals point outward
        for face in mesh.polygons:
            # For a sphere-like object, normal should point somewhat away from center
            face_center = face.center
            dot_product = face_center.dot(face.normal)
            assert dot_product > 0, f"Face normal inconsistency at face {face.index}"

    @classmethod
    def teardown_class(cls):
        # Cleanup
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
