"""
SCAM (Stalker Character Adjustment Manager) Localization System
Korean Language File

This module contains all user-facing text strings for easy translation.
To add support for other languages, create similar files with translated strings.
"""

# Application metadata
APP_INFO = {
    "author": "제작자 v3fish",
    "credits": "감사: repak.exe by github.com/trumank",
    "version": "버전: {version}"
}

# Font configuration for Korean UI
FONTS = {
    "default": ("Malgun Gothic", 10),
    "bold": ("Malgun Gothic", 10, "bold"),
    "small": ("Malgun Gothic", 8),
    "small_bold": ("Malgun Gothic", 9, "bold"),
    "small_italic": ("Malgun Gothic", 9, "italic"),
    "small_italic_bold": ("Malgun Gothic", 8, "italic", "bold"),
    "large": ("Malgun Gothic", 10),
    "large_bold": ("Malgun Gothic", 9, "bold"),
    "tab": ("Malgun Gothic", 10, "bold"),
    "button": ("Malgun Gothic", 10, "bold"),
    "description": ("Malgun Gothic", 10)
}

# Window and dialog titles
TITLES = {
    "new_preset": "새 프리셋",
    "confirm_overwrite": "덮어쓰기 확인", 
    "confirm_removal": "삭제 확인",
    "confirm_force_defaults": "기본값 강제 확인",
    "create_mod_locally": "로컬에서 모드 생성",
    "no_directory_set": "디렉터리가 설정되지 않음",
    "invalid_values": "잘못된 값",
    "instructions": "지시사항",
    "incompatible_mods": "호환되지 않는 모드",
    "success": "성공",
    "error": "오류",
    "warning": "경고",
    "language_selection": "언어 선택"
}

# Button labels
BUTTONS = {
    "ok": "확인",
    "cancel": "취소",
    "load": "불러오기",
    "save": "저장",
    "new_preset": "새 프리셋",
    "open_presets_folder": "프리셋 폴더 열기",
    "create_mod": "모드 생성",
    "update_mod": "모드 업데이트", 
    "remove_mod": "모드 제거",
    "default": "기본값",
    "browse": "찾아보기",
    "open_mod_directory": "모드 디렉터리 열기",
    "remove_mouse_smoothing": "마우스 스무딩 제거",
    "re_enable_mouse_smoothing": "마우스 스무딩 다시 활성화",
    "language": "언어"
}

# Form labels and text
LABELS = {
    "enter_preset_name": "프리셋 이름을 입력하세요:",
    "custom_presets": "사용자 정의 프리셋:",
    "game_directory": "게임 디렉터리:",
    "sync_turn_look_rate": "회전/시점 속도 동기화",
    "force_default_values": "기본값 강제 적용",
    "set_game_directory_note": "자동 모드 설치를 사용하려면 게임 디렉터리를 설정하세요:",
    "example_paths": "예시 경로:",
    "steam_path": "Steam: C:\\Program Files (x86)\\Steam\\steamapps\\common\\S.T.A.L.K.E.R. 2 Heart of Chornobyl",
    "xbox_path": "Xbox: C:\\XboxGames\\S.T.A.L.K.E.R. 2- Heart of Chornobyl (Windows)\\Content",
    "advanced_force_defaults": "고급: 모든 기본값을 모드 파일에 포함합니다. 다른 모드가 특정 기본값을 변경하지 못하게 해야 할 때만 사용하세요.",
    "default_on": "기본값: 켜짐",
    "default_off": "기본값: 꺼짐",
    "default_value": "기본값: {value}",
    "max_value": "최대: {max}",
    "generated_by": "SCAM (스토커 캐릭터 조정 관리자) v3fish 제작",
    "select_language": "언어 선택:",
    "language_restart_note": "언어는 애플리케이션을 다시 시작한 후 변경됩니다."
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
    "default": "기본값",
    "v3fish_recommended": "V3Fish 추천", 
    "xy_sensitivity_fix": "XY 감도 조준 수정"
}

# Tab/Section names
SECTIONS = {
    "movement_params": "이동 매개변수",
    "aiming": "조준"
}

# Success messages
SUCCESS_MESSAGES = {
    "preset_saved": "프리셋이 성공적으로 저장되었습니다!",
    "mod_created": "모드가 성공적으로 생성되었습니다!",
    "mod_updated": "모드가 성공적으로 업데이트되었습니다!",
    "mod_removed": "모드가 성공적으로 제거되었습니다!",
    "mod_created_local": "모드가 현재 폴더에 생성되었습니다.",
    "mouse_settings_removed": "마우스 스무딩 설정이 제거되었습니다",
    "mouse_settings_added": "마우스 스무딩 설정이 추가되었습니다",
    "language_changed": "언어가 {language}로 변경되었습니다. 애플리케이션을 다시 시작해주세요."
}

