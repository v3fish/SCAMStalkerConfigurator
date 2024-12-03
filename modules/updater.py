import requests
import re
from packaging import version
from tkinter import messagebox
import webbrowser
from . import VERSION
import os
import sys
import zipfile
import subprocess
import tempfile
import shutil

class UpdateChecker:
    def __init__(self):
        self.github_api_url = "https://api.github.com/repos/v3fish/SCAMStalkerConfigurator/releases/latest"
        self.current_version = VERSION
        self.download_url = None
        self.app_path = sys.executable if getattr(sys, 'frozen', False) else None
        
    def check_for_updates(self, silent=False):
        if not self.app_path and getattr(sys, 'frozen', False):
            return False
            
        try:
            response = requests.get(self.github_api_url, timeout=5)
            response.raise_for_status()
            
            release_data = response.json()
            latest_version = release_data['tag_name'].lstrip('v')
            self.download_url = next((asset['browser_download_url'] 
                                    for asset in release_data['assets'] 
                                    if asset['name'].endswith('.zip')), None)
            
            if version.parse(latest_version) > version.parse(self.current_version):
                self._show_update_dialog(latest_version)
                return True
            elif not silent:
                messagebox.showinfo("No Updates", "You are running the latest version!")
            return False
            
        except Exception as e:
            if not silent:
                messagebox.showerror("Update Check Failed", 
                    f"Failed to check for updates: {str(e)}\n\n"
                    "Please check your internet connection or try again later.")
            return False
    
    def _show_update_dialog(self, latest_version):
        if messagebox.askyesno("Update Available", 
            f"A new version ({latest_version}) is available!\n\n"
            f"You are currently running version {self.current_version}\n\n"
            "Would you like to update now? The application will restart."):
            self._perform_update()

    def _perform_update(self):
        try:
            # Create temp directory
            with tempfile.TemporaryDirectory() as temp_dir:
                # Download zip file
                response = requests.get(self.download_url, stream=True)
                zip_path = os.path.join(temp_dir, "update.zip")
                with open(zip_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

                # Extract zip
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)

                # Find the exe in the extracted files
                exe_name = os.path.basename(self.app_path)
                extracted_exe = None
                for root, _, files in os.walk(temp_dir):
                    if exe_name in files:
                        extracted_exe = os.path.join(root, exe_name)
                        break

                if not extracted_exe:
                    raise Exception("Could not find executable in update package")

                # Create batch file for update
                batch_path = os.path.join(temp_dir, "update.bat")
                with open(batch_path, 'w') as batch:
                    batch.write('@echo off\n')
                    batch.write('timeout /t 1 /nobreak >nul\n')  # Wait for original process to close
                    batch.write(f'copy /Y "{extracted_exe}" "{self.app_path}"\n')
                    batch.write(f'start "" "{self.app_path}"\n')
                    batch.write('del "%~f0"\n')  # Delete the batch file

                # Run the update batch file and close the application
                subprocess.Popen([batch_path], shell=True)
                sys.exit()

        except Exception as e:
            messagebox.showerror("Update Failed", 
                f"Failed to update: {str(e)}\n\n"
                "Please try downloading the update manually.")
            webbrowser.open("https://github.com/v3fish/SCAMStalkerConfigurator/releases/latest")