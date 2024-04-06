import sys
import os


import maya.standalone
import maya.cmds as cmds

maya.standalone.initialize(name="python")
if not cmds.pluginInfo("mtoa", query=True, loaded=True):
    try:
        cmds.loadPlugin("mtoa")
    except:
        cmds.error("MtoA plugin couldn't be loaded")

obj_file_path = sys.argv[1]
textures_dir = sys.argv[2]
output_path = sys.argv[3]

# obj_file_path = "/home/rapa/myproject/test/obj/iclone.obj"
# textures_dir = "/home/rapa/myproject/test/texture/iclone_texture"
# output_path = "/home/rapa/nn"
sys.path.append("/home/rapa/myproject")

from shader_assigns import ShaderAssigner
from exporter import Exporter
from arnold_render import ArnoldRenderer

exporter = Exporter(output_path)


shaders_assigner = ShaderAssigner(obj_file_path, textures_dir)
shaders_assigner.assign_textures()
exporter.fbx()
arnold_renderer = ArnoldRenderer(output_path)
arnold_renderer.setup_camera_view()
arnold_renderer.render_scene_with_arnold(1, 60)
