import os
import time
from bpy.app.handlers import persistent
from bpy import props, utils
import bpy
import requests

# import requests

bl_info = {
    "name": "notify_render",
    "author": "izumi_ikezaki",
    "version": (1, 0),
    "blender": (4, 2, 8),
    "location": "Rendertab -> Render Panel",
    "description": "Discordに通知するやーつ",
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

    discord_webhook: bpy.props.StringProperty(
        name="discord_webhook",
        description="discordのwebhook",
        default="",
        subtype="PASSWORD",
    )

    def draw(self, context):
        layout = self.layout

        row = layout.row(align=True)
        row.prop(self, "discord_webhook")

@persistent
def send_line_notify(scene):
    discord_webhook = get_preference("discord_webhook")
    print(discord_webhook)
    if not discord_webhook:
        print("レンダリング通知をキャンセル。webhook URLが設定されていません。")
        return
    data = {
        "content": "レンダリングが完了しました"
    }
    response =requests.post(discord_webhook, json=data)
    if response.status_code != 200:
        print("レンダリング通知に失敗。{}:{}".format(response.status_code, response.text))


classes = [IK2MAddonPreferences]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.app.handlers.render_post.append(send_line_notify)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    bpy.app.handlers.render_post.remove(send_line_notify)


if __name__ == "__main__":
    register()
