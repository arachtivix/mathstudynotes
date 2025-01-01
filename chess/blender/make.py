import os
import bpy
from add_3d_text import add_text
from chessboard import ChessBoard
from blender_helper import reset_transformations, setup_cycles_render, center_mesh_vertical
from blender_helper import apply_material_to_mesh, create_wood_material, create_mirror_material
from blender_helper import create_basic_color_material, create_sky_cube, apply_smooth_shading

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

wernerware_text = add_text("Wernerware", white_material, 0.25, "WernerwareText", (0, .25, 1.5), (0.5, 0.5, 0.5))
chess_text = add_text("CHESS", mirror_material, 0.25, "ChessText", (0, -.25, 3), (1.0, 1.0, 1.0))
    
def import_piece(piece_name, mat):
    # Get the path to the assets folder using PYTHONPATH
    # Assuming 'assets' is in your PYTHONPATH
    filepath = os.path.join(os.environ.get('PYTHONPATH', ''), 'assets', piece_name + '.blend')
    
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

# there is almost certainly a more blender-y way to do this as with many things here
# but for now I'll python brute force it
falling_pawns = []
delta = 0.3
obj_grid_width = 5;
space_grid_width = delta * obj_grid_width
min_x = -space_grid_width / 2
min_y = -space_grid_width / 2
min_z = -space_grid_width / 2
grid_center_x = 0
grid_center_y = 0
grid_center_z = 6
for i in range(5):
    for j in range(5):
        for k in range(5):
            if (i + 4 * j + 16 * k) % 2 == 1:
                mat = white_material
            else:
                mat = black_material
            obj = import_piece("pawn", mat)
            x = delta * i + min_x + grid_center_x
            y = delta * j + min_y + grid_center_y
            z = delta * k + min_z + grid_center_z
            obj.location = (x, y, z)
            obj.scale = (.08, .08, .08)
            falling_pawns.append(obj)


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

create_sky_cube(cyan_material, size=100)


def create_stucco_material():
    """Creates a material that looks like stucco"""
    material = bpy.data.materials.new(name="Stucco")
    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    
    # Clear default nodes
    nodes.clear()
    
    # Create nodes
    output = nodes.new('ShaderNodeOutputMaterial')
    principled = nodes.new('ShaderNodeBsdfPrincipled')
    noise = nodes.new('ShaderNodeTexNoise')
    bump = nodes.new('ShaderNodeBump')
    
    # Configure noise texture
    noise.inputs['Scale'].default_value = 50  # Adjust for texture density
    noise.inputs['Detail'].default_value = 8
    noise.inputs['Roughness'].default_value = 0.7
    
    # Configure bump
    bump.inputs['Strength'].default_value = 0.2  # Adjust for bump intensity
    
    # Configure principled BSDF
    principled.inputs['Base Color'].default_value = (1.0, 0.85, 0.4, 1)
    principled.inputs['Roughness'].default_value = 0.9
    
    # Link nodes
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], principled.inputs['Normal'])
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    
    return material

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

def setup_rigid_body_world(substeps=10, solver_iterations=10):
    """
    Sets up the rigid body world simulation parameters
    
    Args:
        gravity: Tuple of (x, y, z) gravity vector (default: standard Earth gravity)
        substeps: Number of simulation substeps (default: 10)
        solver_iterations: Number of constraint solver iterations (default: 10)
    """
    scene = bpy.context.scene
    
    # Create rigid body world if it doesn't exist
    if scene.rigidbody_world is None:
        bpy.ops.rigidbody.world_add()
    
    # Configure the rigid body world
    scene.rigidbody_world.enabled = True
    scene.rigidbody_world.substeps_per_frame = substeps
    scene.rigidbody_world.solver_iterations = solver_iterations

def add_rigid_body(obj, body_type='ACTIVE', mass=1.0, friction=0.5, bounce=0.0, 
                  shape='CONVEX_HULL', mesh_source='FINAL'):
    """
    Adds rigid body physics to an object
    
    Args:
        obj: The object to add physics to
        body_type: 'ACTIVE' or 'PASSIVE' (default: 'ACTIVE')
        mass: Mass in kg (default: 1.0)
        friction: Friction coefficient (default: 0.5)
        bounce: Bounciness/Restitution (default: 0.0)
        shape: Collision shape ('BOX', 'SPHERE', 'CAPSULE', 'CYLINDER', 
               'CONE', 'CONVEX_HULL', 'MESH') (default: 'CONVEX_HULL')
        mesh_source: Source of mesh data ('FINAL', 'DEFORM', 'BASE') (default: 'FINAL')
    """
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
    
    return rb

print("setting up rigid body world")

# Setup physics world if needed
setup_rigid_body_world()

print("adding rigid bodies to objects")
# Add physics to each piece
for piece in pieces:
    add_rigid_body(piece,
                    body_type='ACTIVE',
                    mass=1.0,
                    friction=0.5,
                    bounce=0.1,
                    shape='MESH')
for falling_piece in falling_pawns:
    add_rigid_body(falling_piece,
                    body_type='ACTIVE',
                    mass=1.0,
                    friction=0.5,
                    bounce=0.1,
                    shape='MESH')
add_rigid_body(wernerware_text,
                    body_type='ACTIVE',
                    mass=1.0,
                    friction=0.5,
                    bounce=0.1,
                    shape='MESH')
add_rigid_body(cb.board_obj,
                    body_type='PASSIVE',
                    mass=0,
                    friction=0.5,
                    bounce=0.1,
                    shape='MESH')
add_rigid_body(floor_plane,
                    body_type='PASSIVE',
                    mass=0,
                    friction=0.5,
                    bounce=0.1,
                    shape='MESH')

print("doing some render settings")

# render/camera config
bpy.data.cameras["Camera"].lens = 110.0
setup_cycles_render(False)



def bake_rigid_body_simulation():
    """
    Bakes the rigid body simulation for the entire frame range of the scene
    """
    scene = bpy.context.scene
    
    # Deselect all objects first
    bpy.ops.object.select_all(action='DESELECT')
    
    # Select all objects that have rigid body physics
    for obj in scene.objects:
        if obj.rigid_body is not None:
            obj.select_set(True)
    
    # Ensure we have an active object
    for obj in scene.objects:
        if obj.select_get():
            bpy.context.view_layer.objects.active = obj
            break
            
    # Get the frame range from the scene
    start_frame = scene.frame_start
    end_frame = scene.frame_end
    
    # Ensure rigid body world exists
    if scene.rigidbody_world is None:
        bpy.ops.rigidbody.world_add()
    
    # Bake the simulation
    bpy.ops.object.mode_set(mode='OBJECT')
    print("baking physics - just about to throw it at blender")
    try:
        area = [a for a in bpy.context.screen.areas if a.type=="VIEW_3D"][0]
        with bpy.context.temp_override(area=area):
            bpy.ops.rigidbody.bake_to_keyframes(
                frame_start=start_frame,
                frame_end=end_frame
            )
        print("Baking completed successfully")
    except Exception as e:
        print(f"Error during baking: {e}")

print("baking the physics")

# Call the function to bake
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 150
bake_rigid_body_simulation()

bpy.data.orphans_purge(do_recursive=True)

scene = bpy.context.scene
scene.render.image_settings.file_format = "PNG"
filepath = os.path.join(os.environ.get('PYTHONPATH', ''), 'renders', '')
print(f"saving the render to {filepath}")
scene.render.filepath = filepath

print("saving animation")
bpy.ops.wm.save_mainfile(filepath="/tmp/saved.blend")

print("Create blender file script done")
os._exit(os.EX_OK)