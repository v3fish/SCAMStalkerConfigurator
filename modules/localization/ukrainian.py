"""
SCAM (Stalker Character Adjustment Manager) Localization System
Ukrainian Language File

This module contains all user-facing text strings for easy translation.
To add support for other languages, create similar files with translated strings.
"""

# Application metadata
APP_INFO = {
    "author": "Створив v3fish",
    "credits": "Подяки: repak.exe від github.com/trumank",
    "version": "Версія: {version}"
}

# Font configuration for Ukrainian UI
FONTS = {
    "default": ("Segoe UI", 9,),
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
    "new_preset": "Новий пресет",
    "confirm_overwrite": "Підтвердити перезапис", 
    "confirm_removal": "Підтвердити видалення",
    "confirm_force_defaults": "Підтвердити примусові значення за замовчуванням",
    "create_mod_locally": "Створити мод локально",
    "no_directory_set": "Каталог не встановлено",
    "invalid_values": "Неправильні значення",
    "instructions": "Інструкції",
    "incompatible_mods": "Несумісні моди",
    "success": "Успіх",
    "error": "Помилка",
    "warning": "Попередження",
    "language_selection": "Вибір мови"
}

# Button labels
BUTTONS = {
    "ok": "Гаразд",
    "cancel": "Скасувати",
    "load": "Завантажити",
    "save": "Зберегти",
    "new_preset": "Новий пресет",
    "open_presets_folder": "Відкрити папку пресетів",
    "refresh_presets": "Оновити",
    "create_mod": "Створити мод",
    "update_mod": "Оновити мод", 
    "remove_mod": "Видалити мод",
    "default": "За замовчуванням",
    "browse": "Огляд",
    "open_mod_directory": "Відкрити папку мода",
    "remove_mouse_smoothing": "Вимкнути згладжування миші",
    "remove_water_slowdown": "Прибрати сповільнення у воді",
    "remove_mouse_slowdown": "Прибрати сповільнення миші",
    "remove_camera_shake": "Прибрати тряску камери",
    "remove_aim_block": "Прибрати блокування прицілювання",
    "allow_overweight_movement": "Дозволити рух при перевантаженні",
    "language": "Мова"
}

# Form labels and text
LABELS = {
    "enter_preset_name": "Введіть назву пресету:",
    "custom_presets": "Користувацькі пресети:",
    "game_directory": "Каталог гри:",
    "sync_turn_look_rate": "Синхронізувати швидкість повороту/погляду",
    "force_default_values": "Примусові значення за замовчуванням",
    "set_game_directory_note": "Встановіть каталог гри, якщо хочете використовувати автоматичну установку мода:",
    "example_paths": "Приклади шляхів:",
    "steam_path": "Steam: C:\\Program Files (x86)\\Steam\\steamapps\\common\\S.T.A.L.K.E.R. 2 Heart of Chornobyl",
    "xbox_path": "Xbox: C:\\XboxGames\\S.T.A.L.K.E.R. 2- Heart of Chornobyl (Windows)\\Content",
    "advanced_force_defaults": "Розширені налаштування: Включити всі значення за замовчуванням у файл мода. Використовуйте лише якщо потрібно запобігти зміні певних значень за замовчуванням іншими модами.",
    "default_on": "За замовчуванням: Увімк",
    "default_off": "За замовчуванням: Вимк",
    "default_value": "За замовчуванням: {value}",
    "max_value": "Макс: {max}",
    "generated_by": "Створено SCAM (Stalker Character Adjustment Manager) від v3fish",
    "select_language": "Оберіть мову:",
    "language_restart_note": "Мова зміниться після перезапуску програми.",
    "disable_overweight_restriction_desc": "Прибирає блокування руху при перевантаженні",
    "remove_water_slowdown_desc": "Прибирає сповільнення руху під час ходьби у воді",
    "remove_mouse_slowdown_desc": "Прибирає сповільнення погляду (вода, гранати, аномалії, колючий дріт тощо)",
    "remove_camera_shake_desc": "Прибирає всі ефекти тряски камери (сп'яніння, стрільба, мутанти тощо)",
    "remove_aim_block_desc": "Прибирає блокування прицілювання під час контузії (гранати тощо)"
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
    "default": "За замовчуванням",
    "v3fish_recommended": "Рекомендований V3Fish", 
    "xy_sensitivity_fix": "Виправлення чутливості XY при прицілюванні"
}

