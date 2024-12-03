import requests
import re
from packaging import version
from tkinter import messagebox, Toplevel, ttk
import webbrowser
from . import VERSION
import os
import sys
import zipfile
import subprocess
import shutil
import threading

class UpdateProgressDialog:
    def __init__(self, parent):
        self.window = Toplevel(parent)
        self.window.title("Updating...")
        self.window.geometry("300x150")
        self.window.transient(parent)
        self.window.grab_set()
        
        # Center the window
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'+{x}+{y}')
        
        self.status_label = ttk.Label(self.window, text="Starting update...", wraplength=250)
        self.status_label.pack(pady=10)
        
        self.progress = ttk.Progressbar(self.window, length=200, mode='determinate')
        self.progress.pack(pady=10)
        
        self.detail_label = ttk.Label(self.window, text="", wraplength=250)
        self.detail_label.pack(pady=10)

    def update_status(self, message, progress=None):
        self.status_label.config(text=message)
        if progress is not None:
            self.progress['value'] = progress
        self.window.update()

    def update_detail(self, message):
        self.detail_label.config(text=message)
        self.window.update()

class UpdateChecker:
    def __init__(self, parent_window=None):
        self.github_api_url = "https://api.github.com/repos/v3fish/SCAMStalkerConfigurator/releases/latest"
        self.current_version = VERSION
        self.download_url = None
        self.app_path = sys.executable if getattr(sys, 'frozen', False) else sys.argv[0]
        self.parent_window = parent_window
        self.base_dir = os.path.dirname(os.path.abspath(self.app_path))
        
    def check_for_updates(self, silent=False):
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
            progress_dialog = UpdateProgressDialog(self.parent_window)
            update_thread = threading.Thread(target=lambda: self._perform_update(progress_dialog))
            update_thread.start()

    def _perform_update(self, progress_dialog):
        temp_dir = os.path.join(self.base_dir, 'temp_update')
        
        try:
            # Create temp directory
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            os.makedirs(temp_dir)

            # Download zip file
            progress_dialog.update_status("Downloading update...", 10)
            zip_path = os.path.join(temp_dir, "update.zip")
            
            response = requests.get(self.download_url, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024
            downloaded = 0
            
            with open(zip_path, 'wb') as f:
                for data in response.iter_content(block_size):
                    downloaded += len(data)
                    f.write(data)
                    if total_size:
                        progress = int((downloaded / total_size) * 50)  # Up to 50%
                        progress_dialog.update_status("Downloading update...", progress)
                        progress_dialog.update_detail(f"Downloaded: {downloaded // 1024} KB / {total_size // 1024} KB")

            # Extract zip
            progress_dialog.update_status("Extracting files...", 60)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            # Find the exe
            progress_dialog.update_status("Preparing update...", 80)
            exe_name = os.path.basename(self.app_path)
            extracted_exe = None
            for root, _, files in os.walk(temp_dir):
                if exe_name in files:
                    extracted_exe = os.path.join(root, exe_name)
                    break

            if not extracted_exe:
                raise Exception("Could not find executable in update package")

            # Create batch file
            progress_dialog.update_status("Creating update script...", 90)
            batch_path = os.path.join(temp_dir, "update.bat")
            with open(batch_path, 'w') as batch:
                batch.write('@echo off\n')
                batch.write('timeout /t 2 /nobreak >nul\n')
                batch.write(f'copy /Y "{extracted_exe}" "{self.app_path}"\n')
                batch.write(f'start "" "{self.app_path}"\n')
                batch.write(f'rmdir /S /Q "{temp_dir}"\n')
                batch.write('exit\n')

            # Schedule the final update steps
            progress_dialog.window.after(1000, lambda: self._finish_update(temp_dir, batch_path, progress_dialog))

        except Exception as e:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            messagebox.showerror("Update Failed", 
                f"Failed to update: {str(e)}\n\n"
                "Please try downloading the update manually.")
            webbrowser.open("https://github.com/v3fish/SCAMStalkerConfigurator/releases/latest")
            progress_dialog.window.destroy()

    def _finish_update(self, temp_dir, batch_path, progress_dialog):
        progress_dialog.update_status("Applying update...", 100)
        progress_dialog.update_detail("Restarting application...")
        progress_dialog.window.destroy()
        if self.parent_window:
            self.parent_window.quit()
        subprocess.Popen([batch_path], shell=True)
        sys.exit()