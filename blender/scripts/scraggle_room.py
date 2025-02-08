import bpy
import bmesh
import math
import random
import mathutils

print("======")

# Select all objects
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='SELECT')

# Delete all selected objects
bpy.ops.object.delete()

# Add a new camera
bpy.ops.object.camera_add(location=(3, -8, 4), rotation=(1.1, 0, 0))
camera = bpy.context.object
camera.name = "Default_Camera"

# Set the new camera as the active camera
bpy.context.scene.camera = camera

# Add a new light
light1 = bpy.ops.object.light_add(type='POINT', location=(0, 0, 3))
light = bpy.context.object
light.name = "Default_Light"
light.data.energy = 1000

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
for s in range(sides):
    theta = math.pi * 2 * s / sides
    radius = random.random() * (max_rad - min_rad) + min_rad
    vert = bm.verts.new((math.cos(theta) * radius, math.sin(theta) * radius, 0))
    verts.append(vert)

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

def get_random_place_in_triangle(p1, p2, p3):
    pass