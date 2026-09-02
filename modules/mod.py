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

    def create_mod(self, config, mods_path, parent=None):
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
            required_keys = ['mod_folder_name', 'cfg_folder_name', 'cfg_files']
            for key in required_keys:
                if key not in self.mod_config:
                    raise KeyError(f"'{key}' missing in mod_config.json or database. Please provide all required keys.")
            mod_folder = self.mod_config['mod_folder_name']
            
            aiming_config = config.pop('Aiming', {})
            remove_mouse_smoothing = bool(aiming_config.get('RemoveMouseSmoothing', False))
            remove_mouse_slowdown = bool(aiming_config.get('RemoveMouseSlowdown', False))
            remove_camera_shake = bool(aiming_config.get('RemoveCameraShake', False))
            remove_aim_block = bool(aiming_config.get('RemoveAimBlock', False))
            
            stamina_disable_threshold = None
            if 'VitalParams' in config and 'StaminaDisableThreshold' in config['VitalParams']:
                stamina_disable_threshold = config['VitalParams'].pop('StaminaDisableThreshold')
                if not config['VitalParams']:
                    del config['VitalParams']
            
            disable_overweight_restriction = False
            if 'MovementParams' in config and 'DisableOverweightMovementRestriction' in config['MovementParams']:
                disable_overweight_restriction = bool(config['MovementParams'].pop('DisableOverweightMovementRestriction'))
            
            remove_water_slowdown = False
            if 'MovementParams' in config and 'RemoveWaterSlowdown' in config['MovementParams']:
                remove_water_slowdown = bool(config['MovementParams'].pop('RemoveWaterSlowdown'))
            
            if 'MovementParams' in config and not config['MovementParams']:
                del config['MovementParams']
            
            section_patches, player_patches = self._generate_player_patches(
                stamina_disable_threshold, disable_overweight_restriction, remove_water_slowdown,
                remove_mouse_slowdown)
            
            # Only write Player.cfg if there's actually something to patch - avoids
            # shipping an empty "Player : struct.begin {bpatch} struct.end" file
            # when only an EffectPrototypes/CameraShakePrototypes toggle is checked.
            if config or section_patches or player_patches:
                cfg_content = self._generate_cfg_content(config, section_patches, player_patches)
                self._write_gamedata_cfg(temp_build_dir, mod_folder, 'ObjPrototypes', cfg_content)
            
            if remove_mouse_smoothing:
                self._write_user_input_ini(temp_build_dir, mod_folder)
            
            effect_content = self._generate_effect_prototypes_content(
                remove_mouse_slowdown, remove_camera_shake, remove_aim_block)
            if effect_content:
                self._write_gamedata_cfg(temp_build_dir, mod_folder, 'EffectPrototypes', effect_content)
            
            camera_shake_content = self._generate_camera_shake_prototypes_content(remove_camera_shake)
            if camera_shake_content:
                self._write_gamedata_cfg(temp_build_dir, mod_folder, 'CameraShakePrototypes', camera_shake_content)
            
            self._run_repak(mods_path, repak_path, temp_build_dir, parent=parent)
            
        except Exception as e:
            # Clean up temp directory if there's an error
            if temp_build_dir and os.path.exists(temp_build_dir):
                shutil.rmtree(temp_build_dir)
            raise
        finally:
            # Always clean up temp directory
            if temp_build_dir and os.path.exists(temp_build_dir):
                shutil.rmtree(temp_build_dir)

    def _write_user_input_ini(self, temp_build_dir, mod_folder):
        """Write a UserInput.ini that disables mouse smoothing, same approach as FMAO"""
        input_ini_dir = Path(temp_build_dir) / mod_folder / 'Stalker2' / 'Config'
        input_ini_dir.mkdir(parents=True, exist_ok=True)
        
        content = "[/Script/Engine.InputSettings]\n"
        content += "bViewAccelerationEnabled=False\n"
        content += "bEnableMouseSmoothing=False\n"
        
        with open(input_ini_dir / 'UserInput.ini', 'w', encoding='utf-8') as f:
            f.write(content)

    def _write_gamedata_cfg(self, temp_build_dir, mod_folder, gamedata_category, content):
        """
        Write a {bpatch} cfg file into GameData/<gamedata_category>/<cfg_folder>/<filename>.
        The cfg folder and filename both come from mod_config.json's cfg_files map, so
        adding a new GameData category later is just one new entry there plus a
        _generate_..._content() method - no filenames hardcoded here.
        """
        cfg_folder = self.mod_config['cfg_folder_name']
        cfg_files = self.mod_config.get('cfg_files', {})
        filename = cfg_files.get(gamedata_category)
        if not filename:
            raise KeyError(f"No cfg filename configured for GameData category '{gamedata_category}' "
                            f"in mod_config.json's cfg_files map.")
        
        target_dir = (Path(temp_build_dir) / mod_folder / 'Stalker2' / 'Content' / 'GameLite' / 'GameData'
                       / gamedata_category / cfg_folder)
        target_dir.mkdir(parents=True, exist_ok=True)
        
        with open(target_dir / filename, 'w', encoding='utf-8') as f:
            f.write(content)

    def _generate_effect_prototypes_content(self, remove_mouse_slowdown, remove_camera_shake, remove_aim_block):
        """
        Build removenode lines for GameData/EffectPrototypes. These SIDs are
        top-level structs in EffectPrototypes.cfg, so no {bpatch}/struct.begin
        wrapper is needed - each line is its own root-level patch.
        """
        lines = []
        
        if remove_mouse_slowdown:
            # Look/turn-rate multipliers only - no camera shake, no aim block
            lines += [
                "ConcussionModifyRotate2DAxis", "ConcussionInputInertia2DAxis",
                "ControllerConcussionModifyRotate2DAxis", "ControllerConcussionInputInertia2DAxis",
                "ConcussionModifyRotate2DAxis_2", "ConcussionInputInertia2DAxis_2",
                "ConcussionModifyRotate2DAxis_Buttstock", "ConcussionInputInertia2DAxis_Buttstock",
                "ChemicalAnomalyTurnRateChangeYaw", "ChemicalAnomalyTurnRateChangePitch",
                "FlycatcherTurnRateChangeYaw", "FlycatcherTurnRateChangePitch",
                "BarbedWireTurnRateChangeYaw", "BarbedWireTurnRateChangePitch",
            ]
        
        if remove_aim_block:
            lines += ["ConcussionBlockAim", "ConcussionBlockAim_2", "ConcussionBlockAim_Buttstock"]
        
        if remove_camera_shake:
            lines += [
                "ConcussionCameraShake", "ConcussionCameraShake_2", "ButtStroke_CameraShake",
                "ProjectileCameraShakeInstant", "MutantAttackCameraShake", "MutantMediumAttackCameraShake",
                "MutantStrongAttackCameraShake", "DrunknessCameraShake", "PoppyFieldCameraShake",
                "ControllerCameraShake", "EmissionCameraShake", "QuestDugaFall_CameraShake",
                "QuestDugaActive_CameraShake", "PlatformElevation_CameraShake", "Binoculars01AimCameraShake",
                "Binoculars02AimCameraShake", "Binoculars03AimCameraShake", "PSYAnomalyCamera",
            ]
        
        if not lines:
            return ""
        
        content = "\n".join(f"{sid} : removenode" for sid in lines) + "\n\n"
        content += "// Generated by SCAM (Stalker Character Adjustment Manager) by v3fish\n"
        content += "// Personal use only - redistribution requires author permission\n"
        return content

    def _generate_camera_shake_prototypes_content(self, remove_camera_shake):
        """Build removenode lines for GameData/CameraShakePrototypes (shake assets, includes gunfire)."""
        if not remove_camera_shake:
            return ""
        
        shake_assets = [
            "ShootingCameraShake", "PMShootCameraShake", "UDPShootCameraShake", "ViperShootCameraShake",
            "AKUShootCameraShake", "AK74ShootCameraShake", "M16ShootCameraShake", "ObrezShootCameraShake",
            "TozShootCameraShake", "M860ShootCameraShake", "M10ShootCameraShake", "BucketShootCameraShake",
            "SVDMShootCameraShake", "M701ShootCameraShake", "IntegralShootCameraShake", "G37ShootCameraShake",
            "ForaShootCameraShake", "PKPShootCameraShake", "GaussShootCameraShake", "ZubrShootCameraShake",
            "LavinaShootCameraShake", "RPGShootCameraShake", "SPSAShootCameraShake", "D12ShootCameraShake",
            "Ram2ShootCameraShake", "APBShootCameraShake", "RhinoShootCameraShake", "SVUShootCameraShake",
            "GrimShootCameraShake", "DniproShootCameraShake", "MarkShootCameraShake", "KharodShootCameraShake",
            "KoraShootCameraShake", "ThreeLineShootCameraShake", "ArevShootCameraShake", "SKPShootCameraShake",
            "Fora230ShootCameraShake", "GP3AShootCameraShake", "SVUSQBShootCameraShake", "DummyShootCameraShake",
            "MutantAttackCameraShake", "MutantMediumAttackCameraShake", "MutantStrongAttackCameraShake",
            "ProjectileHitCameraShake", "ButtStrokeCameraShake", "ZulusMeleeAttackCameraShake",
            "ZulusChargeAttackCameraShake", "ZulusFinishAttackCameraShake", "ZulusRunAttackCameraShake",
            "PlatformElevationCameraShake", "DrunkCameraShake", "PoppyFieldCameraShake", "ConcussionCameraShake",
            "ControllerCameraShake", "ConcussionCameraShake_2", "EmissionCameraShake",
            "Binoculars01AimCameraShake", "Binoculars02AimCameraShake", "Binoculars03AimCameraShake",
        ]
        
        content = "\n".join(f"{asset} : removenode" for asset in shake_assets) + "\n\n"
        content += "// Generated by SCAM (Stalker Character Adjustment Manager) by v3fish\n"
        content += "// Personal use only - redistribution requires author permission\n"
        return content

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

    def _format_cfg_value(self, value):
        if isinstance(value, bool):
            return str(value).lower()
        return value

    def _generate_player_patches(self, stamina_disable_threshold, disable_overweight_restriction,
                                  remove_water_slowdown=False, remove_mouse_slowdown=False):
        """
        Build raw cfg snippets for Player-level struct patches that don't fit the
        generic flat section format (nested arrays / removenode).
        
        Returns (section_patches, player_patches):
          - section_patches: {section_name: extra raw lines to merge into that
            section's existing struct.begin {bpatch} block instead of opening a
            second, duplicate block for the same section.
          - player_patches: raw lines that go directly under Player, for keys
            that aren't part of any existing section.
        """
        section_patches = {}
        player_patches = ""
        
        if stamina_disable_threshold is not None:
            # Player -> VitalParams -> StaminaDisableThresholds -> [0].Threshold
            # {bpatch} is required at every nested level so RegenerationDelay/StateTags
            # on [0] are preserved instead of being wiped out.
            lines = "      StaminaDisableThresholds : struct.begin {bpatch}\n"
            lines += "         [0] : struct.begin {bpatch}\n"
            lines += f"            Threshold = {self._format_cfg_value(stamina_disable_threshold)}\n"
            lines += "         struct.end\n"
            lines += "      struct.end\n"
            section_patches['VitalParams'] = lines
        
        if disable_overweight_restriction:
            # Player's DisableMovementWeightThreshold only has a single [0] entry
            # (Overweight, blocking movement). Removing it lets you move freely
            # no matter how overweight you are.
            player_patches += "   DisableMovementWeightThreshold : struct.begin {bpatch}\n"
            player_patches += "      [0] : removenode\n"
            player_patches += "   struct.end\n"
        
        # Player -> WaterContactInfo -> Single/DualCurveEffects. Single = look/aim
        # slowdown (belongs to Remove Mouse Slowdown), Dual = walk-in-water movement
        # slowdown (belongs to Remove Water Slowdown). Merge into one block since
        # both toggles can be checked at once.
        water_fields = ""
        if remove_mouse_slowdown:
            water_fields += "      SingleCurveEffects : removenode\n"
        if remove_water_slowdown:
            water_fields += "      DualCurveEffects : removenode\n"
        if water_fields:
            player_patches += "   WaterContactInfo : struct.begin {bpatch}\n"
            player_patches += water_fields
            player_patches += "   struct.end\n"
        
        return section_patches, player_patches

    def _generate_cfg_content(self, config, section_patches=None, player_patches=""):
        section_patches = section_patches or {}
        content = "Player : struct.begin {bpatch}\n"
        
        # Handle SpendStaminaInSafeZone as a special case - it goes directly under Player
        if 'StaminaPerAction' in config and 'SpendStaminaInSafeZone' in config['StaminaPerAction']:
            content += f"SpendStaminaInSafeZone = {self._format_cfg_value(config['StaminaPerAction']['SpendStaminaInSafeZone'])}\n"
        
        handled_sections = set()
        for section, values in config.items():
            # Create a copy of values to avoid modifying the original
            section_values = values.copy()
            
            # Remove SpendStaminaInSafeZone from StaminaPerAction section as it's handled above
            if section == 'StaminaPerAction' and 'SpendStaminaInSafeZone' in section_values:
                section_values.pop('SpendStaminaInSafeZone')
            
            handled_sections.add(section)
            
            # Only create the section if there are still values left, or a patch needs it
            if section_values or section in section_patches:
                content += f"   {section} : struct.begin {{bpatch}}\n"
                for key, value in section_values.items():
                    content += f"      {key} = {self._format_cfg_value(value)}\n"
                if section in section_patches:
                    content += section_patches[section]
                content += "   struct.end\n"
        
        # Sections that only exist because of a patch (e.g. VitalParams has no
        # normal settings changed, only StaminaDisableThreshold)
        for section, patch in section_patches.items():
            if section not in handled_sections:
                content += f"   {section} : struct.begin {{bpatch}}\n"
                content += patch
                content += "   struct.end\n"
        
        if player_patches:
            content += player_patches
        
        content += "struct.end\n\n"
        content += "// Generated by SCAM (Stalker Character Adjustment Manager) by v3fish\n"
        content += "// Personal use only - redistribution requires author permission\n"
        return content

    def _run_repak(self, mods_path, repak_path, temp_build_dir, parent=None):
        try:
            # Show progress dialog during repak execution
            import tkinter as tk
            from tkinter import ttk
            
            # Create progress window on the same screen as SCAM
            progress_window = tk.Toplevel(parent) if parent is not None else tk.Toplevel()
            progress_window.title("Creating Mod")
            progress_window.geometry("300x100")
            progress_window.resizable(False, False)
            if parent is not None:
                progress_window.transient(parent)
            progress_window.grab_set()
            
            progress_window.update_idletasks()
            if parent is not None:
                parent.update_idletasks()
                x = parent.winfo_x() + (parent.winfo_width() // 2) - 150
                y = parent.winfo_y() + (parent.winfo_height() // 2) - 50
            else:
                x = (progress_window.winfo_screenwidth() // 2) - 150
                y = (progress_window.winfo_screenheight() // 2) - 50
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