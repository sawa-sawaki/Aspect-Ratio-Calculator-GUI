import tkinter as tk
from tkinter import messagebox
import os

from aspect_logic import simplify_aspect_ratio, calculate_new_dimensions, get_image_dimensions
from settings_manager import SettingsManager
from localization_manager import i18n


class GuiLogic:

    def __init__(self, master, entries, input_vars, output_entries, settings, previous_inputs, auto_calculate_image_var):
        self.master = master
        self.i18n = i18n
        self.entries = entries
        self.input_vars = input_vars
        self.output_entries = output_entries
        self.settings = settings
        self.previous_inputs = previous_inputs
        self.auto_calculate_image_var = auto_calculate_image_var

    def _save_settings(self, geometry_str, lang_code):
        settings = self.settings

        settings["geometry"] = geometry_str
        settings["language"] = lang_code
        settings["auto_calculate_image"] = self.auto_calculate_image_var.get()

        for key, entry in self.entries.items():
            settings[key] = entry.get()

        SettingsManager.save_settings(settings)

    def _get_float_value(self, key: str) -> float:
        try:
            val = self.entries[key].get()
            return float(val) if val.strip() else None
        except ValueError:
            return None

    def update_input_entry(self, key: str, value: str):
        var = self.input_vars[key]
        var.set(str(value) if value is not None else "")
        entry = self.entries[key]
        if entry.winfo_exists() and entry.focus_get() == entry:
            entry.icursor(tk.END)

    def update_output_entry(self, key: str, value: float):
        entry = self.output_entries[key]
        entry.config(state='normal')
        entry.delete(0, tk.END)

        if isinstance(value, (int, float)):
            if isinstance(value, float) and value != int(value):
                entry.insert(0, f"{value:.2f}")
            else:
                entry.insert(0, str(int(value)))
        else:
            entry.insert(0, str(value) if value is not None else "")

        entry.config(state='readonly')

    def auto_save_input(self, key: str):
        value = self.entries[key].get()
        if key in ["original_w", "original_h"]:
            self.previous_inputs[f"original_{key}"] = value
        elif key in ["target_ratio_w", "target_ratio_h", "target_w", "target_h"]:
            self.previous_inputs[f"target_{key}"] = value

    def save_current_inputs(self, keys: list[str], prefix: str):
        for key in keys:
            if key in self.entries:
                self.previous_inputs[f"{prefix}_{key}"] = self.entries[key].get()

    def clear_inputs(self, keys: list[str], prefix: str):
        self.save_current_inputs(keys, prefix)
        for key in keys:
            if key in self.entries:
                self.update_input_entry(key, "")

    def restore_inputs(self, keys: list[str], prefix: str):
        restored_count = 0
        for key in keys:
            prev_key = f"{prefix}_{key}"
            if prev_key in self.previous_inputs:
                self.update_input_entry(key, self.previous_inputs[prev_key])
                restored_count += 1
        if restored_count == 0:
            self.settings = SettingsManager.load_settings()
            for key in keys:
                if key in self.entries:
                    value = self.settings.get(key, "")
                    self.update_input_entry(key, value)
        self.save_current_inputs(keys, prefix)

    def calculate_image_dimensions(self):
        image_path = self.entries["image_path"].get()
        if not image_path or not os.path.exists(image_path):
            messagebox.showerror(self.i18n.get_string("title"), self.i18n.get_string("error_file_path"))
            return

        width, height = get_image_dimensions(image_path)

        if width is not None and height is not None:
            self.update_input_entry("original_w", width)
            self.update_input_entry("original_h", height)
        else:
            messagebox.showerror(self.i18n.get_string("title"), self.i18n.get_string("error_image_load"))

    def calculate_aspects(self):
        orig_w = self._get_float_value("original_w")
        orig_h = self._get_float_value("original_h")

        target_ratio_w_val = self._get_float_value("target_ratio_w")
        target_ratio_h_val = self._get_float_value("target_ratio_h")

        target_w = self._get_float_value("target_w")
        target_h = self._get_float_value("target_h")

        original_ratio = simplify_aspect_ratio(orig_w, orig_h)
        final_ratio = original_ratio
        final_w = orig_w
        final_h = orig_h

        target_ratio_str = None
        if target_ratio_w_val is not None and target_ratio_h_val is not None and target_ratio_w_val > 0 and target_ratio_h_val > 0:
            r_w_str = str(int(target_ratio_w_val)) if target_ratio_w_val == int(target_ratio_w_val) else str(target_ratio_w_val)
            r_h_str = str(int(target_ratio_h_val)) if target_ratio_h_val == int(target_ratio_h_val) else str(target_ratio_h_val)
            target_ratio_str = f"{r_w_str}:{r_h_str}"
            final_ratio = target_ratio_str

        if target_ratio_str:
            if target_w is not None and target_h is not None:
                if target_w >= target_h:
                    calculated_w, calculated_h = calculate_new_dimensions(target_ratio_str, target_w, None)
                else:
                    calculated_w, calculated_h = calculate_new_dimensions(target_ratio_str, None, target_h)
                final_w = calculated_w
                final_h = calculated_h

            elif target_w is not None:
                calculated_w, calculated_h = calculate_new_dimensions(target_ratio_str, target_w, None)
                final_w = calculated_w
                final_h = calculated_h

            elif target_h is not None:
                calculated_w, calculated_h = calculate_new_dimensions(target_ratio_str, None, target_h)
                final_w = calculated_w
                final_h = calculated_h

            elif orig_w is not None and orig_h is not None:
                calculated_w, calculated_h = calculate_new_dimensions(target_ratio_str, None, None, orig_w, orig_h)
                final_w = calculated_w
                final_h = calculated_h

            elif orig_w is None and orig_h is None:
                pass

        else:
            final_ratio = original_ratio

            if original_ratio != "N/A" and (target_h is not None or target_w is not None):
                if target_w is not None and target_h is not None:
                    if target_w >= target_h:
                        calculated_w, calculated_h = calculate_new_dimensions(original_ratio, target_w, None)
                    else:
                        calculated_w, calculated_h = calculate_new_dimensions(original_ratio, None, target_h)
                else:
                    calculated_w, calculated_h = calculate_new_dimensions(original_ratio, target_w, target_h)

                final_w = calculated_w
                final_h = calculated_h

            elif original_ratio != "N/A":
                final_w = orig_w
                final_h = orig_h

        self.update_output_entry("original_ratio", original_ratio)
        self.update_output_entry("out_original_w", orig_w)
        self.update_output_entry("out_original_h", orig_h)

        self.update_output_entry("final_ratio", final_ratio)
        self.update_output_entry("out_final_w", final_w)
        self.update_output_entry("out_final_h", final_h)
