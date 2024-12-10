# modules/config_interface.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import configparser
import shutil

class ConfigInterface:
    def __init__(self, parent, config_handler):
        self.parent = parent
        self.config_handler = config_handler
        self.entries = {}
        self.checkboxes = {}
        self.sync_sensitivity = tk.BooleanVar(value=False)
        self.game_dir = tk.StringVar()
        self.dir_entry = None
        self.mouse_btn = None
        self.mod_exists = False
        
        # Add trace to game_dir
        self.game_dir.trace_add('write', self._on_game_dir_change)
        
        self.load_saved_directory()

    def _on_game_dir_change(self, *args):
        """Called whenever game_dir StringVar changes"""
        path = self.game_dir.get()
        if path and os.path.exists(path) and os.path.exists(os.path.join(path, "Stalker2")):
            self._check_mod_exists()
            # Notify parent GUI to update buttons
            if hasattr(self.parent, 'update_mod_buttons'):
                self.parent.update_mod_buttons()

    def _check_mod_exists(self):
        """Internal method to check if mod exists"""
        self.mod_exists = False
        path = self.game_dir.get()
        if path and os.path.exists(path) and os.path.exists(os.path.join(path, "Stalker2")):
            mods_path = os.path.join(path, "Stalker2", "Content", "Paks", "~mods")
            mod_file = os.path.join(mods_path, 'z_SCAMMovementAiming_P.pak')
            self.mod_exists = os.path.exists(mod_file)

    def update_mod_status(self):
        """Public method to check mod status"""
        self._check_mod_exists()

    def validate_game_directory(self, path, show_error=True):
        """Validate directory"""
        if not path:
            return False
            
        valid = os.path.exists(path) and os.path.exists(os.path.join(path, "Stalker2"))
        
        if valid:
            self._check_mod_exists()
        
        if show_error and not valid:
            messagebox.showerror("Error", 
                "Invalid Stalker 2 directory!\n\n"
                "Directory should contain 'Stalker2' folder.\n\n"
                "Example paths:\n"
                "Steam: C:\\Program Files (x86)\\Steam\\steamapps\\common\\S.T.A.L.K.E.R. 2 Heart of Chornobyl\n"
                "Xbox: C:\\XboxGames\\S.T.A.L.K.E.R. 2- Heart of Chornobyl (Windows)\\Content")
        
        return valid

    def load_saved_directory(self):
        try:
            config = configparser.ConfigParser()
            config.read('stalker_location.ini')
            if 'Directory' in config and 'path' in config['Directory']:
                saved_dir = config['Directory']['path']
                if saved_dir and os.path.exists(saved_dir):
                    self.game_dir.set(saved_dir)
                    # Initial mod check
                    self._check_mod_exists()
        except:
            pass

    def save_directory(self, directory):
        if directory:
            config = configparser.ConfigParser()
            config['Directory'] = {'path': directory}
            with open('stalker_location.ini', 'w') as f:
                config.write(f)

    def setup_game_dir_frame(self, frame):
        dir_frame = ttk.Frame(frame)
        dir_frame.pack(fill='x', padx=5, pady=5)

        note_frame = ttk.Frame(dir_frame)
        note_frame.pack(fill='x', pady=(0, 5))
        
        ttk.Label(note_frame, text="Set a game directory if you want to use the automatic mod install:",
                 font=('Arial', 8)).pack(side='left')

        label_frame = ttk.Frame(dir_frame)
        label_frame.pack(fill='x', pady=(0, 5))

        ttk.Label(label_frame, text="Example paths:", font=('Arial', 8)).pack(side='left')
        ttk.Label(label_frame, text="Steam: C:\\Program Files (x86)\\Steam\\steamapps\\common\\S.T.A.L.K.E.R. 2 Heart of Chornobyl", 
                font=('Arial', 8)).pack(side='left', padx=5)
        ttk.Label(label_frame, text="Xbox: C:\\XboxGames\\S.T.A.L.K.E.R. 2- Heart of Chornobyl (Windows)\\Content",
                font=('Arial', 8)).pack(side='left', padx=5)

        input_frame = ttk.Frame(dir_frame)
        input_frame.pack(fill='x')

        ttk.Label(input_frame, text="Game Directory:").pack(side='left', padx=5)
        self.dir_entry = ttk.Entry(input_frame, textvariable=self.game_dir, width=55)
        self.dir_entry.pack(side='left', padx=5, fill='x', expand=True)

        ttk.Button(input_frame, text="Browse", command=self.browse_directory).pack(side='left', padx=5)
        ttk.Button(input_frame, text="Open Mod Directory", command=self.open_game_directory).pack(side='left', padx=5)

    def browse_directory(self):
        dir_path = filedialog.askdirectory(title="Select Stalker 2 Directory")
        if dir_path:
            if self.validate_game_directory(dir_path, show_error=True):
                self.game_dir.set(dir_path)
                self.save_directory(dir_path)

    def open_game_directory(self):
        if not self.game_dir.get():
            if messagebox.askyesno("No Directory Set", 
                "Game directory is not set.\nWould you like to set it now?"):
                self.browse_directory()
            return
            
        if not self.validate_game_directory(self.game_dir.get(), show_error=True):
            return
            
        mods_path = os.path.join(self.game_dir.get(), "Stalker2", "Content", "Paks", "~mods")
        if not os.path.exists(mods_path):
            os.makedirs(mods_path)
        os.startfile(mods_path)

    def validate_mods_directory(self):
        if not self.game_dir.get():
            if messagebox.askyesno("Create Mod Locally", 
                "No game directory set. Would you like to create the mod in the current folder instead?"):
                return (True, os.getcwd())
            return False
            
        if not self.validate_game_directory(self.game_dir.get(), show_error=True):
            return False
            
        mods_path = os.path.join(self.game_dir.get(), "Stalker2", "Content", "Paks", "~mods")
        if not os.path.exists(mods_path):
            os.makedirs(mods_path)
            
        return (False, mods_path)

    def remove_mod(self):
        """Remove the mod file"""
        try:
            if self.game_dir.get() and self.validate_game_directory(self.game_dir.get(), show_error=False):
                mods_path = os.path.join(self.game_dir.get(), "Stalker2", "Content", "Paks", "~mods")
                mod_file = os.path.join(mods_path, 'z_SCAMMovementAiming_P.pak')
                if os.path.exists(mod_file):
                    os.remove(mod_file)
                    self.mod_exists = False
                    return True
            return False
        except Exception as e:
            messagebox.showerror("Error", f"Failed to remove mod: {str(e)}")
            return False

    def get_mouse_smoothing_state(self):
        config_paths = [
            os.path.join(os.getenv('LOCALAPPDATA'), 'Stalker2', 'Saved', 'Config', 'Windows', 'Input.ini'),
            os.path.join(os.getenv('LOCALAPPDATA'), 'Stalker2', 'Saved', 'Config', 'WinGDK', 'Input.ini')
        ]
        
        mouse_settings = {
            'bViewAccelerationEnabled': 'False',
            'bEnableMouseSmoothing': 'False'
        }
        
        for path in config_paths:
            if os.path.exists(path):
                try:
                    with open(path, 'r') as f:
                        content = f.read()
                        if '[/Script/Engine.InputSettings]' in content:
                            # Check if any settings are missing or have different values
                            for setting, value in mouse_settings.items():
                                setting_str = f"{setting}={value}"
                                if setting_str not in content:
                                    return True
                            return False
                except:
                    pass
        return True

    def get_mouse_smoothing_button_text(self):
        return "Remove Mouse Smoothing" if self.get_mouse_smoothing_state() else "Re-Enable Mouse Smoothing"

    def toggle_mouse_smoothing(self):
        config_paths = [
            os.path.join(os.getenv('LOCALAPPDATA'), 'Stalker2', 'Saved', 'Config', 'Windows'),
            os.path.join(os.getenv('LOCALAPPDATA'), 'Stalker2', 'Saved', 'Config', 'WinGDK')
        ]
        
        input_ini_found = False
        current_state = self.get_mouse_smoothing_state()
        new_state = not current_state
        
        mouse_settings = {
            'bViewAccelerationEnabled': 'False',
            'bEnableMouseSmoothing': 'False'
        }
        
        for path in config_paths:
            if not os.path.exists(path):
                continue
                
            input_ini_path = os.path.join(path, 'Input.ini')
            if os.path.exists(input_ini_path):
                try:
                    with open(input_ini_path, 'r') as f:
                        lines = f.readlines()
                    
                    new_content = []
                    sections = {}
                    current_section = None
                    
                    # First pass: organize content into sections
                    for line in lines:
                        stripped_line = line.strip()
                        if stripped_line.startswith('['):
                            current_section = stripped_line
                            sections[current_section] = []
                        elif current_section and stripped_line:
                            if current_section == '[/Script/Engine.InputSettings]':
                                if not any(setting in line for setting in mouse_settings.keys()):
                                    sections[current_section].append(line)
                            else:
                                sections[current_section].append(line)
                    
                    # Second pass: reconstruct content
                    input_settings = '[/Script/Engine.InputSettings]'
                    
                    # Handle InputSettings section
                    if input_settings in sections and sections[input_settings]:
                        new_content.append(f"{input_settings}\n")
                        new_content.extend(sections[input_settings])
                        if not new_state:
                            if not new_content[-1].endswith('\n'):
                                new_content.append('\n')
                    elif not new_state:
                        new_content.append(f"{input_settings}\n")
                    
                    # Add mouse settings if removing mouse smoothing
                    if not new_state:
                        for setting, value in mouse_settings.items():
                            new_content.append(f"{setting}={value}\n")
                    
                    # Add other sections
                    for section, content in sections.items():
                        if section != input_settings:
                            if new_content:
                                new_content.append('\n')
                            new_content.append(f"{section}\n")
                            new_content.extend(content)
                    
                    # Remove trailing empty lines
                    while new_content and new_content[-1].strip() == '':
                        new_content.pop()
                    
                    with open(input_ini_path, 'w') as f:
                        f.writelines(new_content)
                    
                    self.mouse_btn.configure(text=self.get_mouse_smoothing_button_text())
                    messagebox.showinfo("Success", 
                        "Mouse smoothing settings have been " + 
                        ("removed" if new_state else "added"))
                    input_ini_found = True
                    break
                        
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to update Input.ini: {str(e)}")
                    break
        
        if not input_ini_found:
            self.create_default_input_ini(new_state)

    def create_default_input_ini(self, smoothing_enabled):
        try:
            # Read existing content if file exists
            existing_content = {}
            if os.path.exists('Input.ini'):
                with open('Input.ini', 'r') as f:
                    current_section = None
                    for line in f:
                        line = line.strip()
                        if line.startswith('['):
                            current_section = line
                            existing_content[current_section] = []
                        elif current_section and line:
                            if not any(setting in line for setting in ['bViewAccelerationEnabled', 'bEnableMouseSmoothing']):
                                existing_content[current_section].append(line)

            # Create new content
            content = ""
            engine_settings = "[/Script/Engine.InputSettings]\n"
            
            if smoothing_enabled:
                # Remove mouse smoothing settings
                if existing_content.get('[/Script/Engine.InputSettings]'):
                    engine_settings += "\n".join(existing_content['[/Script/Engine.InputSettings]']) + "\n"
            else:
                # Add mouse smoothing settings
                engine_settings += "bViewAccelerationEnabled=False\n"
                engine_settings += "bEnableMouseSmoothing=False\n"
                if existing_content.get('[/Script/Engine.InputSettings]'):
                    engine_settings += "\n".join(existing_content['[/Script/Engine.InputSettings]']) + "\n"
            
            content += engine_settings
            
            # Add other sections
            for section, lines in existing_content.items():
                if section != '[/Script/Engine.InputSettings]':
                    content += f"\n{section}\n" + "\n".join(lines) + "\n"
                    
            with open('Input.ini', 'w') as f:
                f.write(content)
                
            instructions = (
                "SCAM couldn't locate the Stalker 2 Config location.\n\n"
                "An Input.ini file has been created in the current folder.\n\n"
                "Please copy this Input.ini file to one of these locations:\n"
                "• Steam: %LOCALAPPDATA%\\Stalker2\\Saved\\Config\\Windows\n"
                "• Xbox: %LOCALAPPDATA%\\Stalker2\\Saved\\Config\\WinGDK\n"
            )
            messagebox.showinfo("Instructions", instructions)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create Input.ini: {str(e)}")

    def setup_section_frame(self, frame, section):
        row = 0
        for key, value in self.config_handler.default_config[section].items():
            ttk.Label(frame, text=key).grid(row=row, column=0, padx=5, pady=2, sticky='e')
            
            if isinstance(value, bool):
                var = tk.BooleanVar(value=value)
                checkbox = ttk.Checkbutton(frame, variable=var)
                checkbox.grid(row=row, column=1, padx=5, pady=2, sticky='w')
                self.checkboxes[(section, key)] = var
            else:
                entry = ttk.Entry(frame)
                entry.insert(0, str(value))
                entry.grid(row=row, column=1, padx=5, pady=2, sticky='w')
                entry.bind('<KeyRelease>', lambda e, s=section, k=key: self.validate_entry(s, k))
                self.entries[(section, key)] = entry
            
            self.add_value_labels(frame, section, key, value, row)
            row += 1

    def add_value_labels(self, frame, section, key, value, row):
        if not isinstance(value, bool):
            default_text = f"Default: {value}"
            if section in self.config_handler.max_values and key in self.config_handler.max_values[section]:
                default_text += f" | Max: {self.config_handler.max_values[section][key]}"
            ttk.Label(frame, text=default_text, font=('Arial', 8)).grid(
                row=row, column=2, padx=5, pady=2, sticky='w')
        
        if section in self.config_handler.descriptions and key in self.config_handler.descriptions[section]:
            ttk.Label(frame, text=self.config_handler.descriptions[section][key], font=('Arial', 8)).grid(
                row=row, column=3, padx=5, pady=2, sticky='w')

    def setup_movement_frame(self, frame):
        row = 0
        for key, value in self.config_handler.default_config['MovementParams'].items():
            if key not in ['BaseTurnRate', 'BaseLookUpRate']:
                self.create_movement_control(frame, key, value, row)
                row += 1

    def create_movement_control(self, frame, key, value, row):
        ttk.Label(frame, text=key).grid(row=row, column=0, padx=5, pady=2, sticky='e')
        
        if isinstance(value, bool):
            var = tk.BooleanVar(value=value)
            checkbox = ttk.Checkbutton(frame, variable=var)
            checkbox.grid(row=row, column=1, padx=5, pady=2, sticky='w')
            self.checkboxes[('MovementParams', key)] = var
        else:
            entry = ttk.Entry(frame)
            entry.insert(0, str(value))
            entry.grid(row=row, column=1, padx=5, pady=2, sticky='w')
            entry.bind('<KeyRelease>', lambda e, k=key: self.validate_entry('MovementParams', k))
            self.entries[('MovementParams', key)] = entry
            
            self.add_value_labels(frame, 'MovementParams', key, value, row)

    def setup_aiming_section(self, frame):
        controls_frame = ttk.Frame(frame)
        controls_frame.grid(row=0, column=0, columnspan=4, sticky='ew', padx=5, pady=5)
        
        left_frame = ttk.Frame(controls_frame)
        left_frame.pack(side='left')
        
        right_frame = ttk.Frame(controls_frame)
        right_frame.pack(side='right')
        
        if 'Aiming' in self.config_handler.default_config and 'SyncTurnRate' in self.config_handler.default_config['Aiming']:
            self.sync_sensitivity.set(self.config_handler.default_config['Aiming']['SyncTurnRate'])
        
        sync_check = ttk.Checkbutton(left_frame, 
                                   text="Sync Turn/Look Rate", 
                                   variable=self.sync_sensitivity,
                                   command=self.sync_sensitivity_rates)
        sync_check.pack(side='left')
        
        self.mouse_btn = ttk.Button(right_frame, 
                                  text=self.get_mouse_smoothing_button_text(),
                                  command=self.toggle_mouse_smoothing)
        self.mouse_btn.pack(side='right', padx=5)
        
        self.create_aiming_controls(frame)

    def create_aiming_controls(self, frame):
        for row, key in enumerate(['BaseTurnRate', 'BaseLookUpRate'], 1):
            ttk.Label(frame, text=key).grid(row=row, column=0, padx=5, pady=2, sticky='e')
            
            entry = ttk.Entry(frame)
            entry.insert(0, str(self.config_handler.default_config['MovementParams'][key]))
            entry.grid(row=row, column=1, padx=5, pady=2, sticky='w')
            entry.bind('<KeyRelease>', lambda e, k=key: self.validate_aiming_entry(k))
            self.entries[('MovementParams', key)] = entry
            
            self.add_value_labels(frame, 'MovementParams', key, 
                                self.config_handler.default_config['MovementParams'][key], row)

    def sync_sensitivity_rates(self):
        if self.sync_sensitivity.get():
            try:
                turn_value = self.entries[('MovementParams', 'BaseTurnRate')].get()
                value = int(turn_value)
                self.entries[('MovementParams', 'BaseLookUpRate')].delete(0, tk.END)
                self.entries[('MovementParams', 'BaseLookUpRate')].insert(0, str(value))
                self.validate_entry('MovementParams', 'BaseLookUpRate')
            except ValueError:
                pass

    def validate_aiming_entry(self, key):
        entry = self.entries[('MovementParams', key)]
        current_value = entry.get()
        
        try:
            value = int(current_value)
            default_value = str(self.config_handler.default_config['MovementParams'][key])
            
            exceeds_max = False
            if 'MovementParams' in self.config_handler.max_values and key in self.config_handler.max_values['MovementParams']:
                if value > self.config_handler.max_values['MovementParams'][key]:
                    exceeds_max = True
            
            if self.sync_sensitivity.get():
                for rate_key in ['BaseTurnRate', 'BaseLookUpRate']:
                    other_entry = self.entries[('MovementParams', rate_key)]
                    other_entry.delete(0, tk.END)
                    other_entry.insert(0, str(value))
                    other_entry.configure(foreground='red' if exceeds_max else 
                        ('green' if str(value) != default_value else 'black'))
            else:
                entry.configure(foreground='red' if exceeds_max else 
                    ('green' if current_value != default_value else 'black'))
                    
        except ValueError:
            entry.configure(foreground='red')

    def validate_entry(self, section, key):
        entry = self.entries[(section, key)]
        current_value = entry.get().strip()
        default_value = str(self.config_handler.default_config[section][key])

        try:
            if not current_value and isinstance(self.config_handler.default_config[section][key], (int, float)):
                entry.configure(foreground='red')
                return False

            if isinstance(self.config_handler.default_config[section][key], (int, float)):
                if '.' in current_value:
                    value = float(current_value)
                else:
                    value = int(current_value)

                exceeds_max = False
                if section in self.config_handler.max_values and key in self.config_handler.max_values[section]:
                    if value > self.config_handler.max_values[section][key]:
                        exceeds_max = True

                entry.configure(foreground='red' if exceeds_max else 
                              ('green' if current_value != default_value else 'black'))
                return not exceeds_max

            entry.configure(foreground='black')
            return True

        except ValueError:
            entry.configure(foreground='red')
            return False

    def has_invalid_entries(self):
        invalid_values = []
        
        for (section, key), entry in self.entries.items():
            current_value = entry.get().strip()
            default_value = self.config_handler.default_config[section][key]
            
            if isinstance(default_value, (int, float)):
                if not current_value:
                    invalid_values.append(f"{section} - {key}: Cannot be empty")
                    continue
                    
                try:
                    if '.' in current_value:
                        value = float(current_value)
                    else:
                        value = int(current_value)
                        
                    if section in self.config_handler.max_values and key in self.config_handler.max_values[section]:
                        max_val = self.config_handler.max_values[section][key]
                        if value > max_val:
                            invalid_values.append(f"{section} - {key}: Value {value} exceeds maximum of {max_val}")
                except ValueError:
                    invalid_values.append(f"{section} - {key}: Must be a valid number")
            
        return bool(invalid_values), invalid_values

    def has_changes(self):
        for (section, key), entry in self.entries.items():
            current_value = entry.get().strip()
            default_value = str(self.config_handler.default_config[section][key])
            if current_value != default_value:
                return True
                
        for (section, key), checkbox in self.checkboxes.items():
            current_value = checkbox.get()
            default_value = self.config_handler.default_config[section][key]
            if current_value != default_value:
                return True
                
        if 'Aiming' in self.config_handler.default_config and 'SyncTurnRate' in self.config_handler.default_config['Aiming']:
            if self.sync_sensitivity.get() != self.config_handler.default_config['Aiming']['SyncTurnRate']:
                return True
        return False

    def update_entries(self, config):
        for (section, key), entry in self.entries.items():
            default_value = str(self.config_handler.default_config[section][key])
            entry.delete(0, tk.END)
            entry.insert(0, default_value)
            entry.configure(foreground='black')
            
        for (section, key), checkbox in self.checkboxes.items():
            default_value = self.config_handler.default_config[section][key]
            checkbox.set(default_value)

        for section in config:
            for key, value in config[section].items():
                if section == 'Aiming' and key == 'SyncTurnRate':
                    self.sync_sensitivity.set(value)
                elif isinstance(value, bool):
                    if (section, key) in self.checkboxes:
                        self.checkboxes[(section, key)].set(value)
                else:
                    if (section, key) in self.entries:
                        entry = self.entries[(section, key)]
                        entry.delete(0, tk.END)
                        entry.insert(0, str(value))
                        self.validate_entry(section, key)

    def get_current_config(self, include_defaults=False):
        config = {}
        for section in self.config_handler.default_config:
            if section != 'Aiming':
                changed_values = {}
                for key, value in self.config_handler.default_config[section].items():
                    if isinstance(value, bool):
                        current_value = self.checkboxes[(section, key)].get()
                        if include_defaults or current_value != value:
                            changed_values[key] = current_value
                    else:
                        current_value = self.entries[(section, key)].get()
                        default_value = str(value)
                        if include_defaults or current_value != default_value:
                            try:
                                if '.' in current_value:
                                    changed_values[key] = float(current_value)
                                else:
                                    changed_values[key] = int(current_value)
                            except ValueError:
                                messagebox.showerror("Error", f"Invalid value for {key}!")
                                return None
                if changed_values:
                    config[section] = changed_values

        if self.sync_sensitivity.get():
            config['Aiming'] = {'SyncTurnRate': True}

        return config