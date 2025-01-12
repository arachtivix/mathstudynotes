import bpy


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


def create_basic_color_material(name: str, color: tuple):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = color
    return mat