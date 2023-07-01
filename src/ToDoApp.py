from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from typing import Final
import pygame

# import Task
from Task import Task

MAIN_WINDOW_TITLE: Final[str] = "ToDoApp"
MAIN_WINDOW_WIDTH: Final[str] = "500"
MAIN_WINDOW_HEIGHT: Final[str] = "500"
MAIN_WINDOW_SIZE: Final[str] = f"{MAIN_WINDOW_WIDTH}x{MAIN_WINDOW_HEIGHT}"
USAGE_WINDOW_WIDTH: Final[str] = "400"
USAGE_WINDOW_HEIGHT: Final[str] = "400"
USAGE_WINDOW_SIZE: Final[str] = f"{USAGE_WINDOW_WIDTH}x{USAGE_WINDOW_HEIGHT}"
TASK_LIST_FRAME_WIDTH: Final[int] = 300
TASK_LIST_FRAME_HEIGHT: Final[int] = 300

taskList = []
usageWindow = None
lastPushedTaskMenuButton: Menubutton = None
SOUND_FILE: str = "../sound/bark.ogg"


def centerWindow(window) -> None:
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window.winfo_width() // 2)
    y = (screen_height // 2) - (window.winfo_height() // 2)
    window.geometry(f"+{x}+{y}")


def addNewTask() -> None:
    global taskList
    taskNumber = len(taskList) + 1
    taskName = "Task " + str(taskNumber)

    newTask = None
    try:
        newTask = Task(taskName, 10)
    except Exception as e:
        print(f"Exception in generating Task: {e}")
        messagebox.showinfo("ERROR", e)
        return

    newTaskFrame = Frame(
        innerTaskListFrame, width=30, height=10, borderwidth=1, relief="solid"
    )
    newTaskLabel = Label(newTaskFrame, text=taskName, width=30)
    newTaskMenuButton = Menubutton(newTaskFrame, text="setting")
    newTaskMenuButton.menu = Menu(newTaskMenuButton)
    newTaskMenuButton.menu.add_command(
        label="task name", command=lambda: print("task name")
    )
    newTaskMenuButton.menu.add_command(
        label="set time", command=lambda: print("set time")
    )
    newTaskMenuButton.menu.add_command(label="start", command=lambda: print("start"))
    newTaskMenuButton.menu.add_command(label="stop", command=lambda: print("stop"))
    newTaskMenuButton.menu.add_command(label="delete", command=lambda: print("delete"))
    newTaskFrame.pack(fill=X)
    newTaskLabel.pack(side=LEFT)
    newTaskMenuButton.pack(side=RIGHT)
    newTaskMenuButton["menu"] = newTaskMenuButton.menu
    newTaskMenuButton.bind(
        "<Button-1>",
        lambda event, menuButton=newTaskMenuButton: menuButtonAction(menuButton),
    )
    taskList.append(newTaskFrame)


def menuButtonAction(menuButton: Menubutton) -> None:
    global lastPushedTaskMenuButton
    lastPushedTaskMenuButton = menuButton


def _on_mousewheel(event) -> None:
    # canvasの現在のスクロール範囲を取得
    scrollRegion = taskListCanvas.cget("scrollregion")

    if scrollRegion == "":
        return

    scrollRegionList = [int(val) for val in scrollRegion.split()]
    visible_height = taskListCanvas.winfo_height()  # taskListCanvasの可視領域の高さ

    # スクロール可能範囲とtaskListCanvasの可視領域の高さを比較
    if (scrollRegionList[3] - scrollRegionList[1]) > visible_height:
        # スクロールバーを操作
        if event.num == 4:
            taskListCanvas.yview_scroll(-1, "units")
        elif event.num == 5:
            taskListCanvas.yview_scroll(1, "units")


def _on_move(event) -> None:
    global lastPushedTaskMenuButton
    if lastPushedTaskMenuButton is None:
        return
    lastPushedTaskMenuButton.menu.unpost()


def displayUsage() -> None:
    global usageWindow
    if usageWindow is None or not Toplevel.winfo_exists(usageWindow):
        usageWindow = Toplevel()
        usageWindow.title("usage")
        Label(usageWindow, text="hello, world!").pack()
    usageWindow.geometry(USAGE_WINDOW_SIZE)
    centerWindow(usageWindow)
    usageWindow.lift()


def selectSound() -> None:
    global SOUND_FILE
    SOUND_FILE = filedialog.askopenfilename(
        filetypes=[("OGG files", "*.ogg")], initialdir="../sound"
    )


def listenSound() -> None:
    global SOUND_FILE
    pygame.init()
    pygame.mixer.music.load(SOUND_FILE)
    pygame.mixer.music.play()


# ウィンドウを生成
root = Tk()
root.title(MAIN_WINDOW_TITLE)
root.geometry(MAIN_WINDOW_SIZE)
root.bind("<Configure>", _on_move)
centerWindow(root)

taskListFrame = Frame(
    root,
    width=TASK_LIST_FRAME_WIDTH,
    height=TASK_LIST_FRAME_HEIGHT,
    borderwidth=2,
    relief="solid",
)
menuFrame = Frame(root, width=100, height=300, borderwidth=2, relief="solid")
menuFrame.pack_propagate(False)
taskListFrame.grid(row=0, column=0)
menuFrame.grid(row=0, column=1)

taskListCanvas = Canvas(taskListFrame)
taskListScrollbar = Scrollbar(
    taskListFrame, orient="vertical", command=taskListCanvas.yview
)
innerTaskListFrame = Frame(taskListCanvas, borderwidth=2, relief="solid")

innerTaskListFrame.pack(fill=X)
taskListCanvas.pack(side=LEFT, fill=BOTH, expand=True)
taskListScrollbar.pack(side=RIGHT, fill=Y)

taskListCanvas.create_window((0, 0), window=innerTaskListFrame, anchor="nw")
taskListCanvas.configure(yscrollcommand=taskListScrollbar.set)

innerTaskListFrame.bind(
    "<Configure>",
    lambda e: taskListCanvas.configure(scrollregion=taskListCanvas.bbox("all")),
)
taskListCanvas.bind("<Button-4>", _on_mousewheel)
taskListCanvas.bind("<Button-5>", _on_mousewheel)

# メニューにボタンを設置
addTaskButton = Button(menuFrame, text="add task", command=addNewTask)
usageButton = Button(menuFrame, text="usage", command=displayUsage)
setSoundButton = Button(menuFrame, text="set sound", command=selectSound)
listenSoundButton = Button(menuFrame, text="listen sound", command=listenSound)
closeButton = Button(menuFrame, text="close", command=root.destroy)
addTaskButton.pack(side=TOP, pady=10)
usageButton.pack(side=TOP, pady=10)
setSoundButton.pack(side=TOP, pady=10)
listenSoundButton.pack(side=TOP, pady=10)
closeButton.pack(side=TOP, pady=10)

# ウィンドウの表示
root.mainloop()
