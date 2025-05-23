import os
import bpy
import random
from add_3d_text import add_text
from chessboard import ChessBoard
from blender_helper import *
from list_devices import *
from material_helpers import *

print_cuda_devices() # also seems to force it to use CUDA so yay

# Define materials for the chessboard
black_material = create_basic_color_material("Black", (0.02, 0.02, 0.02, 1))
white_material = create_basic_color_material("White", (0.8, 0.8, 0.8, 1))
red_material = create_basic_color_material("Red", (.5, .1, .1, 1))
cyan_material = create_basic_color_material("Cyan", (0, 1, 1, 1))
wood_material = create_wood_material()
mirror_material = create_mirror_material()


bpy.data.objects.remove(bpy.data.objects["Cube"])
# bpy.data.cameras.remove(bpy.data.cameras["Camera"])
# bpy.data.lights.remove(bpy.data.lights["Light"])
    
def import_piece(piece_name, mat):
    # Get the path to the assets folder using PYTHONPATH
    # Assuming 'assets' is in your PYTHONPATH
    filepath = os.path.join(os.environ.get('PYTHONPATH', ''), 'assets', 'chess_pieces', piece_name + '.blend')
    
    # Import the object from the blend file
    with bpy.data.libraries.load(filepath) as (data_from, data_to):
        if piece_name in data_from.objects:
            data_to.objects = [piece_name]
    
    # Link the object to the current scene
    scene = bpy.context.scene
    for obj in data_to.objects:
        if obj is not None:
            scene.collection.objects.link(obj)
    apply_material_to_mesh(obj, mat)
            
    return obj


cb = ChessBoard(black_material=black_material, white_material=white_material, wood_material=wood_material)

queen_object = import_piece("queen", white_material)
king_object = import_piece("king", black_material)
pawn_object = import_piece("pawn", mirror_material)
bishop_object = import_piece("bishop", white_material)
rook_object = import_piece("rook", red_material)

pieces = [queen_object, king_object, pawn_object, bishop_object, rook_object]

for piece in pieces:
    reset_transformations(piece)
    piece.scale = (.08, .08, .08)
    reset_transformations(piece)
    center_mesh_vertical(piece)
    reset_transformations(piece)
    apply_smooth_shading(piece)

cb.place_piece(rook_object, 'c', '2')  # Move rook to a1
cb.place_piece(king_object, 'g', '5')  # Move king to g5
cb.place_piece(pawn_object, 'c', '3')  # Move pawn to c3
cb.place_piece(bishop_object, 'g', '1')  # Move bishop to g1
cb.place_piece(queen_object, 'c', '8')  # Move queen to c8

# there is almost certainly a more blender-y way to do this as with many things here
# but for now I'll python brute force it
delta = 0.45
obj_grid_width = 7;
space_grid_width = delta * obj_grid_width
min_x = -space_grid_width / 2
min_y = -space_grid_width / 2
min_z = -space_grid_width / 2
grid_center_x = 0
grid_center_y = 0
grid_center_z = 13
for i in range(obj_grid_width):
    for j in range(obj_grid_width):
        for k in range(obj_grid_width):
            if (random.uniform(0, 4) < 2):
                continue # space out the pieces a bit towards the bottom
            if (i + 4 * j + 16 * k) % 2 == 1:
                mat = white_material
            else:
                mat = black_material
            obj = import_piece("pawn", mat)
            reset_transformations(piece)
            obj.rotation_euler = (random.uniform(0, 360), random.uniform(0, 360), random.uniform(0, 360))
            obj.scale = (.08, .08, .08)
            reset_transformations(piece)
            center_mesh_vertical(piece)
            reset_transformations(piece)
            apply_smooth_shading(piece)
            x = delta * i + min_x + grid_center_x
            y = delta * j + min_y + grid_center_y
            z = delta * k + min_z + grid_center_z
            obj.location.x += x
            obj.location.y += y
            obj.location.z += z
            pieces.append(obj)

create_sky_cube(cyan_material, size=100)

