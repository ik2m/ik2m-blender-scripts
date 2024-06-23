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
        arp_export_scene = getattr(bpy.ops, "arp_export_scene", None)
        arp_export_scene.fbx("INVOKE_DEFAULT")
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

    setattr(bpy.types.Scene, "ikz_qe_props", props.PointerProperty(type=MyPropGrp))


def unregister():
    for c in register_classes:
        bpy.utils.unregister_class(c)

    delattr(bpy.types.Scene, "ikz_qe_props")


if __name__ == "__main__":
    register()
