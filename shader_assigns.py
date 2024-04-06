import maya.cmds as cmds
import os


class ShaderAssigner:
    def __init__(self, obj_file_path, textures_dir):
        self.obj_file_path = obj_file_path
        self.textures_dir = textures_dir

    def assign_textures(self):
        imported_nodes = cmds.file(
            self.obj_file_path,
            i=True,
            returnNewNodes=True,
            type="OBJ",
            options="mo=1",
            ignoreVersion=True,
            ra=True,
            mergeNamespacesOnClash=False,
            namespace=":",
        )
        transform_nodes = [
            cmds.listRelatives(node, parent=True)[0] for node in imported_nodes if cmds.nodeType(node) == "mesh"
        ]
        # key : 쉐이더그룹(=머테리얼,오브젝트종류), value : 해당 텍스쳐 맵 파일(확장자 포함)
        texture_dir = {
            f.rsplit("_", 2)[-2]: f for f in os.listdir(self.textures_dir) if f.endswith(".exr") or f.endswith(".png")
        }
        print(texture_dir)

        for transform_node in transform_nodes:
            obj_identifier = transform_node.rsplit("_", 1)[-1]  # 오브젝트 식별자 추출
            print("오브젝트식별자", obj_identifier)

            """
            이 전제조건은 실무 경험이 없어서, 저의 기존 작업 방식에서 따왔습니다, 
            저는 항상 섭페에서 해당 텍스쳐가 적용될 오브젝트 이름을 뒤에 붙여서 텍스쳐파일을 뽑았었기 때문입니다. 
            실무에선 실용성이 낮다고 생각이 듭니다
            """
            if obj_identifier in texture_dir:
                material_name = transform_node
                print("material name by object", material_name)
                shader_node, shading_group = self.create_shader(material_name)

                for texture_file in os.listdir(self.textures_dir):
                    texture_file_path = os.path.join(self.textures_dir, texture_file)
                    texture_base_name = os.path.basename(texture_file_path)

                    # 텍스쳐 파일 이름 분석
                    file_parts = texture_base_name.split("_")
                    if len(file_parts) < 3:  # 파일 이름이 기대하는 형식?에 맞지 않으면 건너뜀(기대 형식 : obj이름_오브젝트노드이름_텍스쳐맵이름)
                        continue
                    file_obj_identifier = file_parts[-2]
                    render_pass = file_parts[-1].split(".")[0]  # 확장자 제외

                    # 오브젝트 식별자(언더바 _ 뒤의 내용)와 파일 식별자(텍스쳐맵 두 번째 언더바_뒤의 내용(첫번째는 각 텍스쳐맵의 종류))가 일치하는 경우에만 처리
                    if obj_identifier == file_obj_identifier:
                        file_node = self.create_texture_node(texture_file_path, material_name, render_pass)
                        self.connect_texture_to_shader(render_pass, file_node, shader_node)

                cmds.select(transform_node)
                cmds.hyperShade(assign=shading_group)

    # 쉐이더 노드와 쉐이딩 그룹 노드 생성
    def create_shader(self, material_name):
        shader_node = cmds.shadingNode("aiStandardSurface", asShader=True, name=f"{material_name}_shader")
        shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=f"{material_name}_SG")
        cmds.connectAttr(f"{shader_node}.outColor", f"{shading_group}.surfaceShader", force=True)
        return shader_node, shading_group

    def create_texture_node(self, texture_path, material_name, render_pass):
        texture_node = cmds.shadingNode(
            "file", asTexture=True, isColorManaged=True, name=f"{material_name}_{render_pass}"
        )
        cmds.setAttr(f"{texture_node}.fileTextureName", texture_path, type="string")  # file 노드 경로 지정
        return texture_node

    def connect_texture_to_shader(self, render_pass, texture_node, shader_node):
        # BaseColor 노드 생성
        if render_pass == "BaseColor":
            cmds.setAttr(f"{texture_node}.colorSpace", "sRGB", type="string")
            cmds.connectAttr(f"{texture_node}.outColor", f"{shader_node}.baseColor", force=True)

        # Metalness 노드 생성
        elif render_pass == "Metalness":
            cmds.setAttr(f"{texture_node}.colorSpace", "Raw", type="string")
            cmds.setAttr(f"{texture_node}.alphaIsLuminance", True)
            cmds.connectAttr(f"{texture_node}.outAlpha", f"{shader_node}.metalness", force=True)

        # Roughness 노드 생성
        elif render_pass == "Roughness":
            cmds.setAttr(f"{texture_node}.colorSpace", "Raw", type="string")
            cmds.setAttr(f"{texture_node}.alphaIsLuminance", True)
            cmds.connectAttr(f"{texture_node}.outAlpha", f"{shader_node}.specularRoughness", force=True)

        # Normal 노드 생성
        elif render_pass == "Normal":
            cmds.setAttr(f"{texture_node}.colorSpace", "sRGB", type="string")
            bump_node = cmds.shadingNode("bump2d", asUtility=True, name=f"{texture_node}_bump2d")
            cmds.setAttr(f"{bump_node}.bumpInterp", 1)  # Tangent Space Normals
            cmds.connectAttr(f"{texture_node}.outAlpha", f"{bump_node}.bumpValue", force=True)
            cmds.connectAttr(f"{bump_node}.outNormal", f"{shader_node}.normalCamera", force=True)

        # Height 노드 생성
        elif render_pass == "Height":
            cmds.setAttr(f"{texture_node}.colorSpace", "Raw", type="string")
            cmds.setAttr(f"{texture_node}.alphaIsLuminance", True)
            displacement_node = cmds.shadingNode(
                "displacementShader", asShader=True, name=f"{texture_node}_displacementShader"
            )
            cmds.setAttr(
                f"{displacement_node}.scale", 0.1
            )  # 사실 이 부분은 오브젝트마다(+아티스트마다) 약간씩 수치가 달라 질 수 있습니다, 경험 상 0.1이 섭스턴스 페인터에서 텍스쳐링 할 때에 보여지던 결과물이랑 가장 비슷했습니다.
            cmds.connectAttr(f"{texture_node}.outAlpha", f"{displacement_node}.displacement", force=True)
            shading_group = cmds.listConnections(f"{shader_node}.outColor", type="shadingEngine")[0]
            cmds.connectAttr(f"{displacement_node}.displacement", f"{shading_group}.displacementShader", force=True)

        # Emissive 노드 생성
        elif render_pass == "Emissive":
            cmds.setAttr(f"{texture_node}.colorSpace", "sRGB", type="string")
            print(texture_node)
            cmds.connectAttr(f"{texture_node}.outColor", f"{shader_node}.emissionColor", force=True)
            cmds.setAttr(
                f"{shader_node}.emission", 4
            )  # Emissibve 텍스쳐의 발광 세기 입니다. 기본값은 0 이지만, 결과물에 별로 티가 나질 않아서 4로 해뒀습니다...;;


if __name__ == "__main__":
    # obj_file_path = '/home/rapa/myproject_MATE/test/obj/pipe.obj'
    # textures_dir = '/home/rapa/myproject_MATE/test/texture/pipe_texture1'
    obj_file_path = "/home/rapa/myproject_MATE/test/obj/1.obj"
    textures_dir = "/home/rapa/myproject_MATE/test/texture/1"
    shader_assigner = ShaderAssigner(obj_file_path, textures_dir)
    shader_assigner.assign_textures()
