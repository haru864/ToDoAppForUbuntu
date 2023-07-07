import tkinter as tk
from tkinter import simpledialog, messagebox


class TaskTimeDialog(simpledialog.Dialog):
    def __init__(self, windowParent, windowTitle, initialValueSeconds) -> None:
        self.initHours = tk.IntVar(value=initialValueSeconds // 3600)
        self.initMinutes = tk.IntVar(value=initialValueSeconds % 3600 // 60)
        self.initSeconds = tk.IntVar(value=initialValueSeconds % 60)
        super().__init__(parent=windowParent, title=windowTitle)

    def body(self, master):
        tk.Label(master, text="hours:").grid(row=0)
        tk.Label(master, text="minutes:").grid(row=1)
        tk.Label(master, text="seconds:").grid(row=2)
        self.entry1 = tk.Entry(master, textvariable=self.initHours)
        self.entry2 = tk.Entry(master, textvariable=self.initMinutes)
        self.entry3 = tk.Entry(master, textvariable=self.initSeconds)
        self.entry1.grid(row=0, column=1)
        self.entry2.grid(row=1, column=1)
        self.entry3.grid(row=2, column=1)
        return self.entry1

    def validate(self):
        try:
            inputHours: str = self.entry1.get()
            inputMinutes: str = self.entry2.get()
            inputSeconds: str = self.entry3.get()
            hours, minutes, seconds = 0, 0, 0
            if inputHours != "":
                hours = int(inputHours)
            if inputMinutes != "":
                minutes = int(inputMinutes)
            if inputSeconds != "":
                seconds = int(inputSeconds)
            if (
                hours < 0
                or hours > 24
                or minutes < 0
                or minutes > 59
                or seconds < 0
                or seconds > 59
            ):
                raise ValueError
            self.result: int = self.timeToSeconds(hours, minutes, seconds)
            return 1
        except ValueError:
            messagebox.showerror("ERROR", "hours:0~24, minutes:0~59, seconds:0~59")
            return 0

    def timeToSeconds(self, hours, minutes, seconds) -> int:
        return hours * 3600 + minutes * 60 + seconds
