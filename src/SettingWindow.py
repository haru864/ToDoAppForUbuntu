from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from Task import Task
import json


class SettingWindow:
    def __init__(self, master: Tk = None) -> None:
        self.master = master
        self.window = Toplevel(master)
        self.window.title("Setting")
        self.placeWindow()

        # ラベル作成
        self.labelMaxNumOfTasks = Label(self.window, text="MAX_NUM_OF_TASKS:")
        self.labelSoundFile = Label(self.window, text="SOUND_FILE:")
        self.labelBeepPeriodSeconds = Label(self.window, text="BEEP_PERIOD_SECONDS:")
        self.labelDefaultTaskTime = Label(self.window, text="DEFAULT_TASK_TIME:")
        self.labelMaxNumOfTasks.grid(row=0, column=0)
        self.labelBeepPeriodSeconds.grid(row=1, column=0)
        self.labelDefaultTaskTime.grid(row=2, column=0)
        self.labelSoundFile.grid(row=3, column=0)

        # 数値を入力するテキストボックス作成
        self.entryMaxNumOfTasks = Entry(
            self.window, textvariable=IntVar(value=Task.MAX_NUM_OF_TASKS)
        )
        self.entryBeepPeriodSeconds = Entry(
            self.window, textvariable=IntVar(value=Task.BEEP_PERIOD_SECONDS)
        )
        self.entryDefaultTaskTime = Entry(
            self.window, textvariable=IntVar(value=Task.DEFAULT_TASK_TIME)
        )
        self.entryMaxNumOfTasks.grid(row=0, column=1)
        self.entryBeepPeriodSeconds.grid(row=1, column=1)
        self.entryDefaultTaskTime.grid(row=2, column=1)

        # ファイル選択ダイアログを表示するボタン作成
        self.buttonExplore = Button(
            self.window, text="Browse Files", command=self.browseFiles
        )
        self.buttonExplore.grid(row=4, column=1)

        # ファイルパスを表示するラベル作成
        self.labelSoundFile = Label(self.window, text=Task.SOUND_FILE, fg="blue")
        self.labelSoundFile.grid(row=3, column=1)

        # セーブボタン作成
        self.buttonSave = Button(self.window, text="Save", command=self.saveEntry)
        self.buttonSave.grid(row=5, column=0)

        # クローズボタン作成
        self.buttonClose = Button(self.window, text="Close", command=self.closeWindow)
        self.buttonClose.grid(row=5, column=1)

    def placeWindow(self):
        window_width = self.master.winfo_width()
        window_height = self.master.winfo_height()
        window_x = self.master.winfo_x()
        window_y = self.master.winfo_y()
        new_window_x = window_x + window_width // 2
        new_window_y = window_y - window_height // 2
        # self.window.geometry(f"+{new_window_x}+{new_window_y}")
        self.window.geometry(f"+{window_x}+{window_y}")

    def browseFiles(self):
        filename = filedialog.askopenfilename(
            initialdir="../sound", title="Select a File"
        )
        self.labelSoundFile.configure(text=filename)

    def saveEntry(self):
        data = None
        with open("../setting/conf.json", "r") as confJsonRead:
            data = json.load(confJsonRead)
            print(type(data))
        data["max_num_of_tasks"] = self.entryMaxNumOfTasks.get()
        data["sound_file"] = self.labelSoundFile.cget("text")
        data["beep_period_seconds"] = self.entryBeepPeriodSeconds.get()
        data["default_task_time"] = self.entryDefaultTaskTime.get()
        print(f"updated JSON: {data}")
        # with open("../setting/conf.json", "w") as confJsonWrite:
        #     json.dump(data, confJsonWrite)
        Task.loadSettingFromJson()

    def closeWindow(self):
        self.window.destroy()
