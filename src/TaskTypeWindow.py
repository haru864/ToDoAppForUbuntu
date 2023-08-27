import tkinter as tk
from TaskType import TaskType
from TaskTypeDAO import TaskTypeDAO
from TaskTypeDialog import TaskTypeDialog


class TaskTypeWindow:
    def __init__(self, master: tk.Widget) -> None:
        self.master = master
        self.window = tk.Toplevel(master=self.master)
        self.window.title("Task Type")
        x = master.winfo_x()
        y = master.winfo_y()
        self.window.geometry(f"+{x}+{y}")
        self.taskTypeDAO = TaskTypeDAO("db/todo.db")
        self.displayContents()

    def displayContents(self):
        for child in self.window.winfo_children():
            child.destroy()

        self.registeredTaskTypeList = self.taskTypeDAO.selectAll()
        # print(self.registeredTaskTypeList)

        tk.Label(self.window, text="No").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self.window, text="Task Type").grid(row=0, column=1, padx=10, pady=5)
        self.numberToTaskType: dict[int, TaskType] = {}

        for index, taskType in enumerate(self.registeredTaskTypeList):
            # print(str(index + 1) + ", " + taskType.task_type_name)
            task_type_name_var = tk.StringVar()
            task_type_name_var.set(taskType.task_type_name)
            itemNumber = index + 1
            tk.Label(master=self.window, text=index + 1).grid(
                row=itemNumber, column=0, padx=10, pady=5
            )
            tk.Label(master=self.window, textvariable=task_type_name_var).grid(
                row=itemNumber, column=1, padx=10, pady=5
            )
            tk.Button(
                master=self.window,
                text="Edit",
                command=lambda itemNumber=itemNumber: self.editTaskType(itemNumber),
            ).grid(row=itemNumber, column=2, padx=10, pady=5)
            tk.Button(
                master=self.window,
                text="Delete",
                command=lambda itemNumber=itemNumber: self.deleteTaskType(itemNumber),
            ).grid(row=itemNumber, column=3, padx=10, pady=5)
            self.numberToTaskType[itemNumber] = taskType

        tk.Button(master=self.window, text="Add Type", command=self.addTaskType).grid(
            row=21, column=1, padx=10, pady=5
        )
        tk.Button(master=self.window, text="Close", command=self.close).grid(
            row=21, column=2, padx=10, pady=5
        )

    def editTaskType(self, itemNumber: int):
        TaskTypeDialog(
            master=self.window,
            mode=TaskTypeDialog.EDIT_MODE,
            currentTaskTypeName=self.numberToTaskType[itemNumber].task_type_name,
        )
        self.displayContents()

    def deleteTaskType(self, itemNumber: int):
        self.taskTypeDAO.deleteTaskType(
            self.numberToTaskType[itemNumber].task_type_name
        )
        self.displayContents()

    def addTaskType(self):
        TaskTypeDialog(master=self.window, mode=TaskTypeDialog.ADD_MODE)
        self.displayContents()

    def save(self):
        pass

    def close(self):
        self.window.destroy()
