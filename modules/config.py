# modules/config.py
import configparser
import os
import json
from .localization.language_manager import get_current_localization

class ConfigHandler:
    def __init__(self, base_path, user_data_path=None):
        self.base_path = base_path
        # Use user_data_path for user files, fallback to base_path for backward compatibility
        self.user_data_path = user_data_path if user_data_path is not None else base_path
        self.default_config = {}
        self.descriptions = {}
        self.max_values = {}
        self.preferences_file = os.path.join(self.user_data_path, 'app_preferences.json')
        self.load_default_config()
        self.v3fish_config = self.load_ini_file(os.path.join(base_path, 'default_ini', 'v3fish_recommended.ini'))
        self.xy_fix_config = self.load_ini_file(os.path.join(base_path, 'default_ini', 'xysensitivityfix.ini'))

    def load_preferences(self):
        """Load user preferences from JSON file"""
        if os.path.exists(self.preferences_file):
            try:
                with open(self.preferences_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}

    def save_preferences(self, preferences):
        """Save user preferences to JSON file"""
        try:
            with open(self.preferences_file, 'w') as f:
                json.dump(preferences, f, indent=2)
        except:
            pass

    def get_last_selected_preset(self):
        """Get the last selected preset from preferences"""
        prefs = self.load_preferences()
        return prefs.get('last_selected_preset', '')

    def set_last_selected_preset(self, preset_name):
        """Save the last selected preset to preferences"""
        prefs = self.load_preferences()
        prefs['last_selected_preset'] = preset_name
        self.save_preferences(prefs)

    def get_last_settings(self):
        """Get the last saved settings from preferences"""
        prefs = self.load_preferences()
        return prefs.get('last_settings', {})

    def set_last_settings(self, settings):
        """Save the last settings to preferences"""
        prefs = self.load_preferences()
        prefs['last_settings'] = settings
        # Don't override preset selection when saving settings
        self.save_preferences(prefs)

    def clear_last_settings(self):
        """Clear the last saved settings and preset selection"""
        prefs = self.load_preferences()
        prefs['last_settings'] = {}
        prefs['last_selected_preset'] = ''
        self.save_preferences(prefs)
    
    def clear_last_settings_only(self):
        """Clear only the last saved settings, keep preset selection"""
        prefs = self.load_preferences()
        prefs['last_settings'] = {}
        self.save_preferences(prefs)

    def load_default_config(self):
        config = configparser.ConfigParser()
        config.optionxform = str
        
        # Map language codes to INI file suffixes
        lang_to_ini_suffix = {
            'korean': 'ko',
            'russian': 'ru', 
            'ukrainian': 'uk',
            'chinese': 'zh'
        }
        
        # Try to load language-specific INI file first
        try:
            # Check if app_preferences.json exists and get language from there
            if os.path.exists(self.preferences_file):
                with open(self.preferences_file, 'r') as f:
                    prefs = json.load(f)
                    lang_code = prefs.get('language', 'en')
            else:
                lang_code = 'en'
                
            if lang_code != 'en':  # Skip for English (default)
                # Map language code to INI suffix
                ini_suffix = lang_to_ini_suffix.get(lang_code, lang_code)
                
                # Try to load language-specific INI file
                lang_file = f'default_values_{ini_suffix}.ini'
                lang_path = os.path.join(self.base_path, 'default_ini', lang_file)
                
                if os.path.exists(lang_path):
                    config.read(lang_path, encoding='utf-8')
                else:
                    # Fall back to default if language file doesn't exist
                    config.read(os.path.join(self.base_path, 'default_ini', 'default_values.ini'), encoding='utf-8')
            else:
                # Load default for English
                config.read(os.path.join(self.base_path, 'default_ini', 'default_values.ini'), encoding='utf-8')
        except:
            # Fall back to default if any error occurs
            config.read(os.path.join(self.base_path, 'default_ini', 'default_values.ini'), encoding='utf-8')
        
        for section in config.sections():
            self.default_config[section] = {}
            self.descriptions[section] = {}
            self.max_values[section] = {}
            for key, value in config.items(section):
                if key.startswith(';'): continue
                
                parts = value.split(';', 1)
                value_parts = parts[0].strip().split('|', 1)
                raw_value = value_parts[0].strip()
                max_value = value_parts[1].strip() if len(value_parts) > 1 else None
                description = parts[1].strip() if len(parts) > 1 else ''
                
                try:
                    if raw_value.lower() in ['true', 'false']:
                        self.default_config[section][key] = raw_value.lower() == 'true'
                    elif '.' in raw_value:
                        self.default_config[section][key] = float(raw_value)
                    else:
                        self.default_config[section][key] = int(raw_value)
                except ValueError:
                    self.default_config[section][key] = raw_value
                    
                if max_value:
                    try:
                        if '.' in max_value:
                            self.max_values[section][key] = float(max_value)
                        else:
                            self.max_values[section][key] = int(max_value)
                    except ValueError:
                        pass
                        
                if description:
                    self.descriptions[section][key] = description

    def load_ini_file(self, filename):
        config = configparser.ConfigParser()
        config.optionxform = str
        config.read(filename, encoding='utf-8')
        
        result = {}
        for section in config.sections():
            result[section] = {}
            for key, value in config.items(section):
                if key.startswith(';'): continue
                
                value = value.split(';')[0].strip()
                try:
                    if value.lower() in ['true', 'false']:
                        result[section][key] = value.lower() == 'true'
                    elif '.' in value:
                        result[section][key] = float(value)
                    else:
                        result[section][key] = int(value)
                except ValueError:
                    result[section][key] = value
        return result

    def save_ini_file(self, config, filename):
        ini = configparser.ConfigParser()
        ini.optionxform = str
        for section, values in config.items():
            if values:
                ini[section] = {k: str(v) for k, v in values.items()}
            
        with open(filename, 'w') as f:
            ini.write(f)