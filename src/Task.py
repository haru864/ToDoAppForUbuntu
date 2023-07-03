from tkinter import *
from tkinter import ttk
from typing import Any, Final


class Task:
    MAX_NUM_OF_TASKS: Final[int] = 3
    NUM_OF_USED_TASK_ID: int = 0
    TASK_ID_POOL: bool = [False for i in range(MAX_NUM_OF_TASKS)]

    def __init__(self, master: Frame, taskName: str, leftSeconds: int) -> None:
        self.master = master
        self.taskId: int = self.getTaskID()
        print(f"taskId: {self.taskId}")
        if self.taskId is None:
            raise Exception("Cannot register any more tasks")
        self.taskName: str = taskName
        self.leftSeconds: int = leftSeconds
        self.timerRunning = False

    def getTaskID(self) -> int:
        if Task.NUM_OF_USED_TASK_ID >= Task.MAX_NUM_OF_TASKS:
            return None
        for i in range(Task.MAX_NUM_OF_TASKS):
            newTaskID: int = i
            if Task.TASK_ID_POOL[newTaskID] == False:
                Task.TASK_ID_POOL[newTaskID] = True
                Task.NUM_OF_USED_TASK_ID += 1
                print(f"newTaskID: {newTaskID}")
                return newTaskID
        return None

    def getLeftTimeStr(self):
        seconds: int = self.leftSeconds
        h: int = seconds // 3600
        m: int = (seconds - h * 3600) // 60
        s: int = seconds - h * 3600 - m * 60
        return f"{h:02}:{m:02}:{s:02}"

    def rename(self, newTaskName: str):
        self.taskName = newTaskName

    def delete(self):
        Task.NUM_OF_USED_TASK_ID -= 1
        Task.TASK_ID_POOL[self.taskId] = False

    def start(self):
        self.timerRunning = True

    def stop(self):
        self.timerRunning = False

    def __str__(self) -> str:
        return f"{self.taskId}, {self.taskName}, {self.leftSeconds}"