from tkinter import *
from tkinter import ttk

taskList = []


def addNewTask():
    taskNumber = len(taskList) + 1
    newTaskButton = Button(innerTaskListFrame, text="Task ")
    newTaskButton.pack(fill=X)
    taskList.append(newTaskButton)


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

# メニューにボタンを設置
addTaskButton = Button(menuFrame, text="add task", command=addNewTask)
helpButton = Button(menuFrame, text="help")
closeButton = Button(menuFrame, text="close", command=root.destroy)
addTaskButton.pack(side=TOP, pady=10)
helpButton.pack(side=TOP, pady=10)
closeButton.pack(side=TOP, pady=10)

# ウィンドウの表示
root.mainloop()
