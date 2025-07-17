# modules/config_interface.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import configparser
import shutil
from .localization.language_manager import get_current_localization, t, font

class ConfigInterface:
    def __init__(self, parent, config_handler):
        self.parent = parent
        self.config_handler = config_handler
        # Use the same user_data_path as the config_handler for consistency
        self.user_data_path = config_handler.user_data_path
        self.entries = {}
        self.checkboxes = {}
        self.labels = {}  # Store label references for color changes
        self.default_buttons = {}  # Track default buttons for each setting
        self.notebook = None  # Reference to the notebook widget for tab color updates
        self.sync_sensitivity = tk.BooleanVar(value=False)
        self.game_dir = tk.StringVar()
        self.dir_entry = None
        self.mouse_btn = None
        self.mod_exists = False
        
        # Initialize style object (may be used for other styling)
        self.style = ttk.Style()
        
        # Add trace to game_dir
        self.game_dir.trace_add('write', self._on_game_dir_change)
        
        self.load_saved_directory()

    def find_correct_game_directory(self, selected_path):
        """
        Find the correct Stalker2 game directory even if user selected wrong folder.
        Returns the corrected path or None if not found.
        """
        if not selected_path or not os.path.exists(selected_path):
            return None
        
        # Function to check if a directory is a valid game directory
        def is_valid_game_dir(path):
            stalker2_path = os.path.join(path, "Stalker2")
            return os.path.exists(stalker2_path) and os.path.isdir(stalker2_path)
        
        # First, check if the selected path is already correct
        if is_valid_game_dir(selected_path):
            return selected_path
        
        # If user selected the Stalker2 folder itself, return its parent
        if os.path.basename(selected_path.rstrip(os.sep)) == "Stalker2":
            parent_path = os.path.dirname(selected_path)
            if is_valid_game_dir(parent_path):
                return parent_path
        
        # If user selected the ~mods folder, go up to find the game directory
        # Path structure: GameDir/Stalker2/Content/Paks/~mods
        if os.path.basename(selected_path.rstrip(os.sep)) == "~mods":
            # Go up 4 levels: ~mods -> Paks -> Content -> Stalker2 -> GameDir
            current = selected_path
            for _ in range(4):
                current = os.path.dirname(current)
                if is_valid_game_dir(current):
                    return current
        
        # Search in subdirectories (user might have selected parent folder)
        try:
            for root, dirs, files in os.walk(selected_path):
                if "Stalker2" in dirs:
                    potential_path = root
                    if is_valid_game_dir(potential_path):
                        return potential_path
                # Limit search depth to avoid going too deep
                if root.count(os.sep) - selected_path.count(os.sep) >= 2:
                    break
        except (PermissionError, OSError):
            pass
        
        # Search in parent directories (user might have selected subfolder)
        current_path = selected_path
        for _ in range(3):  # Check up to 3 levels up
            parent_path = os.path.dirname(current_path)
            if parent_path == current_path:  # Reached root
                break
            if is_valid_game_dir(parent_path):
                return parent_path
            current_path = parent_path
        
        # Try common Steam/Xbox alternative paths if user selected wrong subfolder
        common_patterns = [
            "steamapps/common",
            "XboxGames",
            "S.T.A.L.K.E.R. 2",
            "Stalker 2",
            "Heart of Chornobyl"
        ]
        
        # Look for these patterns in the path and try parent directories
        for pattern in common_patterns:
            if pattern.lower() in selected_path.lower():
                test_path = selected_path
                for _ in range(4):  # Check several levels up
                    if is_valid_game_dir(test_path):
                        return test_path
                    parent = os.path.dirname(test_path)
                    if parent == test_path:
                        break
                    test_path = parent
        
        return None

    def set_notebook_reference(self, notebook):
        """Set reference to the notebook widget for tab color updates"""
        self.notebook = notebook

    def has_category_changes(self, section):
        """Check if a specific category has any changes from defaults"""
        # Special case for Aiming section - check aiming-related MovementParams
        if section == 'Aiming':
            # Check sync sensitivity setting
            if 'Aiming' in self.config_handler.default_config and 'SyncTurnRate' in self.config_handler.default_config['Aiming']:
                if self.sync_sensitivity.get() != self.config_handler.default_config['Aiming']['SyncTurnRate']:
                    return True
            
            # Check BaseTurnRate and BaseLookUpRate (displayed in Aiming tab but stored as MovementParams)
            for aiming_key in ['BaseTurnRate', 'BaseLookUpRate']:
                if ('MovementParams', aiming_key) in self.entries:
                    entry = self.entries[('MovementParams', aiming_key)]
                    current_value = entry.get().strip()
                    default_value = str(self.config_handler.default_config['MovementParams'][aiming_key])
                    if current_value != default_value:
                        return True
            return False
        
        # Special case for MovementParams - exclude aiming-related settings that are shown in Aiming tab
        if section == 'MovementParams':
            for (sec, key), entry in self.entries.items():
                if sec == section and key not in ['BaseTurnRate', 'BaseLookUpRate']:
                    current_value = entry.get().strip()
                    default_value = str(self.config_handler.default_config[section][key])
                    if current_value != default_value:
                        return True
            
            for (sec, key), checkbox in self.checkboxes.items():
                if sec == section:
                    current_value = checkbox.get()
                    default_value = self.config_handler.default_config[section][key]
                    if current_value != default_value:
                        return True
            
            return False
        
        # General case for all other sections
        # Check entries
        for (sec, key), entry in self.entries.items():
            if sec == section:
                current_value = entry.get().strip()
                default_value = str(self.config_handler.default_config[section][key])
                if current_value != default_value:
                    return True
        
        # Check checkboxes
        for (sec, key), checkbox in self.checkboxes.items():
            if sec == section:
                current_value = checkbox.get()
                default_value = self.config_handler.default_config[section][key]
                if current_value != default_value:
                    return True
        
        return False

    def update_tab_colors(self):
        """Update tab colors based on category changes"""
        if not self.notebook:
            return
            
        for i in range(self.notebook.index("end")):
            tab_text = self.notebook.tab(i, "text")
            # Remove any existing indicator
            clean_text = tab_text.replace("● ", "").replace("* ", "")
            has_changes = self.has_category_changes(clean_text)
            
            if has_changes:
                # Add green circle indicator to show changes
                if not tab_text.startswith("● "):
                    new_text = "● " + clean_text
                    self.notebook.tab(i, text=new_text)
            else:
                # Remove indicator if no changes
                if tab_text.startswith("● "):
                    self.notebook.tab(i, text=clean_text)

    def reset_to_default(self, section, key):
        """Reset a specific setting to its default value"""
        default_value = self.config_handler.default_config[section][key]
        
        # Special case: if resetting BaseTurnRate or BaseLookUpRate to default, uncheck sync
        if section == 'MovementParams' and key in ['BaseTurnRate', 'BaseLookUpRate']:
            self.sync_sensitivity.set(False)
        
        if isinstance(default_value, bool):
            if (section, key) in self.checkboxes:
                self.checkboxes[(section, key)].set(default_value)
        else:
            if (section, key) in self.entries:
                entry = self.entries[(section, key)]
                entry.delete(0, tk.END)
                entry.insert(0, str(default_value))
                entry.configure(foreground='black')
        
        # Update default button state and label color
        self.update_default_button_state(section, key)
        self.update_label_color(section, key)
        
        # Update tab colors
        self.update_tab_colors()

    def update_default_button_state(self, section, key):
        """Update the state of default button for a specific setting"""
        if (section, key) not in self.default_buttons:
            return
            
        default_value = self.config_handler.default_config[section][key]
        is_default = False
        
        if isinstance(default_value, bool):
            if (section, key) in self.checkboxes:
                current_value = self.checkboxes[(section, key)].get()
                is_default = current_value == default_value
        else:
            if (section, key) in self.entries:
                current_value = self.entries[(section, key)].get().strip()
                is_default = current_value == str(default_value)
        
        # Enable/disable button based on whether value is at default
        button = self.default_buttons[(section, key)]
        if is_default:
            button.configure(state='disabled')
        else:
            button.configure(state='normal')

    def update_all_default_button_states(self):
        """Update all default button states and label colors"""
        for (section, key) in self.default_buttons:
            self.update_default_button_state(section, key)
            self.update_label_color(section, key)

    def _on_checkbox_change(self, section, key):
        """Called when a checkbox value changes"""
        self.update_default_button_state(section, key)
        self.update_label_color(section, key)
        self.update_tab_colors()

    def update_label_color(self, section, key):
        """Update the label color based on whether the value is different from default or invalid"""
        if (section, key) not in self.labels:
            return
            
        label = self.labels[(section, key)]
        default_value = self.config_handler.default_config[section][key]
        
        if isinstance(default_value, bool):
            if (section, key) in self.checkboxes:
                current_value = self.checkboxes[(section, key)].get()
                is_default = current_value == default_value
                # Boolean values can't be invalid, so just green if changed, black if default
                if is_default:
                    label.configure(foreground='black', font=font('bold'))
                else:
                    label.configure(foreground='green', font=font('bold'))
        else:
            if (section, key) in self.entries:
                current_value = self.entries[(section, key)].get().strip()
                is_default = current_value == str(default_value)
                
                # Check if value is invalid
                is_invalid = False
                if isinstance(default_value, (int, float)):
                    # Empty value is invalid
                    if not current_value:
                        is_invalid = True
                    else:
                        try:
                            if '.' in current_value:
                                value = float(current_value)
                            else:
                                value = int(current_value)
                            
                            # Check if exceeds maximum
                            if section in self.config_handler.max_values and key in self.config_handler.max_values[section]:
                                if value > self.config_handler.max_values[section][key]:
                                    is_invalid = True
                        except ValueError:
                            is_invalid = True
                
                # Set label color based on validity and whether it's changed
                if is_invalid:
                    label.configure(foreground='red', font=font('bold'))
                elif is_default:
                    label.configure(foreground='black', font=font('bold'))
                else:
                    label.configure(foreground='green', font=font('bold'))

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
            # Check for both old and new mod file names
            old_mod_file = os.path.join(mods_path, 'z_SCAMMovementAiming_P.pak')
            new_mod_file = os.path.join(mods_path, 'z_SCAM_P.pak')
            self.mod_exists = os.path.exists(old_mod_file) or os.path.exists(new_mod_file)

    def update_mod_status(self):
        """Public method to check mod status"""
        self._check_mod_exists()

    def validate_game_directory(self, path, show_error=True):
        """Validate directory with automatic correction"""
        if not path:
            return False
        
        # Try to find the correct directory
        corrected_path = self.find_correct_game_directory(path)
        
        if corrected_path:
            # Found a valid path (either original or corrected), use it
            self.game_dir.set(corrected_path)
            self.save_directory(corrected_path)
            self._check_mod_exists()
            return True
        
        # No valid directory found
        if show_error:
            loc = get_current_localization()
            messagebox.showerror(loc.get_title("error"), 
                                loc.get_error("invalid_stalker_directory"))
        
        return False

    def load_saved_directory(self):
        try:
            config = configparser.ConfigParser()
            stalker_location_path = os.path.join(self.user_data_path, 'stalker_location.ini')
            config.read(stalker_location_path)
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
            stalker_location_path = os.path.join(self.user_data_path, 'stalker_location.ini')
            with open(stalker_location_path, 'w') as f:
                config.write(f)

    def setup_game_dir_frame(self, frame):
        dir_frame = ttk.Frame(frame)
        dir_frame.pack(fill='x', padx=5, pady=5)

        note_frame = ttk.Frame(dir_frame)
        note_frame.pack(fill='x', pady=(0, 5))
        
        loc = get_current_localization()
        ttk.Label(note_frame, text=loc.get_label("set_game_directory_note"),
                 font=font('small')).pack(side='left', padx=5)
        
        # Example paths
        label_frame = ttk.Frame(dir_frame)
        label_frame.pack(fill='x', pady=2)
        
        ttk.Label(label_frame, text=loc.get_label("example_paths"), font=font('small')).pack(side='left')
        ttk.Label(label_frame, text=loc.get_label("steam_path"),
                 font=font('small')).pack(side='left', padx=5)
        ttk.Label(label_frame, text=loc.get_label("xbox_path"),
                 font=font('small')).pack(side='left', padx=5)
        
        # Directory input
        input_frame = ttk.Frame(dir_frame)
        input_frame.pack(fill='x', pady=2)
        
        ttk.Label(input_frame, text=t("game_directory")).pack(side='left', padx=5)
        self.dir_entry = ttk.Entry(input_frame, textvariable=self.game_dir, width=55)
        self.dir_entry.pack(side='left', padx=5, fill='x', expand=True)

        ttk.Button(input_frame, text=t("browse"), command=self.browse_directory).pack(side='left', padx=5)
        ttk.Button(input_frame, text=t("open_mod_directory"), command=self.open_game_directory).pack(side='left', padx=5)

    def browse_directory(self):
        dir_path = filedialog.askdirectory(title="Select Stalker 2 Directory")
        if dir_path:
            # validate_game_directory now handles correction and setting the directory
            self.validate_game_directory(dir_path, show_error=True)

    def open_game_directory(self):
        if not self.game_dir.get():
            loc = get_current_localization()
            if messagebox.askyesno(loc.get_title("no_directory_set"), 
                                  loc.get_confirmation("set_directory_now")):
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
            loc = get_current_localization()
            if messagebox.askyesno(loc.get_title("create_mod_locally"), 
                                  loc.get_confirmation("create_mod_locally")):
                return (True, os.getcwd())
            return False
            
        if not self.validate_game_directory(self.game_dir.get(), show_error=True):
            return False
            
        mods_path = os.path.join(self.game_dir.get(), "Stalker2", "Content", "Paks", "~mods")
        if not os.path.exists(mods_path):
            os.makedirs(mods_path)
            
        return (False, mods_path)

    def remove_mod(self):
        """Remove the mod file (handles both old and new file names)"""
        try:
            if self.game_dir.get() and self.validate_game_directory(self.game_dir.get(), show_error=False):
                mods_path = os.path.join(self.game_dir.get(), "Stalker2", "Content", "Paks", "~mods")
                # Check for both old and new mod file names
                old_mod_file = os.path.join(mods_path, 'z_SCAMMovementAiming_P.pak')
                new_mod_file = os.path.join(mods_path, 'z_SCAM_P.pak')
                
                removed = False
                if os.path.exists(old_mod_file):
                    os.remove(old_mod_file)
                    removed = True
                if os.path.exists(new_mod_file):
                    os.remove(new_mod_file)
                    removed = True
                
                if removed:
                    self.mod_exists = False
                    return True
            return False
        except Exception as e:
            loc = get_current_localization()
            messagebox.showerror(loc.get_title("error"), 
                                loc.get_error("failed_to_remove_mod", error=str(e)))
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
        loc = get_current_localization()
        return loc.get_button("remove_mouse_smoothing") if self.get_mouse_smoothing_state() else loc.get_button("re_enable_mouse_smoothing")

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
                    loc = get_current_localization()
                    action_text = "removed" if new_state else "added"
                    messagebox.showinfo(loc.get_title("success"), 
                                       loc.get_status("mouse_smoothing_success", action=action_text))
                    input_ini_found = True
                    break
                        
                except Exception as e:
                    loc = get_current_localization()
                    messagebox.showerror(loc.get_title("error"), 
                                        loc.get_error("failed_to_update_input_ini", error=str(e)))
                    break
        
        if not input_ini_found:
            self.create_default_input_ini(new_state)

    def create_default_input_ini(self, smoothing_enabled):
        try:
            # Read existing content if file exists
            existing_content = {}
            input_ini_path = os.path.join(self.user_data_path, 'Input.ini')
            if os.path.exists(input_ini_path):
                with open(input_ini_path, 'r') as f:
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
                    
            with open(input_ini_path, 'w') as f:
                f.write(content)
                
            loc = get_current_localization()
            messagebox.showinfo(loc.get_title("instructions"), 
                               loc.get_instruction("input_ini_manual"))
            
        except Exception as e:
            loc = get_current_localization()
            messagebox.showerror(loc.get_title("error"), 
                                loc.get_error("failed_to_create_input_ini", error=str(e)))

    def setup_section_frame(self, frame, section):
        row = 0
        for key, value in self.config_handler.default_config[section].items():
            label = ttk.Label(frame, text=key, font=font('bold'))
            label.grid(row=row, column=0, padx=5, pady=2, sticky='e')
            self.labels[(section, key)] = label  # Store label reference
            
            if isinstance(value, bool):
                var = tk.BooleanVar(value=value)
                checkbox = ttk.Checkbutton(frame, variable=var)
                checkbox.grid(row=row, column=1, padx=5, pady=2, sticky='w')
                self.checkboxes[(section, key)] = var
                # Add trace to update default button state and tab colors when checkbox changes
                var.trace_add('write', lambda *args, s=section, k=key: self._on_checkbox_change(s, k))
                # Create default button for boolean settings
                default_btn = ttk.Button(frame, text=t("default"), command=lambda s=section, k=key: self.reset_to_default(s, k))
                default_btn.grid(row=row, column=2, padx=5, pady=2, sticky='w')
                self.default_buttons[(section, key)] = default_btn
            else:
                entry = ttk.Entry(frame)
                entry.insert(0, str(value))
                entry.grid(row=row, column=1, padx=5, pady=2, sticky='w')
                entry.bind('<KeyRelease>', lambda e, s=section, k=key: self.validate_entry(s, k))
                self.entries[(section, key)] = entry
                # Create default button for non-boolean settings
                default_btn = ttk.Button(frame, text=t("default"), command=lambda s=section, k=key: self.reset_to_default(s, k))
                default_btn.grid(row=row, column=2, padx=5, pady=2, sticky='w')
                self.default_buttons[(section, key)] = default_btn
            
            self.add_value_labels(frame, section, key, value, row)
            row += 1

    def add_value_labels(self, frame, section, key, value, row):
        loc = get_current_localization()
        if isinstance(value, bool):
            # For boolean values, show "Default: On" or "Default: Off"
            if value:
                default_text = loc.get_label('default_on')
            else:
                default_text = loc.get_label('default_off')
            ttk.Label(frame, text=default_text, font=font('small')).grid(
                row=row, column=3, padx=5, pady=2, sticky='w')
        else:
            # For non-boolean values, show the actual value
            default_text = loc.get_label('default_value', value=value)
            if section in self.config_handler.max_values and key in self.config_handler.max_values[section]:
                default_text += f" | {loc.get_label('max_value', max=self.config_handler.max_values[section][key])}"
            ttk.Label(frame, text=default_text, font=font('small')).grid(
                row=row, column=3, padx=5, pady=2, sticky='w')
        
        if section in self.config_handler.descriptions and key in self.config_handler.descriptions[section]:
            ttk.Label(frame, text=self.config_handler.descriptions[section][key], font=font('description')).grid(
                row=row, column=4, padx=5, pady=2, sticky='w')

    def setup_movement_frame(self, frame):
        row = 0
        for key, value in self.config_handler.default_config['MovementParams'].items():
            if key not in ['BaseTurnRate', 'BaseLookUpRate']:
                self.create_movement_control(frame, key, value, row)
                row += 1

    def create_movement_control(self, frame, key, value, row):
        label = ttk.Label(frame, text=key, font=font('bold'))
        label.grid(row=row, column=0, padx=5, pady=2, sticky='e')
        self.labels[('MovementParams', key)] = label  # Store label reference
        
        if isinstance(value, bool):
            var = tk.BooleanVar(value=value)
            checkbox = ttk.Checkbutton(frame, variable=var)
            checkbox.grid(row=row, column=1, padx=5, pady=2, sticky='w')
            self.checkboxes[('MovementParams', key)] = var
            # Add trace to update default button state and tab colors when checkbox changes
            var.trace_add('write', lambda *args, k=key: self._on_checkbox_change('MovementParams', k))
            # Create default button for boolean settings
            default_btn = ttk.Button(frame, text=t("default"), command=lambda k=key: self.reset_to_default('MovementParams', k))
            default_btn.grid(row=row, column=2, padx=5, pady=2, sticky='w')
            self.default_buttons[('MovementParams', key)] = default_btn
        else:
            entry = ttk.Entry(frame)
            entry.insert(0, str(value))
            entry.grid(row=row, column=1, padx=5, pady=2, sticky='w')
            entry.bind('<KeyRelease>', lambda e, k=key: self.validate_entry('MovementParams', k))
            self.entries[('MovementParams', key)] = entry
            # Create default button for non-boolean settings
            default_btn = ttk.Button(frame, text=t("default"), command=lambda k=key: self.reset_to_default('MovementParams', k))
            default_btn.grid(row=row, column=2, padx=5, pady=2, sticky='w')
            self.default_buttons[('MovementParams', key)] = default_btn
            
        # Always add value labels for both boolean and non-boolean settings
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
                                   text=t("sync_turn_look_rate"), 
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
            label = ttk.Label(frame, text=key, font=font('bold'))
            label.grid(row=row, column=0, padx=5, pady=2, sticky='e')
            self.labels[('MovementParams', key)] = label  # Store label reference
            
            entry = ttk.Entry(frame)
            entry.insert(0, str(self.config_handler.default_config['MovementParams'][key]))
            entry.grid(row=row, column=1, padx=5, pady=2, sticky='w')
            entry.bind('<KeyRelease>', lambda e, k=key: self.validate_aiming_entry(k))
            self.entries[('MovementParams', key)] = entry
            
            # Create default button for aiming settings
            default_btn = ttk.Button(frame, text=t("default"), command=lambda k=key: self.reset_to_default('MovementParams', k))
            default_btn.grid(row=row, column=2, padx=5, pady=2, sticky='w')
            self.default_buttons[('MovementParams', key)] = default_btn
            
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
        
        # Update label colors for both aiming controls
        self.update_label_color('MovementParams', 'BaseTurnRate')
        self.update_label_color('MovementParams', 'BaseLookUpRate')
        
        # Update tab colors as sync setting change affects aiming section
        self.update_tab_colors()

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
                    # Update default button state and label color for both entries
                    self.update_default_button_state('MovementParams', rate_key)
                    self.update_label_color('MovementParams', rate_key)
            else:
                entry.configure(foreground='red' if exceeds_max else 
                    ('green' if current_value != default_value else 'black'))
                # Update default button state and label color for this entry
                self.update_default_button_state('MovementParams', key)
                self.update_label_color('MovementParams', key)
            
            # Update tab colors
            self.update_tab_colors()
                    
        except ValueError:
            entry.configure(foreground='red')
            self.update_default_button_state('MovementParams', key)
            self.update_label_color('MovementParams', key)
            self.update_tab_colors()

    def validate_entry(self, section, key):
        entry = self.entries[(section, key)]
        current_value = entry.get().strip()
        default_value = str(self.config_handler.default_config[section][key])

        try:
            if not current_value and isinstance(self.config_handler.default_config[section][key], (int, float)):
                entry.configure(foreground='red')
                self.update_default_button_state(section, key)
                self.update_label_color(section, key)
                self.update_tab_colors()
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
                
                # Update default button state, label color, and tab colors
                self.update_default_button_state(section, key)
                self.update_label_color(section, key)
                self.update_tab_colors()
                return not exceeds_max

            entry.configure(foreground='black')
            self.update_default_button_state(section, key)
            self.update_label_color(section, key)
            self.update_tab_colors()
            return True

        except ValueError:
            entry.configure(foreground='red')
            self.update_default_button_state(section, key)
            self.update_label_color(section, key)
            self.update_tab_colors()
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
        
        # Update all default button states and tab colors after loading configuration
        self.update_all_default_button_states()
        self.update_tab_colors()

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
                                loc = get_current_localization()
                                messagebox.showerror(loc.get_title("error"), 
                                                    loc.get_error("invalid_value_for_key", key=key))
                                return None
                if changed_values:
                    config[section] = changed_values

        if self.sync_sensitivity.get():
            config['Aiming'] = {'SyncTurnRate': True}

        return config