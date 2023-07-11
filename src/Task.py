from tkinter import *
from typing import Final
import pygame
import time
import threading
from TaskTimeDialog import TaskTimeDialog
import json


class Task:
    MAX_NUM_OF_TASKS: int = 3
    SOUND_FILE: str = None
    BEEP_PERIOD_SECONDS: int = 5
    DEFAULT_TASK_TIME: int = 3
    NAME_TO_TASK_DICT: dict = dict()
    REGISTERED_TASK_NAME_SET: set[str] = set()
    ROOT_WIDGET = None

    def __init__(self, taskName: str, leftSeconds: int) -> None:
        if len(Task.REGISTERED_TASK_NAME_SET) >= Task.MAX_NUM_OF_TASKS:
            raise Exception("Cannot register any more tasks")
        if taskName in Task.REGISTERED_TASK_NAME_SET:
            raise Exception("This task name is already used")
        self.taskName: str = taskName
        Task.REGISTERED_TASK_NAME_SET.add(taskName)
        Task.NAME_TO_TASK_DICT[taskName] = self
        self.leftSeconds: int = leftSeconds
        self.isTimerRunning = False
        self.isBeeping = False

    @classmethod
    def loadSettingFromJson(cls):
        with open("setting/conf.json", "r") as confJson:
            data = json.load(confJson)
            print(f"loaded JSON: {data}")
            Task.MAX_NUM_OF_TASKS = data["max_num_of_tasks"]
            Task.SOUND_FILE = data["sound_file"]
            Task.BEEP_PERIOD_SECONDS = data["beep_period_seconds"]
            Task.DEFAULT_TASK_TIME = data["default_task_time"]

    def registerLabel(self, taskNameLabel: Label, leftSecondsLabel: Label):
        self.taskNameLabel: Label = taskNameLabel
        self.leftSecondsLabel: Label = leftSecondsLabel

    def getLeftTimeStr(self):
        seconds: int = self.leftSeconds
        h: int = seconds // 3600
        m: int = (seconds - h * 3600) // 60
        s: int = seconds - h * 3600 - m * 60
        return f"{h:02}:{m:02}:{s:02}"

    @classmethod
    def setRootWidget(cls, root):
        Task.ROOT_WIDGET = root

    def setLeftSeconds(self):
        dialog = TaskTimeDialog(
            windowParent=self.leftSecondsLabel,
            windowTitle="Task Period Update",
            initialValueSeconds=Task.DEFAULT_TASK_TIME,
        )
        if dialog.result is None:
            return
        self.leftSeconds = dialog.result
        self.leftSecondsLabel.config(text=self.getLeftTimeStr())

    @classmethod
    def setBeepPeriod(cls):
        dialog = TaskTimeDialog(
            windowParent=Task.ROOT_WIDGET,
            windowTitle="Beep Period Update",
            initialValueSeconds=Task.BEEP_PERIOD_SECONDS,
        )
        if dialog.result is None:
            return
        Task.BEEP_PERIOD_SECONDS = dialog.result

    def rename(self, newTaskName: str):
        self.taskName = newTaskName

    def removeFromRegisteredTasksList(self) -> None:
        for i in len(Task.REGISTERED_TASKS_LIST):
            if Task.REGISTERED_TASKS_LIST[i] is self:
                del Task.REGISTERED_TASKS_LIST[i]
                return
        print(f"removed from {Task.REGISTERED_TASKS_LIST}")

    def startTask(self):
        self.isTimerRunning = True
        self.decrementTime()

    def stopTask(self):
        self.isTimerRunning = False
        self.stopBeep()

    def startBeep(self):
        self.isBeeping = True
        self.taskNameLabel.config(fg="red")
        threading.Thread(target=self.beep).start()

    def stopBeep(self):
        self.isBeeping = False
        self.taskNameLabel.config(fg="black")

    def beep(self):
        pygame.init()
        pygame.mixer.music.load(Task.SOUND_FILE)
        start_time = time.time()
        while self.isBeeping:
            elapsed_time = time.time() - start_time
            if elapsed_time >= Task.BEEP_PERIOD_SECONDS:
                pygame.mixer.music.stop()
                break
            while pygame.mixer.music.get_busy():
                if self.isBeeping is False:
                    pygame.mixer.music.stop()
                    break
                time.sleep(0.001)
            pygame.mixer.music.play()
        self.isBeeping = False

    def decrementTime(self):
        if self.isTimerRunning and self.leftSeconds > 0:
            self.leftSeconds -= 1
            self.leftSecondsLabel.config(text=self.getLeftTimeStr())
            self.leftSecondsLabel.after(1000, self.decrementTime)
        elif self.isTimerRunning and self.leftSeconds == 0:
            self.isTimerRunning = False
            self.startBeep()

    def __str__(self) -> str:
        return f"taskName:{self.taskName}, leftSeconds;{self.leftSeconds}"
