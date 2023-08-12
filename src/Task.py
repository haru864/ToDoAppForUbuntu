import tkinter as tk
import pygame
import time
import threading
from typing import Optional
from Setting import Setting


class Task:
    ROOT_WIDGET = None

    def __init__(
        self, taskName: Optional[str | None], leftSeconds: Optional[int | None]
    ) -> None:
        if taskName is None:
            raise Exception("Task Name can't be empty")
        if (
            leftSeconds is None
            or isinstance(leftSeconds, int) == False
            or leftSeconds < 0
        ):
            raise Exception("Task time must be digit")
        self.taskName: str = taskName
        self.leftSeconds: int = leftSeconds
        self.isTimerRunning = False
        self.isBeeping = False

    def registerLabel(self, taskNameLabel: tk.Label, leftSecondsLabel: tk.Label):
        self.taskNameLabel: tk.Label = taskNameLabel
        self.leftSecondsLabel: tk.Label = leftSecondsLabel

    def getLeftTimeStr(self):
        seconds: int = self.leftSeconds
        h: int = seconds // 3600
        m: int = (seconds - h * 3600) // 60
        s: int = seconds - h * 3600 - m * 60
        return f"{h:02}:{m:02}:{s:02}"

    @classmethod
    def setRootWidget(cls, root):
        Task.ROOT_WIDGET = root

    def rename(self, newTaskName: str) -> None:
        self.taskName = newTaskName

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
        pygame.mixer.music.load(Setting.SOUND_FILE)
        start_time = time.time()
        while self.isBeeping:
            elapsed_time = time.time() - start_time
            if elapsed_time >= Setting.BEEP_PERIOD_SECONDS:
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
        return f"taskName:{self.taskName}, leftSeconds:{self.leftSeconds}"

    def __repr__(self):
        return f"{{{self.taskName},{self.leftSeconds},{self.isTimerRunning},{self.isBeeping}}}"
