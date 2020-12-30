import bpy
import os
import json


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


class QuickExport(bpy.types.Operator):
    bl_idname = "ikezaki.quick_export"
    bl_label = "quick export"
    bl_description = "指定の場所に自分用の設定でエクスポートするやつ"

    default_path = bpy.context.blend_data.filepath.rstrip(
        bpy.path.basename(bpy.context.blend_data.filepath))
    default_name = bpy.path.basename(
        bpy.context.blend_data.filepath).split(".")[0]
    extension = ".fbx"

    def execute(self, context):
        props = context.scene.ikezaki_qe_props
        p = props.option_path or self.default_path
        n = props.option_name or self.default_name

        filepath = p+n+self.extension

        setting_path = bpy.context.blend_data.filepath.rstrip(
            bpy.path.basename(bpy.context.blend_data.filepath))+'my_export_setting.json'
        setting_open = open(setting_path, 'r')
        setting = json.load(setting_open)

        setting['filepath'] = filepath
        setting['object_types'] = set(
            setting['object_types'])  # jsonでは配列になってしまうのでset化

        bpy.ops.export_scene.fbx(
            **(setting)
        )
        return{'FINISHED'}


class QuickExportLayoutPanel(bpy.types.Panel):
    bl_category = "Ikezaki"
    bl_label = "quick export"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    # bl_context = ""

    def draw(self, context):
        layout = self.layout

        props = context.scene.ikezaki_qe_props
        row = layout.row()
        row.prop(props, "option_path")
        row = layout.row()
        row.prop(props, "option_name")

        row = layout.row()
        row.scale_y = 2.0
        row.operator(QuickExport.bl_idname)


regist_classes = (
    QuickExportLayoutPanel,
    QuickExport,
    MyPropGrp
)


def register():
    for c in regist_classes:
        bpy.utils.register_class(c)

    bpy.types.Scene.ikezaki_qe_props = bpy.props.PointerProperty(
        type=MyPropGrp)


def unregister():
    for c in regist_classes:
        bpy.utils.unregister_class(c)

    del bpy.types.Scene.ikezaki_qe_props


if __name__ == "__main__":
    register()
