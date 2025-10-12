import json
import os

SETTINGS_FILE = 'user/settings.json'


class SettingsManager:

    @staticmethod
    def _ensure_directory_exists(file_path: str):
        dir_name = os.path.dirname(file_path)

        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

    @classmethod
    def load_settings(cls, settings_file_path: str = None) -> dict:
        file_path = settings_file_path or SETTINGS_FILE

        cls._ensure_directory_exists(file_path)

        if not os.path.exists(file_path):
            return {}

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            print(f"警告: 設定ファイルのロードに失敗しました ({file_path}): {e}")
            return {}

    @classmethod
    def save_settings(cls, settings: dict, settings_file_path: str = None):
        file_path = settings_file_path or SETTINGS_FILE

        cls._ensure_directory_exists(file_path)

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"エラー: 設定ファイルの保存に失敗しました ({file_path}): {e}")
