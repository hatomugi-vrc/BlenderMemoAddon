import bpy
import os
# from datetime import datetime, timedelta
from datetime import datetime
import shutil

# 日本語ラベル定義
class J:
    PANEL_NAME = "はとむぎつーる"
    PANEL_LABEL = "このファイルをバックアップ"

# プロパティグループ
class BackupItem(bpy.types.PropertyGroup):
    # text: bpy.props.StringProperty(name="テキスト", default="")
    backup_path: bpy.props.StringProperty(
        name="バックアップパス",
        default=""
    )
    backup_name: bpy.props.StringProperty(
        name="バックアップ名", 
        default="未保存"
    )
    last_backup_time: bpy.props.StringProperty(
        name="最終バックアップ日時",
        default=""
    )

def get_backup_filename():
    """バックアップ用のファイル名を生成"""
    # 現在のファイルパスを取得
    current_file = bpy.data.filepath
    
    if not current_file:
        return None
    
    # ファイル名とディレクトリを分離
    directory, filename = os.path.split(current_file)
    name, ext = os.path.splitext(filename)
    
    # 現在時刻を取得して30分区切り
    now = datetime.now()
    
    # 30分区切り（分を30で割って切り捨て、30を掛ける）
    minute_rounded = (now.minute // 30) * 30
    rounded_time = now.replace(minute=minute_rounded, second=0, microsecond=0)
    
    # ファイル名用の時刻フォーマット
    time_str = rounded_time.strftime("%Y%m%d_%H.%Mh")
    
    # 新しいファイル名を生成
    new_filename = f"{name}.bk{time_str}{ext}"
    
    return os.path.join(directory, new_filename)

class BACKUP_OT_auto_backup(bpy.types.Operator):
    bl_idname = "backup.auto_backup"
    bl_label = "保存してバックアップ"
    bl_description = "現在のファイルを保存してからバックアップします"
    
    def execute(self, context):
        current_file = bpy.data.filepath
        
        # ファイルが未保存の場合、まず保存する
        if not current_file:
            bpy.ops.wm.save_mainfile('INVOKE_AREA')
            self.report({'INFO'}, "ファイルを保存してから再度実行してください")
            return {'CANCELLED'}
        
        # 現在の変更を保存
        bpy.ops.wm.save_mainfile()
        
        # バックアップファイル名を生成
        backup_path = get_backup_filename()
        
        if not backup_path:
            self.report({'ERROR'}, "バックアップファイル名の生成に失敗しました")
            return {'CANCELLED'}
        
        try:
            # ファイルをコピーしてバックアップ
            shutil.copy2(current_file, backup_path)
            
            # プロパティを更新
            context.scene.backupItem.backup_path = backup_path
            context.scene.backupItem.backup_name = os.path.basename(backup_path)
            context.scene.backupItem.last_backup_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            self.report({'INFO'}, f"バックアップ完了: {os.path.basename(backup_path)}")
        except Exception as e:
            self.report({'ERROR'}, f"バックアップ失敗: {str(e)}")
            return {'CANCELLED'}
        
        return {'FINISHED'}
    
# UIパネル
class VIEW3D_PT_blender_backup(bpy.types.Panel):
    bl_label = J.PANEL_LABEL
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = J.PANEL_NAME

    def draw(self, context):
        layout = self.layout
        item = context.scene.backupItem

        # 現在のファイル状態を表示
        current_file = bpy.data.filepath
        if not current_file:
            layout.label(text="ファイルが保存されていません", icon='ERROR')
            layout.operator("backup.auto_backup", text="保存してバックアップ", icon='FILE_BACKUP')
            return
        
        # ファイル情報を表示
        box = layout.box()
        box.label(text="現在のファイル:", icon='FILE_BLEND')
        box.label(text=os.path.basename(current_file))
        
        # バックアップ情報を表示
        layout.separator()
        layout.label(text="バックアップファイル名:", icon='BACK')
        
        # 次のバックアップファイル名をプレビュー表示
        next_backup = get_backup_filename()
        if next_backup:
            backup_box = layout.box()
            backup_box.label(text=os.path.basename(next_backup))
        
        # 最後のバックアップ情報を表示
        if item.backup_name:
            layout.separator()
            layout.label(text="最後のバックアップ:", icon='CHECKMARK')
            last_box = layout.box()
            last_box.label(text=item.backup_name)
            if item.last_backup_time:
                last_box.label(text=f"日時: {item.last_backup_time}")
        
        # 操作ボタン
        layout.separator()
        layout.operator("backup.auto_backup", text="保存してバックアップ", icon='FILE_BACKUP')


# # プロパティグループ拡張
# class BackupItem(bpy.types.PropertyGroup):
#     src_path: bpy.props.StringProperty(name="現在のファイルパス", default="")
#     dst_path: bpy.props.StringProperty(name="保存先ファイルパス", default="")

# # バックアップ保存オペレーター
# class BACKUP_OT_save(bpy.types.Operator):
#     bl_idname = "backup.save"
#     bl_label = "バックアップ保存"

#     def execute(self, context):
#         scene = context.scene
#         item = scene.backup

#         if not bpy.data.filepath:
#             self.report({'ERROR'}, "まず.blendファイルを保存してください")
#             return {'CANCELLED'}

#         # 元ファイル名
#         src_path = bpy.data.filepath
#         item.src_path = src_path
#         dirname = os.path.dirname(src_path)
#         basename = os.path.basename(src_path)

#         # 30分区切りの時刻フォーマット
#         now = datetime.now()
#         minute_block = (now.minute // 30) * 30
#         rounded_time = now.replace(minute=minute_block, second=0, microsecond=0)
#         time_str = rounded_time.strftime("%Y%m%d_%H.%Mh")

#         # 新しいファイル名
#         dst_name = f"bk_{time_str}_{basename}"
#         dst_path = os.path.join(dirname, dst_name)
#         item.dst_path = dst_path

#         # 保存処理
#         bpy.ops.wm.save_as_mainfile(filepath=dst_path, copy=True)
#         self.report({'INFO'}, f"バックアップ保存: {dst_path}")
#         return {'FINISHED'}

# # 保存先を手動で変更するオペレーター
# class BACKUP_OT_change_path(bpy.types.Operator):
#     bl_idname = "backup.change_path"
#     bl_label = "保存先を変更"

#     filepath: bpy.props.StringProperty(subtype="FILE_PATH")

#     def execute(self, context):
#         context.scene.backup.dst_path = self.filepath
#         return {'FINISHED'}

#     def invoke(self, context, event):
#         context.window_manager.fileselect_add(self)
#         return {'RUNNING_MODAL'}

# # プロパティ初期化用ハンドラ
# def update_backup_paths(scene):
#     if not bpy.data.filepath:
#         return
#     item = scene.backup
#     src_path = bpy.data.filepath
#     item.src_path = src_path
#     dirname = os.path.dirname(src_path)
#     basename = os.path.basename(src_path)

#     # 30分区切りの時刻
#     from datetime import datetime
#     now = datetime.now()
#     minute_block = (now.minute // 30) * 30
#     rounded_time = now.replace(minute=minute_block, second=0, microsecond=0)

#     # ".0h" / ".5h" を明示
#     half = ".0h" if rounded_time.minute == 0 else ".5h"
#     time_str = rounded_time.strftime("%Y%m%d_%H") + half

#     # 保存ファイル名
#     dst_name = f"bk_{time_str}_{basename}"
#     item.dst_path = os.path.join(dirname, dst_name)
    
# # UIパネル
# class VIEW3D_PT_blender_backup(bpy.types.Panel):
#     bl_label = J.PANEL_LABEL
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_category = J.PANEL_NAME

#     def draw(self, context):
#         layout = self.layout
#         item = context.scene.backup

#         # 毎回描画時に保存パスを更新（30分単位で切り替わる）
#         update_backup_paths(context.scene)

#         layout.label(text="現在のファイル:")
#         layout.label(text=item.src_path if item.src_path else "未保存")

#         layout.separator()
#         layout.label(text="バックアップ先:")
#         layout.label(text=item.dst_path if item.dst_path else "未設定")

#         row = layout.row(align=True)
#         row.operator("backup.save", text="保存", icon="FILE_TICK")
#         row.operator("backup.change_path", text="保存先を変更", icon="FILE_FOLDER")