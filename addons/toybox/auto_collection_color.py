import bpy
from bpy.app.handlers import persistent


def set_collection_color(collection):
    """
    コレクションに色をつける
    """
    name = str.lower(collection.name)
    if "backup" in name:
        collection.color_tag = "COLOR_01"
        return
    if "cache" in name:
        collection.color_tag = "COLOR_01"
        return
    if "draft" in name:
        collection.color_tag = "COLOR_02"
        return
    return


@persistent
def auto_set_collection_color(dummy1, dummy2):
    for collection in bpy.data.collections:
        if collection.color_tag == "NONE":
            set_collection_color(collection)


def register():
    bpy.app.handlers.depsgraph_update_post.append(auto_set_collection_color)


def unregister():
    bpy.app.handlers.depsgraph_update_post.remove(auto_set_collection_color)
