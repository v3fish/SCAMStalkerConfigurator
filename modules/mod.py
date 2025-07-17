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
from tkinter import messagebox

class ModCreator:
    def __init__(self, base_path):
        self.base_path = base_path
        if getattr(sys, 'frozen', False):
            self.exe_dir = os.path.dirname(sys.executable)
        else:
            self.exe_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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
            repak_folder_path = os.path.join(self.exe_dir, 'repak')
            raise FileNotFoundError(loc.get_error("repak_not_found", repak_path=repak_folder_path))

        try:
            # Remove old mod file if it exists (for people upgrading from old version)
            old_mod_file = os.path.join(mods_path, 'z_SCAMMovementAiming_P.pak')
            if os.path.exists(old_mod_file):
                os.remove(old_mod_file)
            
            # Create mod only after confirming repak exists
            mod_path = Path('z_SCAM_P/Stalker2/Content/GameLite/GameData/ObjPrototypes')
            mod_path.mkdir(parents=True, exist_ok=True)
            
            if 'Aiming' in config:
                del config['Aiming']
            
            cfg_content = self._generate_cfg_content(config)
            
            with open(mod_path / 'zSCAM.cfg', 'w') as f:
                f.write(cfg_content)
            
            self._run_repak(mods_path, repak_path)
        except Exception as e:
            # Clean up any created folders if there's an error
            if os.path.exists('z_SCAM_P'):
                shutil.rmtree('z_SCAM_P')
            raise

    def _find_repak(self):
        """Find repak.exe in the correct location only"""
        # First check if it's bundled
        bundled_path = os.path.join(self.base_path, 'repak', 'repak.exe')
        if os.path.exists(bundled_path):
            return bundled_path

        # If not bundled, check next to the executable/script
        external_path = os.path.join(self.exe_dir, 'repak', 'repak.exe')
        if os.path.exists(external_path):
            return external_path

        return None

    def _generate_cfg_content(self, config):
        content = "CustomPlayer : struct.begin {refurl=../ObjPrototypes.cfg; refkey=Player}\n"
        
        # Handle SpendStaminaInSafeZone as a special case - it goes directly under CustomPlayer
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
        content += "// Personal use only — redistribution requires author permission\n"
        return content

    def _run_repak(self, mods_path, repak_path):
        try:
            subprocess.run([repak_path, 'pack', 'z_SCAM_P'], check=True)
            shutil.move('z_SCAM_P.pak', os.path.join(mods_path, 'z_SCAM_P.pak'))
            shutil.rmtree('z_SCAM_P')
        except subprocess.CalledProcessError as e:
            if os.path.exists('z_SCAM_P'):
                shutil.rmtree('z_SCAM_P')
            from .localization.language_manager import get_current_localization
            loc = get_current_localization()
            raise RuntimeError(loc.get_error("failed_to_run_repak", error=str(e)))
        except Exception as e:
            if os.path.exists('z_SCAM_P'):
                shutil.rmtree('z_SCAM_P')
            from .localization.language_manager import get_current_localization
            loc = get_current_localization()
            raise RuntimeError(loc.get_error("error_during_mod_creation", error=str(e)))