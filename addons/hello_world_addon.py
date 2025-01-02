bl_info = {
    "name": "Hello World Addon",
    "blender": (3, 0, 0),
    "category": "Object",
}

import bpy

# オペレーター定義
class OBJECT_OT_create_hello_world(bpy.types.Operator):
    """Create a Text Object with Custom Message"""
    bl_idname = "object.create_hello_world"
    bl_label = "Create Custom Text"
    bl_options = {'REGISTER', 'UNDO'}

    # テキストを指定するプロパティ
    text: bpy.props.StringProperty(
        name="Text",
        description="The text to display",
        default="Hello World"
    )

    def execute(self, context):
        # テキストオブジェクトを作成
        bpy.ops.object.text_add(location=(0, 0, 0))
        text_obj = context.object
        text_obj.data.body = self.text
        self.report({'INFO'}, f"Created Text: {self.text}")
        return {'FINISHED'}

# メニューにエントリを追加する関数
def menu_func(self, context):
    self.layout.operator(
        OBJECT_OT_create_hello_world.bl_idname,
        text="Create Custom Text"
    ).text = "Hello World"  # デフォルト値

# アドオンの登録と解除
def register():
    bpy.utils.register_class(OBJECT_OT_create_hello_world)
    bpy.types.VIEW3D_MT_add.append(menu_func)  # メニューに追加

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_create_hello_world)
    bpy.types.VIEW3D_MT_add.remove(menu_func)  # メニューから削除

if __name__ == "__main__":
    register()


# usage bpy.ops.object.create_hello_world(text="Hello World!!!")
