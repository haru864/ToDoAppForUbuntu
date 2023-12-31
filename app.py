from typing import Any
import os
import eel
import json
import pygame
import tkinter
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox
import sqlite3
import pandas
from sklearn import linear_model


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
def showRegisteredTaskType() -> None:
    query: str = "SELECT DISTINCT task_type FROM task_info ORDER BY task_type"
    query_result: list[Any] = None
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = dict_factory
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(query)
        query_result = cursor.fetchall()
    task_type_list: list[str] = []
    for elem in query_result:
        task_type_list.append(elem["task_type"])
    messagebox.showinfo(title="登録済みタスク種別", message="\n".join(task_type_list))
    return None


@eel.expose
def clearCompletedTaskInfo() -> None:
    sql: str = "DELETE FROM task_info WHERE is_completed = 1"
    with sqlite3.connect(DB_PATH) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    return None


@eel.expose
def deleteFromTaskInfo() -> None:
    task_type = simpledialog.askstring(
        "入力ボックス",
        "タスク種別を入力してください。",
    )
    sql: str = "DELETE FROM task_info WHERE task_type = ?"
    with sqlite3.connect(DB_PATH) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(sql, (task_type,))
        conn.commit()
    return None


@eel.expose
def getRegisteredTask() -> str | None:
    sql: str = "SELECT * FROM task_info WHERE is_completed = 0 ORDER BY task_name"
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
def advanceTaskTime(task_id: int) -> None:
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
def changeTaskTime(task_id: int, new_task_time: int) -> None:
    update: str = "UPDATE task_info SET remaining_time_seconds = ? WHERE id = ?"
    with sqlite3.connect(DB_PATH) as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(update, (new_task_time, task_id))
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


@eel.expose
def receiveNewTaskTime() -> int | None:
    top = tkinter.Toplevel()
    top.withdraw()
    while new_task_time_str := simpledialog.askstring(
        "作業時間変更", "新しい作業時間を入力してください", parent=top
    ):
        try:
            if new_task_time_str is None:
                top.destroy()
                return None
            new_task_time: int = int(new_task_time_str)
            return new_task_time
        except Exception:
            messagebox.showerror("エラー", "作業時間は整数(秒単位)で指定して下さい。")
    top.destroy()
    return None


@eel.expose
def predictTaskTime(
    task_type: str, difficulty_level: int, estimated_time_seconds: int
) -> int | None:
    query: str = "SELECT * FROM task_info WHERE is_completed = 1"
    with sqlite3.connect(DB_PATH) as conn:
        df = pandas.read_sql_query(query, conn)
    if df.empty:
        return None

    task_type_set: set[str] = set(df["task_type"].tolist())
    task_type_mapping: dict[str, int] = {}
    for num, curr_task_type in enumerate(task_type_set):
        task_type_mapping[curr_task_type] = num

    filtered_df = df[df["task_type"] == task_type]
    if filtered_df.empty:
        return None
    df_preprocessed: pandas.DataFrame = filtered_df.copy(deep=True)
    df_preprocessed["task_type"] = df_preprocessed["task_type"].map(task_type_mapping)

    reg = linear_model.LinearRegression()
    x = df_preprocessed[["task_type", "difficulty_level", "estimated_time_seconds"]]
    y = df_preprocessed["total_elapsed_time_seconds"]
    reg.fit(x, y)

    input_df = pandas.DataFrame(
        data=[[task_type_mapping[task_type], difficulty_level, estimated_time_seconds]],
        columns=["task_type", "difficulty_level", "estimated_time_seconds"],
    )
    y_pred = reg.predict(input_df)
    return y_pred[0]


root = tkinter.Tk()
root.withdraw()
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
