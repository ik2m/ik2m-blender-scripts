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


class DisableHairOnViewport(bpy.types.Operator):
    """Disable Hair objects on Viewport"""

    bl_idname = "object.disable_hair_on_viewport"
    bl_label = "Disable Hair on Viewport"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        view_layer = context.view_layer

        for obj in view_layer.objects:
            print(obj.name)
            print(obj.type)
            if (
                obj.type
                == "CURVES"
                # and getattr(obj.data, "bevel_object", None) is not None
            ):
                print("name")
                obj.hide_viewport = True

        return {"FINISHED"}


class EnableHairOnViewport(bpy.types.Operator):
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
    layout.operator(DisableHairOnViewport.bl_idname, icon="HIDE_ON")
    layout.operator(EnableHairOnViewport.bl_idname, icon="HIDE_OFF")


def register():
    bpy.utils.register_class(DisableHairOnViewport)
    bpy.utils.register_class(EnableHairOnViewport)
    bpy.types.OUTLINER_MT_object.append(draw_menu)
    bpy.types.OUTLINER_MT_collection.append(draw_menu)
    bpy.types.OUTLINER_MT_context_menu.append(draw_menu)


def unregister():
    bpy.types.OUTLINER_MT_context_menu.remove(draw_menu)
    bpy.types.OUTLINER_MT_collection.remove(draw_menu)
    bpy.types.OUTLINER_MT_object.remove(draw_menu)
    bpy.utils.unregister_class(EnableHairOnViewport)
    bpy.utils.unregister_class(DisableHairOnViewport)


if __name__ == "__main__":
    register()
