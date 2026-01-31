import bpy

# 日本語ラベル定義
class J:
    PANEL_NAME = "はとむぎつーる"
    PANEL_LABEL = "メモ"

# メモ用プロパティグループ
class MemoItem(bpy.types.PropertyGroup):
    text: bpy.props.StringProperty(name="テキスト", default="")
    locked: bpy.props.BoolProperty(name="ロック", default=False)
    checked: bpy.props.BoolProperty(name="完了", default=False)
    
# メモ追加オペレーター
class MEMO_OT_add(bpy.types.Operator):
    bl_idname = "memo.add"
    bl_label = ""

    def execute(self, context):
        context.scene.memoList.add()
        return {'FINISHED'}

# メモ削除オペレーター
class MEMO_OT_remove(bpy.types.Operator):
    bl_idname = "memo.remove"
    bl_label = ""
    index: bpy.props.IntProperty()

    def execute(self, context):
        memos = context.scene.memoList
        if 0 <= self.index < len(memos):
            memos.remove(self.index)
        return {'FINISHED'}

class MEMO_OT_move(bpy.types.Operator):
    bl_idname = "memo.move"
    bl_label = ""
    direction: bpy.props.StringProperty()  # up or down
    index: bpy.props.IntProperty()

    def execute(self, context):
        memos = context.scene.memoList
        index = self.index
        
        if self.direction == 'UP' and index > 0:
            memos.move(index, index-1)
        elif self.direction == 'DOWN' and index < len(memos) - 1:
            memos.move(index, index+1)
        
        return {'FINISHED'}

# UIパネル
class VIEW3D_PT_blender_memo(bpy.types.Panel):
    bl_label = J.PANEL_LABEL
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = J.PANEL_NAME

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        memos = scene.memoList

        for index, memo in enumerate(memos):
            row = layout.row(align=True)
        
            # Todoチェックボックス
            row.prop(memo, "checked", text="", icon='CHECKBOX_HLT' if memo.checked else 'CHECKBOX_DEHLT')
                        

            # メモ内容
            if memo.locked:
                row.label(text=memo.text)
            else:
                row.prop(memo, "text", text="")

            # 上移動ボタン
            move_up = row.operator("memo.move", text="", icon='TRIA_UP')
            move_up.direction = 'UP'
            move_up.index = index
            
            # 下移動ボタン
            move_down = row.operator("memo.move", text="", icon='TRIA_DOWN')
            move_down.direction = 'DOWN'
            move_down.index = index
            
            # ロックボタン
            row.prop(memo, "locked", text="", icon="LOCKED" if memo.locked else "UNLOCKED")
            
            # 削除ボタン
            row.operator("memo.remove", text="", icon="TRASH").index = index
            
        # 追加ボタン（アイコンのみ）
        layout.operator("memo.add", text="", icon="ADD")