# Warning messages
WARNING_MESSAGES = {
    "make_changes_before_saving": "프리셋을 저장하기 전에 변경사항을 만드세요!",
    "make_changes_before_creating": "모드를 생성하기 전에 변경사항을 만드세요!",
    "incompatible_mods_detected": """Fluid Movement Aiming Overhaul이 설치되어 있는 것 같습니다.

게임을 플레이하기 전에 이 모드들을 제거해주세요:
{mod_list}

좋은 사냥 되세요, 스토커."""
}

# Error messages
ERROR_MESSAGES = {
    "invalid_values_details": "모든 값이 올바른지 확인해주세요!\n\n세부사항:\n{details}",
    "invalid_values_fix": "다음 문제들을 수정해야 합니다:\n\n{issues}",
    "invalid_stalker_directory": """잘못된 스토커 2 디렉터리입니다!

디렉터리에 'Stalker2' 폴더가 있어야 합니다.

예시 경로:
Steam: C:\\Program Files (x86)\\Steam\\steamapps\\common\\S.T.A.L.K.E.R. 2 Heart of Chornobyl
Xbox: C:\\XboxGames\\S.T.A.L.K.E.R. 2- Heart of Chornobyl (Windows)\\Content""",
    "failed_to_create_mod": "모드 생성에 실패했습니다: {error}",
    "failed_to_remove_mod": "모드 제거에 실패했습니다: {error}",
    "failed_to_update_input_ini": "Input.ini 업데이트에 실패했습니다: {error}",
    "failed_to_create_input_ini": "Input.ini 생성에 실패했습니다: {error}",
    "failed_to_run_repak": "repak 실행에 실패했습니다: {error}",
    "error_during_mod_creation": "모드 생성 중 오류가 발생했습니다: {error}",
    "repak_not_found": """repak.exe를 찾을 수 없습니다! Repak은 {data_folder}/repak 폴더에 있어야 합니다.

'{data_folder}/repak' 폴더가 존재하고 그 안에 repak.exe가 있는지 확인해주세요.
repak 폴더는 다음 위치에 있어야 합니다: {repak_path}

예상 폴더 구조:
Stalker Character Adjustment Manager.exe
└─ {data_folder}
   └─ repak
      └─ repak.exe""",
    "database_not_found": "default_config.db를 찾을 수 없습니다! {data_folder} 폴더가 존재하고 그 안에 default_config.db가 있는지 확인해주세요.",
    "value_cannot_be_empty": "{section} - {key}: 비어있을 수 없습니다",
    "value_exceeds_maximum": "{section} - {key}: 값 {value}가 최대값 {max}를 초과합니다",
    "value_must_be_number": "{section} - {key}: 유효한 숫자여야 합니다",
    "invalid_value_for_key": "{key}에 대한 잘못된 값입니다!"
}

# Confirmation messages
CONFIRMATIONS = {
    "overwrite_preset": "프리셋 '{preset}'을 덮어쓰시겠습니까?",
    "remove_mod": "정말로 모드를 제거하시겠습니까?",
    "force_defaults_warning": """기본값 강제 적용이 활성화되었습니다. 이것은 변경되지 않은 값들을 포함하여 모든 값을 모드 파일에 포함시킵니다. 이는 다른 모드가 기본값을 변경하지 못하게 해야 할 때만 사용해야 하는 고급 옵션입니다.

계속하시겠습니까?""",
    "set_directory_now": "게임 디렉터리가 설정되지 않았습니다.\n지금 설정하시겠습니까?",
    "create_mod_locally": "게임 디렉터리가 설정되지 않았습니다. 현재 폴더에서 모드를 생성하시겠습니까?"
}

# Instructions and help text
INSTRUCTIONS = {
    "input_ini_manual": """SCAM이 스토커 2 설정 위치를 찾을 수 없었습니다.

Input.ini 파일이 현재 폴더에 생성되었습니다.

이 Input.ini 파일을 다음 위치 중 하나에 복사해주세요:
• Steam: %LOCALAPPDATA%\\Stalker2\\Saved\\Config\\Windows
• Xbox: %LOCALAPPDATA%\\Stalker2\\Saved\\Config\\WinGDK"""
}

# Status indicators  
STATUS = {
    "mouse_smoothing_success": "마우스 스무딩 설정이 {action}되었습니다"
} 