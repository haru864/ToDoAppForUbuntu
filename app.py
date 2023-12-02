from typing import Any
import os
import eel
import json
import pygame
import tkinter
from tkinter import filedialog
from tkinter import messagebox
import sqlite3


DB_PATH: str = "db/todo.db"
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


@eel.expose
def registerTask(
    task_name: str,
    task_type: str,
    difficulty_level: int,
    is_completed: int,
    estimated_time_seconds: int,
    remaining_time_seconds: int,
    total_elapsed_time_seconds: int,
) -> int | None:
    data: dict[str, Any] = {
        "task_name": task_name,
        "task_type": task_type,
        "difficulty_level": difficulty_level,
        "is_completed": is_completed,
        "estimated_time_seconds": estimated_time_seconds,
        "remaining_time_seconds": remaining_time_seconds,
        "total_elapsed_time_seconds": total_elapsed_time_seconds,
    }
    with sqlite3.connect(DB_PATH) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        sql: str = "INSERT INTO task_info (task_name, task_type, difficulty_level, is_completed, estimated_time_seconds, remaining_time_seconds, total_elapsed_time_seconds) VALUES (:task_name, :task_type, :difficulty_level, :is_completed, :estimated_time_seconds, :remaining_time_seconds, :total_elapsed_time_seconds)"
        cursor.execute(sql, data)
        conn.commit()
        inserted_id: int | None = cursor.lastrowid
    return inserted_id


@eel.expose
def getRegisteredTask() -> str:
    sql: str = "SELECT * FROM task_info WHERE is_completed = 0"
    query_result: list[Any] = None
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = dict_factory
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(sql)
        query_result = cursor.fetchall()
    return json.dumps(query_result)


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


eel.start("index.html", size=(window_width, window_height), port=port)
