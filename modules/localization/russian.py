"""
SCAM (Stalker Character Adjustment Manager) Localization System
Russian Language File

This module contains all user-facing text strings for easy translation.
To add support for other languages, create similar files with translated strings.
"""

# Application metadata
APP_INFO = {
    "author": "Создал v3fish",
    "credits": "Благодарности: repak.exe от github.com/trumank",
    "version": "Версия: {version}"
}

# Font configuration for Russian UI
FONTS = {
    "default": ("Segoe UI", 9),
    "bold": ("Segoe UI", 9, "bold"),
    "small": ("Segoe UI", 8),
    "small_bold": ("Segoe UI", 8, "bold"),
    "small_italic": ("Segoe UI", 8, "italic"),
    "small_italic_bold": ("Segoe UI", 8, "italic", "bold"),
    "large": ("Segoe UI", 10),
    "large_bold": ("Segoe UI", 10, "bold"),
    "tab": ("Segoe UI", 10, "bold"),
    "button": ("Segoe UI", 10, "bold"),
    "description": ("Segoe UI", 9)
}

# Window and dialog titles
TITLES = {
    "new_preset": "Новый пресет",
    "confirm_overwrite": "Подтвердить перезапись", 
    "confirm_removal": "Подтвердить удаление",
    "confirm_force_defaults": "Подтвердить принудительные значения по умолчанию",
    "create_mod_locally": "Создать мод локально",
    "no_directory_set": "Каталог не задан",
    "invalid_values": "Неверные значения",
    "instructions": "Инструкции",
    "incompatible_mods": "Несовместимые моды",
    "success": "Успех",
    "error": "Ошибка",
    "warning": "Предупреждение",
    "language_selection": "Выбор языка"
}

# Button labels
BUTTONS = {
    "ok": "ОК",
    "cancel": "Отмена",
    "load": "Загрузить",
    "save": "Сохранить",
    "new_preset": "Новый пресет",
    "open_presets_folder": "Открыть папку пресетов",
    "create_mod": "Создать мод",
    "update_mod": "Обновить мод", 
    "remove_mod": "Удалить мод",
    "default": "По умолчанию",
    "browse": "Обзор",
    "open_mod_directory": "Открыть папку мода",
    "remove_mouse_smoothing": "Убрать сглаживание мыши",
    "re_enable_mouse_smoothing": "Включить сглаживание мыши",
    "language": "Язык"
}

# Form labels and text
LABELS = {
    "enter_preset_name": "Введите имя пресета:",
    "custom_presets": "Пользовательские пресеты:",
    "game_directory": "Каталог игры:",
    "sync_turn_look_rate": "Синхронизировать скорость поворота/взгляда",
    "force_default_values": "Принудительные значения по умолчанию",
    "set_game_directory_note": "Укажите каталог игры, если хотите использовать автоматическую установку мода:",
    "example_paths": "Примеры путей:",
    "steam_path": "Steam: C:\\Program Files (x86)\\Steam\\steamapps\\common\\S.T.A.L.K.E.R. 2 Heart of Chornobyl",
    "xbox_path": "Xbox: C:\\XboxGames\\S.T.A.L.K.E.R. 2- Heart of Chornobyl (Windows)\\Content",
    "advanced_force_defaults": "Расширенные настройки: Включить все значения по умолчанию в файл мода. Используйте только если нужно предотвратить изменение других модов определенных значений по умолчанию.",
    "default_on": "По умолчанию: Вкл",
    "default_off": "По умолчанию: Выкл",
    "default_value": "По умолчанию: {value}",
    "max_value": "Макс: {max}",
    "generated_by": "Создано SCAM (Stalker Character Adjustment Manager) от v3fish",
    "select_language": "Выберите язык:",
    "language_restart_note": "Язык изменится после перезапуска приложения."
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
    "default": "По умолчанию",
    "v3fish_recommended": "Рекомендованный V3Fish", 
    "xy_sensitivity_fix": "Исправление чувствительности XY при прицеливании"
}

# Tab/Section names
SECTIONS = {
    "movement_params": "Параметры движения",
    "aiming": "Прицеливание"
}

