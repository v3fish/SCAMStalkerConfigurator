"""
This module uses repak.exe by trumank (https://github.com/trumank)
Licensed under MIT License and Apache License 2.0
"""
# modules/mod.py
import os
import subprocess
import shutil
from pathlib import Path
import sys
import json
from tkinter import messagebox
from .config import DATA_FOLDER_NAME

class ModCreator:
    def __init__(self, base_path):
        self.base_path = base_path
        if getattr(sys, 'frozen', False):
            self.exe_dir = os.path.dirname(sys.executable)
        else:
            self.exe_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Load mod configuration
        self.mod_config = self._load_mod_config()
    
    def _load_mod_config(self):
        """Load mod configuration from JSON file if available, otherwise from SQLite database (default_config.db)"""
        import sqlite3
        import json
        # Try JSON file first (for development)
        config_path = os.path.join(self.base_path, 'default_ini', 'mod_config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            if 'mod_settings' not in config:
                raise ValueError(f"'mod_settings' key missing in {config_path}")
            return config['mod_settings']
        # Fallback to DB (for EXE)
        if getattr(sys, 'frozen', False):
            # For frozen exe, look in data folder next to executable
            base_dir = os.path.dirname(sys.executable)
            db_path = os.path.join(base_dir, DATA_FOLDER_NAME, 'default_config.db')
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

    def find_pak_files(self, directory):
        """Recursively find .pak files in directory and its subdirectories"""
        pak_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.pak'):
                    pak_files.append(os.path.join(root, file))
        return pak_files

    def check_incompatible_mods(self, mods_path):
        """Check for incompatible mods in the mods directory and its subdirectories"""
        if not os.path.exists(mods_path):
            return
            
        incompatible_keywords = ['FluidMovementAim', 'FMAO']
        found_mods = []
        
        pak_files = self.find_pak_files(mods_path)
        for file_path in pak_files:
            filename = os.path.basename(file_path)
            if any(keyword in filename for keyword in incompatible_keywords):
                found_mods.append(filename)
                    
        if found_mods:
            from .localization.language_manager import get_current_localization
            loc = get_current_localization()
            messagebox.showwarning(loc.get_title("incompatible_mods"), 
                                  loc.get_warning("incompatible_mods_detected", 
                                                 mod_list="\n".join(found_mods)))

    def create_mod(self, config, mods_path):
        # Check for incompatible mods first
        self.check_incompatible_mods(mods_path)
        
        # Only look in the correct repak folder location
        repak_path = self._find_repak()
        if not repak_path:
            from .localization.language_manager import get_current_localization
            loc = get_current_localization()
            repak_folder_path = os.path.join(self.exe_dir, DATA_FOLDER_NAME, 'repak')
            raise FileNotFoundError(loc.get_error("repak_not_found", repak_path=repak_folder_path))

        # Create temporary build directory
        import tempfile
        temp_build_dir = None
        
        try:
            # Remove old mod file if it exists (for people upgrading from old version)
            old_mod_file = os.path.join(mods_path, 'z_SCAMMovementAiming_P.pak')
            if os.path.exists(old_mod_file):
                os.remove(old_mod_file)
            
            # Create temporary directory for mod building
            temp_build_dir = tempfile.mkdtemp(prefix='pak_mod_builder')
            
            # Enforce all config keys must be present
            required_keys = ['mod_folder_name', 'cfg_folder_name', 'cfg_file_name']
            for key in required_keys:
                if key not in self.mod_config:
                    raise KeyError(f"'{key}' missing in mod_config.json or database. Please provide all required keys.")
            mod_folder = self.mod_config['mod_folder_name']
            cfg_folder = self.mod_config['cfg_folder_name']
            cfg_file = self.mod_config['cfg_file_name']
            
            mod_path = Path(temp_build_dir) / mod_folder / 'Stalker2' / 'Content' / 'GameLite' / 'GameData' / 'ObjPrototypes' / cfg_folder
            mod_path.mkdir(parents=True, exist_ok=True)
            
            if 'Aiming' in config:
                del config['Aiming']
            
            cfg_content = self._generate_cfg_content(config)
            
            with open(mod_path / cfg_file, 'w', encoding='utf-8') as f:
                f.write(cfg_content)
            
            self._run_repak(mods_path, repak_path, temp_build_dir)
            
        except Exception as e:
            # Clean up temp directory if there's an error
            if temp_build_dir and os.path.exists(temp_build_dir):
                shutil.rmtree(temp_build_dir)
            raise
        finally:
            # Always clean up temp directory
            if temp_build_dir and os.path.exists(temp_build_dir):
                shutil.rmtree(temp_build_dir)

    def _find_repak(self):
        """Find repak.exe in the correct location only"""
        # Check in data folder next to executable
        data_path = os.path.join(self.exe_dir, DATA_FOLDER_NAME, 'repak', 'repak.exe')
        if os.path.exists(data_path):
            return data_path

        # Fallback: check if it's bundled (for development)
        bundled_path = os.path.join(self.base_path, 'repak', 'repak.exe')
        if os.path.exists(bundled_path):
            return bundled_path

        # Fallback: check next to the executable/script (legacy)
        external_path = os.path.join(self.exe_dir, 'repak', 'repak.exe')
        if os.path.exists(external_path):
            return external_path

        return None

    def _generate_cfg_content(self, config):
        content = "PlayerCustom : struct.begin {refurl=../../ObjPrototypes.cfg; refkey=Player}\n"
        
        # Handle SpendStaminaInSafeZone as a special case - it goes directly under PlayerCustom
        if 'StaminaPerAction' in config and 'SpendStaminaInSafeZone' in config['StaminaPerAction']:
            content += f"SpendStaminaInSafeZone = {config['StaminaPerAction']['SpendStaminaInSafeZone']}\n"
        
        for section, values in config.items():
            # Create a copy of values to avoid modifying the original
            section_values = values.copy()
            
            # Remove SpendStaminaInSafeZone from StaminaPerAction section as it's handled above
            if section == 'StaminaPerAction' and 'SpendStaminaInSafeZone' in section_values:
                section_values.pop('SpendStaminaInSafeZone')
            
            # Only create the section if there are still values left
            if section_values:
                content += f"   {section} : struct.begin\n"
                for key, value in section_values.items():
                    content += f"      {key} = {value}\n"
                content += "   struct.end\n"
        
        content += "struct.end\n\n"
        content += "// Generated by SCAM (Stalker Character Adjustment Manager) by v3fish\n"
        content += "// Personal use only - redistribution requires author permission\n"
        return content

    def _run_repak(self, mods_path, repak_path, temp_build_dir):
        try:
            # Show progress dialog during repak execution
            import tkinter as tk
            from tkinter import ttk
            
            # Create progress window
            progress_window = tk.Toplevel()
            progress_window.title("Creating Mod")
            progress_window.geometry("300x100")
            progress_window.resizable(False, False)
            progress_window.transient()
            progress_window.grab_set()
            
            # Center the window
            progress_window.update_idletasks()
            x = (progress_window.winfo_screenwidth() // 2) - (150)
            y = (progress_window.winfo_screenheight() // 2) - (50)
            progress_window.geometry(f"+{x}+{y}")
            
            # Add content
            ttk.Label(progress_window, text="Creating mod file, please wait...").pack(pady=15)
            progress_bar = ttk.Progressbar(progress_window, mode='indeterminate', length=250)
            progress_bar.pack(pady=(0, 15))
            progress_bar.start(10)
            
            # Update the window to show it
            progress_window.update()
            
            try:
                # Change to temp directory for repak execution
                original_cwd = os.getcwd()
                os.chdir(temp_build_dir)
                
                # Set up subprocess parameters to hide CMD window
                startupinfo = None
                creationflags = 0
                if os.name == 'nt':  # Windows
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    startupinfo.wShowWindow = subprocess.SW_HIDE
                    creationflags = subprocess.CREATE_NO_WINDOW
                
                # Get mod folder name from config
                mod_folder = self.mod_config.get('mod_folder_name', 'z_SCAM_P')
                
                # Run repak subprocess (hidden)
                subprocess.run([repak_path, 'pack', mod_folder], 
                             check=True,
                             startupinfo=startupinfo,
                             creationflags=creationflags)
                
                # Move the created pak file to destination
                pak_file = os.path.join(temp_build_dir, f'{mod_folder}.pak')
                if os.path.exists(pak_file):
                    shutil.move(pak_file, os.path.join(mods_path, f'{mod_folder}.pak'))
                
                # Restore original working directory
                os.chdir(original_cwd)
                
            finally:
                # Always close the progress window
                progress_window.destroy()
                
        except subprocess.CalledProcessError as e:
            from .localization.language_manager import get_current_localization
            loc = get_current_localization()
            raise RuntimeError(loc.get_error("failed_to_run_repak", error=str(e)))
        except Exception as e:
            from .localization.language_manager import get_current_localization
            loc = get_current_localization()
            raise RuntimeError(loc.get_error("error_during_mod_creation", error=str(e)))