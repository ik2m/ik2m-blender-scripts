from bpy import utils
import bpy
from . import auto_collection_color

bl_info = {
    "name": "ik2m_toybox",
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


class DevPanel(bpy.types.Panel):
    bl_category = "ik2m"
    bl_idname = "IK2M_PT_DevPanel"
    bl_label = "for dev"
    bl_description = "開発に使うやつ"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    # bl_context = ""
    def draw(self, context):
        layout = self.layout

        # obj = context.object

        # row = layout.row()
        # row.label(text="Active object is: " + obj.name)
        # row = layout.row()
        # row.prop(obj, "name")

        row = layout.row()
        row.operator("script.reload", icon="FILE_REFRESH")


classes = [DevPanel]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    auto_collection_color.register()


def unregister():
    auto_collection_color.unregister()

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
