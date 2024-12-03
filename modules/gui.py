# modules/gui.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sys
import os
from .config import ConfigHandler
from .mod import ModCreator
from .config_interface import ConfigInterface
from .updater import UpdateChecker
from . import VERSION

class PresetDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.result = None
        
        # Configure window
        self.title("New Preset")
        self.geometry("300x120")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        # Center the window
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")
        
        # Create and pack widgets
        ttk.Label(self, text="Enter preset name:").pack(padx=20, pady=(20,5))
        
        self.entry = ttk.Entry(self, width=40)
        self.entry.pack(padx=20, pady=5)
        
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="OK", command=self.ok).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side='left', padx=5)
        
        self.entry.focus_set()
        self.bind('<Return>', lambda e: self.ok())
        self.bind('<Escape>', lambda e: self.cancel())

    def ok(self):
        self.result = self.entry.get()
        self.destroy()

    def cancel(self):
        self.destroy()
        
class MovementConfigEditor:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title(f"SCAM - Stalker Configurator Aiming & Movement v{VERSION}")
        self.window.geometry("1000x850")

        if getattr(sys, 'frozen', False):
            self.base_path = sys._MEIPASS
        else:
            self.base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

        self.config_handler = ConfigHandler(self.base_path)
        self.mod_creator = ModCreator(self.base_path)
        self.config_interface = ConfigInterface(self.window, self.config_handler)
        self.update_checker = UpdateChecker()
        
        self.force_defaults = tk.BooleanVar(value=False)
        self.setup_gui()
        
        # Check for updates silently on startup
        self.window.after(1000, lambda: self.update_checker.check_for_updates(silent=True))

    def setup_gui(self):
        self.setup_credits_frame()
        self.config_interface.setup_game_dir_frame(self.window)
        self.setup_top_frame()
        self.setup_main_content()

    def setup_credits_frame(self):
        credits_frame = ttk.Frame(self.window)
        credits_frame.pack(fill='x', padx=5, pady=5)
        
        # Add update check button
        update_btn = ttk.Button(credits_frame, text="Check for Updates",
                              command=lambda: self.update_checker.check_for_updates(silent=False))
        update_btn.pack(side='left', padx=5)
        
        credits_label = ttk.Label(credits_frame, 
                                text=f"Made by v3fish | Credits: repak.exe by github.com/trumank | Version: {VERSION}",
                                font=('Arial', 8, 'italic bold'))  # Changed font to include bold
        credits_label.pack(side='right')

    def setup_top_frame(self):
        top_frame = ttk.Frame(self.window)
        top_frame.pack(fill='x', padx=5, pady=5)
        self.setup_preset_controls(top_frame)
        self.setup_recommended_presets(top_frame)
        self.setup_advanced_options(top_frame)

    def setup_preset_controls(self, parent):
        preset_frame = ttk.Frame(parent)
        preset_frame.pack(side='top', fill='x', padx=5, pady=5)
        
        ttk.Label(preset_frame, text="Custom Presets:").pack(side='left', padx=5)
        self.preset_var = tk.StringVar()
        self.preset_combo = ttk.Combobox(preset_frame, textvariable=self.preset_var, state="readonly")
        self.preset_combo.pack(side='left', padx=5)
        
        ttk.Button(preset_frame, text="Load", command=self.load_custom_preset).pack(side='left', padx=5)
        ttk.Button(preset_frame, text="Save", command=self.save_preset).pack(side='left', padx=5)
        ttk.Button(preset_frame, text="New Preset", command=self.new_preset).pack(side='left', padx=5)
        ttk.Button(preset_frame, text="Open Presets Folder", command=self.open_presets_folder).pack(side='left', padx=5)
        
        create_mod_btn = ttk.Button(preset_frame, text="Create Mod", command=self.create_mod, style='Big.TButton')
        create_mod_btn.pack(side='right', padx=5, ipady=5, ipadx=10)
        
        style = ttk.Style()
        style.configure('Big.TButton', font=('Arial', 10, 'bold'))

        if os.path.exists('Presets'):
            self.load_presets()

    def setup_recommended_presets(self, parent):
        recommended_frame = ttk.Frame(parent)
        recommended_frame.pack(side='top', fill='x', pady=10)
        
        buttons_frame = ttk.Frame(recommended_frame)
        buttons_frame.pack(expand=True)
        
        ttk.Button(buttons_frame, text="Default", command=self.load_default).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="V3Fish Recommended", command=self.load_v3fish).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="XY Sensitivity Aim Fix", command=self.load_xy_fix).pack(side='left', padx=5)

    def setup_advanced_options(self, parent):
        advanced_frame = ttk.Frame(parent)
        advanced_frame.pack(side='top', fill='x', padx=5, pady=5)
        
        force_defaults_check = ttk.Checkbutton(advanced_frame, 
                                             text="Force Default Values", 
                                             variable=self.force_defaults)
        force_defaults_check.pack(side='left', padx=5)
        
        ttk.Label(advanced_frame, 
                 text="Advanced: Include all default values in mod file. Use only if you need to prevent other mods from changing specific values.",
                 font=('Arial', 8, 'italic')).pack(side='left', padx=5)

    def setup_main_content(self):
        container = ttk.Frame(self.window)
        container.pack(fill='both', expand=True, padx=5, pady=5)
        
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        
        main_frame = ttk.Frame(canvas)
        main_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=main_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill='both', expand=True)

        self.create_section_tabs(notebook)

    def create_section_tabs(self, notebook):
        for section in self.config_handler.default_config:
            if section not in ['MovementParams', 'Aiming']:
                frame = ttk.Frame(notebook)
                notebook.add(frame, text=section)
                self.config_interface.setup_section_frame(frame, section)

        if 'MovementParams' in self.config_handler.default_config:
            frame = ttk.Frame(notebook)
            notebook.add(frame, text='MovementParams')
            self.config_interface.setup_movement_frame(frame)
        
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Aiming")
        self.config_interface.setup_aiming_section(frame)

    def load_presets(self):
        if not os.path.exists('Presets'):
            return
        presets = [f.replace('.ini', '') for f in os.listdir('Presets') if f.endswith('.ini')]
        self.preset_combo['values'] = presets

    def load_default(self):
        self.config_interface.sync_sensitivity.set(False)
        self.force_defaults.set(False)
        self.config_interface.update_entries(self.config_handler.default_config)

    def load_xy_fix(self):
        self.config_interface.update_entries(self.config_handler.xy_fix_config)

    def load_v3fish(self):
        self.config_interface.update_entries(self.config_handler.v3fish_config)

    def load_custom_preset(self):
        selected = self.preset_var.get()
        if not selected:
            return
        config = self.config_handler.load_ini_file(os.path.join('Presets', f'{selected}.ini'))
        self.config_interface.update_entries(config)

    def open_presets_folder(self):
        presets_path = os.path.abspath('Presets')
        if not os.path.exists(presets_path):
            os.makedirs(presets_path)
        os.startfile(presets_path)

    def new_preset(self):
        if self.config_interface.has_invalid_entries():
            messagebox.showerror("Error", "Please verify all values are correct!")
            return
            
        if not self.config_interface.has_changes():
            messagebox.showwarning("Warning", "Make changes before saving a preset!")
            return

        dialog = PresetDialog(self.window)
        self.window.wait_window(dialog)
        name = dialog.result
        
        if not name:
            return
            
        config = self.config_interface.get_current_config()
            
        if not os.path.exists('Presets'):
            os.makedirs('Presets')
            
        self.config_handler.save_ini_file(config, f'Presets/{name}.ini')
        self.load_presets()
        self.preset_var.set(name)
        messagebox.showinfo("Success", "Preset saved successfully!")

    def save_preset(self):
        if not self.preset_var.get():
            self.new_preset()
            return
            
        if self.config_interface.has_invalid_entries():
            messagebox.showerror("Error", "Please verify all values are correct!")
            return
            
        if not self.config_interface.has_changes():
            messagebox.showwarning("Warning", "Make changes before saving a preset!")
            return

        if not messagebox.askyesno("Confirm Overwrite", f"Do you want to overwrite the preset '{self.preset_var.get()}'?"):
            return
            
        config = self.config_interface.get_current_config()
        self.config_handler.save_ini_file(config, f'Presets/{self.preset_var.get()}.ini')
        messagebox.showinfo("Success", "Preset saved successfully!")

    def create_mod(self):
        if self.config_interface.has_invalid_entries():
            messagebox.showerror("Error", "Please verify all values are correct!")
            return

        if not self.config_interface.has_changes() and not self.force_defaults.get():
            messagebox.showwarning("Warning", "Make changes before creating a mod!")
            return

        mods_check = self.config_interface.validate_mods_directory()
        if not mods_check:
            return

        if self.force_defaults.get():
            if not messagebox.askyesno("Confirm Force Defaults", 
                                     "Force Default Values is enabled. This will include ALL values in the mod file, " +
                                     "including unchanged ones. This is an advanced option that should only be used " +
                                     "if you need to prevent other mods from changing specific values.\n\n" +
                                     "Are you sure you want to continue?"):
                return

        config = self.config_interface.get_current_config(include_defaults=self.force_defaults.get())
        try:
            is_local, mod_path = mods_check
            self.mod_creator.create_mod(config, mod_path)
            messagebox.showinfo("Success", "Mod created successfully!" + 
                              ("\nThe mod has been created in the current folder." if is_local else ""))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create mod: {str(e)}")

    def run(self):
        self.window.mainloop()