from typing import Any
import eel
import json
import pygame

SETTING_FILE_RELATIVE_PATH: str = "setting/setting.json"
SOUND_FILE_PATH: str = "sound/bark.ogg"

with open("setting/setting.json", "r") as setting_file:
    setting_data: dict[str, Any] = json.load(setting_file)
    window_width: int = setting_data["width"]
    window_height: int = setting_data["height"]
    port: int = setting_data["port"]

eel.init("web", allowed_extensions=[".js", ".html"])


@eel.expose
def startSound() -> None:
    pygame.init()
    pygame.mixer.music.load(SOUND_FILE_PATH)
    pygame.mixer.music.play(-1)
    return None


@eel.expose
def stopSound() -> None:
    pygame.mixer.music.stop()
    return None


eel.start("index.html", size=(window_width, window_height), port=port)
