import tkinter as tk
from tkinter import filedialog
from SettingJson import SettingJson
from tkinter import simpledialog, messagebox
import inspect


class SettingDialog(simpledialog.Dialog):
    def __init__(self, master: tk.Tk) -> None:
        self.max_num_of_tasks: int = None
        self.beep_period_seconds: int = None
        self.sound_file: str = None
        super().__init__(parent=master, title="Setting")

    def body(self, master) -> None:
        # ラベル作成
        self.labelMaxNumOfTasks = tk.Label(master, text="MAX_NUM_OF_TASKS:")
        self.labelSoundFile = tk.Label(master, text="SOUND_FILE:")
        self.labelBeepPeriodSeconds = tk.Label(master, text="BEEP_PERIOD_SECONDS:")
        self.labelMaxNumOfTasks.grid(row=0, column=0)
        self.labelBeepPeriodSeconds.grid(row=1, column=0)
        self.labelSoundFile.grid(row=2, column=0)

        # 数値を入力するテキストボックス作成
        self.entryMaxNumOfTasks = tk.Entry(
            master, textvariable=tk.IntVar(value=SettingJson.max_num_of_tasks)
        )
        self.entryBeepPeriodSeconds = tk.Entry(
            master, textvariable=tk.IntVar(value=SettingJson.beep_period_seconds)
        )
        self.entryMaxNumOfTasks.grid(row=0, column=1)
        self.entryBeepPeriodSeconds.grid(row=1, column=1)

        # ファイルパスを表示するラベル作成
        self.labelSoundFile = tk.Label(master, text=SettingJson.sound_file, fg="blue")
        self.labelSoundFile.grid(row=2, column=1)

        # ファイル選択ダイアログを表示するボタン作成
        self.buttonExplore = tk.Button(
            master, text="Browse Files", command=self._browseFiles
        )
        self.buttonExplore.grid(row=3, column=1)

    def _browseFiles(self) -> None:
        filename = filedialog.askopenfilename(
            filetypes=[("OGG files", "*.ogg")],
            initialdir="sound",
            title="Select a File",
        )
        self.labelSoundFile.configure(text=filename)

    def validate(self) -> bool:
        try:
            self.max_num_of_tasks: int = int(self.entryMaxNumOfTasks.get())
            self.beep_period_seconds: int = int(self.entryBeepPeriodSeconds.get())
            self.sound_file: str = self.labelSoundFile.cget("text")
            return True
        except Exception as e:
            print(f"{self.__class__}.{inspect.currentframe().f_code.co_name}: {e}")
            messagebox.showerror("ERROR", str(e))
            return False

    def apply(self) -> None:
        SettingJson.changeSetting(
            new_max_num_of_tasks=self.max_num_of_tasks,
            new_beep_period_seconds=self.beep_period_seconds,
            new_sound_file=self.sound_file,
        )
        SettingJson.updateSettingJson()