# Tab/Section names
SECTIONS = {
    "movement_params": "Параметри руху",
    "aiming": "Прицілювання"
}

# Success messages
SUCCESS_MESSAGES = {
    "preset_saved": "Пресет успішно збережено!",
    "mod_created": "Мод успішно створено!",
    "mod_updated": "Мод успішно оновлено!",
    "mod_removed": "Мод успішно видалено!",
    "mod_created_local": "Мод було створено в поточній папці.",
    "mouse_settings_removed": "Налаштування згладжування миші видалено",
    "mouse_settings_added": "Налаштування згладжування миші додано",
    "language_changed": "Мову змінено на {language}. Будь ласка, перезапустіть програму."
}

# Warning messages
WARNING_MESSAGES = {
    "make_changes_before_saving": "Внесіть зміни перед збереженням пресету!",
    "make_changes_before_creating": "Внесіть зміни перед створенням мода!",
    "incompatible_mods_detected": """Схоже, що у вас встановлено Fluid Movement Aiming Overhaul.

Будь ласка, видаліть ці моди перед грою:
{mod_list}

Вдалого полювання, Сталкере."""
}

# Error messages
ERROR_MESSAGES = {
    "invalid_values_details": "Будь ласка, перевірте правильність всіх значень!\n\nДеталі:\n{details}",
    "invalid_values_fix": "Наступні проблеми потрібно виправити:\n\n{issues}",
    "invalid_stalker_directory": """Неправильний каталог Stalker 2!

Каталог повинен містити папку 'Stalker2'.

Приклади шляхів:
Steam: C:\\Program Files (x86)\\Steam\\steamapps\\common\\S.T.A.L.K.E.R. 2 Heart of Chornobyl
Xbox: C:\\XboxGames\\S.T.A.L.K.E.R. 2- Heart of Chornobyl (Windows)\\Content""",
    "failed_to_create_mod": "Не вдалося створити мод: {error}",
    "failed_to_remove_mod": "Не вдалося видалити мод: {error}",
    "failed_to_run_repak": "Не вдалося запустити repak: {error}",
    "error_during_mod_creation": "Помилка при створенні мода: {error}",
    "repak_not_found": """repak.exe не знайдено! Repak повинен бути в папці {data_folder}/repak.

Будь ласка, переконайтеся, що папка '{data_folder}/repak' існує і містить repak.exe.
Папка repak повинна бути в: {repak_path}

Очікувана структура папок:
Stalker Character Adjustment Manager.exe
└─ {data_folder}
   └─ repak
      └─ repak.exe""",
    "database_not_found": "default_config.db не знайдено! Будь ласка, переконайтеся, що папка {data_folder} існує і містить default_config.db.",
    "value_cannot_be_empty": "{section} - {key}: Не може бути порожнім",
    "value_exceeds_maximum": "{section} - {key}: Значення {value} перевищує максимум {max}",
    "value_must_be_number": "{section} - {key}: Повинно бути дійсним числом",
    "invalid_value_for_key": "Неправильне значення для {key}!"
}

# Confirmation messages
CONFIRMATIONS = {
    "overwrite_preset": "Хочете перезаписати пресет '{preset}'?",
    "remove_mod": "Ви впевнені, що хочете видалити мод?",
    "force_defaults_warning": """Увімкнено опцію 'Примусові значення за замовчуванням'. Це включить УСІ значення у файл мода, включно з незміненими. Це розширена опція, яка повинна використовуватися лише якщо потрібно запобігти зміні значень за замовчуванням іншими модами.

Ви впевнені, що хочете продовжити?""",
    "set_directory_now": "Каталог гри не встановлено.\nХочете встановити його зараз?",
    "create_mod_locally": "Каталог гри не встановлено. Хочете створити мод у поточній папці?"
}

# Instructions and help text
INSTRUCTIONS = {}

# Status indicators  
STATUS = {}
