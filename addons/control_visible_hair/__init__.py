from bpy import utils
import bpy

bl_info = {
    "name": "ikz_control_Hair_on_Viewport",
    "author": "izumi_ikezaki",
    "version": (1, 0),
    "blender": (3, 6, 0),
    "location": "",
    "description": "ヘアーオブジェクトは重くなりがちなので非表示にするスクリプト",
    "warning": "",
    "doc_url": "",
    "category": "Object",
}


class DisableHairOnViewportOperator(bpy.types.Operator):
    """Disable Hair objects on Viewport"""

    bl_idname = "object.disable_hair_on_viewport"
    bl_label = "Disable Hair on Viewport"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        view_layer = context.view_layer

        for obj in view_layer.objects:
            if (
                obj.type
                == "CURVES"
                # and getattr(obj.data, "bevel_object", None) is not None
            ):
                obj.hide_viewport = True

        return {"FINISHED"}


class EnableHairOnViewportOperator(bpy.types.Operator):
    """Disable Hair objects on Viewport"""

    bl_idname = "object.enable_hair_on_viewport"
    bl_label = "Enable Hair on Viewport"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        view_layer = context.view_layer
        for obj in view_layer.objects:
            if obj.type == "CURVES":
                obj.hide_viewport = False

        return {"FINISHED"}


def draw_menu(self, context):
    # アウトライナの右クリックで表示する
    layout = self.layout
    layout.separator()
    layout.operator(DisableHairOnViewportOperator.bl_idname, icon="HIDE_ON")
    layout.operator(EnableHairOnViewportOperator.bl_idname, icon="HIDE_OFF")


classes = [DisableHairOnViewportOperator, EnableHairOnViewportOperator]


def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.OUTLINER_MT_object.append(draw_menu)
    bpy.types.OUTLINER_MT_collection.append(draw_menu)
    bpy.types.OUTLINER_MT_context_menu.append(draw_menu)


def unregister():
    bpy.types.OUTLINER_MT_context_menu.remove(draw_menu)
    bpy.types.OUTLINER_MT_collection.remove(draw_menu)
    bpy.types.OUTLINER_MT_object.remove(draw_menu)
    for c in reversed(classes):
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()
