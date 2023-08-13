import tkinter as tk
from typing import Optional
from Task import Task
from TasksJson import TasksJson
from Setting import Setting
from tkinter import simpledialog, messagebox


class AddTaskDialog(simpledialog.Dialog):
    def __init__(self, master: tk.Tk) -> None:
        self.task: Task = None
        super().__init__(parent=master, title="Add Task")

    def body(self, master):
        # ラベルを生成
        self.taskNameLabel = tk.Label(master, text="Task Name:")
        self.taskTimeHeadLineLabel = tk.Label(master, text="Time")
        self.taskTimeHoursLabel = tk.Label(master, text="hours:")
        self.taskTimeMinutesLabel = tk.Label(master, text="minutes:")
        self.taskTimeSecondsLabel = tk.Label(master, text="seconds:")
        self.taskNameLabel.grid(row=0)
        self.taskTimeHeadLineLabel.grid(row=1)
        self.taskTimeHoursLabel.grid(row=2)
        self.taskTimeMinutesLabel.grid(row=3)
        self.taskTimeSecondsLabel.grid(row=4)

        # エントリーを生成
        self.taskNameEntry = tk.Entry(master)
        self.taskTimeHoursEntry = tk.Entry(master)
        self.taskTimeMinutesEntry = tk.Entry(master)
        self.taskTimeSecondsEntry = tk.Entry(master)
        self.taskNameEntry.grid(row=0, column=1)
        self.taskTimeHoursEntry.grid(row=2, column=1)
        self.taskTimeMinutesEntry.grid(row=3, column=1)
        self.taskTimeSecondsEntry.grid(row=4, column=1)

    def validate(self) -> None:
        try:
            taskName: str = self.taskNameEntry.get()
            leftSeconds: int = self._convertToSeconds()
            self.task = Task(taskName, leftSeconds)
            tasksJson = TasksJson()
            if tasksJson.getNumOfTasksRegisteredInJson() + 1 > Setting.MAX_NUM_OF_TASKS:
                raise Exception("Cannot register any more tasks")
            if tasksJson.isRegisteredTaskName(self.task.taskName) == True:
                raise Exception("This task name is already used")
            tasksJson.addTaskToTasksJson(self.task)
            return True
        except Exception as e:
            print(f"AddTaskWindow.addTask(): {e}")
            messagebox.showerror("ERROR", str(e))
            return False

    def apply(self) -> None:
        self.result: Task = self.task

    def _convertToSeconds(self) -> int:
        try:
            hoursInt: int = int(self.taskTimeHoursEntry.get())
            minutesInt: int = int(self.taskTimeMinutesEntry.get())
            secondsInt: int = int(self.taskTimeSecondsEntry.get())
            return hoursInt * 3600 + minutesInt * 60 + secondsInt
        except Exception as e:
            print(f"AddTaskWindow._convertToSeconds(): {e}")
            messagebox.showinfo("ERROR", str(e))
            return None
