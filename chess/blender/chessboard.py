import bpy
import bmesh
from blender_helper import reset_transformations


class ChessBoard():
    def __init__(self, black_material, white_material, wood_material):
        self.black_material = black_material
        self.white_material = white_material
        self.wood_material = wood_material
        self.board_obj = None # initailized in create_chessboard()
        coords = self.__create_chessboard__()
        self.coords_by_file_and_rank = {}
        for coord in coords:
            self.coords_by_file_and_rank[(coord[3], coord[4])] = coord

    def __create_chessboard__(self):
        # Create a cube mesh
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=2.0)
        
        # Scale to make it more board-like (thinner in Z direction)
        for v in bm.verts:
            v.co.z *= 0.1
        
        # Get the top face for subdivision
        top_face = None
        for face in bm.faces:
            if face.normal.z > 0.9:  # Finding the top face
                top_face = face
                break
        
        # Subdivide the top face into 8x8 grid
        bmesh.ops.subdivide_edges(bm,
            edges=top_face.edges,
            cuts=7,  # This creates 8x8 grid
            use_grid_fill=True)
        
        # Create a new mesh and object
        mesh = bpy.data.meshes.new('ChessBoard')
        self.board_obj = bpy.data.objects.new('ChessBoard', mesh)
        
        # Link object to scene
        bpy.context.collection.objects.link(self.board_obj)
        
        # Write the bmesh into the mesh
        bm.to_mesh(mesh)
        bm.free()
        
        self.board_obj.data.materials.append(self.white_material)
        self.board_obj.data.materials.append(self.black_material)
        self.board_obj.data.materials.append(self.wood_material)
        
        # Assign materials in a checkerboard pattern
        bpy.context.view_layer.objects.active = self.board_obj
        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(self.board_obj.data)
        
        for face in bm.faces:
            if face.normal.z > 0.9:  # Top faces get checkerboard pattern
                center = face.calc_center_median()
                # Convert world position to grid position
                x = int((center.x + 1) * 4)  # +1 to shift from -1,1 to 0,8 range
                y = int((center.y + 1) * 4)
                # Set material index based on checkerboard pattern
                face.material_index = (x + y + 1) % 2
            else:  # Sides and bottom get wood material
                face.material_index = 2
        
        # Update the mesh and return to object mode
        bmesh.update_edit_mesh(self.board_obj.data)
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Store coordinates and chess positions
        positions = []
        for face in self.board_obj.data.polygons:
            if face.normal.z > 0.9:  # Only top faces
                # Get center of face in world space
                center = face.center
                
                # Convert world position to chess coordinates
                x = int((center.x + 1) * 4)  # +1 to shift from -1,1 to 0,7 range
                y = int((center.y + 1) * 4)
                
                # Convert to chess notation (file, rank)
                file = chr(97 + x)  # 'a' through 'h'
                rank = str(y + 1)   # '1' through '8'
                
                # Store position tuple: (x, y, z, file, rank, is_white)
                positions.append((
                    center.x,
                    center.y,
                    0.1,  # Height above board
                    file,
                    rank,
                    face.material_index == 0  # True for white squares
                ))
        reset_transformations(self.board_obj)

        return positions


    def place_piece(self, piece_obj, file, rank):
        """
        Move a piece to a specific chess square
        Args:
            piece_obj: The Blender object to move
            file: Chess file (a-h)
            rank: Chess rank (1-8)
        """
        # Get the coordinates for the target square
        target_coords = self.coords_by_file_and_rank.get((file, rank))
        if target_coords is None:
            raise ValueError(f"No coordinates found for rank {rank} and file {file}")

        # calculate piece placement with a tiny space buffer so the physics doesn't cause the pieces to hop off the board
        piece_z = 0.01 + self.board_obj.dimensions.z / 2 + piece_obj.dimensions.z / 2

        # Move the piece to the target location
        # The first two values in target_coords are the X,Y coordinates
        piece_obj.location = (target_coords[0], target_coords[1], piece_z)
