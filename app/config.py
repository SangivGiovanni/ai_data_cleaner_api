import os
import tomllib

with open("pyproject.toml", "rb") as f:
    config = tomllib.load(f).get("tool", {}).get("ai_data_cleaner_api", {})

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
