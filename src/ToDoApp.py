from tkinter import *
from tkinter import ttk

taskList = []


def addNewTask():
    taskNumber = len(taskList) + 1
    newTaskButton = Button(innerTaskListFrame, text="Task " + str(taskNumber))
    newTaskButton.pack(fill=X)
    taskList.append(newTaskButton)


def _on_mousewheel(event):
    # canvasの現在のスクロール範囲を取得
    scrollregion = taskListCanvas.cget("scrollregion")

    if scrollregion == "":
        return

    scrollregion = [int(val) for val in scrollregion.split()]
    visible_height = taskListCanvas.winfo_height()  # taskListCanvasの可視領域の高さ

    # スクロール可能範囲とtaskListCanvasの可視領域の高さを比較
    if (scrollregion[3] - scrollregion[1]) > visible_height:
        # スクロールバーを操作
        if event.num == 4:
            taskListCanvas.yview_scroll(-1, "units")
        elif event.num == 5:
            taskListCanvas.yview_scroll(1, "units")


# ウィンドウを生成
root = Tk()
root.title("ToDoApp")
root.geometry("500x500")

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
helpButton = Button(menuFrame, text="help")
closeButton = Button(menuFrame, text="close", command=root.destroy)
addTaskButton.pack(side=TOP, pady=10)
helpButton.pack(side=TOP, pady=10)
closeButton.pack(side=TOP, pady=10)

# ウィンドウの表示
root.mainloop()
