from tkinter import *
from tkinter import ttk
from typing import Final

MAIN_WINDOW_TITLE: Final = "ToDoApp"
MAIN_WINDOW_SIZE: Final = "500x500"
USAGE_WINDOW_SIZE: Final = "400x400"

taskList = []
usageWindow = None


def centerWindow(window):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (window.winfo_width() // 2)
    y = (screen_height // 2) - (window.winfo_height() // 2)
    window.geometry(f"+{x}+{y}")


def addNewTask():
    taskNumber = len(taskList) + 1
    newTaskButton = Button(innerTaskListFrame, text="Task " + str(taskNumber))
    newTaskButton.pack(fill=X)
    taskList.append(newTaskButton)


def _on_mousewheel(event):
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


def displayUsage():
    global usageWindow
    if usageWindow is None or not Toplevel.winfo_exists(usageWindow):
        usageWindow = Toplevel()
        usageWindow.title("usage")
        Label(usageWindow, text="hello, world!").pack()
    usageWindow.geometry(USAGE_WINDOW_SIZE)
    centerWindow(usageWindow)
    usageWindow.lift()


# ウィンドウを生成
root = Tk()
root.title(MAIN_WINDOW_TITLE)
root.geometry(MAIN_WINDOW_SIZE)
centerWindow(root)

taskListFrame = Frame(root, width=300, height=300, borderwidth=2, relief="solid")
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
closeButton = Button(menuFrame, text="close", command=root.destroy)
addTaskButton.pack(side=TOP, pady=10)
usageButton.pack(side=TOP, pady=10)
closeButton.pack(side=TOP, pady=10)

# ウィンドウの表示
root.mainloop()
