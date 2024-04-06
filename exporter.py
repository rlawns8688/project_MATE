import maya.cmds as cmds
import os

if not cmds.pluginInfo("fbxmaya", query=True, loaded=True):
    cmds.loadPlugin("fbxmaya")


class Exporter:
    def __init__(self, output_path):
        self.output_path = output_path

    """
    텍스쳐가 적용 된 오브젝트를 내보내는 파일형식을 지정합니다"
    alembic으로 내보내면 머테리얼은 내보내지지 않는 문제가 있었는데
    아직은 해결하지 못했습니다...
    """

    def ensure_output_path_exists(self):
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path, exist_ok=True)

    def alembic(self):
        # 현재 프레임 가져오기 = 1프레임
        current_frame = cmds.currentTime(query=True)
        # Alembic 파일 경로 설정
        abc_export_path = os.path.join(self.output_path, "export.abc")
        # Alembic 내보내기 설정
        job_string = '-frameRange {0} {0} -dataFormat ogawa -file "{1}"'.format(current_frame, abc_export_path)
        # Alembic 내보내기 실행
        cmds.AbcExport(j=job_string)

    def fbx(self):
        # FBX 파일 경로 설정
        self.ensure_output_path_exists()
        fbx_export_path = os.path.join(self.output_path, "export.fbx")

        if os.path.exists(fbx_export_path):
            os.remove(fbx_export_path)

        # 메시타입의 노드만 선택해서 내보냄
        all_meshes = cmds.ls(type="mesh", r=True)
        all_transforms = cmds.listRelatives(all_meshes, parent=True, fullPath=True) or []
        cmds.select(all_transforms, r=True)
        # FBX 파일로 내보내기
        cmds.file(fbx_export_path, force=True, options="v=0;textures=1;materials=1;", typ="FBX export", es=True)
        # 선택 클리어
        cmds.select(clear=True)


# a = Exporter("/home/rapa/out")
# a.alembic()
