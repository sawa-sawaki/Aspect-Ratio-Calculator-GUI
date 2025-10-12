import tkinter as tk
from tkinter import ttk, filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD
from settings_manager import SettingsManager
from localization_manager import i18n
from gui_logic import GuiLogic


class AspectRatioCalculator(TkinterDnD.Tk):

    def __init__(self):
        super().__init__()

        self.i18n = i18n
        self.entries = {}
        self.input_vars = {}
        self.output_entries = {}
        self.labels = {}
        self.output_label_keys = {}
        self.settings = {}
        self.previous_inputs = {}
        self.settings_window = None

        self._load_settings()

        self.auto_calculate_image_var = tk.BooleanVar(value=self.settings.get("auto_calculate_image", True))

        self.logic = GuiLogic(
            self, self.entries, self.input_vars, self.output_entries,
            self.settings, self.previous_inputs, self.auto_calculate_image_var
        )

        self._set_geometry_and_title()

        self.resizable(True, True)

        self._create_widgets()
        self._setup_context_menu()

        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _set_geometry_and_title(self):
        self.title(self.i18n.get_string("title"))

        geometry_str = self.settings.get("geometry", "450x690+100+100")

        try:
            parts = geometry_str.split('+')
            size_part = parts[0]
            pos_x = int(parts[1])
            pos_y = int(parts[2])

            w, h = map(int, size_part.split('x'))

            screen_w = self.winfo_screenwidth()
            screen_h = self.winfo_screenheight()

            new_x = max(0, min(pos_x, screen_w - w))
            new_y = max(0, min(pos_y, screen_h - h))

            self.geometry(f"{w}x{h}+{new_x}+{new_y}")

        except Exception:
            self.geometry("450x690+100+100")

    def _on_closing(self):
        self.logic._save_settings(self.geometry(), self.i18n.current_code)
        self.destroy()

    def _load_settings(self):
        self.settings = SettingsManager.load_settings()

    def _change_language(self, lang_code: str):
        if self.i18n.set_language(lang_code):
            self.title(self.i18n.get_string("title"))
            self._update_all_texts()
            self.logic._save_settings(self.geometry(), self.i18n.current_code)

    def _update_all_texts(self):
        valid_labels = {key: widget for key, widget in self.labels.items() if widget.winfo_exists()}

        for key, widget in valid_labels.items():
            if isinstance(widget, ttk.Label):
                if key == "language_label":
                    continue

                if key in self.output_label_keys:
                    text_key = self.output_label_keys[key]
                else:
                    text_key = key

                if text_key.endswith("section") or text_key.endswith("file_path"):
                    suffix = ""
                else:
                    suffix = ":"

                widget.config(text=self.i18n.get_string(text_key) + suffix)

            elif isinstance(widget, ttk.Button):
                button_key = key.replace("_original", "").replace("_target", "")
                widget.config(text=self.i18n.get_string(button_key))

        lang_choices = self.i18n.get_available_languages()
        current_name = next((name for name, code in lang_choices.items() if code == self.i18n.current_code), self.i18n.default_code)
        self.lang_var.set(current_name)

    def _setup_context_menu(self):
        self.context_menu = tk.Menu(self, tearoff=0)

        def do_copy(widget):
            try:
                if widget.selection_present():
                    widget.event_generate('<<Copy>>')
                else:
                    self.clipboard_clear()
                    content = widget.get()
                    self.clipboard_append(content)
            except tk.TclError:
                pass

        def do_paste(widget):
            try:
                if str(widget.cget('state')) == 'normal':
                    widget.event_generate('<<Paste>>')
            except tk.TclError:
                pass

        def show_context_menu(event):
            widget = self.focus_get()
            if not isinstance(widget, (ttk.Entry, tk.Entry)):
                widget = event.widget

            if not isinstance(widget, (ttk.Entry, tk.Entry)):
                return

            self.context_menu.delete(0, tk.END)
            self.context_menu.add_command(label=self.i18n.get_string("copy"),
                                          command=lambda w=widget: do_copy(w))

            if str(widget.cget('state')) == 'normal':
                self.context_menu.add_command(label=self.i18n.get_string("paste"),
                                              command=lambda w=widget: do_paste(w))

            if self.context_menu.index(tk.END) is not None:
                self.context_menu.tk_popup(event.x_root, event.y_root)

        self.bind_class("Entry", "<Button-3>", show_context_menu)
        self.bind_class("TEntry", "<Button-3>", show_context_menu)

    def _on_settings_window_configure(self, event):
        if self.settings_window and self.settings_window.winfo_exists():
            try:
                geometry_str = self.settings_window.winfo_geometry()
                self.settings["settings_window_geometry"] = geometry_str
            except tk.TclError:
                pass

    def _on_settings_window_close(self):
        self._on_settings_window_configure(None)
        SettingsManager.save_settings(self.settings)
        if self.settings_window and self.settings_window.winfo_exists():
            self.settings_window.grab_release()
            self.settings_window.destroy()
            self.settings_window = None

    def _create_settings_window(self):
        if self.settings_window and self.settings_window.winfo_exists():
            self.settings_window.lift()
            return

        self.settings_window = tk.Toplevel(self)
        self.settings_window.title(self.i18n.get_string("settings"))
        self.settings_window.transient(self)
        self.settings_window.grab_set()
        saved_geometry = self.settings.get("settings_window_geometry")
        geometry_applied = False
        if saved_geometry:
            try:
                self.settings_window.geometry(saved_geometry)
                self.settings_window.update_idletasks()
                geometry_applied = True
            except tk.TclError:
                pass
        self.update_idletasks()
        main_w = self.winfo_width()
        main_h = self.winfo_height()
        main_x = self.winfo_x()
        main_y = self.winfo_y()

        self.settings_window.update_idletasks()
        if not geometry_applied:
            win_w = 300
            win_h = 150
        else:
            win_w = self.settings_window.winfo_width()
            win_h = self.settings_window.winfo_height()

        pos_x = main_x + (main_w // 2) - (win_w // 2)
        pos_y = main_y + (main_h // 2) - (win_h // 2)

        self.settings_window.geometry(f"{win_w}x{win_h}+{pos_x}+{pos_y}")
        self.settings_window.columnconfigure(0, weight=1)
        self.settings_window.columnconfigure(2, weight=1)
        frame = ttk.Frame(self.settings_window, padding="10")
        frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        auto_calc_label = ttk.Label(frame, text=self.i18n.get_string("auto_calc_image_dim") + ":")
        auto_calc_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        auto_calc_check = ttk.Checkbutton(frame,
                                          text=self.i18n.get_string("on_off"),
                                          variable=self.auto_calculate_image_var)
        auto_calc_check.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

        close_button = ttk.Button(frame, text=self.i18n.get_string("close"), command=self._on_settings_window_close)
        close_button.grid(row=2, column=0, columnspan=2, pady=10)
        self.settings_window.bind("<Configure>", self._on_settings_window_configure)
        self.settings_window.protocol("WM_DELETE_WINDOW", self._on_settings_window_close)

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=0)
        main_frame.columnconfigure(1, weight=0)
        main_frame.columnconfigure(2, weight=1)
        config_lang_frame = ttk.Frame(main_frame)
        config_lang_frame.grid(row=0, column=0, columnspan=3, sticky=tk.E, padx=5, pady=2)

        settings_button = ttk.Button(config_lang_frame, text=self.i18n.get_string("settings_button"),
                                     command=self._create_settings_window)
        self.labels["settings_button"] = settings_button
        settings_button.grid(row=0, column=0, sticky=tk.W, padx=(0, 5))

        lang_label = ttk.Label(config_lang_frame, text="language:")
        lang_label.grid(row=0, column=1, sticky=tk.W, padx=(0, 5))
        self.labels["language_label"] = lang_label

        lang_choices = self.i18n.get_available_languages()
        lang_names = list(lang_choices.keys())

        current_name = next((name for name, code in lang_choices.items() if code == self.i18n.current_code), self.i18n.default_code)

        self.lang_var = tk.StringVar(self)
        self.lang_var.set(current_name)

        lang_menu = ttk.OptionMenu(config_lang_frame, self.lang_var, current_name, *lang_names,
                                   command=lambda choice: self._change_language(lang_choices[choice]))
        lang_menu.config(width=8)
        lang_menu.grid(row=0, column=2, sticky=tk.E)
        row_num = 1
        label = ttk.Label(main_frame, text=self.i18n.get_string('image_section'), font=('Arial', 10, 'bold'))
        label.grid(row=row_num, column=0, columnspan=3, pady=(0, 5), sticky=tk.W)
        self.labels["image_section"] = label
        row_num += 1
        label = ttk.Label(main_frame, text=self.i18n.get_string("file_path") + ":")
        label.grid(row=row_num, column=0, sticky=tk.W, padx=5, pady=2)
        self.labels["file_path"] = label
        button = ttk.Button(main_frame, text=self.i18n.get_string("browse"), command=self._open_file_dialog)
        button.grid(row=row_num, column=1, sticky=tk.W, padx=5)
        self.labels["browse"] = button

        row_num += 1
        image_path_var = tk.StringVar(self)
        self.input_vars["image_path"] = image_path_var

        image_path_entry = ttk.Entry(main_frame, width=40, textvariable=image_path_var)
        image_path_entry.grid(row=row_num, column=0, columnspan=3, sticky=(tk.W, tk.E), padx=5, pady=2)
        self.entries["image_path"] = image_path_entry

        image_path_entry.drop_target_register(DND_FILES)
        image_path_entry.dnd_bind('<<Drop>>', self._handle_drop)

        row_num += 1
        button = ttk.Button(main_frame, text=self.i18n.get_string("calculate_image"), command=self.logic.calculate_image_dimensions)
        button.grid(row=row_num, column=0, columnspan=3, pady=(5, 5), sticky=(tk.W, tk.E))
        self.labels["calculate_image"] = button
        row_num += 1
        label = ttk.Label(main_frame, text=self.i18n.get_string('original_section'), font=('Arial', 10, 'bold'))
        label.grid(row=row_num, column=0, columnspan=3, pady=(10, 5), sticky=tk.W)
        self.labels["original_section"] = label

        row_num += 1
        self._add_input_field(main_frame, "width_original", row_num, "original_w", span=2)
        row_num += 1
        self._add_input_field(main_frame, "height_original", row_num, "original_h", span=2)
        orig_btn_frame = ttk.Frame(main_frame)
        orig_btn_frame.grid(row=row_num + 1, column=0, columnspan=3, sticky=tk.W + tk.E, pady=(0, 10))
        orig_btn_frame.columnconfigure(0, weight=1)
        orig_btn_frame.columnconfigure(1, weight=1)

        orig_clear_button = ttk.Button(orig_btn_frame, text=self.i18n.get_string("clear_button"),
                                       command=lambda: self.logic.clear_inputs(["original_w", "original_h"], "original"))
        orig_clear_button.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=2)
        self.labels["clear_button_original"] = orig_clear_button

        orig_restore_button = ttk.Button(orig_btn_frame, text=self.i18n.get_string("restore_button"),
                                         command=lambda: self.logic.restore_inputs(["original_w", "original_h"], "original"))
        orig_restore_button.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=2)
        self.labels["restore_button_original"] = orig_restore_button
        row_num += 2
        label = ttk.Label(main_frame, text=self.i18n.get_string('target_section'), font=('Arial', 10, 'bold'))
        label.grid(row=row_num, column=0, columnspan=3, pady=(0, 5), sticky=tk.W)
        self.labels["target_section"] = label

        row_num += 1
        label = ttk.Label(main_frame, text=self.i18n.get_string("aspect_ratio_target") + ":")
        label.grid(row=row_num, column=0, sticky=tk.W, padx=5, pady=2)
        self.labels["aspect_ratio_target"] = label

        ratio_frame = ttk.Frame(main_frame)
        ratio_frame.grid(row=row_num, column=1, columnspan=2, sticky=tk.W, padx=5, pady=2)

        entry_w = self._add_ratio_input(ratio_frame, "target_ratio_w", 0, 0, 7)
        self.entries["target_ratio_w"] = entry_w

        ttk.Label(ratio_frame, text=":").grid(row=0, column=1, sticky=tk.W, padx=0)

        entry_h = self._add_ratio_input(ratio_frame, "target_ratio_h", 0, 2, 7)
        self.entries["target_ratio_h"] = entry_h

        row_num += 1
        self._add_input_field(main_frame, "width_target", row_num, "target_w", span=2)
        row_num += 1
        self._add_input_field(main_frame, "height_target", row_num, "target_h", span=2)
        target_btn_frame = ttk.Frame(main_frame)
        target_btn_frame.grid(row=row_num + 1, column=0, columnspan=3, sticky=tk.W + tk.E, pady=(10, 5))
        target_btn_frame.columnconfigure(0, weight=1)
        target_btn_frame.columnconfigure(1, weight=1)

        target_clear_button = ttk.Button(target_btn_frame, text=self.i18n.get_string("clear_button"),
                                         command=lambda: self.logic.clear_inputs(["target_ratio_w", "target_ratio_h", "target_w", "target_h"], "target"))
        target_clear_button.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=2)
        self.labels["clear_button_target"] = target_clear_button

        target_restore_button = ttk.Button(target_btn_frame, text=self.i18n.get_string("restore_button"),
                                           command=lambda: self.logic.restore_inputs(["target_ratio_w", "target_ratio_h", "target_w", "target_h"], "target"))
        target_restore_button.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=2)
        self.labels["restore_button_target"] = target_restore_button
        row_num += 2
        button = ttk.Button(main_frame, text=self.i18n.get_string("calculate_main"), command=self.logic.calculate_aspects)
        button.grid(row=row_num, column=0, columnspan=3, pady=(0, 10), sticky=(tk.W, tk.E))
        self.labels["calculate_main"] = button
        row_num += 1
        label = ttk.Label(main_frame, text=self.i18n.get_string('result_section'), font=('Arial', 10, 'bold'))
        label.grid(row=row_num, column=0, columnspan=3, pady=(5, 5), sticky=tk.W)
        self.labels["result_section"] = label

        row_num += 1
        self._add_output_entry(main_frame, "ratio_original", row_num, "original_ratio", span=2)
        row_num += 1
        self._add_output_entry(main_frame, "ratio_final", row_num, "final_ratio", span=2)

        row_num += 1
        ttk.Separator(main_frame, orient='horizontal').grid(row=row_num, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        row_num += 1

        self._add_output_entry(main_frame, "width_original", row_num, "out_original_w", span=2)
        row_num += 1
        self._add_output_entry(main_frame, "height_original", row_num, "out_original_h", span=2)
        row_num += 1
        self._add_output_entry(main_frame, "width_final", row_num, "out_final_w", span=2)
        row_num += 1
        self._add_output_entry(main_frame, "height_final", row_num, "out_final_h", span=2)

        self._load_input_values_after_widgets()
        self._update_all_texts()

    def _load_input_values_after_widgets(self):
        for key, value in self.settings.items():
            if key in self.entries and value is not None and str(value).strip() != "":
                self.logic.update_input_entry(key, str(value))

        self.logic.save_current_inputs(["original_w", "original_h"], "original")
        self.logic.save_current_inputs(["target_ratio_w", "target_ratio_h", "target_w", "target_h"], "target")

    def _add_input_field(self, parent, key_text: str, row: int, key: str, span: int = 1):
        label = ttk.Label(parent, text=self.i18n.get_string(key_text) + ":")
        label.grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
        self.labels[key_text] = label

        var = tk.StringVar(self)
        self.input_vars[key] = var

        entry = ttk.Entry(parent, width=15, justify='right', textvariable=var)
        entry.grid(row=row, column=1, columnspan=span, sticky=(tk.W, tk.E), padx=5, pady=2)
        self.entries[key] = entry

        var.trace_add('write', lambda *args, k=key: self.logic.auto_save_input(k))

        return entry

    def _add_ratio_input(self, parent, key: str, row: int, col: int, width: int):
        var = tk.StringVar(self)
        self.input_vars[key] = var

        entry = ttk.Entry(parent, width=width, justify='right', textvariable=var)
        entry.grid(row=row, column=col, sticky=tk.W, padx=(0, 0))

        var.trace_add('write', lambda *args, k=key: self.logic.auto_save_input(k))

        return entry

    def _add_output_entry(self, parent, key_text: str, row: int, key: str, span: int = 1):
        label = ttk.Label(parent, text=self.i18n.get_string(key_text) + ":")
        label.grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)

        self.labels[key] = label
        self.output_label_keys[key] = key_text

        output_entry = ttk.Entry(parent, width=15, state='readonly', justify='right')
        output_entry.grid(row=row, column=1, columnspan=span, sticky=(tk.W, tk.E), padx=5, pady=2)
        self.output_entries[key] = output_entry

    def _open_file_dialog(self):
        file_types = [("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.webp")]
        file_path = filedialog.askopenfilename(
            title=self.i18n.get_string("title"),
            filetypes=file_types
        )
        if file_path:
            self.logic.update_input_entry("image_path", file_path)
            if self.auto_calculate_image_var.get():
                self.logic.calculate_image_dimensions()

    def _handle_drop(self, event):
        dropped_path_raw = event.data.strip()

        if dropped_path_raw.startswith('{') and dropped_path_raw.endswith('}'):
            file_path = dropped_path_raw[1:-1]
        elif ' ' in dropped_path_raw:
            files = dropped_path_raw.split(' ')
            file_path = files[0].strip('{}')
        else:
            file_path = dropped_path_raw

        self.logic.update_input_entry("image_path", file_path)

        if self.auto_calculate_image_var.get():
            self.logic.calculate_image_dimensions()
