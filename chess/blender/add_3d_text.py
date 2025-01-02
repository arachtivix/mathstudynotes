import bpy
from blender_helper import apply_material_to_mesh


def add_text(text, material, extrude_amt, objName, loc, scale):
    # Create a new text object
    text_data = bpy.data.curves.new(name=objName + "data", type='FONT')
    text_obj = bpy.data.objects.new(name=objName, object_data=text_data)
    bpy.context.scene.collection.objects.link(text_obj)

    # Set the text content
    text_data.body = text

    # Position and scale the text
    text_obj.location = (0, 0, 0)
    text_obj.data.align_x = 'CENTER'
    text_obj.data.align_y = 'CENTER'

    # Select the text object
    bpy.context.view_layer.objects.active = text_obj
    text_obj.select_set(True)

    # Convert text to mesh
    bpy.ops.object.convert(target='MESH')

    # Enter edit mode
    bpy.ops.object.mode_set(mode='EDIT')

    # Select all vertices
    bpy.ops.mesh.select_all(action='SELECT')

    # Extrude the mesh
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, extrude_amt)})

    # Return to object mode
    bpy.ops.object.mode_set(mode='OBJECT')

    text_obj.scale = scale
    text_obj.location = loc
    apply_material_to_mesh(text_obj, material)
    bpy.ops.object.select_all(action='DESELECT')

    return text_obj