import bpy


class ApplyPose(bpy.types.Operator):
    bl_idname = "ikz.apply_pose"
    bl_label = "apply pose"
    bl_description = "現状のポーズをレフトポーズにする"

    @classmethod
    def poll(cls, context):
        return (
            context.active_object.type == "ARMATURE"
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


class ApplyPoseLayoutPanel(bpy.types.Panel):
    bl_category = "ikz"
    bl_label = "apply pose"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    # bl_context = ""

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.scale_y = 2.0
        row.operator(ApplyPose.bl_idname)


register_classes = (
    ApplyPoseLayoutPanel,
    ApplyPose,
)


def register():
    for c in register_classes:
        bpy.utils.register_class(c)


def unregister():
    for c in register_classes:
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()
