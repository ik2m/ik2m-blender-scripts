import os
import time
from bpy.app.handlers import persistent
from bpy import props, utils
import bpy

# import requests

bl_info = {
    "name": "ik2m_auto_save_render",
    "author": "izumi_ikezaki",
    "version": (1, 0),
    "blender": (4, 2, 8),
    "location": "Rendertab -> Render Panel",
    "description": "Automatically save the image after rendering",
    "warning": "test",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Render",
}


def get_preference(key):
    """
    設定を読み出す
    """
    name_without_suffix = __name__.partition(".")[0]
    return getattr(
        bpy.context.preferences.addons[name_without_suffix].preferences, key, None
    )


class IK2MAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    auto_save_path: bpy.props.StringProperty(
        name="path", description="保存先のパス", default="", subtype="DIR_PATH"
    )

    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.prop(self, "auto_save_path")


@persistent
def set_base_path(self):
    """
    ベースパスをセット
    """
    return


@persistent
def auto_save_render(scene):
    """
    レンダリング後にやること
    """
    output_path = get_preference("auto_save_path")
    if not output_path:
        print("自動保存をキャンセル。保存先パスが設定されていません。")
        return
    if not os.path.isdir(output_path):
        print("自動保存をキャンセル。存在しないパスが設定されています :" + output_path)
        return

    rndr = scene.render
    file_fmt: str = rndr.image_settings.file_format

    if file_fmt == "OPEN_EXR_MULTILAYER":
        extension = ".exr"
    elif file_fmt == "JPEG":
        extension = ".jpg"
    elif file_fmt == "PNG":
        extension = ".png"
    else:
        print("自動保存をキャンセル。対応していない画像形式 :" + file_fmt)
        return

    datestamp = time.strftime("%Y%m%d") + "_" + time.strftime("%H%M%S")

    save_name = os.path.join(output_path, f"{datestamp}{extension}")

    image = bpy.data.images["Render Result"]
    if not image:
        print("自動保存をキャンセル。保存する画像の取得に失敗しました。")
        return
    if os.path.isfile(save_name):
        print("自動保存をキャンセル。すでに存在しています。:" + save_name)
        return

    print("Auto_Save:", save_name)
    image.save_render(save_name, scene=None)

classes = [IK2MAddonPreferences]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.app.handlers.render_complete.append(auto_save_render)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    bpy.app.handlers.render_complete.remove(auto_save_render)


if __name__ == "__main__":
    register()
