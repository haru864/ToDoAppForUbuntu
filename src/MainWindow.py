import tkinter as tk
import pygame
from typing import Final
from TasksJson import TasksJson
from tkinter import simpledialog
from Task import Task
from tkinter import messagebox
from SettingWindow import SettingWindow
from Setting import Setting

usageWindow = None
lastPushedTaskMenuButton: tk.Menubutton = None

MAIN_WINDOW_TITLE: Final[str] = "ToDoApp"
MAIN_WINDOW_WIDTH: Final[str] = "800"
MAIN_WINDOW_HEIGHT: Final[str] = "600"
MAIN_WINDOW_SIZE: Final[str] = f"{MAIN_WINDOW_WIDTH}x{MAIN_WINDOW_HEIGHT}"
USAGE_WINDOW_WIDTH: Final[str] = "400"
USAGE_WINDOW_HEIGHT: Final[str] = "400"
USAGE_WINDOW_SIZE: Final[str] = f"{USAGE_WINDOW_WIDTH}x{USAGE_WINDOW_HEIGHT}"


class MainWindow(tk.Tk):
    TASK_LIST_FRAME_WIDTH: Final[int] = 650
    TASK_LIST_FRAME_HEIGHT: Final[int] = 500
    NAME_TO_TASK_DICT: dict[str, "Task"] = {}

    def __init__(self) -> None:
        super().__init__()
        self.title(MAIN_WINDOW_TITLE)
        self.bind("<Configure>", self._on_move)
        self.centerWindow(self)
        self.geometry("")
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

        # タスクリスト欄を生成
        self.taskListFrame = tk.Frame(
            self,
            width=MainWindow.TASK_LIST_FRAME_WIDTH,
            height=MainWindow.TASK_LIST_FRAME_HEIGHT,
            borderwidth=2,
            relief="solid",
        )
        self.taskListFrame.grid(row=0, column=0)

        # タスクバーを生成
        self.taskListCanvas = tk.Canvas(
            self.taskListFrame,
            width=MainWindow.TASK_LIST_FRAME_WIDTH,
            height=MainWindow.TASK_LIST_FRAME_HEIGHT,
        )
        self.taskListScrollbar = tk.Scrollbar(
            self.taskListFrame,
            orient="vertical",
            command=self.taskListCanvas.yview,
        )
        self.innerTaskListFrame = tk.Frame(
            self.taskListCanvas, borderwidth=2, relief="solid"
        )
        self.innerTaskListFrame.pack(fill=tk.X)
        self.taskListCanvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.taskListScrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.taskListCanvas.create_window(
            (0, 0), window=self.innerTaskListFrame, anchor="nw"
        )
        self.taskListCanvas.configure(yscrollcommand=self.taskListScrollbar.set)
        self.innerTaskListFrame.bind(
            "<Configure>",
            lambda e: self.taskListCanvas.configure(
                scrollregion=self.taskListCanvas.bbox("all")
            ),
        )
        self.taskListCanvas.bind("<Button-4>", self._on_mousewheel)
        self.taskListCanvas.bind("<Button-5>", self._on_mousewheel)

        # 登録済みタスクを読み込み
        tasksJson = TasksJson()
        tasksJson.loadTasksJson()
        print(f"loading tasksJson... {tasksJson}")
        for currTask in tasksJson.registeredTasksList:
            self.addTask(currTask)

        # メニュー欄を生成
        menuFrame = tk.Frame(self, width=100, height=300, borderwidth=2, relief="solid")
        menuFrame.grid(row=0, column=1)

        # メニュー欄にボタンを設置
        addTaskButton = tk.Button(menuFrame, text="add task", command=self.addTask)
        usageButton = tk.Button(menuFrame, text="usage", command=self.displayUsage)
        listenSoundButton = tk.Button(
            menuFrame, text="listen sound", command=self.listenSound
        )
        settingButton = tk.Button(menuFrame, text="setting", command=self.editSetting)
        closeButton = tk.Button(menuFrame, text="close", command=self.closeApp)
        addTaskButton.pack(side=tk.TOP, padx=5, pady=10)
        usageButton.pack(side=tk.TOP, padx=5, pady=10)
        listenSoundButton.pack(side=tk.TOP, padx=5, pady=10)
        settingButton.pack(side=tk.TOP, padx=5, pady=10)
        closeButton.pack(side=tk.TOP, padx=5, pady=10)

    def addTask(self, task: Task = None) -> None:
        newTask = None
        if task is None:
            taskName: str = simpledialog.askstring("Task Name", "Write Task Name")
            try:
                newTask = Task(taskName, Setting.DEFAULT_TASK_TIME)
                if len(MainWindow.NAME_TO_TASK_DICT) >= Setting.MAX_NUM_OF_TASKS:
                    raise Exception("Cannot register any more tasks")
                if taskName in MainWindow.NAME_TO_TASK_DICT:
                    raise Exception("This task name is already used")
            except Exception as e:
                print(f"MainWindow.addTask: {e}")
                messagebox.showerror("ERROR", e)
                return
        else:
            newTask = task
        MainWindow.NAME_TO_TASK_DICT[newTask.taskName] = newTask

        taskFrame = tk.Frame(
            self.innerTaskListFrame,
            width=70,
            height=10,
            borderwidth=0.5,
            relief="solid",
        )
        taskLabel = tk.Label(taskFrame, text=newTask.taskName, width=45)
        timeLabel = tk.Label(taskFrame, text=newTask.getLeftTimeStr())
        newTask.registerLabel(taskLabel, timeLabel)

        taskMenuButton = tk.Menubutton(taskFrame, text="SETTING", relief="groove")
        taskMenuButton.menu = tk.Menu(taskMenuButton)
        taskMenuButton.menu.add_command(
            label="rename",
            command=lambda label=taskLabel: self.renameTask(label),
        )
        taskMenuButton.menu.add_command(
            label="set time",
            command=lambda: newTask.setLeftSeconds(),
        )
        taskMenuButton.menu.add_command(
            label="delete",
            command=lambda frame=taskFrame, task=newTask: self.deleteTask(frame, task),
        )
        startButton = tk.Button(
            taskFrame, text="START", command=lambda task=newTask: task.startTask()
        )
        stopButton = tk.Button(
            taskFrame, text="STOP", command=lambda task=newTask: task.stopTask()
        )

        taskFrame.pack(fill=tk.X)
        taskLabel.pack(side=tk.LEFT)
        timeLabel.pack(side=tk.LEFT)
        taskMenuButton.pack(side=tk.LEFT)
        startButton.pack(side=tk.LEFT)
        stopButton.pack(side=tk.LEFT)
        taskMenuButton["menu"] = taskMenuButton.menu
        taskMenuButton.bind(
            "<Button-1>",
            lambda event, menuButton=taskMenuButton: self.menuButtonAction(menuButton),
        )

    def _on_mousewheel(self, event) -> None:
        scrollRegion = self.taskListCanvas.cget("scrollregion")
        if scrollRegion == "":
            return
        scrollRegionList = [int(val) for val in scrollRegion.split()]
        visible_height = self.taskListCanvas.winfo_height()
        if (scrollRegionList[3] - scrollRegionList[1]) > visible_height:
            if event.num == 4:
                self.taskListCanvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.taskListCanvas.yview_scroll(1, "units")

    def displayUsage(self) -> None:
        global usageWindow
        if usageWindow is None or not tk.Toplevel.winfo_exists(usageWindow):
            usageWindow = tk.Toplevel()
            usageWindow.title("usage")
            tk.Label(usageWindow, text="hello, world!").pack()
        usageWindow.geometry(USAGE_WINDOW_SIZE)
        self.centerWindow(usageWindow)
        usageWindow.lift()

    def centerWindow(self, window) -> None:
        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (window.winfo_width() // 2)
        y = (screen_height // 2) - (window.winfo_height() // 2)
        window.geometry(f"+{x}+{y}")

    def listenSound(self) -> None:
        pygame.init()
        pygame.mixer.music.load(Setting.SOUND_FILE)
        pygame.mixer.music.play()

    def editSetting(self):
        SettingWindow(MainWindow.ROOT)

    def renameTask(self, label: tk.Label):
        currentTaskName: str = label.cget("text")
        newTaskName: str = simpledialog.askstring(
            "New Task Name", "Write New Task Name"
        )
        if newTaskName in MainWindow.NAME_TO_TASK_DICT:
            messagebox.showerror("ERROR", "This Task Name is already used")
            return
        currentTask: Task = MainWindow.NAME_TO_TASK_DICT[currentTaskName]
        currentTask.rename(newTaskName)
        label.config(text=newTaskName)

    def deleteTask(self, frame: tk.Frame, task: Task) -> None:
        global lastPushedTaskMenuButton
        frame.destroy()
        lastPushedTaskMenuButton = None
        MainWindow.NAME_TO_TASK_DICT.pop(task.taskName)

    def menuButtonAction(self, menuButton: tk.Menubutton) -> None:
        global lastPushedTaskMenuButton
        lastPushedTaskMenuButton = menuButton

    def saveTasks(self) -> None:
        try:
            tasksJson = TasksJson()
            tasklist = list(MainWindow.NAME_TO_TASK_DICT.values())
            tasksJson.updateTaskList(tasklist)
            tasksJson.saveRegisteredTasks()
        except Exception as e:
            print(f"MainWindow.saveTasks: {e}")
            messagebox.showerror("ERROR", e)
            return

    def closeApp(self) -> None:
        print("closing application...")
        self.saveTasks()
        self.destroy()

    def _on_move(self, event=None) -> None:
        global lastPushedTaskMenuButton
        if lastPushedTaskMenuButton is None:
            return
        lastPushedTaskMenuButton.menu.unpost()

    def _on_closing(self) -> None:
        self.closeApp()
