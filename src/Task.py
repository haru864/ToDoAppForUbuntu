from tkinter import *
from typing import Final
import pygame
import time
import threading
from TaskTimeDialog import TaskTimeDialog


class Task:
    MAX_NUM_OF_TASKS: Final[int] = 3
    NUM_OF_USED_TASK_ID: int = 0
    TASK_ID_POOL: bool = [False for i in range(MAX_NUM_OF_TASKS)]
    SOUND_FILE: str = "../sound/bark.ogg"
    BEEP_PERIOD_SECONDS: int = 5
    DEFAULT_TASK_TIME: Final[int] = 3
    ROOT_WIDGET = None

    def __init__(self, taskName: str, leftSeconds: int) -> None:
        self.taskId: int = self.getTaskID()
        if self.taskId is None:
            raise Exception("Cannot register any more tasks")
        self.taskName: str = taskName
        self.leftSeconds: int = leftSeconds
        self.isTimerRunning = False
        self.isBeeping = False

    def registerLabel(self, taskNameLabel: Label, leftSecondsLabel: Label):
        self.taskNameLabel: Label = taskNameLabel
        self.leftSecondsLabel: Label = leftSecondsLabel

    def getTaskID(self) -> int:
        if Task.NUM_OF_USED_TASK_ID >= Task.MAX_NUM_OF_TASKS:
            return None
        for i in range(Task.MAX_NUM_OF_TASKS):
            newTaskID: int = i
            if Task.TASK_ID_POOL[newTaskID] == False:
                Task.TASK_ID_POOL[newTaskID] = True
                Task.NUM_OF_USED_TASK_ID += 1
                return newTaskID
        return None

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

    def delete(self):
        Task.NUM_OF_USED_TASK_ID -= 1
        Task.TASK_ID_POOL[self.taskId] = False

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
        return f"{self.taskId}, {self.taskName}, {self.leftSeconds}"
