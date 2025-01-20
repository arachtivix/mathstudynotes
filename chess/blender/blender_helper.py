import bpy


def reset_transformations(obj):
    # Deselect all objects and select our target object
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    
    # Apply all transformations to the mesh data
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

def setup_cycles_render(use_denoise=False, samples=100):
    """
    Set up Cycles render engine and configure denoising
    Args:
        use_denoise: Boolean to enable/disable denoising (default: False)
    """
    # Get the scene context
    scene = bpy.context.scene
    
    # Set render engine to Cycles
    scene.render.engine = 'CYCLES'
    
    # Configure denoising
    if hasattr(scene, 'cycles'):  # Check if cycles is available
        # Disable denoising in viewport
        scene.cycles.use_denoising = use_denoise
        scene.cycles.samples = samples
        
        # Disable denoising in view layer
        for layer in scene.view_layers:
            if hasattr(layer, 'cycles'):
                layer.cycles.denoising_store_passes = False
                layer.cycles.use_denoising = False


def setup_eevee_render():
    """
    Set up Eevee render engine
    """
    # Get the scene context
    scene = bpy.context.scene

    # Set render engine to Eevee
    scene.render.engine = 'BLENDER_EEVEE'


def center_mesh_vertical(obj):
    """
    Transforms the vertices of a mesh so that the highest and lowest z-coordinates 
    are equidistant from the xy plane.
    
    Args:
        obj: Blender mesh object to transform
    """
    if obj.type != 'MESH':
        return
    
    # Get mesh data in world space
    mesh = obj.data
    matrix_world = obj.matrix_world
    
    # Get all z-coordinates of vertices in world space
    z_coords = [(matrix_world @ vert.co).z for vert in mesh.vertices]
    
    if not z_coords:
        return
        
    # Find highest and lowest points
    max_z = max(z_coords)
    min_z = min(z_coords)
    
    # Calculate the current center and desired offset
    current_center = (max_z + min_z) / 2
    offset = -current_center  # This will center the mesh at z=0
    
    # Create translation matrix
    translation = obj.matrix_world.copy()
    translation.translation.z += offset
    
    # Apply the transformation
    obj.matrix_world = translation


def apply_material_to_mesh(mesh, material):
    """
    Apply a material to a mesh object
    Args:
        mesh: Blender mesh object
        material: Blender material object
    """
    if mesh.data.materials:
        mesh.data.materials[0] = material
    else:
        mesh.data.materials.append(material)


def create_wood_material():
    wood_material = bpy.data.materials.new(name="Wood")
    wood_material.use_nodes = True
    wood_material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.4, 0.2, 0.0, 1)

    nodes = wood_material.node_tree.nodes
    links = wood_material.node_tree.links

    # Clear default nodes
    nodes.clear()

    # Create nodes for wood texture
    output = nodes.new('ShaderNodeOutputMaterial')
    principled = nodes.new('ShaderNodeBsdfPrincipled')
    tex_coord = nodes.new('ShaderNodeTexCoord')
    mapping = nodes.new('ShaderNodeMapping')
    wood_tex = nodes.new('ShaderNodeTexNoise')
    color_ramp = nodes.new('ShaderNodeValToRGB')

    # Set up wood texture properties
    wood_tex.inputs['Scale'].default_value = 20.0
    wood_tex.inputs['Detail'].default_value = 10.0

    # Setup color ramp for wood color
    color_ramp.color_ramp.elements[0].position = 0.3
    color_ramp.color_ramp.elements[0].color = (0.2, 0.1, 0.05, 1.0)  # Dark brown
    color_ramp.color_ramp.elements[1].position = 0.7
    color_ramp.color_ramp.elements[1].color = (0.4, 0.2, 0.1, 1.0)  # Light brown

    # Connect nodes
    links.new(tex_coord.outputs['Generated'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], wood_tex.inputs['Vector'])
    links.new(wood_tex.outputs['Fac'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], principled.inputs['Base Color'])
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])

    # Set material roughness
    principled.inputs['Roughness'].default_value = 0.7
    return wood_material


def create_mirror_material():
    # Create mirror material
    mirror_material = bpy.data.materials.new(name="Mirror")
    mirror_material.use_nodes = True
    nodes = mirror_material.node_tree.nodes
    links = mirror_material.node_tree.links

    # Clear default nodes
    nodes.clear()

    # Create nodes for mirror material
    output = nodes.new('ShaderNodeOutputMaterial')
    principled = nodes.new('ShaderNodeBsdfPrincipled')

    # Set up mirror properties
    principled.inputs['Base Color'].default_value = (1, 1, 1, 1)  # White
    principled.inputs['Metallic'].default_value = 1.0  # Full metallic
    principled.inputs['Roughness'].default_value = 0.0  # No roughness for perfect mirror
    principled.inputs['Specular'].default_value = 1.0  # Full specular
    principled.inputs['IOR'].default_value = 2.0  # Higher IOR for more reflectivity

    # Connect nodes
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    return mirror_material


def create_sky_cube(material, size=10.0):
    """
    Creates a cube with faces visible from the inside
    
    Args:
        material: Blender material to apply to the cube
        size: Size of the cube (default: 1.0)
    
    Returns:
        The created cube object
    """
    # Create a cube
    bpy.ops.mesh.primitive_cube_add(size=size)
    cube = bpy.context.active_object
    
    # Switch to edit mode
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Ensure we're in face selection mode
    bpy.context.tool_settings.mesh_select_mode = (False, False, True)
    
    # Select all faces
    bpy.ops.mesh.select_all(action='SELECT')
    
    # Recalculate normals inside
    bpy.ops.mesh.normals_make_consistent(inside=True)
    
    # Return to object mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Apply the material
    apply_material_to_mesh(cube, material)
    
    return cube


def apply_smooth_shading(obj):
    """
    Applies smooth shading to a given object by setting all polygons to smooth
    and enabling auto smooth normals.
    
    Args:
        obj: Blender object to smooth
    """
    if obj.type != 'MESH':
        return
        
    # Get the mesh data
    mesh = obj.data
    
    # Enable auto smooth
    mesh.use_auto_smooth = True
    # mesh.auto_smooth_angle = 3.14159  # 180 degrees in radians
    
    # Set all polygons to smooth
    for face in mesh.polygons:
        face.use_smooth = True
        
    # Optional: Recalculate normals (outside)
    import bmesh
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()


def bake_rigid_body_simulation(start_frame, end_frame, scene):
    """
    Bakes the rigid body simulation for the entire frame range of the scene
    """
    
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