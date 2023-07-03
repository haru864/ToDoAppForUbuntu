from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import simpledialog
from typing import Final
import pygame
from Task import Task
from TaskTimeDialog import TaskTimeDialog

MAIN_WINDOW_TITLE: Final[str] = "ToDoApp"
MAIN_WINDOW_WIDTH: Final[str] = "800"
MAIN_WINDOW_HEIGHT: Final[str] = "600"
MAIN_WINDOW_SIZE: Final[str] = f"{MAIN_WINDOW_WIDTH}x{MAIN_WINDOW_HEIGHT}"
USAGE_WINDOW_WIDTH: Final[str] = "400"
USAGE_WINDOW_HEIGHT: Final[str] = "400"
USAGE_WINDOW_SIZE: Final[str] = f"{USAGE_WINDOW_WIDTH}x{USAGE_WINDOW_HEIGHT}"
TASK_LIST_FRAME_WIDTH: Final[int] = 650
TASK_LIST_FRAME_HEIGHT: Final[int] = 500

usageWindow = None
lastPushedTaskMenuButton: Menubutton = None
SOUND_FILE: str = "../sound/bark.ogg"
taskname_to_task_dict = {}


def centerWindow(window) -> None:
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window.winfo_width() // 2)
    y = (screen_height // 2) - (window.winfo_height() // 2)
    window.geometry(f"+{x}+{y}")


def addTask() -> None:
    taskFrame = Frame(
        innerTaskListFrame, width=70, height=10, borderwidth=0.5, relief="solid"
    )
    taskName = "New Task " + str(len(taskname_to_task_dict) + 1)
    newTask = None
    try:
        newTask = Task(taskFrame, taskName, 10)
    except Exception as e:
        print(f"Exception in generating Task: {e}")
        messagebox.showinfo("ERROR", e)
        return
    taskLabel = Label(taskFrame, text=taskName, width=45)
    timeLabel = Label(taskFrame, text=newTask.getLeftTimeStr())
    taskMenuButton = Menubutton(taskFrame, text="SETTING", relief="groove")
    taskMenuButton.menu = Menu(taskMenuButton)
    taskMenuButton.menu.add_command(
        label="rename",
        command=lambda label=taskLabel: renameTask(label),
    )
    taskMenuButton.menu.add_command(
        label="set time",
        command=lambda label=timeLabel, task=newTask: setTime(label, task),
    )
    taskMenuButton.menu.add_command(
        label="delete",
        command=lambda frame=taskFrame, task=newTask: deleteTask(frame, task),
    )
    startButton = Button(
        taskFrame,
        text="START",
        command=lambda label=timeLabel, task=newTask: startTask(label, task),
    )
    stopButton = Button(
        taskFrame,
        text="STOP",
        command=lambda frame=timeLabel, task=newTask: stopTask(frame, task),
    )

    taskFrame.pack(fill=X)
    taskLabel.pack(side=LEFT)
    timeLabel.pack(side=LEFT)
    taskMenuButton.pack(side=LEFT)
    startButton.pack(side=LEFT)
    stopButton.pack(side=LEFT)
    taskMenuButton["menu"] = taskMenuButton.menu
    taskMenuButton.bind(
        "<Button-1>",
        lambda event, menuButton=taskMenuButton: menuButtonAction(menuButton),
    )

    taskname_to_task_dict[newTask.taskName] = newTask


def startTask(label: Label, task: Task):
    task.timerRunning = True
    decrementTime(label, task)


def stopTask(label: Label, task: Task):
    task.timerRunning = False


def decrementTime(label: Label, task: Task):
    print("decrementTime called")
    if task.timerRunning and task.leftSeconds > 0:
        task.leftSeconds -= 1
        label.config(text=task.getLeftTimeStr())
        label.after(1000, decrementTime(label, task))


def setTime(label: Label, task: Task):
    dialog = TaskTimeDialog(label)
    task.leftSeconds = dialog.result
    label.config(text=task.getLeftTimeStr())


def renameTask(label: Label):
    global taskname_to_task_dict
    currentTaskName: str = label.cget("text")
    newTaskName: str = simpledialog.askstring("New Task Name", "Write New Task Name")
    if taskname_to_task_dict.get(newTaskName) is not None:
        messagebox.showerror("ERROR", "This Task Name is already used")
        return
    currentTask: Task = taskname_to_task_dict[currentTaskName]
    currentTask.rename(newTaskName)
    del taskname_to_task_dict[currentTaskName]
    taskname_to_task_dict[newTaskName] = currentTask
    label.config(text=newTaskName)


def deleteTask(frame: Frame, task: Task) -> None:
    global lastPushedTaskMenuButton
    frame.destroy()
    task.delete()
    del taskname_to_task_dict[task.taskName]
    lastPushedTaskMenuButton = None


def menuButtonAction(menuButton: Menubutton) -> None:
    global lastPushedTaskMenuButton
    lastPushedTaskMenuButton = menuButton


def _on_mousewheel(event) -> None:
    scrollRegion = taskListCanvas.cget("scrollregion")
    if scrollRegion == "":
        return
    scrollRegionList = [int(val) for val in scrollRegion.split()]
    visible_height = taskListCanvas.winfo_height()
    if (scrollRegionList[3] - scrollRegionList[1]) > visible_height:
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

taskListCanvas = Canvas(
    taskListFrame,
    width=TASK_LIST_FRAME_WIDTH,
    height=TASK_LIST_FRAME_HEIGHT,
)
taskListScrollbar = Scrollbar(
    taskListFrame,
    orient="vertical",
    command=taskListCanvas.yview,
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
addTaskButton = Button(menuFrame, text="add task", command=addTask)
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
