from tkinter import *
from typing import Final
from Task import Task
from TasksJson import TasksJson
from MainWindow import MainWindow
from ConfJson import ConfJson
from Setting import Setting

MAIN_WINDOW_TITLE: Final[str] = "ToDoApp"
MAIN_WINDOW_WIDTH: Final[str] = "800"
MAIN_WINDOW_HEIGHT: Final[str] = "600"
MAIN_WINDOW_SIZE: Final[str] = f"{MAIN_WINDOW_WIDTH}x{MAIN_WINDOW_HEIGHT}"


lastPushedTaskMenuButton: Menubutton = None
tasksJson: TasksJson = None


def _on_move(event) -> None:
    global lastPushedTaskMenuButton
    if lastPushedTaskMenuButton is None:
        return
    lastPushedTaskMenuButton.menu.unpost()


def centerWindow(window) -> None:
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window.winfo_width() // 2)
    y = (screen_height // 2) - (window.winfo_height() // 2)
    window.geometry(f"+{x}+{y}")


def main():
    # 設定ファイル読み込み
    confJson = ConfJson()
    Setting.updateSetting(
        newMaxNumOfTasks=confJson.max_num_of_tasks,
        newBeepPeriodSeconds=confJson.beep_period_seconds,
        newDefaultTaskTime=confJson.default_task_time,
        newSoundFile=confJson.sound_file,
    )

    # メインウィンドウを生成
    root = Tk()
    root.title(MAIN_WINDOW_TITLE)
    root.bind("<Configure>", _on_move)
    centerWindow(root)
    mainWIndow = MainWindow(root=root)

    # メインウィンドウを表示
    root.geometry("")
    root.mainloop()


if __name__ == "__main__":
    main()
