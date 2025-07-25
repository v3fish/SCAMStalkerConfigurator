"""
SCAM (Stalker Character Adjustment Manager) Localization System
English Language File

This module contains all user-facing text strings for easy translation.
To add support for other languages, create similar files with translated strings.
"""

# Application metadata
APP_INFO = {
    "author": "Made by v3fish",
    "credits": "Credits: repak.exe by github.com/trumank",
    "version": "Version: {version}"
}

# Font configuration for English UI
FONTS = {
    "default": ("Arial", 9),
    "bold": ("Arial", 9, "bold"),
    "small": ("Arial", 8),
    "small_bold": ("Arial", 8, "bold"),
    "small_italic": ("Arial", 8, "italic"),
    "small_italic_bold": ("Arial", 8, "italic", "bold"),
    "large": ("Arial", 10),
    "large_bold": ("Arial", 10, "bold"),
    "tab": ("Arial", 10, "bold"),
    "button": ("Arial", 10, "bold"),
    "description": ("Arial", 8)
}

# Window and dialog titles
TITLES = {
    "new_preset": "New Preset",
    "confirm_overwrite": "Confirm Overwrite", 
    "confirm_removal": "Confirm Removal",
    "confirm_force_defaults": "Confirm Force Defaults",
    "create_mod_locally": "Create Mod Locally",
    "no_directory_set": "No Directory Set",
    "invalid_values": "Invalid Values",
    "instructions": "Instructions",
    "incompatible_mods": "Incompatible Mods",
    "success": "Success",
    "error": "Error",
    "warning": "Warning",
    "language_selection": "Language Selection"
}

# Button labels
BUTTONS = {
    "ok": "OK",
    "cancel": "Cancel",
    "load": "Load",
    "save": "Save",
    "new_preset": "New Preset",
    "open_presets_folder": "Open Presets Folder",
    "create_mod": "Create Mod",
    "update_mod": "Update Mod", 
    "remove_mod": "Remove Mod",
    "default": "Default",
    "browse": "Browse",
    "open_mod_directory": "Open Mod Directory",
    "remove_mouse_smoothing": "Remove Mouse Smoothing",
    "re_enable_mouse_smoothing": "Re-Enable Mouse Smoothing",
    "language": "Language"
}

# Form labels and text
LABELS = {
    "enter_preset_name": "Enter preset name:",
    "custom_presets": "Custom Presets:",
    "game_directory": "Game Directory:",
    "sync_turn_look_rate": "Sync Turn/Look Rate",
    "force_default_values": "Force Default Values",
    "set_game_directory_note": "Set a game directory if you want to use the automatic mod install:",
    "example_paths": "Example paths:",
    "steam_path": "Steam: C:\\Program Files (x86)\\Steam\\steamapps\\common\\S.T.A.L.K.E.R. 2 Heart of Chornobyl",
    "xbox_path": "Xbox: C:\\XboxGames\\S.T.A.L.K.E.R. 2- Heart of Chornobyl (Windows)\\Content",
    "advanced_force_defaults": "Advanced: Include all default values in mod file. Use only if you need to prevent other mods from changing specific values from default.",
    "default_on": "Default: On",
    "default_off": "Default: Off",
    "default_value": "Default: {value}",
    "max_value": "Max: {max}",
    "generated_by": "Generated by SCAM (Stalker Character Adjustment Manager) by v3fish",
    "select_language": "Select Language:",
    "language_restart_note": "Language will change after restarting the application."
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
    "default": "Default",
    "v3fish_recommended": "V3Fish Recommended", 
    "xy_sensitivity_fix": "XY Sensitivity Aim Fix"
}

# Tab/Section names
SECTIONS = {
    "movement_params": "MovementParams",
    "aiming": "Aiming"
}

# Success messages
SUCCESS_MESSAGES = {
    "preset_saved": "Preset saved successfully!",
    "mod_created": "Mod created successfully!",
    "mod_updated": "Mod updated successfully!",
    "mod_removed": "Mod removed successfully!",
    "mod_created_local": "The mod has been created in the current folder.",
    "mouse_settings_removed": "Mouse smoothing settings have been removed",
    "mouse_settings_added": "Mouse smoothing settings have been added",
    "language_changed": "Language changed to {language}. Please restart the application."
}

# Warning messages
WARNING_MESSAGES = {
    "make_changes_before_saving": "Make changes before saving a preset!",
    "make_changes_before_creating": "Make changes before creating a mod!",
    "incompatible_mods_detected": """It looks like you have Fluid Movement Aiming Overhaul installed.

Please remove these mods before playing:
{mod_list}

Good hunting, Stalker."""
}

# Error messages
ERROR_MESSAGES = {
    "invalid_values_details": "Please verify all values are correct!\n\nDetails:\n{details}",
    "invalid_values_fix": "The following issues need to be fixed:\n\n{issues}",
    "invalid_stalker_directory": """Invalid Stalker 2 directory!

Directory should contain 'Stalker2' folder.

Example paths:
Steam: C:\\Program Files (x86)\\Steam\\steamapps\\common\\S.T.A.L.K.E.R. 2 Heart of Chornobyl
Xbox: C:\\XboxGames\\S.T.A.L.K.E.R. 2- Heart of Chornobyl (Windows)\\Content""",
    "failed_to_create_mod": "Failed to create mod: {error}",
    "failed_to_remove_mod": "Failed to remove mod: {error}",
    "failed_to_update_input_ini": "Failed to update Input.ini: {error}",
    "failed_to_create_input_ini": "Failed to create Input.ini: {error}",
    "failed_to_run_repak": "Failed to run repak: {error}",
    "error_during_mod_creation": "Error during mod creation: {error}",
    "repak_not_found": """repak.exe not found! Repak should be in the {data_folder}/repak folder.

Please make sure the '{data_folder}/repak' folder exists and contains repak.exe.
The repak folder should be at: {repak_path}

Expected folder structure:
Stalker Character Adjustment Manager.exe
└─ {data_folder}
   └─ repak
      └─ repak.exe""",
    "database_not_found": "default_config.db not found! Please make sure the {data_folder} folder exists and contains default_config.db.",
    "value_cannot_be_empty": "{section} - {key}: Cannot be empty",
    "value_exceeds_maximum": "{section} - {key}: Value {value} exceeds maximum of {max}",
    "value_must_be_number": "{section} - {key}: Must be a valid number",
    "invalid_value_for_key": "Invalid value for {key}!"
}

# Confirmation messages
CONFIRMATIONS = {
    "overwrite_preset": "Do you want to overwrite the preset '{preset}'?",
    "remove_mod": "Are you sure you want to remove the mod?",
    "force_defaults_warning": """Force Default Values is enabled. This will include ALL values in the mod file, including unchanged ones. This is an advanced option that should only be used if you need to prevent other mods from changing default values.

Are you sure you want to continue?""",
    "set_directory_now": "Game directory is not set.\nWould you like to set it now?",
    "create_mod_locally": "No game directory set. Would you like to create the mod in the current folder instead?"
}

# Instructions and help text
INSTRUCTIONS = {
    "input_ini_manual": """SCAM couldn't locate the Stalker 2 Config location.

An Input.ini file has been created in the current folder.

Please copy this Input.ini file to one of these locations:
• Steam: %LOCALAPPDATA%\\Stalker2\\Saved\\Config\\Windows
• Xbox: %LOCALAPPDATA%\\Stalker2\\Saved\\Config\\WinGDK"""
}

# Status indicators  
STATUS = {
    "mouse_smoothing_success": "Mouse smoothing settings have been {action}"
} 