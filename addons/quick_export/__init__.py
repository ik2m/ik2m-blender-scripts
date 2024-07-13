import bpy
import json
from bpy import props, path, utils
from bpy.ops import export_scene

bl_info = {
    "name": "ikz_quick_export",
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
    bl_idname = "ikz.quick_export"
    bl_label = "quick export"
    bl_description = "指定の場所に自分用の設定でエクスポートするやつ"

    extension = ".fbx"

    def execute(self, context):
        default_path = bpy.context.blend_data.filepath.rstrip(
            bpy.path.basename(bpy.context.blend_data.filepath)
        )
        default_name = bpy.path.basename(bpy.context.blend_data.filepath).split(".")[0]

        setting = getattr(context.scene, "ikz_qe_props", None)
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
    bl_idname = "ikz.export_better_fbx"
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
    bl_idname = "ikz.export_auto_rig_pro_fbx"
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
        # set the file path output here
        # scene.arp_export_twist = True
        file_output = ""

        scene = bpy.context.scene

        print("\nScene Properties:")
        for prop in scene.bl_rna.properties:
            if not prop.is_readonly:
                value = getattr(scene, prop.identifier)
                print(f"  {prop.identifier}: {value}")

        scene.arp_ge_fp = "//output.fbx"

        scene.arp_engine_type = "UNITY"
        scene.arp_export_rig_type = "HUMANOID"

        # Rig
        scene.arp_ge_sel_only = False  # selected object only
        scene.arp_ge_sel_bones_only = False  # selected bone only
        scene.arp_keep_bend_bones = False  # Rig Definition > Advanced
        scene.arp_push_bend = False  # Rig Definition > Push Additive
        scene.arp_full_facial = True  # Rig Definition > Full Facial
        scene.arp_export_twist = True  # Rig Definition > Export Twist
        scene.arp_twist_fac = 0.5  # Rig Definition > Twist Amount
        scene.arp_ge_master_traj = False  # Rig Definition > Export Root Bone (c_traj)
        scene.arp_export_noparent = (
            False  # Rig Definition > No Parents (allow animated stretch)
        )
        scene.arp_export_renaming = False  # Rig Definition > Rename Bones from File
        scene.arp_export_rig_name = "root"  # Rig Definition > Rig Name
        scene.arp_units_x100 = True  # Units > Units x100
        scene.arp_export_bake_axis_convert = False  # Units > Bake Axis Conversion
        scene.arp_ue_root_motion = True  # Root Motion > Root Motion

        # Animations
        scene.arp_bake_anim = False  # Bake Animations

        # Misc
        scene.arp_global_scale = 1  # Global Scale
        scene.arp_mesh_smooth_type = "OFF"  # Geometry > Smooth
        scene.arp_use_tspace = False  # Geometry > Tangent Space
        scene.arp_apply_mods = True  # Geometry > Apply Modifiers
        scene.arp_apply_subsurf = True  # Geometry > Apply Subsurf Modifiers
        scene.arp_export_triangulate = False  # Geometry > Triangulate
        scene.arp_ge_vcol_type = "SRGB"  # Geometry > Vertex Colors
        scene.arp_fix_fbx_rot = False  # Debug > Fix Rotations
        scene.arp_fix_fbx_matrix = True  # Debug > Fix Matrices
        scene.arp_ge_add_dummy_mesh = False  # Debug > Add Dummy Mesh
        scene.arp_ge_force_rest_pose_export = True  # Debug > Force Rest Pose Export
        scene.arp_init_fbx_rot = (
            True  # Armature Axes > Initialize Fbx Armature Rotation
        )
        scene.arp_init_fbx_rot_mesh = (
            True  # Armature Axes > Initialize Fbx Meshes Rotation
        )
        # scene.arp_export_bake_axis_convert = (
        #     True  # Armature Axes > Bake Axis Conversion
        # )
        scene.arp_bone_axis_primary_export = "Y"  # Bone Axes > Primary
        scene.arp_bone_axis_secondary_export = "Y"  # Bone Axes > Secondary
        scene.arp_export_tex = True  # Textures > Embed Textures

        # run export
        bpy.ops.arp.arp_export_fbx_panel("INVOKE_DEFAULT", filepath=file_output)
        return {"FINISHED"}


class Panel(bpy.types.Panel):
    bl_category = "ikz"
    bl_idname = "IKZ_PT_QuickExport"
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

        setting = getattr(context.scene, "ikz_qe_props", None)
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


register_classes = {
    Panel,
    QuickExportOperator,
    ExportBetterFbxOperator,
    ExportAutoRigProFbxOperator,
    MyPropGrp,
}


def register():
    for c in register_classes:
        bpy.utils.register_class(c)

    setattr(bpy.types.Scene, "ikz_qe_props", props.PointerProperty(type=MyPropGrp))


def unregister():
    for c in register_classes:
        bpy.utils.unregister_class(c)

    delattr(bpy.types.Scene, "ikz_qe_props")


if __name__ == "__main__":
    register()
