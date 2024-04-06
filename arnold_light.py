import maya.cmds as cmds
import mtoa.utils as mutils

"""
그룹 노드를 받아서 바운딩박스를 생성합니다.
바운딩 박스는 씬에 있는 오브젝트가 차지하는 공간,위치를 입력받는 노드이고,
자동으로 조명들을 배치하는데에 핵심적인 요소입니다.
예를 들어, 오브젝트의 크기가 너무 커버리면 그만큼 멀어져서 조명이 배치됩니다.
그리고 오브젝트의 형태에 골고루 비추기 위해 좀 더 센 조명이 생성됩니다.  
"""

def calculate_group_bounding_box_size(group):
    # 그룹 노드의 바운딩 박스를 계산합니다.
    bbox = cmds.exactWorldBoundingBox(group, calculateExactly=True)

    # 바운딩 박스 크기를 계산합니다.
    size_x = bbox[3] - bbox[0]
    size_y = bbox[4] - bbox[1]
    size_z = bbox[5] - bbox[2]

    # 가장 큰 차원의 크기를 반환합니다.
    max_size = max(size_x, size_y, size_z)
    return max_size


"""
삼점조명을 썼습니다.
따뜻한 톤과 차가운 톤의 대비로 형태감을 더 잘 표현할 수 있다는 
이론을 기반으로 이렇게 라이팅을 세팅하였습니다.
사실 정확히는 잘 모릅니다,,,
"""


def create_lighting_for_group(group_node):
    if not cmds.pluginInfo("mtoa", query=True, loaded=True):
        cmds.loadPlugin("mtoa")

    # 기존 라이트 제거
    for light in cmds.ls(lights=True):
        cmds.delete(light)

    max_size = calculate_group_bounding_box_size(group_node)
    light_intensity = 1.0 + (max_size / 15.0)
    light_distance = max_size * 2

    # 주 조명 (Key Light)
    key_light = cmds.directionalLight(name="keyLight")
    cmds.setAttr(f"{key_light}.intensity", light_intensity)
    cmds.setAttr(f"{key_light}.color", 1, 1, 1, type="double3")  # 순백색으로 설정
    cmds.move(light_distance, light_distance, light_distance, key_light)
    cmds.rotate(-30, 45, 0, key_light)

    # 보조 조명 (Fill Light)
    fill_light = cmds.directionalLight(name="fillLight")
    cmds.setAttr(f"{fill_light}.intensity", light_intensity * 0.5)
    cmds.setAttr(f"{fill_light}.color", 0.5, 0.5, 1, type="double3")  # 차가운 톤
    cmds.move(-light_distance, light_distance, 0, fill_light)
    cmds.rotate(-30, 100, 0, fill_light)

    # 백 라이트 (Back Light)
    back_light = cmds.directionalLight(name="backLight")
    cmds.setAttr(f"{back_light}.intensity", light_intensity * 0.75)
    cmds.setAttr(f"{back_light}.color", 1, 0.55, 0.5, type="double3")  # 따뜻한 톤
    cmds.move(0, light_distance, -light_distance, back_light)
    cmds.rotate(-30, 180, 0, back_light)
