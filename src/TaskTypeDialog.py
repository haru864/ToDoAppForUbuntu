import tkinter as tk
from tkinter import simpledialog, messagebox
from TaskType import TaskType
from TaskTypeDAO import TaskTypeDAO
import inspect
from typing import Optional


class TaskTypeDialog(simpledialog.Dialog):
    EDIT_MODE: str = "edit"
    ADD_MODE: str = "add"

    def __init__(
        self, master: tk.Widget, mode: str, currentTaskTypeName: Optional[str] = None
    ) -> None:
        self.mode = mode
        self.currentTaskTypeName = currentTaskTypeName
        if self.mode == TaskTypeDialog.EDIT_MODE:
            if self.currentTaskTypeName == None:
                messagebox.showerror("ERROR", "Specify current task type name")
                return
            windowTitle: str = "Edit Task Type Name"
        elif self.mode == TaskTypeDialog.ADD_MODE:
            windowTitle: str = "Add Task Type"
        super().__init__(parent=master, title=windowTitle)

    def body(self, master):
        self.taskTypeNameLabel = tk.Label(master, text="Task Type Name:")
        self.taskTypeNameLabel.grid(row=0, column=0)
        self.taskTypeNameEntry = tk.Entry(master)
        self.taskTypeNameEntry.grid(row=0, column=1)

    def validate(self) -> None:
        try:
            inputTaskTypeName: str = self.taskTypeNameEntry.get()
            self._checkTaskTypeName(inputTaskTypeName)
            taskTypeDAO = TaskTypeDAO("db/todo.db")
            if self.mode == TaskTypeDialog.EDIT_MODE:
                taskTypeDAO.updateTaskTypeName(
                    currTaskTypeName=self.currentTaskTypeName,
                    newTaskTypeName=inputTaskTypeName,
                )
            elif self.mode == TaskTypeDialog.ADD_MODE:
                taskTypeDAO.insertNewTaskType(inputTaskTypeName)
            return True
        except Exception as e:
            print(f"{self.__class__}.{inspect.currentframe().f_code.co_name}: {e}")
            messagebox.showerror("ERROR", str(e))
            return False

    def _checkTaskTypeName(self, taskTypeName: str) -> None:
        if taskTypeName == "" or taskTypeName is None:
            raise Exception("Task type name must have one or more characters")
        taskTypeDAO = TaskTypeDAO("db/todo.db")
        registeredTaskType = taskTypeDAO.selectAll()
        registeredTaskTypeName = [
            taskType.task_type_name for taskType in registeredTaskType
        ]
        if taskTypeName in registeredTaskTypeName:
            raise Exception("This name is already used")
