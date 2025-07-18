"""
SCAM (Stalker Character Adjustment Manager) Localization System
Chinese Language File

This module contains all user-facing text strings for easy translation.
To add support for other languages, create similar files with translated strings.
"""

# Application metadata
APP_INFO = {
    "author": "制作者：v3fish",
    "credits": "鸣谢：repak.exe 由 github.com/trumank 提供",
    "version": "版本：{version}"
}

# Font configuration for Chinese UI
FONTS = {
    "default": ("Microsoft YaHei", 10),
    "bold": ("Microsoft YaHei", 10, "bold"),
    "small": ("Microsoft YaHei", 8),
    "small_bold": ("Microsoft YaHei", 9, "bold"),
    "small_italic": ("Microsoft YaHei", 9, "italic"),
    "small_italic_bold": ("Microsoft YaHei", 8, "italic", "bold"),
    "large": ("Microsoft YaHei", 10),
    "large_bold": ("Microsoft YaHei", 9, "bold"),
    "tab": ("Microsoft YaHei", 10, "bold"),
    "button": ("Microsoft YaHei", 10, "bold"),
    "description": ("Microsoft YaHei", 10)
}

# Window and dialog titles
TITLES = {
    "new_preset": "新建预设",
    "confirm_overwrite": "确认覆盖", 
    "confirm_removal": "确认移除",
    "confirm_force_defaults": "确认强制默认值",
    "create_mod_locally": "在本地创建模组",
    "no_directory_set": "未设置目录",
    "invalid_values": "无效值",
    "instructions": "说明",
    "incompatible_mods": "不兼容的模组",
    "success": "成功",
    "error": "错误",
    "warning": "警告",
    "language_selection": "语言选择"
}

# Button labels
BUTTONS = {
    "ok": "确定",
    "cancel": "取消",
    "load": "加载",
    "save": "保存",
    "new_preset": "新建预设",
    "open_presets_folder": "打开预设文件夹",
    "create_mod": "创建模组",
    "update_mod": "更新模组", 
    "remove_mod": "移除模组",
    "default": "默认",
    "browse": "浏览",
    "open_mod_directory": "打开模组目录",
    "remove_mouse_smoothing": "移除鼠标平滑",
    "re_enable_mouse_smoothing": "重新启用鼠标平滑",
    "language": "语言"
}

# Form labels and text
LABELS = {
    "enter_preset_name": "输入预设名称：",
    "custom_presets": "自定义预设：",
    "game_directory": "游戏目录：",
    "sync_turn_look_rate": "同步转向/观察速率",
    "force_default_values": "强制默认值",
    "set_game_directory_note": "如果要使用自动模组安装，请设置游戏目录：",
    "example_paths": "示例路径：",
    "steam_path": "Steam：C:\\Program Files (x86)\\Steam\\steamapps\\common\\S.T.A.L.K.E.R. 2 Heart of Chornobyl",
    "xbox_path": "Xbox：C:\\XboxGames\\S.T.A.L.K.E.R. 2- Heart of Chornobyl (Windows)\\Content",
    "advanced_force_defaults": "高级：在模组文件中包含所有默认值。仅在需要阻止其他模组更改特定默认值时使用。",
    "default_on": "默认：开启",
    "default_off": "默认：关闭",
    "default_value": "默认：{value}",
    "max_value": "最大值：{max}",
    "generated_by": "由 SCAM（潜行者角色调整管理器）v3fish 生成",
    "select_language": "选择语言：",
    "language_restart_note": "语言将在重启应用程序后更改。"
}

# Language names (in their native script)
LANGUAGES = {
    "english": "English",
    "russian": "Русский",
    "ukrainian": "Українська",
    "korean": "한국어",
    "chinese": "简体中文"
}

# Preset names
PRESETS = {
    "default": "默认",
    "v3fish_recommended": "V3Fish 推荐", 
    "xy_sensitivity_fix": "XY 灵敏度瞄准修复"
}

