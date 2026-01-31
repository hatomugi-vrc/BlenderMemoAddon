# プログラム的に使ってないように見えるがアドオンインポート時これがないとエラーになる
bl_info = {
    "name": "はとむぎつーる",
    "blender": (2, 80, 0),
    "category": "3D View",
}

import bpy
from . import memoTool
from . import backupTool

# クラスリスト
classes = [
    #メモツール
    memoTool.MemoItem,
    memoTool.MEMO_OT_add,
    memoTool.MEMO_OT_remove,
    memoTool.MEMO_OT_move,
    memoTool.VIEW3D_PT_blender_memo,

    #バックアップツール
    backupTool.BackupItem,
    # backupTool.BACKUP_OT_change_path,
    backupTool.BACKUP_OT_auto_backup,
    backupTool.VIEW3D_PT_blender_backup,
    
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    # プロパティ登録
    bpy.types.Scene.memoList = bpy.props.CollectionProperty(type=memoTool.MemoItem)
    bpy.types.Scene.backupItem = bpy.props.PointerProperty(type=backupTool.BackupItem)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.memoList
    del bpy.types.Scene.backupItem

if __name__ == "__main__":
    register()
