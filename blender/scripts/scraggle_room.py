import bpy
import bmesh
import math
import random
import mathutils

# makes a scraggly room-shaped mesh

print("======")

# Select all objects
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='SELECT')

# Delete all selected objects
bpy.ops.object.delete()

# Create a new mesh and object
mesh = bpy.data.meshes.new('PolygonMesh')
polygon_obj = bpy.data.objects.new('PolygonObject', mesh)

# Link the object to the scene
scene = bpy.context.scene
scene.collection.objects.link(polygon_obj)

# Set the object as the active object
bpy.context.view_layer.objects.active = polygon_obj
polygon_obj.select_set(True)

# Create a new bmesh object and add a polygon
bm = bmesh.new()

sides = 40
max_rad = 5
min_rad = 2
verts = []
locs = []
for s in range(sides):
    theta = math.pi * 2 * s / sides
    radius = random.random() * (max_rad - min_rad) + min_rad
    loc = (math.cos(theta) * radius, math.sin(theta) * radius, 0)
    vert = bm.verts.new(loc)
    verts.append(vert)
    locs.append(loc)

# Update the bmesh and create the face
bm.faces.new(verts)
bm.to_mesh(mesh)
bm.free()

# Update the mesh with the new data
mesh.update()

def extrude_face(obj, distance):
    # Get the object
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Select all faces
    bpy.ops.mesh.select_all(action='SELECT')
    
    # Extrude the faces along their normals by the specified distance
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, distance)})
    
    # Return to object mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
extrude_face(polygon_obj, .2)
bpy.ops.object.mode_set(mode='EDIT')

bm = bmesh.from_edit_mesh(polygon_obj.data)
selected_faces = [f for f in bm.faces if f.select]

if len(selected_faces) != 1:
    raise Exception("Expected single selected face, facing up")
    
bpy.ops.mesh.inset(thickness=0.2, depth=0, release_confirm=True)

curr_selection = [f for f in bm.faces if f.select][0]
curr_selection.select = False

up = mathutils.Vector((0.0,0.0,1.0))
for f in bm.faces:
    f_norm = mathutils.Vector(f.normal)
    if f_norm.angle(up) < 0.01 and f != curr_selection:
        f.select = True
        
bpy.ops.mesh.extrude_context_move(TRANSFORM_OT_translate={"value":(0, 0, 0.75)})

def get_random_point_along_line(t1, t2):
    d1 = t1[0] - t2[0]
    d2 = t1[1] - t2[1]
    d3 = t1[2] - t2[2]
    rnd = random.random()
    return (t2[0] + rnd * d1, t2[1] + rnd * d2, t2[2] + rnd * d3)

def avg_points(pts):
    xsum = sum([p[0] for p in pts])
    ysum = sum([p[1] for p in pts])
    zsum = sum([p[2] for p in pts])
    pts_ct = len(pts)
    return (xsum / pts_ct, ysum / pts_ct, zsum / pts_ct)

def get_random_place_in_triangle(t1):
    p1 = t1[0]
    p2 = t1[1]
    p3 = t1[2]
    m1 = get_random_point_along_line(p1, p2)
    m2 = get_random_point_along_line(p2, p3)
    m3 = get_random_point_along_line(p3, p1)
    return avg_points([m1, m2, m3])

def get_all_triangles(vs):
    locs = [v for v in vs]
    centers = [(0.0,0.0,0.0)] * len(locs)
    offByOnes = locs[1:]
    offByOnes.append(locs[0])
    return [t for t in zip(locs, centers, offByOnes)]

def get_random_inbounds(ts):
    r_ind = random.randint(0, len(ts) - 1)
    at_floor = get_random_place_in_triangle(ts[r_ind])
    return (at_floor[0], at_floor[1], 0.5)

ts = get_all_triangles(locs)
cam_loc = get_random_inbounds(ts)

# Return to object mode
bpy.ops.object.mode_set(mode='OBJECT')

# Add a new camera
bpy.ops.object.camera_add(location=cam_loc, rotation=(1.1, 0, 0))
camera = bpy.context.object
camera.name = "Default_Camera"

# Set the new camera as the active camera
bpy.context.scene.camera = camera


def look_at(obj_camera, ptup):
    pvec = mathutils.Vector(ptup)
    loc_camera = obj_camera.matrix_world.to_translation()

    direction = pvec - loc_camera
    # point the cameras '-Z' and use its 'Y' as up
    rot_quat = direction.to_track_quat('-Z', 'Y')

    # assume we're using euler rotation
    obj_camera.rotation_euler = rot_quat.to_euler()
    
look_loc = get_random_inbounds(ts)
look_at(camera, look_loc)

# Add a new light
light_loc = get_random_inbounds(ts)
light1 = bpy.ops.object.light_add(type='POINT', location=light_loc)
light = bpy.context.object
light.name = "Default_Light"
light.data.energy = 1000

# Set the file path where you want to save the rendered image
file_path = "C:\\Users\\danie\\blender_pics\\" + str(random.randint(0,1000000))

# Set the render settings
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.filepath = file_path

# Render the current frame and save it
bpy.ops.render.render(write_still=True)

print(f"Rendered image saved to {file_path}")