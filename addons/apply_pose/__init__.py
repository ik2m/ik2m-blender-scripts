from bpy import utils, ops
from bpy.ops import object, pose
import bpy

bl_info = {
    "name": "ik2m_apply_pose",
    "author": "izumi_ikezaki",
    "version": (1, 0),
    "blender": (3, 6, 0),
    "location": "",
    "description": "apply pose",
    "warning": "test",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object",
}


class ApplyPoseOperator(bpy.types.Operator):
    bl_idname = "ik2m.apply_pose"
    bl_label = "apply pose"
    bl_description = "現状のポーズをレフトポーズにする"

    @classmethod
    def poll(cls, context):
        return (
            getattr(context.active_object, "type", None) == "ARMATURE"
        )  # and context.mode == 'ARMATURE'

    def execute(self, context):
        armature = context.active_object
        for mesh in armature.children:
            if mesh.active_shape_key is not None:
                continue  # シェイプキーがあると現状無視される
            for mod in mesh.modifiers:
                if mod.type == "ARMATURE":
                    armature_mod = mod
            override = context.copy()
            override["object"] = mesh
            bpy.ops.object.modifier_copy(override, modifier=armature_mod.name)
            for mod in mesh.modifiers:
                if mod.type == "ARMATURE":
                    armature_mod_copy = mod
            bpy.ops.object.modifier_apply(override, modifier=armature_mod_copy.name)

        override = context.copy()
        bpy.ops.object.mode_set(mode="POSE")
        bpy.ops.pose.armature_apply(override)  # ここもcontext overrideしたい
        bpy.ops.object.mode_set(mode="OBJECT")
        return {"FINISHED"}


class ApplyPosePanel(bpy.types.Panel):
    bl_category = "ik2m"
    bl_idname = "ik2m_PT_ApplyPose"
    bl_label = "apply pose"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    # bl_context = ""

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.scale_y = 2.0
        row.operator(ApplyPoseOperator.bl_idname)


classes = [ApplyPosePanel, ApplyPoseOperator]


def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in reversed(classes):
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()
