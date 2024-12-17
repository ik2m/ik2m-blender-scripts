import bpy
import json
import os
from bpy import props, path, utils
from bpy.ops import export_scene

bl_info = {
    "name": "ik2m_quick_export",
    "author": "izumi_ikezaki",
    "version": (1, 0),
    "blender": (3, 6, 0),
    "location": "",
    "description": "",
    "warning": "test",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object",
}


class MyPropGrp(bpy.types.PropertyGroup):
    option_path: bpy.props.StringProperty(
        name="path",
        description="エクスポート先のパス\nデフォルトではファイル名",
        default="",
    )
    option_name: bpy.props.StringProperty(
        name="name",
        description="エクスポート先のファイル名\nデフォルトではファイル名",
        default="",
    )


class QuickExportOperator(bpy.types.Operator):
    bl_idname = "ik2m.quick_export"
    bl_label = "quick export"
    bl_description = "指定の場所に自分用の設定でエクスポートするやつ"

    extension = ".fbx"

    def execute(self, context):
        default_path = bpy.context.blend_data.filepath.rstrip(
            bpy.path.basename(bpy.context.blend_data.filepath)
        )
        default_name = bpy.path.basename(bpy.context.blend_data.filepath).split(".")[0]

        setting = getattr(context.scene, "ik2m_qe_props", None)
        p = setting.option_path or default_path
        n = setting.option_name or default_name

        filepath = p + n + self.extension

        setting_path = (
            bpy.context.blend_data.filepath.rstrip(
                bpy.path.basename(bpy.context.blend_data.filepath)
            )
            + "my_export_setting.json"
        )
        setting_open = open(setting_path, "r")
        setting = json.load(setting_open)

        setting["filepath"] = filepath
        setting["object_types"] = set(
            setting["object_types"]
        )  # jsonでは配列になってしまうのでset化

        bpy.ops.export_scene.fbx(**(setting))
        return {"FINISHED"}


class ExportBetterFbxOperator(bpy.types.Operator):
    bl_idname = "ik2m.export_better_fbx"
    bl_label = "export_better_fbx"
    bl_description = "エクスポート"

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        better_export = getattr(bpy.ops, "better_export", None)
        if hasattr(better_export, "fbx") and better_export.fbx.poll():
            return self.execute(context)

        self.report({"ERROR"}, "better_exportがないと動かないよ")
        return {"CANCELLED"}

    def execute(self, context):
        better_export = getattr(bpy.ops, "better_export", None)
        better_export.fbx("INVOKE_DEFAULT")
        return {"FINISHED"}


