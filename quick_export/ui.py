import bpy
import os


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

        composed_path = p+n+self.extension

        bpy.ops.export_scene.fbx(
            filepath=composed_path,
            check_existing=True,
            filter_glob="*.fbx",
            use_selection=False,
            use_active_collection=False,
            global_scale=1.0,
            apply_unit_scale=True,  # 単位を適用
            apply_scale_options='FBX_SCALE_ALL',
            bake_space_transform=False,
            object_types={'EMPTY', 'MESH', 'ARMATURE'},
            use_mesh_modifiers=True,
            mesh_smooth_type='OFF',
            use_subsurf=False,
            use_mesh_edges=False,
            use_tspace=False,
            use_custom_props=False,
            add_leaf_bones=False,
            primary_bone_axis='Y',
            secondary_bone_axis='X',
            use_armature_deform_only=True,
            armature_nodetype='NULL',
            bake_anim=False,
            bake_anim_use_all_bones=True,
            bake_anim_use_nla_strips=True,
            bake_anim_use_all_actions=True,
            bake_anim_force_startend_keying=True,
            bake_anim_step=1.0,
            bake_anim_simplify_factor=1.0,
            path_mode='RELATIVE',
            embed_textures=False,
            batch_mode='OFF',
            use_batch_own_dir=True,
            use_metadata=True,
            axis_forward='-Z',
            axis_up='Y'
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