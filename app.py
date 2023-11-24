from typing import Any
import eel
import json

SETTING_FILE_RELATIVE_PATH: str = "setting/setting.json"

with open("setting/setting.json", "r") as setting_file:
    setting_data: dict[str, Any] = json.load(setting_file)
    window_width: int = setting_data["width"]
    window_height: int = setting_data["height"]
    port: int = setting_data["port"]

eel.init("web", allowed_extensions=[".js", ".html"])
eel.start("index.html", size=(window_width, window_height), port=port)
