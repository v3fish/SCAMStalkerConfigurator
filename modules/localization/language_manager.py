"""
Language Manager for SCAM Localization System

Handles language selection, switching, and provides centralized access to localized strings.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# Global variable to store current localization
_current_localization = None

def get_data_folder_name():
    """Get the data folder name without circular imports"""
    try:
        from modules.config import DATA_FOLDER_NAME
        return DATA_FOLDER_NAME
    except ImportError:
        return "data"  # Fallback to default

class LanguageManager:
    """
    Manages language selection and localization loading
    """
    
    def __init__(self, base_path, user_data_path=None):
        self.base_path = base_path
        # Use user_data_path for user files, fallback to base_path for backward compatibility
        self.user_data_path = user_data_path if user_data_path is not None else base_path
        self.preferences_file = os.path.join(self.user_data_path, 'app_preferences.json')
        self.current_language = self.load_saved_language()
        self.available_languages = self.discover_languages()
        self.load_language(self.current_language)

    def load_saved_language(self):
        """Load the saved language preference"""
        try:
            if os.path.exists(self.preferences_file):
                with open(self.preferences_file, 'r') as f:
                    prefs = json.load(f)
                    return prefs.get('language', 'en')
        except:
            pass
        return 'en'

    def discover_languages(self):
        """Discover available language files"""
        languages = {'en': 'English'}  # Always have English as default
        
        try:
            import os
            localization_dir = os.path.dirname(__file__)
            for filename in os.listdir(localization_dir):
                if filename.endswith('.py') and filename not in ['__init__.py', 'language_manager.py', 'english.py']:
                    lang_code = filename[:-3]  # Remove .py extension
                    try:
                        lang_module = __import__(f'modules.localization.{lang_code}', fromlist=[lang_code])
                        if hasattr(lang_module, 'LANGUAGES') and lang_code in lang_module.LANGUAGES:
                            languages[lang_code] = lang_module.LANGUAGES[lang_code]
                        else:
                            languages[lang_code] = lang_code.capitalize()
                    except ImportError:
                        pass
        except:
            pass
        
        return languages

    def save_language_preference(self, language_code):
        """Save the language preference"""
        try:
            prefs = {}
            if os.path.exists(self.preferences_file):
                with open(self.preferences_file, 'r') as f:
                    prefs = json.load(f)
            
            prefs['language'] = language_code
            
            with open(self.preferences_file, 'w', encoding='utf-8') as f:
                json.dump(prefs, f, indent=2)
        except:
            pass

    def load_language(self, language_code):
        """Load a specific language"""
        global _current_localization
        
        self.current_language = language_code
        
        if language_code == 'en':
            from . import english as lang_module
        else:
            # Try to import other language files if they exist
            try:
                lang_module = __import__(f'modules.localization.{language_code}', fromlist=[language_code])
            except ImportError:
                from . import english as lang_module  # Fallback to English

        _current_localization = Localization(lang_module)

    def get_available_languages(self):
        """Get list of available languages"""
        return self.available_languages

    def change_language(self, language_code):
        """Change the current language"""
        if language_code in self.available_languages:
            self.save_language_preference(language_code)
            self.load_language(language_code)
            return True
        return False

    def show_language_selection_dialog(self, parent, refresh_callback=None):
        """Show language selection dialog"""
        dialog = LanguageSelectionDialog(parent, self, refresh_callback)
        return dialog.result

class LanguageSelectionDialog(tk.Toplevel):
    """
    Dialog for selecting application language
    """
    
    def __init__(self, parent, language_manager, refresh_callback=None):
        super().__init__(parent)
        self.language_manager = language_manager
        self.refresh_callback = refresh_callback
        self.result = None
        
        # Get current localization for UI text
        loc = get_current_localization()
        
        # Configure window
        self.title(loc.get_title("language_selection"))
        self.geometry("350x250")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        # Set window icon - same as main window
        try:
            # Get the base path from the language manager
            base_path = language_manager.base_path
            icon_path = os.path.join(base_path, 'ico', 'icon2.ico')
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except Exception:
            pass  # If icon setting fails, continue without it
        
        # Center the window
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")
        
        self.setup_ui(loc)

    def setup_ui(self, loc):
        """Setup the dialog UI"""
        # Main frame
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill='both', expand=True)
        
        # Title label
        title_label = ttk.Label(main_frame, text=loc.get_label("select_language"), 
                               font=loc.get_font('large_bold'))
        title_label.pack(pady=(0, 10))
        
        # Language selection frame
        lang_frame = ttk.Frame(main_frame)
        lang_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        # Language listbox with scrollbar
        listbox_frame = ttk.Frame(lang_frame)
        listbox_frame.pack(fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(listbox_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.language_listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set,
                                          font=loc.get_font('large'), height=4)
        self.language_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.configure(command=self.language_listbox.yview)
        
        # Populate languages
        self.language_codes = []
        current_index = 0
        for i, (code, name) in enumerate(self.language_manager.get_available_languages().items()):
            self.language_listbox.insert(tk.END, name)
            self.language_codes.append(code)
            if code == self.language_manager.current_language:
                current_index = i
        
        # Select current language
        self.language_listbox.selection_set(current_index)
        self.language_listbox.see(current_index)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=(10, 0))
        
        ttk.Button(button_frame, text=loc.get_button("ok"), 
                  command=self.ok).pack(side='right', padx=(5, 0))
        ttk.Button(button_frame, text=loc.get_button("cancel"), 
                  command=self.cancel).pack(side='right')
        
        # Bind events
        self.language_listbox.bind('<Double-Button-1>', lambda e: self.ok())
        self.bind('<Return>', lambda e: self.ok())
        self.bind('<Escape>', lambda e: self.cancel())
        
        # Focus on listbox
        self.language_listbox.focus_set()

    def ok(self):
        """Handle OK button"""
        selection = self.language_listbox.curselection()
        if selection:
            selected_code = self.language_codes[selection[0]]
            selected_name = self.language_manager.get_available_languages()[selected_code]
            
            # Change language
            if self.language_manager.change_language(selected_code):
                self.result = selected_code
                
                # Trigger UI refresh if callback provided
                if self.refresh_callback:
                    self.refresh_callback()
        
        self.destroy()

    def cancel(self):
        """Handle Cancel button"""
        self.destroy()

class Localization:
    """
    Localization class to manage all text strings.
    
    Usage:
        loc = Localization(language_module)
        title = loc.get_app_title("1.0.0")
        error = loc.get_error("invalid_stalker_directory")
    """
    
    def __init__(self, language_module):
        self.lang = language_module
        
    def get_app_title(self, version):
        """Get the application title with version - hardcoded in English"""
        return f"SCAM - Stalker Character Adjustment Manager v{version}"
        
    def get_credits_text(self, version):
        """Get the full credits text"""
        return f"{self.lang.APP_INFO['author']} | {self.lang.APP_INFO['credits']} | {self.lang.APP_INFO['version'].format(version=version)}"
        
    def get_title(self, key):
        """Get a window/dialog title"""
        return self.lang.TITLES.get(key, key)
        
    def get_button(self, key):
        """Get a button label"""
        return self.lang.BUTTONS.get(key, key)
        
    def get_label(self, key, **kwargs):
        """Get a form label with optional formatting"""
        text = self.lang.LABELS.get(key, key)
        kwargs['data_folder'] = get_data_folder_name()
        return text.format(**kwargs) if kwargs else text
        
    def get_language(self, key):
        """Get a language name"""
        return self.lang.LANGUAGES.get(key, key)
        
    def get_preset(self, key):
        """Get a preset name"""
        return self.lang.PRESETS.get(key, key)
        
    def get_section(self, key):
        """Get a section/tab name"""
        return self.lang.SECTIONS.get(key, key)
        
    def get_success(self, key, **kwargs):
        """Get a success message with optional formatting"""
        text = self.lang.SUCCESS_MESSAGES.get(key, key)
        kwargs['data_folder'] = get_data_folder_name()
        return text.format(**kwargs) if kwargs else text
        
    def get_warning(self, key, **kwargs):
        """Get a warning message with optional formatting"""
        text = self.lang.WARNING_MESSAGES.get(key, key)
        kwargs['data_folder'] = get_data_folder_name()
        return text.format(**kwargs) if kwargs else text
        
    def get_error(self, key, **kwargs):
        """Get an error message with optional formatting"""
        text = self.lang.ERROR_MESSAGES.get(key, key)
        kwargs['data_folder'] = get_data_folder_name()
        return text.format(**kwargs) if kwargs else text
        
    def get_confirmation(self, key, **kwargs):
        """Get a confirmation message with optional formatting"""
        text = self.lang.CONFIRMATIONS.get(key, key)
        kwargs['data_folder'] = get_data_folder_name()
        return text.format(**kwargs) if kwargs else text
        
    def get_instruction(self, key, **kwargs):
        """Get an instruction text with optional formatting"""
        text = self.lang.INSTRUCTIONS.get(key, key)
        kwargs['data_folder'] = get_data_folder_name()
        return text.format(**kwargs) if kwargs else text
        
    def get_status(self, key, **kwargs):
        """Get a status message with optional formatting"""
        text = self.lang.STATUS.get(key, key)
        kwargs['data_folder'] = get_data_folder_name()
        return text.format(**kwargs) if kwargs else text
        
    def get_font(self, key):
        """Get a font configuration"""
        if hasattr(self.lang, 'FONTS'):
            return self.lang.FONTS.get(key, ('Arial', 9))
        return ('Arial', 9)  # Default font

def get_current_localization():
    """Get the current localization instance"""
    global _current_localization
    if _current_localization is None:
        # Initialize with English as default
        from . import english as lang_module
        _current_localization = Localization(lang_module)
    return _current_localization

# Convenience functions for easy access
def get_text(category, key, **kwargs):
    """
    Get localized text from any category.
    
    Args:
        category: One of 'title', 'button', 'label', 'preset', 
                 'section', 'success', 'warning', 'error', 'confirmation', 
                 'instruction', 'status'
        key: The text key
        **kwargs: Format arguments
    """
    loc = get_current_localization()
    method_map = {
        'title': loc.get_title,
        'button': loc.get_button,
        'label': loc.get_label,
        'language': loc.get_language,
        'preset': loc.get_preset,
        'section': loc.get_section,
        'success': loc.get_success,
        'warning': loc.get_warning,
        'error': loc.get_error,
        'confirmation': loc.get_confirmation,
        'instruction': loc.get_instruction,
        'status': loc.get_status
    }
    
    method = method_map.get(category)
    if method:
        return method(key, **kwargs)
    return key

# Direct access functions for most common use cases
def t(key, **kwargs):
    """Quick access function for common text (tries button, then label, then title)"""
    loc = get_current_localization()
    if hasattr(loc.lang, 'BUTTONS') and key in loc.lang.BUTTONS:
        return loc.get_button(key)
    elif hasattr(loc.lang, 'LABELS') and key in loc.lang.LABELS:
        return loc.get_label(key, **kwargs)
    elif hasattr(loc.lang, 'TITLES') and key in loc.lang.TITLES:
        return loc.get_title(key)
    return key

def error(key, **kwargs):
    """Quick access for error messages"""
    return get_current_localization().get_error(key, **kwargs)

def success(key, **kwargs):
    """Quick access for success messages"""
    return get_current_localization().get_success(key, **kwargs)

def warning(key, **kwargs):
    """Quick access for warning messages"""
    return get_current_localization().get_warning(key, **kwargs)

def confirm(key, **kwargs):
    """Quick access for confirmation messages"""
    return get_current_localization().get_confirmation(key, **kwargs)

def font(key):
    """Quick access for font configurations"""
    return get_current_localization().get_font(key) 