# Tab/Section names
SECTIONS = {
    "movement_params": "移动参数",
    "aiming": "瞄准"
}

# Success messages
SUCCESS_MESSAGES = {
    "preset_saved": "预设保存成功！",
    "mod_created": "模组创建成功！",
    "mod_updated": "模组更新成功！",
    "mod_removed": "模组移除成功！",
    "mod_created_local": "模组已在当前文件夹中创建。",
    "mouse_settings_removed": "鼠标平滑设置已被移除",
    "mouse_settings_added": "鼠标平滑设置已被添加",
    "language_changed": "语言已更改为 {language}。请重启应用程序。"
}

# Warning messages
WARNING_MESSAGES = {
    "make_changes_before_saving": "保存预设前请先进行更改！",
    "make_changes_before_creating": "创建模组前请先进行更改！",
    "incompatible_mods_detected": """看起来您已安装了流体移动瞄准大修模组。

请在游戏前移除这些模组：
{mod_list}

祝您狩猎愉快，潜行者。"""
}

# Error messages
ERROR_MESSAGES = {
    "invalid_values_details": "请验证所有值是否正确！\n\n详细信息：\n{details}",
    "invalid_values_fix": "需要修复以下问题：\n\n{issues}",
    "invalid_stalker_directory": """无效的潜行者 2 目录！

目录应包含 'Stalker2' 文件夹。

示例路径：
Steam：C:\\Program Files (x86)\\Steam\\steamapps\\common\\S.T.A.L.K.E.R. 2 Heart of Chornobyl
Xbox：C:\\XboxGames\\S.T.A.L.K.E.R. 2- Heart of Chornobyl (Windows)\\Content""",
    "failed_to_create_mod": "创建模组失败：{error}",
    "failed_to_remove_mod": "移除模组失败：{error}",
    "failed_to_update_input_ini": "更新 Input.ini 失败：{error}",
    "failed_to_create_input_ini": "创建 Input.ini 失败：{error}",
    "failed_to_run_repak": "运行 repak 失败：{error}",
    "error_during_mod_creation": "创建模组期间出错：{error}",
    "repak_not_found": """找不到 repak.exe！Repak 已与应用程序捆绑。

请确保 'repak' 文件夹存在并包含 repak.exe。
repak 文件夹应位于：{repak_path}

文件夹结构应为：
您的安装文件夹
   └─ Stalker Character Adjustment Manager.exe
   └─ repak
      └─ repak.exe""",
    "value_cannot_be_empty": "{section} - {key}：不能为空",
    "value_exceeds_maximum": "{section} - {key}：值 {value} 超过最大值 {max}",
    "value_must_be_number": "{section} - {key}：必须是有效数字",
    "invalid_value_for_key": "{key} 的值无效！"
}

# Confirmation messages
CONFIRMATIONS = {
    "overwrite_preset": "您要覆盖预设 '{preset}' 吗？",
    "remove_mod": "您确定要移除模组吗？",
    "force_defaults_warning": """强制默认值已启用。这将在模组文件中包含所有值，包括未更改的值。这是一个高级选项，仅在需要阻止其他模组更改默认值时使用。

您确定要继续吗？""",
    "set_directory_now": "游戏目录未设置。\n您想现在设置吗？",
    "create_mod_locally": "未设置游戏目录。您想在当前文件夹中创建模组吗？"
}

# Instructions and help text
INSTRUCTIONS = {
    "input_ini_manual": """SCAM 无法找到潜行者 2 配置位置。

已在当前文件夹中创建 Input.ini 文件。

请将此 Input.ini 文件复制到以下位置之一：
• Steam：%LOCALAPPDATA%\\Stalker2\\Saved\\Config\\Windows
• Xbox：%LOCALAPPDATA%\\Stalker2\\Saved\\Config\\WinGDK"""
}

# Status indicators  
STATUS = {
    "mouse_smoothing_success": "鼠标平滑设置已 {action}"
} 