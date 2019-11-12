bl_info = {
    "name": "Exec nvim",
    "category": "3D View",
    "author": "asshole",
    "version": (0, 4, 8),
    "blender": (2, 80, 0),

}

import bpy
# from neovim import attach


class ExecNvim(bpy.types.Operator):
    """Object Cursor Array"""
    bl_idname = "object.cursor_array"
    bl_label = "Exec Nvim"
    bl_options = {'REGISTER', 'UNDO'}

    total = bpy.props.IntProperty(name="Steps", default=2, min=1, max=100)

    def execute(self, context):
        # nvim = attach('socket', path = '\\\\.\\pipe\\nvim-10592-0')
        # cube = bpy.data.objects['Cube']
        # cube.location.z -= 2
        # scene = context.scene
        # cursor = scene.cursor_location
        # obj = scene.objects.active
        # for i in range(self.total):
            # obj_new = obj.copy()
            # scene.objects.link(obj_new)
            # factor = i / self.total
            # obj_new.location = (obj.location * factor) + (cursor * (1.0 - factor))

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(ExecNvim.bl_idname)

# store keymaps here to access after registration
addon_keymaps = []


def register():
    bpy.utils.register_class(ExecNvim)
    bpy.types.VIEW3D_MT_object.append(menu_func)

    # handle the keymap
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
    kmi = km.keymap_items.new(ExecNvim.bl_idname, 'F9', 'PRESS', ctrl=True, shift=True)
    kmi.properties.total = 4
    addon_keymaps.append(km)

def unregister():
    bpy.utils.unregister_class(ExecNvim)
    bpy.types.VIEW3D_MT_object.remove(menu_func)

    # handle the keymap
    wm = bpy.context.window_manager
    for km in addon_keymaps:
        wm.keyconfigs.addon.keymaps.remove(km)
    # clear the list
    del addon_keymaps[:]


if __name__ == "__main__":
    register()
