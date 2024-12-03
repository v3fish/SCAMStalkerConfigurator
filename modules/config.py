# modules/config.py
import configparser
import os

class ConfigHandler:
    def __init__(self, base_path):
        self.base_path = base_path
        self.default_config = {}
        self.descriptions = {}
        self.max_values = {}
        self.load_default_config()
        self.v3fish_config = self.load_ini_file(os.path.join(base_path, 'default_ini', 'v3fish_recommended.ini'))
        self.xy_fix_config = self.load_ini_file(os.path.join(base_path, 'default_ini', 'xysensitivityfix.ini'))

    def load_default_config(self):
        config = configparser.ConfigParser()
        config.optionxform = str
        config.read(os.path.join(self.base_path, 'default_ini', 'default_values.ini'))
        
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
        config.read(filename)
        
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