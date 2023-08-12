import tkinter as tk
from tkinter import messagebox
from typing import Optional
from Task import Task
from TasksJson import TasksJson
from Setting import Setting


class AddTaskWindow:
    def __init__(self, master: tk.Tk) -> None:
        self.master = master
        self.window = tk.Toplevel(master)
        self.window.title("Add Task")
        self.placeWindow()
        self.taskName: str = None
        self.leftSeconds: int = None

        # ラベルを生成
        self.taskNameLabel = tk.Label(self.window, text="Task Name:")
        self.taskTimeHeadLineLabel = tk.Label(self.window, text="Time")
        self.taskTimeHoursLabel = tk.Label(self.window, text="hours:")
        self.taskTimeMinutesLabel = tk.Label(self.window, text="minutes:")
        self.taskTimeSecondsLabel = tk.Label(self.window, text="seconds:")
        self.taskNameLabel.grid(row=0)
        self.taskTimeHeadLineLabel.grid(row=1)
        self.taskTimeHoursLabel.grid(row=2)
        self.taskTimeMinutesLabel.grid(row=3)
        self.taskTimeSecondsLabel.grid(row=4)

        # エントリーを生成
        self.taskNameEntry = tk.Entry(self.window)
        self.taskTimeHoursEntry = tk.Entry(self.window)
        self.taskTimeMinutesEntry = tk.Entry(self.window)
        self.taskTimeSecondsEntry = tk.Entry(self.window)
        self.taskNameEntry.grid(row=0, column=1)
        self.taskTimeHoursEntry.grid(row=2, column=1)
        self.taskTimeMinutesEntry.grid(row=3, column=1)
        self.taskTimeSecondsEntry.grid(row=4, column=1)

        # OKボタン作成
        self.buttonSave = tk.Button(self.window, text="OK", command=self.addTask)
        self.buttonSave.grid(row=5, column=0)

        # Cancelボタン作成
        self.buttonClose = tk.Button(self.window, text="Cancel", command=self.cancel)
        self.buttonClose.grid(row=5, column=1)

    def placeWindow(self) -> None:
        # window_width = self.master.winfo_width()
        # window_height = self.master.winfo_height()
        window_x = self.master.winfo_x()
        window_y = self.master.winfo_y()
        # new_window_x = window_x + window_width // 2
        # new_window_y = window_y - window_height // 2
        # self.window.geometry(f"+{new_window_x}+{new_window_y}")
        self.window.geometry(f"+{window_x}+{window_y}")

    def addTask(self) -> None:
        try:
            taskName: str = self.taskNameEntry.get()
            leftSeconds: int = self.convertToSeconds()
            newTask = Task(taskName, leftSeconds)
            tasksJson = TasksJson()
            if tasksJson.getNumOfTasksRegisteredInJson() + 1 > Setting.MAX_NUM_OF_TASKS:
                raise Exception("Cannot register any more tasks")
            if tasksJson.isRegisteredTaskName(newTask.taskName) == True:
                raise Exception("This task name is already used")
            tasksJson.addTaskToTasksJson(newTask)
            self.window.destroy()
        except Exception as e:
            print(f"AddTaskWindow.addTask(): {e}")
            messagebox.showerror("ERROR", str(e))

    def cancel(self) -> None:
        self.window.destroy()

    def convertToSeconds(self) -> int:
        try:
            hoursInt: int = int(self.taskTimeHoursEntry.get())
            minutesInt: int = int(self.taskTimeMinutesEntry.get())
            secondsInt: int = int(self.taskTimeHoursEntry.get())
            return hoursInt * 3600 + minutesInt * 60 + secondsInt
        except Exception as e:
            print(f"AddTaskWindow.convertToSeconds(): {e}")
            messagebox.showinfo("ERROR", str(e))
            return None
