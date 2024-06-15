from bpy import utils
from bpy.ops import object
import bpy

bl_info = {
    "name": "ikz_create_library_override",
    "author": "izumi_ikezaki",
    "version": (1, 0),
    "blender": (3, 6, 0),
    "location": "",
    "description": "create library override",
    "warning": "test",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object",
}


class CreateLibraryOverrideOperator(bpy.types.Operator):
    bl_idname = "object.create_library_override"
    bl_label = "Create Library Override"

    def execute(self, context):

        bpy.ops.object.make_override_library()

        return {"FINISHED"}


def draw_menu(self, context):
    # アウトライナの右クリックで表示する
    layout = self.layout
    layout.separator()
    layout.operator(CreateLibraryOverrideOperator.bl_idname)


def register():
    bpy.utils.register_class(CreateLibraryOverrideOperator)
    bpy.types.OUTLINER_MT_object.append(draw_menu)


def unregister():
    bpy.types.OUTLINER_MT_object.remove(draw_menu)
    bpy.utils.unregister_class(CreateLibraryOverrideOperator)


if __name__ == "__main__":
    register()
