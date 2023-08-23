import tkinter as tk
from tkinter import simpledialog, messagebox
from TaskType import TaskType
from TaskTypeDAO import TaskTypeDAO
import inspect


class TaskTypeDialog(simpledialog.Dialog):
    def __init__(self, master: tk.Widget) -> None:
        super().__init__(master, "Add Task Type")

    def body(self, master):
        self.taskTypeNameLabel = tk.Label(master, text="Task Type Name:")
        self.taskTypeNameLabel.grid(row=0, column=0)
        self.taskTypeNameEntry = tk.Entry(master)
        self.taskTypeNameEntry.grid(row=0, column=1)

    def validate(self) -> None:
        try:
            inputTaskTypeName: str = self.taskTypeNameEntry.get()
            taskTypeDAO = TaskTypeDAO("db/todo.db")
            registeredTaskType = taskTypeDAO.selectAll()
            registeredTaskTypeName = [
                taskType.task_type_name for taskType in registeredTaskType
            ]
            if inputTaskTypeName in registeredTaskTypeName:
                raise Exception("This name is already used")
            taskTypeDAO.insertNewTaskType(inputTaskTypeName)
            return True
        except Exception as e:
            print(f"{self.__class__}.{inspect.currentframe().f_code.co_name}: {e}")
            messagebox.showerror("ERROR", str(e))
            return False
