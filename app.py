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
SUPPORTED_SOUND_FILE_FORMATS: list[str] = [".ogg", ".mp3"]

with open("setting/setting.json", "r") as setting_file:
    setting_data: dict[str, Any] = json.load(setting_file)

eel.init("web", allowed_extensions=[".js", ".html"])


@eel.expose
def selectSound() -> None:
    root = tkinter.Tk()
    root.withdraw()
    while file_path := filedialog.askopenfilename():
        _, file_extension = os.path.splitext(file_path)
        if file_extension not in SUPPORTED_SOUND_FILE_FORMATS:
            messagebox.showerror("エラー", "選択可能なファイルは.oogまたは.mp3です。")
            continue
        with open("setting/setting.json", "w") as f:
            setting_data["sound"] = file_path
            f.write(json.dumps(setting_data))
        break
    return None


@eel.expose
def startSound() -> None:
    pygame.init()
    pygame.mixer.music.load(setting_data["sound"])
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


@eel.expose
def setCompleteFlagOnTask(task_id: int) -> None:
    sql: str = "UPDATE task_info SET is_completed = 1 WHERE id = ?"
    with sqlite3.connect(DB_PATH) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(sql, (task_id,))
    return None


@eel.expose
def deleteRegisteredTask(task_id: int) -> None:
    sql: str = "DELETE FROM task_info WHERE id = ?"
    with sqlite3.connect(DB_PATH) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(sql, (task_id,))
    return None


@eel.expose
def updateTaskTime(task_id: int) -> None:
    query: str = "SELECT remaining_time_seconds, total_elapsed_time_seconds FROM task_info WHERE id = ?"
    update: str = "UPDATE task_info SET remaining_time_seconds = ?, total_elapsed_time_seconds = ? WHERE id = ?"
    with sqlite3.connect(DB_PATH) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(query, (task_id,))
        current_remaining_time, current_total_elapsed_time = cursor.fetchone()
        updated_remaining_time: int = current_remaining_time - 1
        updated_total_elapsed_time: int = current_total_elapsed_time + 1
        cursor.execute(
            update, (updated_remaining_time, updated_total_elapsed_time, task_id)
        )
    return None


@eel.expose
def getRemainingTime(task_id: int) -> int:
    query: str = "SELECT remaining_time_seconds FROM task_info WHERE id = ?"
    with sqlite3.connect(DB_PATH) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(query, (task_id,))
        current_remaining_time: int = cursor.fetchone()[0]
    return current_remaining_time


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


root = tkinter.Tk()
monitor_height: int = root.winfo_screenheight()
monitor_width: int = root.winfo_screenwidth()
left: int = (monitor_width - setting_data["width"]) // 2
top: int = (monitor_height - setting_data["height"]) // 2

eel.start(
    "index.html",
    size=(setting_data["width"], setting_data["height"]),
    port=setting_data["port"],
    position=(left, top),
)
