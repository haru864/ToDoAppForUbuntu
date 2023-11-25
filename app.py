from typing import Any
import os
import eel
import json
import pygame
import tkinter
from tkinter import filedialog
from tkinter import messagebox

SETTING_FILE_RELATIVE_PATH: str = "setting/setting.json"
SOUND_FILE_PATH: str = "sound/bark.ogg"
SUPPORTED_SOUND_FILE_FORMATS: list[str] = [".ogg", ".mp3"]

with open("setting/setting.json", "r") as setting_file:
    setting_data: dict[str, Any] = json.load(setting_file)
    window_width: int = setting_data["width"]
    window_height: int = setting_data["height"]
    port: int = setting_data["port"]

eel.init("web", allowed_extensions=[".js", ".html"])


@eel.expose
def selectSound() -> None:
    global SOUND_FILE_PATH
    root = tkinter.Tk()
    root.withdraw()
    while file_path := filedialog.askopenfilename():
        _, file_extension = os.path.splitext(file_path)
        if file_extension in SUPPORTED_SOUND_FILE_FORMATS:
            SOUND_FILE_PATH = file_path
            break
        messagebox.showerror("エラー", "選択可能なファイルは.oogまたは.mp3です。")
    return None


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
