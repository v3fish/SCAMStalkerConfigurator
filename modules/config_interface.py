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
        self.load_saved_directory()

    def load_saved_directory(self):
        try:
            config = configparser.ConfigParser()
            config.read('stalker_location.ini')
            if 'Directory' in config and 'path' in config['Directory']:
                saved_dir = config['Directory']['path']
                if saved_dir and self.validate_game_directory(saved_dir, show_error=False):
                    self.game_dir.set(saved_dir)
                    self.update_directory_status(True)
        except:
            pass

    def save_directory(self, directory):
        config = configparser.ConfigParser()
        config['Directory'] = {'path': directory}
        with open('stalker_location.ini', 'w') as f:
            config.write(f)

    def setup_game_dir_frame(self, frame):
        dir_frame = ttk.Frame(frame)
        dir_frame.pack(fill='x', padx=5, pady=5)
    
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
        self.dir_entry = ttk.Entry(input_frame, textvariable=self.game_dir, width=60)
        self.dir_entry.pack(side='left', padx=5, fill='x', expand=True)
    
        self.game_dir.trace('w', lambda *args: self.validate_game_directory(self.game_dir.get()))
    
        ttk.Button(input_frame, text="Browse", command=self.browse_directory).pack(side='left', padx=5)
        ttk.Button(input_frame, text="Open Mod Directory", command=self.open_game_directory).pack(side='left', padx=5)

    def browse_directory(self):
        dir_path = filedialog.askdirectory(title="Select Stalker 2 Directory")
        if dir_path:
            if self.validate_game_directory(dir_path):
                self.game_dir.set(dir_path)
                self.save_directory(dir_path)

    def validate_game_directory(self, path, show_error=True):
        if not path:
            self.update_directory_status(False)
            return False
            
        valid = os.path.exists(path) and os.path.exists(os.path.join(path, "Stalker2"))
        
        if valid:
            self.save_directory(path)
            
        if show_error and not valid:
            messagebox.showerror("Error", 
                "Invalid Stalker 2 directory!\n\n"
                "Directory should contain 'Stalker2' folder.\n\n"
                "Example paths:\n"
                "Steam: C:\\Program Files (x86)\\Steam\\steamapps\\common\\S.T.A.L.K.E.R. 2 Heart of Chornobyl\n"
                "Xbox: C:\\XboxGames\\S.T.A.L.K.E.R. 2- Heart of Chornobyl (Windows)\\Content")
        
        self.update_directory_status(valid)
        return valid

    def update_directory_status(self, valid):
        if self.dir_entry:
            self.dir_entry.configure(foreground='green' if valid else 'red')

    def open_game_directory(self):
        if not self.game_dir.get():
            messagebox.showerror("Error", "Please set the game directory first!")
            return
       
        if not self.validate_game_directory(self.game_dir.get()):
            return
       
        mods_path = os.path.join(self.game_dir.get(), "Stalker2", "Content", "Paks", "~mods")
        if not os.path.exists(mods_path):
            messagebox.showerror("Error", 
                "~mods folder not found!\n\n"
                "Please create the following folder:\n"
                f"{mods_path}")
            return
        os.startfile(mods_path)

    def validate_mods_directory(self):
        if not self.game_dir.get():
            messagebox.showerror("Error", "Please set the game directory first!")
            return False
            
        mods_path = os.path.join(self.game_dir.get(), "Stalker2", "Content", "Paks", "~mods")
        if not os.path.exists(mods_path):
            messagebox.showerror("Error", 
                "~mods folder not found!\n\n"
                "Please create the following folder:\n"
                f"{mods_path}\n\n"
                "Or verify your game directory is set correctly.")
            return False
            
        return True

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
        # Create controls frame at the top
        controls_frame = ttk.Frame(frame)
        controls_frame.grid(row=0, column=0, columnspan=4, sticky='ew', padx=5, pady=5)
        
        # Left side frame for sync sensitivity
        left_frame = ttk.Frame(controls_frame)
        left_frame.pack(side='left')
        
        # Right side frame for mouse smoothing button
        right_frame = ttk.Frame(controls_frame)
        right_frame.pack(side='right')
        
        # Add sync sensitivity checkbox
        if 'Aiming' in self.config_handler.default_config and 'SyncTurnRate' in self.config_handler.default_config['Aiming']:
            self.sync_sensitivity.set(self.config_handler.default_config['Aiming']['SyncTurnRate'])
        
        sync_check = ttk.Checkbutton(left_frame, 
                                   text="Sync Turn/Look Rate", 
                                   variable=self.sync_sensitivity,
                                   command=self.sync_sensitivity_rates)
        sync_check.pack(side='left')
        
        # Add mouse smoothing button
        mouse_btn = ttk.Button(right_frame, 
                             text="Remove Mouse Smoothing", 
                             command=self.remove_mouse_smoothing)
        mouse_btn.pack(side='right', padx=5)
        
        # Create aiming rate controls starting at row 1
        self.create_aiming_controls(frame)

    def create_aiming_controls(self, frame):
        # Start at row 1 since controls frame is at row 0
        for row, key in enumerate(['BaseTurnRate', 'BaseLookUpRate'], 1):
            ttk.Label(frame, text=key).grid(row=row, column=0, padx=5, pady=2, sticky='e')
            
            entry = ttk.Entry(frame)
            entry.insert(0, str(self.config_handler.default_config['MovementParams'][key]))
            entry.grid(row=row, column=1, padx=5, pady=2, sticky='w')
            entry.bind('<KeyRelease>', lambda e, k=key: self.validate_aiming_entry(k))
            self.entries[('MovementParams', key)] = entry
            
            self.add_value_labels(frame, 'MovementParams', key, 
                                self.config_handler.default_config['MovementParams'][key], row)

    def remove_mouse_smoothing(self):
        # Define the paths to check
        config_paths = [
            os.path.join(os.getenv('LOCALAPPDATA'), 'Stalker2', 'Saved', 'Config', 'Windows'),
            os.path.join(os.getenv('LOCALAPPDATA'), 'Stalker2', 'Saved', 'Config', 'WinGDK')
        ]
        
        input_ini_found = False
        
        # Check each path for Input.ini
        for path in config_paths:
            if not os.path.exists(path):
                continue
                
            input_ini_path = os.path.join(path, 'Input.ini')
            if os.path.exists(input_ini_path):
                try:
                    # Read existing content first to check if already disabled
                    with open(input_ini_path, 'r') as f:
                        content = f.read()
                        if '[/Script/Engine.InputSettings]' in content and 'bEnableMouseSmoothing=False' in content:
                            messagebox.showinfo("Info", 
                                "Input.ini has already been updated to remove mouse smoothing/acceleration.")
                            return

                    if not messagebox.askyesno("Confirm", 
                        "Would you like SCAM to update your Input.ini?"):
                        return
                        
                    # Update the file if needed
                    with open(input_ini_path, 'a+') as f:
                        f.seek(0)
                        content = f.read()
                        
                        # Only add if not already present
                        if '[/Script/Engine.InputSettings]' not in content:
                            f.write('\n[/Script/Engine.InputSettings]\n')
                        if 'bEnableMouseSmoothing=False' not in content:
                            f.write('bEnableMouseSmoothing=False\n')
                    
                    messagebox.showinfo("Success", 
                        "Mouse smoothing has been disabled in Input.ini")
                    input_ini_found = True
                    break
                except Exception as e:
                    messagebox.showerror("Error", 
                        f"Failed to update Input.ini: {str(e)}")
                    break
        
        if not input_ini_found:
            local_input_ini = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                         '..', 'default_ini', 'Input.ini')
            if messagebox.askyesno("Input.ini Not Found", 
                "Could not find or update Input.ini. Would you like to open the location " +
                "where you need to place the Input.ini file?"):
                try:
                    # Copy Input.ini to current directory
                    shutil.copy(local_input_ini, 'Input.ini')
                    # Open the Windows config folder
                    default_path = os.path.join(os.getenv('LOCALAPPDATA'), 
                                              'Stalker2', 'Saved', 'Config', 'Windows')
                    if not os.path.exists(default_path):
                        os.makedirs(default_path)
                    os.startfile(default_path)
                except Exception as e:
                    messagebox.showerror("Error", 
                        f"Failed to copy Input.ini or open folder: {str(e)}")

    def sync_sensitivity_rates(self):
        if self.sync_sensitivity.get():
            turn_value = self.entries[('MovementParams', 'BaseTurnRate')].get()
            try:
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
            if 'MovementParams' in self.config_handler.max_values and key in self.config_handler.max_values['MovementParams']:
                if value > self.config_handler.max_values['MovementParams'][key]:
                    entry.configure(foreground='red')
                    return False
                    
            if self.sync_sensitivity.get():
                for rate_key in ['BaseTurnRate', 'BaseLookUpRate']:
                    entry = self.entries[('MovementParams', rate_key)]
                    default_value = str(self.config_handler.default_config['MovementParams'][rate_key])
                    entry.delete(0, tk.END)
                    entry.insert(0, str(value))
                    entry.configure(foreground='green' if str(value) != default_value else 'black')
            else:
                default_value = str(self.config_handler.default_config['MovementParams'][key])
                entry.configure(foreground='green' if current_value != default_value else 'black')
        except ValueError:
            entry.configure(foreground='red')

    def validate_entry(self, section, key):
        entry = self.entries[(section, key)]
        default_value = str(self.config_handler.default_config[section][key])
        current_value = entry.get()

        try:
            if not current_value:
                entry.configure(foreground='red')
                return False

            if '.' in current_value:
                value = float(current_value)
            else:
                value = int(current_value)

            if section in self.config_handler.max_values and key in self.config_handler.max_values[section]:
                if value > self.config_handler.max_values[section][key]:
                    entry.configure(foreground='red')
                    return False

            entry.configure(foreground='green' if str(current_value) != default_value else 'black')
            return True
        except ValueError:
            entry.configure(foreground='red')
            return False

    def has_invalid_entries(self):
        return any(entry.cget('foreground') == 'red' or not entry.get() 
                  for entry in self.entries.values())

    def has_changes(self):
        for (section, key), entry in self.entries.items():
            current_value = entry.get()
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