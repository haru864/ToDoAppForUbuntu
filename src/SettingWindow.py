import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from Setting import Setting
from ConfJson import ConfJson


class SettingWindow:
    def __init__(self, master: tk.Tk = None) -> None:
        self.master = master
        self.window = tk.Toplevel(master)
        self.window.title("Setting")
        self.placeWindow()

        # ラベル作成
        self.labelMaxNumOfTasks = tk.Label(self.window, text="MAX_NUM_OF_TASKS:")
        self.labelSoundFile = tk.Label(self.window, text="SOUND_FILE:")
        self.labelBeepPeriodSeconds = tk.Label(self.window, text="BEEP_PERIOD_SECONDS:")
        self.labelDefaultTaskTime = tk.Label(self.window, text="DEFAULT_TASK_TIME:")
        self.labelMaxNumOfTasks.grid(row=0, column=0)
        self.labelBeepPeriodSeconds.grid(row=1, column=0)
        self.labelDefaultTaskTime.grid(row=2, column=0)
        self.labelSoundFile.grid(row=3, column=0)

        # 数値を入力するテキストボックス作成
        self.entryMaxNumOfTasks = tk.Entry(
            self.window, textvariable=tk.IntVar(value=Setting.MAX_NUM_OF_TASKS)
        )
        self.entryBeepPeriodSeconds = tk.Entry(
            self.window, textvariable=tk.IntVar(value=Setting.BEEP_PERIOD_SECONDS)
        )
        self.entryDefaultTaskTime = tk.Entry(
            self.window, textvariable=tk.IntVar(value=Setting.DEFAULT_TASK_TIME)
        )
        self.entryMaxNumOfTasks.grid(row=0, column=1)
        self.entryBeepPeriodSeconds.grid(row=1, column=1)
        self.entryDefaultTaskTime.grid(row=2, column=1)

        # ファイル選択ダイアログを表示するボタン作成
        self.buttonExplore = tk.Button(
            self.window, text="Browse Files", command=self.browseFiles
        )
        self.buttonExplore.grid(row=4, column=1)

        # ファイルパスを表示するラベル作成
        self.labelSoundFile = tk.Label(self.window, text=Setting.SOUND_FILE, fg="blue")
        self.labelSoundFile.grid(row=3, column=1)

        # セーブボタン作成
        self.buttonSave = tk.Button(self.window, text="Save", command=self.saveEntry)
        self.buttonSave.grid(row=5, column=0)

        # クローズボタン作成
        self.buttonClose = tk.Button(
            self.window, text="Close", command=self.closeWindow
        )
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
            filetypes=[("OGG files", "*.ogg")],
            initialdir="sound",
            title="Select a File",
        )
        self.labelSoundFile.configure(text=filename)

    def saveEntry(self):
        newMaxNumOfTasks = None
        newBeepPeriodSeconds = None
        newDefaultTaskTime = None
        newSoundFile = None
        try:
            newMaxNumOfTasks = int(self.entryMaxNumOfTasks.get())
            newBeepPeriodSeconds = int(self.entryBeepPeriodSeconds.get())
            newDefaultTaskTime = int(self.entryDefaultTaskTime.get())
            newSoundFile = self.labelSoundFile.cget("text")
        except Exception as e:
            print(f"SettingWindow.saveEntry(): {e}")
            errMsgString: str = e.args[0]
            messagebox.showinfo("ERROR", errMsgString)
        try:
            Setting.updateSetting(
                newMaxNumOfTasks=newMaxNumOfTasks,
                newBeepPeriodSeconds=newBeepPeriodSeconds,
                newDefaultTaskTime=newDefaultTaskTime,
                newSoundFile=newSoundFile,
            )
            confJson = ConfJson()
            confJson.updateConfJsonFileBySetting()
            self.closeWindow()
        except Exception as e:
            print(f"SettingWindow.saveEntry(): {e}")
            errMsgList: list = e.args[0]
            errMsgString: str = "\n".join(errMsgList)
            messagebox.showinfo("ERROR", errMsgString)

    def closeWindow(self):
        self.window.destroy()
