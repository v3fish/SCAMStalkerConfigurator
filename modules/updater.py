# modules/updater.py
try:
    import requests
    from packaging import version
    UPDATE_CHECKING_ENABLED = True
except ImportError:
    # If either requests OR packaging is missing, disable update checking
    UPDATE_CHECKING_ENABLED = False
from tkinter import messagebox
import webbrowser
from . import VERSION

class UpdateChecker:
    def __init__(self):
        self.github_api_url = "https://api.github.com/repos/v3fish/SCAMStalkerConfigurator/releases/latest"
        self.current_version = VERSION
        
    def check_for_updates(self, silent=False):
        if not UPDATE_CHECKING_ENABLED:
            if not silent:
                messagebox.showinfo("Updates Disabled", 
                    "Update checking is disabled. Please install both 'requests' and 'packaging' packages to enable this feature.")
            return False
            
        try:
            response = requests.get(self.github_api_url, timeout=5)
            response.raise_for_status()
            
            release_data = response.json()
            latest_version = release_data['tag_name'].lstrip('v')
            
            if version.parse(latest_version) > version.parse(self.current_version):
                if messagebox.askyesno("Update Available", 
                    f"A new version ({latest_version}) is available!\n\n"
                    f"You are currently running version {self.current_version}\n\n"
                    "Would you like to open the download page?"):
                    webbrowser.open("https://github.com/v3fish/SCAMStalkerConfigurator/releases/latest")
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