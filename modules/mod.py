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

class ModCreator:
    def __init__(self, base_path):
        self.base_path = base_path
        # Get the actual executable directory or script directory
        if getattr(sys, 'frozen', False):
            self.exe_dir = os.path.dirname(sys.executable)
        else:
            self.exe_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def create_mod(self, config, mods_path):
        # Only look in the correct repak folder location
        repak_path = self._find_repak()
        if not repak_path:
            raise FileNotFoundError(
                "repak.exe not found!\n\n"
                "Please create a folder named 'repak' and place repak.exe inside it.\n"
                f"The repak folder should be at: {os.path.join(self.exe_dir, 'repak')}\n\n"
                "Folder structure should be:\n"
                "📁 Your Installation Folder\n"
                "   └─📄 Stalker Configurator Aiming Movement.exe\n"
                "   └─📁 repak\n"
                "      └─📄 repak.exe"
            )

        try:
            # Create mod only after confirming repak exists
            mod_path = Path('z_SCAMMovementAiming_P/Stalker2/Content/GameLite/GameData/ObjPrototypes')
            mod_path.mkdir(parents=True, exist_ok=True)
            
            if 'Aiming' in config:
                del config['Aiming']
            
            cfg_content = self._generate_cfg_content(config)
            
            with open(mod_path / 'SCAM.cfg', 'w') as f:
                f.write(cfg_content)
            
            self._run_repak(mods_path, repak_path)
        except Exception as e:
            # Clean up any created folders if there's an error
            if os.path.exists('z_SCAMMovementAiming_P'):
                shutil.rmtree('z_SCAMMovementAiming_P')
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
        for section, values in config.items():
            content += f"   {section} : struct.begin\n"
            for key, value in values.items():
                content += f"      {key} = {value}\n"
            content += "   struct.end\n"
        content += "struct.end"
        return content

    def _run_repak(self, mods_path, repak_path):
        try:
            subprocess.run([repak_path, 'pack', 'z_SCAMMovementAiming_P'], check=True)
            shutil.move('z_SCAMMovementAiming_P.pak', os.path.join(mods_path, 'z_SCAMMovementAiming_P.pak'))
            shutil.rmtree('z_SCAMMovementAiming_P')
        except subprocess.CalledProcessError as e:
            if os.path.exists('z_SCAMMovementAiming_P'):
                shutil.rmtree('z_SCAMMovementAiming_P')
            raise RuntimeError(f"Failed to run repak: {str(e)}")
        except Exception as e:
            if os.path.exists('z_SCAMMovementAiming_P'):
                shutil.rmtree('z_SCAMMovementAiming_P')
            raise RuntimeError(f"Error during mod creation: {str(e)}")