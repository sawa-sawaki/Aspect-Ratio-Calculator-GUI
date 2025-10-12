import os
import json
import locale
import difflib

from settings_manager import SettingsManager


class LocalizationManager:

    def __init__(self, lang_folder: str = "language", default_code: str = "en"):
        self.lang_folder = lang_folder
        self.default_code = default_code
        self.available_codes = self._get_available_language_codes()
        self.loaded_data = {}
        self.current_code = self._get_initial_language_code()
        self.current_strings = self._load_language_data(self.current_code)

    def _get_available_language_codes(self) -> set:
        codes = set()
        if not os.path.exists(self.lang_folder):
            print(f"警告: 言語フォルダ '{self.lang_folder}' が見つかりません。")
            return codes

        for filename in os.listdir(self.lang_folder):
            if filename.endswith(".json"):
                lang_code = filename[:-5].lower()
                codes.add(lang_code)

        return codes

    def _load_language_data(self, lang_code: str) -> dict:
        if lang_code in self.loaded_data:
            return self.loaded_data[lang_code]

        if lang_code not in self.available_codes:
            if self.default_code in self.available_codes:
                return self._load_language_data(self.default_code)
            return {}

        data = self._load_language_data_from_file(lang_code)
        self.loaded_data[lang_code] = data
        return data

    def _load_language_data_from_file(self, lang_code: str) -> dict:
        filepath = os.path.join(self.lang_folder, f"{lang_code}.json")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"エラー: 言語ファイル '{filepath}' のロードに失敗しました: {e}")
            return {}

    def _get_os_language_code_candidates(self) -> list:
        candidates = []
        try:
            system_locale, _ = locale.getdefaultlocale()

            if system_locale:
                code_with_country = system_locale.split('.')[0].replace('-', '_').lower()

                if code_with_country:
                    candidates.append(code_with_country)
                    if '_' in code_with_country:
                        lang_code = code_with_country.split('_')[0]
                        candidates.append(lang_code)
                    if len(code_with_country) > 5 and len(code_with_country.split('_')[0]) > 2:
                        candidates.append(code_with_country[:2])

        except Exception:
            pass
        return list(dict.fromkeys([c for c in candidates if c]))

    def _calculate_match_score(self, os_code: str, available_code: str) -> float:
        if not os_code or not available_code:
            return 0.0
        s = difflib.SequenceMatcher(None, os_code, available_code)
        return s.ratio()

    def _find_best_match(self, os_candidates: list, available_codes: set) -> str | None:
        direct_matches = list(set(os_candidates) & available_codes)
        if len(direct_matches) == 1:
            return direct_matches[0]
        if len(direct_matches) > 1:
            return max(direct_matches, key=len)
        best_match = None
        highest_score = -1.0

        for os_code in os_candidates:
            for available_code in available_codes:
                score = self._calculate_match_score(os_code, available_code)

                if score > highest_score:
                    highest_score = score
                    best_match = available_code
                elif score == highest_score and best_match is not None:
                    if len(available_code) > len(best_match):
                        best_match = available_code
        if highest_score <= 0:
            return None

        return best_match

    def _get_initial_language_code(self) -> str:
        settings = SettingsManager.load_settings()
        saved_code = settings.get("language")
        if saved_code and saved_code in self.available_codes:
            return saved_code
        os_candidates = self._get_os_language_code_candidates()
        best_match = self._find_best_match(os_candidates, self.available_codes)

        if best_match:
            return best_match
        if self.default_code in self.available_codes:
            return self.default_code
        if self.available_codes:
            return next(iter(self.available_codes))
        return self.default_code

    def get_available_languages(self) -> dict:
        lang_map = {}
        for code in self.available_codes:
            data = self._load_language_data(code)
            lang_map[data.get("language_name", code)] = code

        return lang_map

    def set_language(self, lang_code: str) -> bool:
        if lang_code in self.available_codes:
            self.current_code = lang_code
            self.current_strings = self._load_language_data(lang_code)
            return True
        return False

    def get_string(self, key: str) -> str:
        default_strings_en = self.loaded_data.get(self.default_code)
        if default_strings_en is None and self.default_code in self.available_codes:
            default_strings_en = self._load_language_data(self.default_code)

        return (self.current_strings.get(key) or
                (default_strings_en or {}).get(key) or
                f"<{key}>")
i18n = LocalizationManager()
