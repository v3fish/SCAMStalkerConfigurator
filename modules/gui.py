# modules/gui.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sys
import os
from .config import ConfigHandler
from .mod import ModCreator
from .config_interface import ConfigInterface
from .localization.language_manager import LanguageManager, get_current_localization, t, error, success, warning, confirm
# Removed updater import to eliminate network functionality and potential AV false positives
from . import VERSION

class PresetDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.result = None
        
        # Get current localization
        loc = get_current_localization()
        
        # Configure window
        self.title(loc.get_title("new_preset"))
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
        ttk.Label(self, text=loc.get_label("enter_preset_name")).pack(padx=20, pady=(20,5))
        
        self.entry = ttk.Entry(self, width=40)
        self.entry.pack(padx=20, pady=5)
        
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text=loc.get_button("ok"), command=self.ok).pack(side='left', padx=5)
        ttk.Button(button_frame, text=loc.get_button("cancel"), command=self.cancel).pack(side='left', padx=5)
        
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
        self.window.geometry("1000x965")

        if getattr(sys, 'frozen', False):
            # For reading bundled resources (INI files, icons, etc.)
            self.base_path = sys._MEIPASS
            # For writing user data (preferences, etc.) - use exe directory
            self.user_data_path = os.path.dirname(sys.executable)
        else:
            # For development, use the same path for both
            self.base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
            self.user_data_path = self.base_path

        # Set window icon
        try:
            icon_path = os.path.join(self.base_path, 'ico', 'icon2.ico')
            if os.path.exists(icon_path):
                self.window.iconbitmap(icon_path)
        except Exception:
            pass  # If icon setting fails, continue without it

        self.config_handler = ConfigHandler(self.base_path, self.user_data_path)
        self.mod_creator = ModCreator(self.base_path)
        self.config_interface = ConfigInterface(self.window, self.config_handler)
        self.language_manager = LanguageManager(self.base_path, self.user_data_path)
        # Removed update_checker initialization
        
        # Set window title after language manager is initialized
        loc = get_current_localization()
        self.window.title(loc.get_app_title(VERSION))
        
        self.force_defaults = tk.BooleanVar(value=False)
        
        # Add window close handler to save current state
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.setup_gui()
        
        # Restore last settings after GUI is set up
        self.restore_last_settings()
        
        # Removed update functionality

    def on_closing(self):
        """Handle window closing event to save current state"""
        try:
            # Save current preset selection if one is selected
            if hasattr(self, 'preset_var') and self.preset_var.get():
                self.config_handler.set_last_selected_preset(self.preset_var.get())
        except Exception:
            # Don't let saving errors prevent application from closing
            pass
        
        # Close the application
        self.window.destroy()

    def setup_gui(self):
        self.setup_credits_frame()
        self.config_interface.setup_game_dir_frame(self.window)
        self.setup_top_frame()
        self.setup_main_content()

    def setup_credits_frame(self):
        credits_frame = ttk.Frame(self.window)
        credits_frame.pack(fill='x', padx=5, pady=5)
        
        # Language button (LEFT SIDE)
        language_btn = ttk.Button(credits_frame, 
                                text=t("language"),
                                command=self.show_language_selection)
        language_btn.pack(side='left', padx=5)
        
        loc = get_current_localization()
        credits_label = ttk.Label(credits_frame, 
                                text=loc.get_credits_text(VERSION),
                                font=('Arial', 8, 'italic bold'))
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
        
        ttk.Label(preset_frame, text=t("custom_presets")).pack(side='left', padx=5)
        self.preset_var = tk.StringVar()
        self.preset_combo = ttk.Combobox(preset_frame, textvariable=self.preset_var, state="readonly")
        self.preset_combo.pack(side='left', padx=5)
        
        # Add trace to automatically save preset selection when changed
        self.preset_var.trace_add('write', self.on_preset_selection_changed)
        
        ttk.Button(preset_frame, text=t("load"), command=self.load_custom_preset).pack(side='left', padx=5)
        ttk.Button(preset_frame, text=t("save"), command=self.save_preset).pack(side='left', padx=5)
        ttk.Button(preset_frame, text=t("new_preset"), command=self.new_preset).pack(side='left', padx=5)
        ttk.Button(preset_frame, text=t("open_presets_folder"), command=self.open_presets_folder).pack(side='left', padx=5)
        
        # Create buttons frame for mod-related buttons
        self.mod_buttons_frame = ttk.Frame(preset_frame)
        self.mod_buttons_frame.pack(side='right', padx=5)
        
        # Create mod buttons with initial state
        self.create_mod_btn = ttk.Button(self.mod_buttons_frame, text=t("create_mod"), 
                                       command=self.create_mod, style='Big.TButton')
        self.update_mod_btn = ttk.Button(self.mod_buttons_frame, text=t("update_mod"), 
                                       command=self.create_mod, style='Big.TButton')
        self.remove_mod_btn = ttk.Button(self.mod_buttons_frame, text=t("remove_mod"),
                                       command=self.remove_mod)
        
        # Update button states
        self.config_interface.update_mod_status()
        self.update_mod_buttons()
        
        # Add trace to game_dir for button updates
        self.config_interface.game_dir.trace_add('write', lambda *args: self.update_mod_buttons())
        
        style = ttk.Style()
        style.configure('Big.TButton', font=('Arial', 10, 'bold'))
        style.configure('TNotebook.Tab', font=('Arial', 10, 'bold'), padding=[10, 4])

        if os.path.exists('Presets'):
            self.load_presets()

    def update_mod_buttons(self):
        """Update the visibility and state of mod-related buttons"""
        # Remove all buttons first
        self.create_mod_btn.pack_forget()
        self.update_mod_btn.pack_forget()
        self.remove_mod_btn.pack_forget()
        
        # Get fresh mod status
        self.config_interface.update_mod_status()
        
        if self.config_interface.game_dir.get() and self.config_interface.validate_game_directory(self.config_interface.game_dir.get(), show_error=False):
            if self.config_interface.mod_exists:
                # Show Update and Remove buttons
                self.update_mod_btn.pack(side='right', padx=5, ipady=5, ipadx=10)
                self.remove_mod_btn.pack(side='right', padx=5)
            else:
                # Show Create button
                self.create_mod_btn.pack(side='right', padx=5, ipady=5, ipadx=10)
        else:
            # If no game directory, only show Create button
            self.create_mod_btn.pack(side='right', padx=5, ipady=5, ipadx=10)

    def setup_recommended_presets(self, parent):
        recommended_frame = ttk.Frame(parent)
        recommended_frame.pack(side='top', fill='x', pady=10)
        
        buttons_frame = ttk.Frame(recommended_frame)
        buttons_frame.pack(padx=5)
        
        loc = get_current_localization()
        ttk.Button(buttons_frame, text=loc.get_preset("default"), command=self.load_default).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text=loc.get_preset("v3fish_recommended"), command=self.load_v3fish).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text=loc.get_preset("xy_sensitivity_fix"), command=self.load_xy_fix).pack(side='left', padx=5)

    def setup_advanced_options(self, parent):
        advanced_frame = ttk.Frame(parent)
        advanced_frame.pack(side='top', fill='x', padx=5, pady=5)
        
        force_defaults_check = ttk.Checkbutton(advanced_frame, 
                                             text=t("force_default_values"), 
                                             variable=self.force_defaults)
        force_defaults_check.pack(side='left', padx=5)
        
        loc = get_current_localization()
        ttk.Label(advanced_frame, 
                 text=loc.get_label("advanced_force_defaults"),
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

        # Add mouse wheel scrolling support
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_to_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbind_from_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")
        
        # Bind mouse wheel events when mouse enters/leaves the canvas
        canvas.bind('<Enter>', _bind_to_mousewheel)
        canvas.bind('<Leave>', _unbind_from_mousewheel)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill='both', expand=True)

        self.create_section_tabs(notebook)

    def create_section_tabs(self, notebook):
        # Set the notebook reference in config_interface so it can update tab colors
        self.config_interface.set_notebook_reference(notebook)
        
        for section in self.config_handler.default_config:
            if section not in ['MovementParams', 'Aiming']:
                frame = ttk.Frame(notebook)
                notebook.add(frame, text=section)
                self.config_interface.setup_section_frame(frame, section)

        if 'MovementParams' in self.config_handler.default_config:
            frame = ttk.Frame(notebook)
            # Keep MovementParams in English - don't translate
            notebook.add(frame, text="MovementParams")
            self.config_interface.setup_movement_frame(frame)
        
        frame = ttk.Frame(notebook)
        # Keep Aiming in English - don't translate
        notebook.add(frame, text="Aiming")
        self.config_interface.setup_aiming_section(frame)
        
        # Initialize default button states and tab colors
        self.config_interface.update_all_default_button_states()
        self.config_interface.update_tab_colors()

    def load_presets(self):
        if not os.path.exists('Presets'):
            return
        presets = [f.replace('.ini', '') for f in os.listdir('Presets') if f.endswith('.ini')]
        self.preset_combo['values'] = presets
        
        # Always restore last selected preset
        last_preset = self.config_handler.get_last_selected_preset()
        if last_preset and last_preset in presets:
            self.preset_var.set(last_preset)

    def load_default(self):
        self.config_interface.sync_sensitivity.set(False)
        self.force_defaults.set(False)
        self.config_interface.update_entries(self.config_handler.default_config)
        # Clear last settings when loading default (but keep preset selection)
        self.config_handler.set_last_settings({})

    def load_xy_fix(self):
        self.config_interface.update_entries(self.config_handler.xy_fix_config)
        # Clear last settings when loading XY fix (but keep preset selection)
        self.config_handler.set_last_settings({})

    def load_v3fish(self):
        self.config_interface.update_entries(self.config_handler.v3fish_config)
        # Clear last settings when loading v3fish (but keep preset selection)
        self.config_handler.set_last_settings({})

    def load_custom_preset(self):
        selected = self.preset_var.get()
        if not selected:
            return
        config = self.config_handler.load_ini_file(os.path.join('Presets', f'{selected}.ini'))
        self.config_interface.update_entries(config)
        # Save the selected preset (but don't clear settings since user might have customized after preset)
        self.config_handler.set_last_selected_preset(selected)

    def open_presets_folder(self):
        presets_path = os.path.abspath('Presets')
        if not os.path.exists(presets_path):
            os.makedirs(presets_path)
        os.startfile(presets_path)

    def new_preset(self):
        has_invalid, invalid_values = self.config_interface.has_invalid_entries()
        if has_invalid:
            loc = get_current_localization()
            messagebox.showerror(loc.get_title("error"), 
                                loc.get_error("invalid_values_details", details="\n".join(invalid_values)))
            return
            
        if not self.config_interface.has_changes():
            loc = get_current_localization()
            messagebox.showwarning(loc.get_title("warning"), 
                                 loc.get_warning("make_changes_before_saving"))
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
        # Save the newly created preset as the last selected and clear last settings
        self.config_handler.set_last_selected_preset(name)
        self.config_handler.set_last_settings({})
        loc = get_current_localization()
        messagebox.showinfo(loc.get_title("success"), 
                           loc.get_success("preset_saved"))

    def save_preset(self):
        if not self.preset_var.get():
            self.new_preset()
            return
            
        has_invalid, invalid_values = self.config_interface.has_invalid_entries()
        if has_invalid:
            loc = get_current_localization()
            messagebox.showerror(loc.get_title("error"), 
                                loc.get_error("invalid_values_details", details="\n".join(invalid_values)))
            return
            
        if not self.config_interface.has_changes():
            loc = get_current_localization()
            messagebox.showwarning(loc.get_title("warning"), 
                                 loc.get_warning("make_changes_before_saving"))
            return

        loc = get_current_localization()
        if not messagebox.askyesno(loc.get_title("confirm_overwrite"), 
                                 loc.get_confirmation("overwrite_preset", preset=self.preset_var.get())):
            return
            
        config = self.config_interface.get_current_config()
        self.config_handler.save_ini_file(config, f'Presets/{self.preset_var.get()}.ini')
        # Save the current preset as the last selected and clear last settings
        self.config_handler.set_last_selected_preset(self.preset_var.get())
        self.config_handler.set_last_settings({})
        messagebox.showinfo(loc.get_title("success"), 
                           loc.get_success("preset_saved"))

    def restore_last_settings(self):
        """Restore the last saved settings when the app starts"""
        last_settings = self.config_handler.get_last_settings()
        if last_settings:
            # Restore configuration
            if 'config' in last_settings:
                self.config_interface.update_entries(last_settings['config'])
            
            # Restore sync sensitivity state
            if 'sync_sensitivity' in last_settings:
                self.config_interface.sync_sensitivity.set(last_settings['sync_sensitivity'])
            
            # Restore force defaults state
            if 'force_defaults' in last_settings:
                self.force_defaults.set(last_settings['force_defaults'])

    def remove_mod(self):
        """Handle mod removal"""
        loc = get_current_localization()
        if not messagebox.askyesno(loc.get_title("confirm_removal"), 
                                 loc.get_confirmation("remove_mod")):
            return
            
        if self.config_interface.remove_mod():
            # Clear last settings when mod is removed (but keep preset selection)
            self.config_handler.clear_last_settings_only()
            self.update_mod_buttons()
            messagebox.showinfo(loc.get_title("success"), 
                               loc.get_success("mod_removed"))

    def create_mod(self):
        has_invalid, invalid_values = self.config_interface.has_invalid_entries()
        if has_invalid:
            loc = get_current_localization()
            messagebox.showerror(loc.get_title("invalid_values"), 
                                loc.get_error("invalid_values_fix", issues="\n".join(invalid_values)))
            return

        if not self.config_interface.has_changes() and not self.force_defaults.get():
            loc = get_current_localization()
            messagebox.showwarning(loc.get_title("warning"), 
                                 loc.get_warning("make_changes_before_creating"))
            return

        mods_check = self.config_interface.validate_mods_directory()
        if not mods_check:
            return

        if self.force_defaults.get():
            loc = get_current_localization()
            if not messagebox.askyesno(loc.get_title("confirm_force_defaults"), 
                                     loc.get_confirmation("force_defaults_warning")):
                return
                
        config = self.config_interface.get_current_config(include_defaults=self.force_defaults.get())
        if not config:
            return
        
        try:
            is_local, mod_path = mods_check
            self.mod_creator.create_mod(config, mod_path)
            
            # Save current settings after successful mod creation
            full_config = self.config_interface.get_current_config(include_defaults=True)
            if full_config:
                # Include sync sensitivity state and force defaults state
                settings_to_save = {
                    'config': full_config,
                    'sync_sensitivity': self.config_interface.sync_sensitivity.get(),
                    'force_defaults': self.force_defaults.get()
                }
                self.config_handler.set_last_settings(settings_to_save)
            
            # Update buttons after successful creation
            self.config_interface.update_mod_status()
            self.update_mod_buttons()
            
            loc = get_current_localization()
            if self.config_interface.mod_exists and self.config_interface.game_dir.get():
                messagebox.showinfo(loc.get_title("success"), 
                                   loc.get_success("mod_updated"))
            else:
                success_msg = loc.get_success("mod_created")
                if is_local:
                    success_msg += f"\n{loc.get_success('mod_created_local')}"
                messagebox.showinfo(loc.get_title("success"), success_msg)
        except Exception as e:
            loc = get_current_localization()
            messagebox.showerror(loc.get_title("error"), 
                                loc.get_error("failed_to_create_mod", error=str(e)))

    def show_language_selection(self):
        """Show language selection dialog"""
        self.language_manager.show_language_selection_dialog(self.window, self.refresh_ui)
    
    def refresh_ui(self):
        """Refresh all UI text after language change"""
        loc = get_current_localization()
        self.window.title(loc.get_app_title(VERSION))
        
        # Reload configuration with new language-specific INI file
        self.config_handler.load_default_config()
        
        # Clear and recreate the UI
        for widget in self.window.winfo_children():
            widget.destroy()
        
        # Recreate config interface with new config
        self.config_interface = ConfigInterface(self.window, self.config_handler)
        
        self.setup_gui()
        
        # Restore last settings after recreating the UI
        self.restore_last_settings()

    def run(self):
        self.window.mainloop()

    def on_preset_selection_changed(self, *args):
        """Called when the preset selection changes in the dropdown"""
        try:
            selected_preset = self.preset_var.get()
            if selected_preset:
                # Save the newly selected preset
                self.config_handler.set_last_selected_preset(selected_preset)
        except Exception:
            # Don't let saving errors cause issues
            pass