def add_floor_plane(size=10, z_position=-0.1):
    """
    Adds a plane to act as a floor
    Args:
        size: Size of the plane
        z_position: Height position of the plane
    """
    bpy.ops.mesh.primitive_plane_add(size=size)
    plane = bpy.context.active_object
    plane.location.z = z_position
    
    # Create and assign stucco material
    stucco_material = create_stucco_material()
    plane.data.materials.append(stucco_material)
    
    return plane


print("adding floor plane")

floor_plane = add_floor_plane(z_position=-0.5)

def setup_rigid_body_world(substeps=40, solver_iterations=40):
    scene = bpy.context.scene
    
    # Create rigid body world if it doesn't exist
    if scene.rigidbody_world is None:
        bpy.ops.rigidbody.world_add()
    
    # Configure the rigid body world
    scene.rigidbody_world.enabled = True
    scene.rigidbody_world.substeps_per_frame = substeps
    scene.rigidbody_world.solver_iterations = solver_iterations
    scene.rigidbody_world.time_scale = .333


def add_rigid_body(obj, body_type='ACTIVE', mass=1.0, friction=0.5, bounce=0.0, 
                  shape='CONVEX_HULL', mesh_source='FINAL'):
    # Select and make active
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    
    # Add rigid body if it doesn't exist
    if not obj.rigid_body:
        bpy.ops.rigidbody.object_add()
    
    # Configure rigid body settings
    rb = obj.rigid_body
    rb.type = body_type
    rb.mass = mass
    rb.friction = friction
    rb.restitution = bounce
    rb.collision_shape = shape
    rb.mesh_source = mesh_source
    rb.use_margin = False
    
    return rb

print("setting up rigid body world")

# Setup physics world if needed
setup_rigid_body_world()

wernerware_text = add_text("Wernerware", white_material, 0.25, "WernerwareText", (0, .25, 1.5), (0.5, 0.5, 0.5))
wernerware_text.rotation_euler = (0.1, 0.1, 0.0)
apply_smooth_shading(wernerware_text)
chess_text = add_text("CHESS", mirror_material, 0.25, "ChessText", (0, -.25, 5), (1.0, 1.0, 1.0))
chess_text.rotation_euler = (0.1, 0.1, 0.0)
apply_smooth_shading(chess_text)

print("adding rigid bodies to objects")
# Add physics to each piece
for piece in pieces:
    add_rigid_body(piece,
                    body_type='ACTIVE',
                    mass=1.0,
                    friction=0.9,
                    bounce=0.6)
add_rigid_body(wernerware_text,
                    body_type='ACTIVE',
                    mass=1.0,
                    friction=0.9,
                    bounce=0.4)
add_rigid_body(chess_text,
                    body_type='ACTIVE',
                    mass=1.0,
                    friction=0.9,
                    bounce=0.4)
add_rigid_body(cb.board_obj,
                    body_type='PASSIVE',
                    mass=0,
                    friction=0.9,
                    bounce=0.4)
add_rigid_body(floor_plane,
                    body_type='PASSIVE',
                    mass=0,
                    friction=0.9,
                    bounce=0.1)

print("doing some render settings")

# render/camera config
bpy.data.cameras["Camera"].lens = 110.0
enable_cuda_gpu(bpy.context.scene)

print("baking the physics")
start_frame = 1;
end_frame = 10;
scene = bpy.context.scene
setup_eevee_render()

scene.frame_start = start_frame
scene.frame_end = end_frame

# Call the function to bake
bake_rigid_body_simulation(start_frame=start_frame, end_frame=end_frame, scene=scene)

bpy.data.orphans_purge(do_recursive=True)

scene.render.image_settings.file_format = "PNG"
filepath = os.path.join(os.environ.get('PYTHONPATH', ''), 'renders', '')

print(f"saving the render to {filepath}")
scene.render.filepath = filepath

print("saving animation")
bpy.ops.wm.save_mainfile(filepath="/tmp/saved.blend")

print("Create blender file script done")
os._exit(os.EX_OK)