# Success messages
SUCCESS_MESSAGES = {
    "preset_saved": "Пресет успешно сохранен!",
    "mod_created": "Мод успешно создан!",
    "mod_updated": "Мод успешно обновлен!",
    "mod_removed": "Мод успешно удален!",
    "mod_created_local": "Мод был создан в текущей папке.",
    "mouse_settings_removed": "Настройки сглаживания мыши были удалены",
    "mouse_settings_added": "Настройки сглаживания мыши были добавлены",
    "language_changed": "Язык изменен на {language}. Пожалуйста, перезапустите приложение."
}

# Warning messages
WARNING_MESSAGES = {
    "make_changes_before_saving": "Внесите изменения перед сохранением пресета!",
    "make_changes_before_creating": "Внесите изменения перед созданием мода!",
    "incompatible_mods_detected": """Похоже, что у вас установлен Fluid Movement Aiming Overhaul.

Пожалуйста, удалите эти моды перед игрой:
{mod_list}

Удачной охоты, Сталкер."""
}

# Error messages
ERROR_MESSAGES = {
    "invalid_values_details": "Пожалуйста, проверьте правильность всех значений!\n\nДетали:\n{details}",
    "invalid_values_fix": "Следующие проблемы нужно исправить:\n\n{issues}",
    "invalid_stalker_directory": """Неверный каталог Stalker 2!

Каталог должен содержать папку 'Stalker2'.

Примеры путей:
Steam: C:\\Program Files (x86)\\Steam\\steamapps\\common\\S.T.A.L.K.E.R. 2 Heart of Chornobyl
Xbox: C:\\XboxGames\\S.T.A.L.K.E.R. 2- Heart of Chornobyl (Windows)\\Content""",
    "failed_to_create_mod": "Не удалось создать мод: {error}",
    "failed_to_remove_mod": "Не удалось удалить мод: {error}",
    "failed_to_update_input_ini": "Не удалось обновить Input.ini: {error}",
    "failed_to_create_input_ini": "Не удалось создать Input.ini: {error}",
    "failed_to_run_repak": "Не удалось запустить repak: {error}",
    "error_during_mod_creation": "Ошибка при создании мода: {error}",
    "repak_not_found": """repak.exe не найден! Repak был включен в приложение.

Пожалуйста, убедитесь, что папка 'repak' существует и содержит repak.exe.
Папка repak должна быть в: {repak_path}

Структура папок должна быть:
📁 Ваша папка установки
   └─📄 Stalker Character Adjustment Manager.exe
   └─📁 repak
      └─📄 repak.exe""",
    "value_cannot_be_empty": "{section} - {key}: Не может быть пустым",
    "value_exceeds_maximum": "{section} - {key}: Значение {value} превышает максимум {max}",
    "value_must_be_number": "{section} - {key}: Должно быть действительным числом",
    "invalid_value_for_key": "Неверное значение для {key}!"
}

# Confirmation messages
CONFIRMATIONS = {
    "overwrite_preset": "Хотите перезаписать пресет '{preset}'?",
    "remove_mod": "Вы уверены, что хотите удалить мод?",
    "force_defaults_warning": """Включена опция 'Принудительные значения по умолчанию'. Это включит ВСЕ значения в файл мода, включая неизмененные. Это расширенная опция, которая должна использоваться только если нужно предотвратить изменение других модов значений по умолчанию.

Вы уверены, что хотите продолжить?""",
    "set_directory_now": "Каталог игры не задан.\nХотите задать его сейчас?",
    "create_mod_locally": "Каталог игры не задан. Хотите создать мод в текущей папке?"
}

# Instructions and help text
INSTRUCTIONS = {
    "input_ini_manual": """SCAM не смог найти расположение конфигурации Stalker 2.

Файл Input.ini был создан в текущей папке.

Пожалуйста, скопируйте этот файл Input.ini в одно из следующих мест:
• Steam: %LOCALAPPDATA%\\Stalker2\\Saved\\Config\\Windows
• Xbox: %LOCALAPPDATA%\\Stalker2\\Saved\\Config\\WinGDK"""
}

# Status indicators  
STATUS = {
    "mouse_smoothing_success": "Настройки сглаживания мыши были {action}"
} 