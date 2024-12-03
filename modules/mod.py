# modules/mod.py
import os
import subprocess
import shutil
from pathlib import Path

class ModCreator:
    def __init__(self, base_path):
        self.base_path = base_path

    def create_mod(self, config, mods_path):
        mod_path = Path('z_SCAMMovementAiming_P/Stalker2/Content/GameLite/GameData/ObjPrototypes')
        mod_path.mkdir(parents=True, exist_ok=True)
        
        if 'Aiming' in config:
            del config['Aiming']
        
        cfg_content = self._generate_cfg_content(config)
        
        with open(mod_path / 'SCAM.cfg', 'w') as f:
            f.write(cfg_content)
        
        self._run_repak(mods_path)

    def _generate_cfg_content(self, config):
        content = "CustomPlayer : struct.begin {refurl=../ObjPrototypes.cfg; refkey=Player}\n"
        for section, values in config.items():
            content += f"   {section} : struct.begin\n"
            for key, value in values.items():
                content += f"      {key} = {value}\n"
            content += "   struct.end\n"
        content += "struct.end"
        return content

    def _run_repak(self, mods_path):
        repak_path = os.path.join(self.base_path, 'repak', 'repak.exe')
        if not os.path.exists(repak_path):
            raise FileNotFoundError("repak.exe not found in repak folder!")
            
        try:
            subprocess.run([repak_path, 'pack', 'z_SCAMMovementAiming_P'], check=True)
            shutil.move('z_SCAMMovementAiming_P.pak', os.path.join(mods_path, 'z_SCAMMovementAiming_P.pak'))
            shutil.rmtree('z_SCAMMovementAiming_P')
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to run repak: {str(e)}")
        except Exception as e:
            if os.path.exists('z_SCAMMovementAiming_P'):
                shutil.rmtree('z_SCAMMovementAiming_P')
            raise RuntimeError(f"Error during mod creation: {str(e)}")