class ExportAutoRigProFbxOperator(bpy.types.Operator):
    bl_idname = "ik2m.export_auto_rig_pro_fbx"
    bl_label = "export_auto_rig_pro_fbx"
    bl_description = "エクスポート"

    @classmethod
    def poll(cls, context):
        return any(obj for obj in context.selected_objects if obj.type == "ARMATURE")

    def invoke(self, context, event):
        arp_export_scene = getattr(bpy.ops, "arp_export_scene", None)
        if hasattr(arp_export_scene, "fbx") and arp_export_scene.fbx.poll():
            return self.execute(context)

        self.report({"ERROR"}, "auto_rig_proがないと動かないよ")
        return {"CANCELLED"}

    def execute(self, context):
        """
        @see https://www.lucky3d.fr/auto-rig-pro/doc/ge_export_doc.html#export-by-script
        """

        for_md = {
            "path": "//for_md",
            "arp": {
                "arp_engine_type": "UNITY",
                "arp_export_rig_type": "HUMANOID",
                # Rig
                "arp_ge_sel_only": False,  # selected object only
                "arp_ge_sel_bones_only": False,  # selected bone only
                "arp_keep_bend_bones": False,  # Rig Definition > Advanced
                "arp_push_bend": False,  # Rig Definition > Push Additive
                "arp_full_facial": True,  # Rig Definition > Full Facial
                "arp_export_twist": True,  # Rig Definition > Export Twist
                "arp_twist_fac": 0.5,  # Rig Definition > Twist Amount
                "arp_ge_master_traj": False,  # Rig Definition > Export Root Bone (c_traj)
                "arp_export_noparent": False,  # Rig Definition > No Parents (allow animated stretch)
                "arp_export_renaming": False,  # Rig Definition > Rename Bones from File
                "arp_export_rig_name": "root",  # Rig Definition > Rig Name
                "arp_units_x100": True,  # Units > Units x100
                "arp_export_bake_axis_convert": False,  # Units > Bake Axis Conversion
                "arp_ue_root_motion": True,  # Root Motion > Root Motion
                # Animations
                "arp_bake_anim": False,  # Bake Animations
                # Misc
                "arp_global_scale": 1,  # Global Scale
                "arp_mesh_smooth_type": "OFF",  # Geometry > Smooth
                "arp_use_tspace": False,  # Geometry > Tangent Space
                "arp_apply_mods": True,  # Geometry > Apply Modifiers
                "arp_apply_subsurf": True,  # Geometry > Apply Subsurf Modifiers
                "arp_export_triangulate": False,  # Geometry > Triangulate
                "arp_ge_vcol_type": "SRGB",  # Geometry > Vertex Colors
                "arp_fix_fbx_rot": False,  # Debug > Fix Rotations
                "arp_fix_fbx_matrix": True,  # Debug > Fix Matrices
                "arp_ge_add_dummy_mesh": False,  # Debug > Add Dummy Mesh
                "arp_ge_force_rest_pose_export": True,  # Debug > Force Rest Pose Export
                "arp_init_fbx_rot": True,  # Armature Axes > Initialize Fbx Armature Rotation
                "arp_init_fbx_rot_mesh": True,  # Armature Axes > Initialize Fbx Meshes Rotation
                # "arp_export_bake_axis_convert": True,  # Armature Axes > Bake Axis Conversion,
                "arp_bone_axis_primary_export": "Y",  # Bone Axes > Primary
                "arp_bone_axis_secondary_export": "Y",  # Bone Axes > Secondary
                "arp_export_tex": True,  # Textures > Embed Textures
            },
        }

        scene = bpy.context.scene

        # print("\nScene Properties:")
        # for prop in scene.bl_rna.properties:
        #     if not prop.is_readonly:
        #         value = getattr(scene, prop.identifier)
        #         print(f"  {prop.identifier}: {value}")

        # set outputpath
        blend_file_path = bpy.data.filepath
        if not blend_file_path:
            # パス
            return {"CANCELLED"}
        filename = os.path.basename(blend_file_path).replace(".blend", ".fbx")
        scene.arp_ge_fp = os.path.join(for_md["path"], filename)

        # set_setting
        for key, value in for_md["arp"].items():
            if hasattr(scene, key):
                scene[key] = value
            else:
                print(f"unknown property. {key}: {value}")

        # run export
        bpy.ops.arp.arp_export_fbx_panel("INVOKE_DEFAULT")
        return {"FINISHED"}


class Panel(bpy.types.Panel):
    bl_category = "ik2m"
    bl_idname = "ik2m_PT_QuickExport"
    bl_label = "quick export"
    bl_description = "エクスポートする"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    # bl_context = ""

    def draw(self, context):
        """
        :param context:
        :return:
        """
        layout = self.layout

        setting = getattr(context.scene, "ik2m_qe_props", None)
        # row = layout.row()
        # row.prop(setting, "option_path")
        # row = layout.row()
        # row.prop(setting, "option_name")

        row = layout.row()
        row.scale_y = 2.0
        row.operator(QuickExportOperator.bl_idname)

        row = layout.row()
        row.scale_y = 2.0
        row.operator(ExportBetterFbxOperator.bl_idname)

        row = layout.row()
        row.scale_y = 2.0
        row.operator(ExportAutoRigProFbxOperator.bl_idname)


register_classes = [
    Panel,
    QuickExportOperator,
    ExportBetterFbxOperator,
    ExportAutoRigProFbxOperator,
    MyPropGrp,
]


def register():
    for c in register_classes:
        bpy.utils.register_class(c)

    setattr(bpy.types.Scene, "ik2m_qe_props", props.PointerProperty(type=MyPropGrp))


def unregister():
    for c in reversed(register_classes):
        bpy.utils.unregister_class(c)

    delattr(bpy.types.Scene, "ik2m_qe_props")


if __name__ == "__main__":
    register()
