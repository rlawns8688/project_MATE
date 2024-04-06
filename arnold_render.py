import maya.cmds as cmds
import os
import subprocess
import mtoa.core as core


core.createOptions()  # 마야의 아놀드 렌더러 옵션에 접근하는 함수입니다, set_arnold_render_options 함수는 이 구문이 없으면 계속 에러가 났었습니다.
import sys

sys.path.append("/home/rapa/myproject_MATE")

import arnold_light as al
from shader_assigns import ShaderAssigner


class ArnoldRenderer:
    def __init__(self, output_path):
        self.output_path = output_path

    # 카메라와 라이팅을 세팅합니다, 그룹 노드가 생성되면, 해당 그룹의 transfrom을 기준으로 조명을 생성합니다.
    def setup_camera_view(self, camera="persp"):
        mesh_objects = cmds.ls(type="mesh")
        transform_nodes = [
            cmds.listRelatives(mesh, parent=True)[0] for mesh in mesh_objects if cmds.listRelatives(mesh, parent=True)
        ]

        # 메시 오브젝트들을 그룹화합니다.
        if transform_nodes:
            group_mesh = cmds.group(transform_nodes, name="meshGroup")
        else:
            group_mesh = None
            print("No mesh objects found to group.")

        # 그룹 노드에 턴어라운뷰로 키프레임을 적용합니다.
        if group_mesh:
            cmds.select(group_mesh)
            cmds.viewFit(camera, fitFactor=0)
            cmds.setKeyframe(group_mesh, attribute="rotateY", t=1, v=0)
            cmds.setKeyframe(group_mesh, attribute="rotateY", t=60, v=360)
            # 그룹 노드에 라이팅을 적용합니다.
            al.create_lighting_for_group(group_mesh)
            cmds.select(clear=True)
        else:
            print("카메라와 라이팅을 세팅할 group이 없습니다.")

    # 렌더링 관련 함수들을 순차적으로 실행합니다
    def render_scene_with_arnold(self, start_frame, end_frame):
        self.ensure_output_path_exists()
        self.configure_global_render_settings(start_frame, end_frame)
        self.set_render_resolution(1920, 1080)
        self.set_arnold_render_options()
        self.set_render_output_prefix()
        self.render_frames(start_frame, end_frame)
        self.convert_frames_to_video(start_frame)

    # 디렉토리가 없으면 생성해서 실행합니다
    def ensure_output_path_exists(self):
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path, exist_ok=True)

    # 글로벌 렌더세팅 관련 함수입니다, 경로나 이미지포멧, 렌더링 범위를 지정합니다.
    def configure_global_render_settings(self, start_frame, end_frame):
        cmds.setAttr("defaultRenderGlobals.startFrame", start_frame)
        cmds.setAttr("defaultRenderGlobals.endFrame", end_frame)
        cmds.setAttr("defaultRenderGlobals.currentRenderer", "arnold", type="string")

    # 렌더링 해상도를 지정합니다
    def set_render_resolution(self, width, height):
        cmds.setAttr("defaultResolution.width", width)
        cmds.setAttr("defaultResolution.height", height)

    # 아놀드 렌더링 관련 함수입니다. 샘플링과 Depth에 관한 설정입니다(렌더링 속도가 너무 느려져서 전체 1로 낮췄습니다.)
    def set_arnold_render_options(self):
        cmds.setAttr("defaultArnoldRenderOptions.AASamples", 2)  # 안티에일리싱 수치입니다, 1하고 2의 차이가 커서 2로 설정했습니다.
        cmds.setAttr("defaultArnoldRenderOptions.GIDiffuseSamples", 1)
        cmds.setAttr("defaultArnoldRenderOptions.GISpecularSamples", 1)
        cmds.setAttr("defaultArnoldRenderOptions.GITransmissionSamples", 1)
        cmds.setAttr("defaultArnoldRenderOptions.GITotalDepth", 1)
        cmds.setAttr("defaultArnoldRenderOptions.GIDiffuseDepth", 1)
        cmds.setAttr("defaultArnoldRenderOptions.GISpecularDepth", 1)
        cmds.setAttr("defaultArnoldDriver.ai_translator", "png", type="string")
        # cmds.setAttr("defaultArnoldDriver.ai_translator", "exr", type="string")

    # 렌더링 출력 경로와 출력파일명을 지정합니다
    def set_render_output_prefix(self):
        file_prefix = os.path.join(self.output_path, "frame_<Frame>").replace("\\", "/")
        cmds.setAttr("defaultRenderGlobals.imageFilePrefix", file_prefix, type="string")

    # 렌더링이 실행되는 함수입니다
    def render_frames(self, start_frame, end_frame):
        for frame in range(start_frame, end_frame + 1):
            cmds.currentTime(frame)
            print(f"{frame} rendering .... ")
            cmds.arnoldRender(cam="persp")

    # 렌더링이 종료된 후 생성된 이미지시퀀스들로 mov파일을 생성합니다
    def convert_frames_to_video(self, start_frame):
        ffmpeg_cmd = [
            "ffmpeg",
            "-framerate",
            "24",
            "-y",
            "-start_number",
            str(start_frame),
            "-i",
            f"{self.output_path}/frame_%04d.png",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            f"{self.output_path}/final_output.mov",
        ]
        subprocess.run(ffmpeg_cmd)

    """
    playblast를 출력하는 함수입니다.
    anold render or playblast 중 선택하는 옵션을 제공하려 했었지만
    결과물의 퀄리티가 생각보다 너무 좋지 않아서 사용 안하게 되었습니다.
    그리고 무엇보다도 batch 모드로 스크립트를 실행할때에만 실행됩니다 ..
    """

    def create_playblast(self, start_frame, end_frame, width=1920, height=1080):
        filename = os.path.join(self.output_path, "playblast.mov")
        # 따로 커스텀을 한 게 아니라면, modelPanel4가 persp뷰로 기본설정되어있습니다
        cmds.modelEditor("modelPanel4", edit=True, displayTextures=True, displayAppearance="smoothShaded")
        cmds.playblast(
            format="qt",
            filename=filename,
            sequenceTime=0,
            clearCache=1,
            forceOverwrite=True,
            viewer=False,
            offScreen=True,
            showOrnaments=False,
            fp=4,
            percent=100,
            compression="H.264",
            quality=100,
            widthHeight=[width, height],
            startTime=start_frame,
            endTime=end_frame,
        )
        print(f"Playblast created: {filename}")


if __name__ == "__main__":
    output_path = "/home/rapa/myproject_MATE/test/arnold"
    obj_file_path = "/home/rapa/myproject_MATE/test/obj/1.obj"
    textures_dir = "/home/rapa/myproject_MATE/test/texture/1"
    shaders_assigner = ShaderAssigner(obj_file_path, textures_dir)
    shaders_assigner.assign_textures()
    arnold_renderer = ArnoldRenderer(output_path)
    arnold_renderer.setup_camera_view()
    # arnold_renderer.render_scene_with_arnold(1, 2)
    # arnold_renderer.create_playblast(1, 300)
