# modules/config_interface.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import configparser
import shutil
import json
from .localization.language_manager import get_current_localization, t, font
import sys

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
        self.remove_mouse_smoothing = tk.BooleanVar(value=False)
        self.disable_overweight_restriction = tk.BooleanVar(value=False)
        self.remove_water_slowdown = tk.BooleanVar(value=False)
        self.remove_mouse_slowdown = tk.BooleanVar(value=False)
        self.remove_camera_shake = tk.BooleanVar(value=False)
        self.remove_aim_block = tk.BooleanVar(value=False)
        self.game_dir = tk.StringVar()
        self.dir_entry = None
        self.mod_exists = False
        
        # Load mod configuration
        self.mod_config = self._load_mod_config()
        
        # Initialize style object (may be used for other styling)
        self.style = ttk.Style()
        
        # Add trace to game_dir
        self.game_dir.trace_add('write', self._on_game_dir_change)
        
        self.load_saved_directory()
    
    def _load_mod_config(self):
        """Load mod configuration from JSON file if available, otherwise from SQLite database (default_config.db)"""
        import sqlite3
        import json
        import sys
        # Try JSON file first (for development)
        if getattr(sys, 'frozen', False):
            exe_dir = os.path.dirname(sys.executable)
        else:
            exe_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(exe_dir, 'default_ini', 'mod_config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            if 'mod_settings' not in config:
                raise ValueError(f"'mod_settings' key missing in {config_path}")
            return config['mod_settings']
        # Fallback to DB (for EXE)
        if getattr(sys, 'frozen', False):
            exe_dir = os.path.dirname(sys.executable)
        else:
            exe_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        from .config import DATA_FOLDER_NAME
        if getattr(sys, 'frozen', False):
            # For frozen exe, look in data folder next to executable
            db_path = os.path.join(exe_dir, DATA_FOLDER_NAME, 'default_config.db')
        else:
            # For development, look in data folder in current directory
            db_path = os.path.join(DATA_FOLDER_NAME, 'default_config.db')
        
        if not os.path.exists(db_path):
            from .localization.language_manager import get_current_localization
            loc = get_current_localization()
            raise FileNotFoundError(loc.get_error("database_not_found", db_path=db_path))
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT content FROM config_files WHERE filename = 'mod_config.json'")
        row = cursor.fetchone()
        conn.close()
        if not row:
            raise FileNotFoundError("mod_config.json not found in database")
        config = json.loads(row[0])
        if 'mod_settings' not in config:
            raise ValueError("'mod_settings' key missing in mod_config.json from database")
        return config['mod_settings']

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

    @staticmethod
    def _is_value_at_default(current_value, default_value):
        """Compare an entry's raw text to its default value, numerically if the default is a number."""
        if isinstance(default_value, (int, float)) and not isinstance(default_value, bool):
            try:
                return float(current_value) == float(default_value)
            except (TypeError, ValueError):
                return False
        return current_value == str(default_value)

    def has_category_changes(self, section):
        """Check if a specific category has any changes from defaults"""
        # Special case for Aiming section - check aiming-related MovementParams
        if section == 'Aiming':
            # Check sync sensitivity setting
            if 'Aiming' in self.config_handler.default_config and 'SyncTurnRate' in self.config_handler.default_config['Aiming']:
                if self.sync_sensitivity.get() != self.config_handler.default_config['Aiming']['SyncTurnRate']:
                    return True
            
            # Check remove mouse smoothing setting (default is off/False)
            if self.remove_mouse_smoothing.get():
                return True
            
            # Check remove mouse slowdown / camera shake / aim block (default is off/False)
            if self.remove_mouse_slowdown.get() or self.remove_camera_shake.get() or self.remove_aim_block.get():
                return True
            
            # Check BaseTurnRate and BaseLookUpRate (displayed in Aiming tab but stored as MovementParams)
            for aiming_key in ['BaseTurnRate', 'BaseLookUpRate']:
                if ('MovementParams', aiming_key) in self.entries:
                    entry = self.entries[('MovementParams', aiming_key)]
                    current_value = entry.get().strip()
                    default_value = self.config_handler.default_config['MovementParams'][aiming_key]
                    if not self._is_value_at_default(current_value, default_value):
                        return True
            return False
        
        # Special case for MovementParams - exclude aiming-related settings that are shown in Aiming tab
        if section == 'MovementParams':
            for (sec, key), entry in self.entries.items():
                if sec == section and key not in ['BaseTurnRate', 'BaseLookUpRate']:
                    current_value = entry.get().strip()
                    default_value = self.config_handler.default_config[section][key]
                    if not self._is_value_at_default(current_value, default_value):
                        return True
            
            for (sec, key), checkbox in self.checkboxes.items():
                if sec == section:
                    current_value = checkbox.get()
                    default_value = self.config_handler.default_config[section][key]
                    if current_value != default_value:
                        return True
            
            # Check disable overweight movement restriction setting (default is off/False)
            if self.disable_overweight_restriction.get():
                return True
            
            # Check remove water slowdown setting (default is off/False)
            if self.remove_water_slowdown.get():
                return True
            
            return False
        
        # General case for all other sections
        # Check entries
        for (sec, key), entry in self.entries.items():
            if sec == section:
                current_value = entry.get().strip()
                default_value = self.config_handler.default_config[section][key]
                if not self._is_value_at_default(current_value, default_value):
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
                is_default = self._is_value_at_default(current_value, default_value)
        
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
                is_default = self._is_value_at_default(current_value, default_value)
                
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
            mod_folder = self.mod_config.get('mod_folder_name', 'z_SCAM_P')
            new_mod_file = os.path.join(mods_path, f'{mod_folder}.pak')
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
            with open(stalker_location_path, 'w', encoding='utf-8') as f:
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
                mod_folder = self.mod_config.get('mod_folder_name', 'z_SCAM_P')
                new_mod_file = os.path.join(mods_path, f'{mod_folder}.pak')
                
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

    def _on_remove_mouse_smoothing_change(self):
        """Called when the remove mouse smoothing checkbox changes"""
        if ('Aiming', 'RemoveMouseSmoothing') in self.labels:
            label = self.labels[('Aiming', 'RemoveMouseSmoothing')]
            if self.remove_mouse_smoothing.get():
                label.configure(foreground='green', font=font('bold'))
            else:
                label.configure(foreground='black', font=font('bold'))
        self.update_tab_colors()

    def _on_disable_overweight_restriction_change(self):
        """Called when the disable overweight movement restriction checkbox changes"""
        if ('MovementParams', 'DisableOverweightMovementRestriction') in self.labels:
            label = self.labels[('MovementParams', 'DisableOverweightMovementRestriction')]
            if self.disable_overweight_restriction.get():
                label.configure(foreground='green', font=font('bold'))
            else:
                label.configure(foreground='black', font=font('bold'))
        self.update_tab_colors()

    def reset_remove_mouse_smoothing(self):
        self.remove_mouse_smoothing.set(False)
        self._on_remove_mouse_smoothing_change()

    def reset_disable_overweight_restriction(self):
        self.disable_overweight_restriction.set(False)
        self._on_disable_overweight_restriction_change()

    def _on_remove_water_slowdown_change(self):
        """Called when the remove water slowdown checkbox changes"""
        if ('MovementParams', 'RemoveWaterSlowdown') in self.labels:
            label = self.labels[('MovementParams', 'RemoveWaterSlowdown')]
            if self.remove_water_slowdown.get():
                label.configure(foreground='green', font=font('bold'))
            else:
                label.configure(foreground='black', font=font('bold'))
        self.update_tab_colors()

    def reset_remove_water_slowdown(self):
        self.remove_water_slowdown.set(False)
        self._on_remove_water_slowdown_change()

    def _on_remove_mouse_slowdown_change(self):
        """Called when the remove mouse slowdown checkbox changes"""
        if ('Aiming', 'RemoveMouseSlowdown') in self.labels:
            label = self.labels[('Aiming', 'RemoveMouseSlowdown')]
            if self.remove_mouse_slowdown.get():
                label.configure(foreground='green', font=font('bold'))
            else:
                label.configure(foreground='black', font=font('bold'))
        self.update_tab_colors()

    def reset_remove_mouse_slowdown(self):
        self.remove_mouse_slowdown.set(False)
        self._on_remove_mouse_slowdown_change()

    def _on_remove_camera_shake_change(self):
        """Called when the remove camera shake checkbox changes"""
        if ('Aiming', 'RemoveCameraShake') in self.labels:
            label = self.labels[('Aiming', 'RemoveCameraShake')]
            if self.remove_camera_shake.get():
                label.configure(foreground='green', font=font('bold'))
            else:
                label.configure(foreground='black', font=font('bold'))
        self.update_tab_colors()

    def reset_remove_camera_shake(self):
        self.remove_camera_shake.set(False)
        self._on_remove_camera_shake_change()

    def _on_remove_aim_block_change(self):
        """Called when the remove aim block checkbox changes"""
        if ('Aiming', 'RemoveAimBlock') in self.labels:
            label = self.labels[('Aiming', 'RemoveAimBlock')]
            if self.remove_aim_block.get():
                label.configure(foreground='green', font=font('bold'))
            else:
                label.configure(foreground='black', font=font('bold'))
        self.update_tab_colors()

    def reset_remove_aim_block(self):
        self.remove_aim_block.set(False)
        self._on_remove_aim_block_change()

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
        
        # DisableMovementWeightThreshold toggle - named to match the base game's cfg field
        loc = get_current_localization()
        
        overweight_label = ttk.Label(frame, text=loc.get_button('allow_overweight_movement'), font=font('bold'))
        overweight_label.grid(row=row, column=0, padx=5, pady=2, sticky='e')
        self.labels[('MovementParams', 'DisableOverweightMovementRestriction')] = overweight_label
        
        overweight_check = ttk.Checkbutton(frame, variable=self.disable_overweight_restriction,
                                         command=self._on_disable_overweight_restriction_change)
        overweight_check.grid(row=row, column=1, padx=5, pady=2, sticky='w')
        
        overweight_default_btn = ttk.Button(frame, text=t("default"), command=self.reset_disable_overweight_restriction)
        overweight_default_btn.grid(row=row, column=2, padx=5, pady=2, sticky='w')
        
        ttk.Label(frame, text=loc.get_label('default_off'), font=font('small')).grid(
            row=row, column=3, padx=5, pady=2, sticky='w')
        ttk.Label(frame, text=loc.get_label('disable_overweight_restriction_desc'), font=font('description')).grid(
            row=row, column=4, padx=5, pady=2, sticky='w')
        row += 1
        
        # Remove Water Slowdown toggle
        water_label = ttk.Label(frame, text=loc.get_button('remove_water_slowdown'), font=font('bold'))
        water_label.grid(row=row, column=0, padx=5, pady=2, sticky='e')
        self.labels[('MovementParams', 'RemoveWaterSlowdown')] = water_label
        
        water_check = ttk.Checkbutton(frame, variable=self.remove_water_slowdown,
                                    command=self._on_remove_water_slowdown_change)
        water_check.grid(row=row, column=1, padx=5, pady=2, sticky='w')
        
        water_default_btn = ttk.Button(frame, text=t("default"), command=self.reset_remove_water_slowdown)
        water_default_btn.grid(row=row, column=2, padx=5, pady=2, sticky='w')
        
        ttk.Label(frame, text=loc.get_label('default_off'), font=font('small')).grid(
            row=row, column=3, padx=5, pady=2, sticky='w')
        ttk.Label(frame, text=loc.get_label('remove_water_slowdown_desc'), font=font('description')).grid(
            row=row, column=4, padx=5, pady=2, sticky='w')

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
        
        if 'Aiming' in self.config_handler.default_config and 'SyncTurnRate' in self.config_handler.default_config['Aiming']:
            self.sync_sensitivity.set(self.config_handler.default_config['Aiming']['SyncTurnRate'])
        
        sync_check = ttk.Checkbutton(left_frame, 
                                   text=t("sync_turn_look_rate"), 
                                   variable=self.sync_sensitivity,
                                   command=self.sync_sensitivity_rates)
        sync_check.pack(side='left')
        
        self.create_aiming_controls(frame)

    def create_aiming_controls(self, frame):
        for row, key in enumerate(['BaseTurnRate', 'BaseLookUpRate'], 1):
            label = ttk.Label(frame, text=key, font=font('bold'))
            label.grid(row=row, column=0, padx=5, pady=2, sticky='e')
            self.labels[('MovementParams', key)] = label  # Store label reference
            
            default_value = self.config_handler.default_config['MovementParams'][key]
            
            entry = ttk.Entry(frame)
            entry.insert(0, str(default_value))
            entry.grid(row=row, column=1, padx=5, pady=2, sticky='w')
            entry.bind('<KeyRelease>', lambda e, k=key: self.validate_aiming_entry(k))
            self.entries[('MovementParams', key)] = entry
            
            # Create default button for aiming settings
            default_btn = ttk.Button(frame, text=t("default"), command=lambda k=key: self.reset_to_default('MovementParams', k))
            default_btn.grid(row=row, column=2, padx=5, pady=2, sticky='w')
            self.default_buttons[('MovementParams', key)] = default_btn
            
            self.add_value_labels(frame, 'MovementParams', key, default_value, row)
        
        # Remove Mouse Smoothing toggle - placed under BaseTurnRate/BaseLookUpRate
        smoothing_row = 3
        loc = get_current_localization()
        
        smoothing_label = ttk.Label(frame, text=loc.get_button("remove_mouse_smoothing"), font=font('bold'))
        smoothing_label.grid(row=smoothing_row, column=0, padx=5, pady=2, sticky='e')
        self.labels[('Aiming', 'RemoveMouseSmoothing')] = smoothing_label
        
        smoothing_check = ttk.Checkbutton(frame, variable=self.remove_mouse_smoothing,
                                        command=self._on_remove_mouse_smoothing_change)
        smoothing_check.grid(row=smoothing_row, column=1, padx=5, pady=2, sticky='w')
        
        smoothing_default_btn = ttk.Button(frame, text=t("default"), command=self.reset_remove_mouse_smoothing)
        smoothing_default_btn.grid(row=smoothing_row, column=2, padx=5, pady=2, sticky='w')
        
        ttk.Label(frame, text=loc.get_label('default_off'), font=font('small')).grid(
            row=smoothing_row, column=3, padx=5, pady=2, sticky='w')
        
        # Remove Mouse Slowdown, Remove Camera Shake, Remove Aim Block toggles
        toggle_defs = [
            (4, self.remove_mouse_slowdown, self._on_remove_mouse_slowdown_change, self.reset_remove_mouse_slowdown,
             'RemoveMouseSlowdown', 'remove_mouse_slowdown', 'remove_mouse_slowdown_desc'),
            (5, self.remove_camera_shake, self._on_remove_camera_shake_change, self.reset_remove_camera_shake,
             'RemoveCameraShake', 'remove_camera_shake', 'remove_camera_shake_desc'),
            (6, self.remove_aim_block, self._on_remove_aim_block_change, self.reset_remove_aim_block,
             'RemoveAimBlock', 'remove_aim_block', 'remove_aim_block_desc'),
        ]
        
        for toggle_row, var, change_handler, reset_handler, label_key, button_key, desc_key in toggle_defs:
            label = ttk.Label(frame, text=loc.get_button(button_key), font=font('bold'))
            label.grid(row=toggle_row, column=0, padx=5, pady=2, sticky='e')
            self.labels[('Aiming', label_key)] = label
            
            check = ttk.Checkbutton(frame, variable=var, command=change_handler)
            check.grid(row=toggle_row, column=1, padx=5, pady=2, sticky='w')
            
            default_btn = ttk.Button(frame, text=t("default"), command=reset_handler)
            default_btn.grid(row=toggle_row, column=2, padx=5, pady=2, sticky='w')
            
            ttk.Label(frame, text=loc.get_label('default_off'), font=font('small')).grid(
                row=toggle_row, column=3, padx=5, pady=2, sticky='w')
            ttk.Label(frame, text=loc.get_label(desc_key), font=font('description')).grid(
                row=toggle_row, column=4, padx=5, pady=2, sticky='w')

    def sync_sensitivity_rates(self):
        if self.sync_sensitivity.get():
            try:
                turn_value = self.entries[('MovementParams', 'BaseTurnRate')].get()
                value = round(float(turn_value))
                self.entries[('MovementParams', 'BaseLookUpRate')].delete(0, tk.END)
                self.entries[('MovementParams', 'BaseLookUpRate')].insert(0, str(value))
                # Use validate_aiming_entry instead of validate_entry for aiming controls
                self.validate_aiming_entry('BaseLookUpRate')
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
            # BaseTurnRate/BaseLookUpRate must be whole numbers - round decimals instead of rejecting them
            value = round(float(current_value))
            if current_value.strip() != str(value):
                cursor_pos = entry.index(tk.INSERT)
                entry.delete(0, tk.END)
                entry.insert(0, str(value))
                entry.icursor(min(cursor_pos, len(str(value))))
                current_value = str(value)
            
            default_value = self.config_handler.default_config['MovementParams'][key]
            
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
                        ('black' if self._is_value_at_default(str(value), default_value) else 'green'))
                    # Update default button state and label color for both entries
                    self.update_default_button_state('MovementParams', rate_key)
                    self.update_label_color('MovementParams', rate_key)
            else:
                entry.configure(foreground='red' if exceeds_max else 
                    ('black' if self._is_value_at_default(current_value, default_value) else 'green'))
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

        try:
            actual_default_value = self.config_handler.default_config[section][key]
            
            if not current_value and isinstance(actual_default_value, (int, float)):
                entry.configure(foreground='red')
                self.update_default_button_state(section, key)
                self.update_label_color(section, key)
                self.update_tab_colors()
                return False

            if isinstance(actual_default_value, (int, float)):
                if '.' in current_value:
                    value = float(current_value)
                else:
                    value = int(current_value)

                exceeds_max = False
                if section in self.config_handler.max_values and key in self.config_handler.max_values[section]:
                    if value > self.config_handler.max_values[section][key]:
                        exceeds_max = True

                entry.configure(foreground='red' if exceeds_max else 
                              ('black' if self._is_value_at_default(current_value, actual_default_value) else 'green'))
                
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
            default_value = self.config_handler.default_config[section][key]
            
            if not self._is_value_at_default(current_value, default_value):
                return True
                
        for (section, key), checkbox in self.checkboxes.items():
            default_value = self.config_handler.default_config[section][key]
            
            current_value = checkbox.get()
            if current_value != default_value:
                return True
                
        if 'Aiming' in self.config_handler.default_config and 'SyncTurnRate' in self.config_handler.default_config['Aiming']:
            if self.sync_sensitivity.get() != self.config_handler.default_config['Aiming']['SyncTurnRate']:
                return True
        
        if self.remove_mouse_smoothing.get():
            return True
        
        if self.disable_overweight_restriction.get():
            return True
        
        if self.remove_water_slowdown.get() or self.remove_mouse_slowdown.get() or \
           self.remove_camera_shake.get() or self.remove_aim_block.get():
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

        # Reset the opt-in toggles to their defaults (off) before applying the new config
        self.remove_mouse_smoothing.set(False)
        self.disable_overweight_restriction.set(False)
        self.remove_water_slowdown.set(False)
        self.remove_mouse_slowdown.set(False)
        self.remove_camera_shake.set(False)
        self.remove_aim_block.set(False)
        
        for section in config:
            for key, value in config[section].items():
                if section == 'Aiming' and key == 'SyncTurnRate':
                    self.sync_sensitivity.set(value)
                elif section == 'Aiming' and key == 'RemoveMouseSmoothing':
                    self.remove_mouse_smoothing.set(value)
                elif section == 'Aiming' and key == 'RemoveMouseSlowdown':
                    self.remove_mouse_slowdown.set(value)
                elif section == 'Aiming' and key == 'RemoveCameraShake':
                    self.remove_camera_shake.set(value)
                elif section == 'Aiming' and key == 'RemoveAimBlock':
                    self.remove_aim_block.set(value)
                elif section == 'MovementParams' and key == 'DisableOverweightMovementRestriction':
                    self.disable_overweight_restriction.set(value)
                elif section == 'MovementParams' and key == 'RemoveWaterSlowdown':
                    self.remove_water_slowdown.set(value)
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
        self._on_remove_mouse_smoothing_change()
        self._on_disable_overweight_restriction_change()
        self._on_remove_water_slowdown_change()
        self._on_remove_mouse_slowdown_change()
        self._on_remove_camera_shake_change()
        self._on_remove_aim_block_change()
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
                        # StaminaDisableThreshold is an opt-in override, not a normal
                        # tunable value, so Force Defaults should never write it unless
                        # the user actually changed it themselves.
                        force_include = include_defaults and key != 'StaminaDisableThreshold'
                        if force_include or not self._is_value_at_default(current_value, value):
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

        aiming_settings = {}
        if self.sync_sensitivity.get():
            aiming_settings['SyncTurnRate'] = True
        if self.remove_mouse_smoothing.get():
            aiming_settings['RemoveMouseSmoothing'] = True
        if self.remove_mouse_slowdown.get():
            aiming_settings['RemoveMouseSlowdown'] = True
        if self.remove_camera_shake.get():
            aiming_settings['RemoveCameraShake'] = True
        if self.remove_aim_block.get():
            aiming_settings['RemoveAimBlock'] = True
        if aiming_settings:
            config['Aiming'] = aiming_settings
        
        if self.disable_overweight_restriction.get():
            config.setdefault('MovementParams', {})['DisableOverweightMovementRestriction'] = True
        
        if self.remove_water_slowdown.get():
            config.setdefault('MovementParams', {})['RemoveWaterSlowdown'] = True

        return config