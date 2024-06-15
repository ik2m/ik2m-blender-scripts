from bpy import utils
import bpy

bl_info = {
    "name": "ikz_dev_panel",
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
    bl_category = "ikz"
    bl_idname = "IKZ_PT_DevPanel"
    bl_label = "for dev"
    bl_description = "開発に使うやつ"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    # bl_context = ""
    def draw(self, context):
        layout = self.layout

        obj = context.object

        # row = layout.row()
        # row.label(text="Active object is: " + obj.name)
        # row = layout.row()
        # row.prop(obj, "name")

        row = layout.row()
        row.operator("script.reload")


def register():
    bpy.utils.register_class(DevPanel)


def unregister():
    bpy.utils.unregister_class(DevPanel)


if __name__ == "__main__":
    register()
