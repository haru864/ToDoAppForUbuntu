import tkinter as tk
from TaskType import TaskType
from TaskTypeDAO import TaskTypeDAO


class TaskTypeWindow:
    def __init__(self, master: tk.Widget) -> None:
        self.master = master
        self.window = tk.Toplevel(master=self.master)
        self.window.title("Task Type")
        x = master.winfo_x()
        y = master.winfo_y()
        self.window.geometry(f"+{x}+{y}")

        taskTypeDAO = TaskTypeDAO("db/todo.db")
        self.registeredTaskTypeList = taskTypeDAO.selectAll()
        print(self.registeredTaskTypeList)

        tk.Label(self.window, text="No").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self.window, text="Task Type").grid(row=0, column=1, padx=10, pady=5)

        for index, taskType in enumerate(self.registeredTaskTypeList):
            # print(str(index + 1) + ", " + taskType.task_type_name)
            task_type_name_var = tk.StringVar()
            task_type_name_var.set(taskType.task_type_name)
            tk.Label(master=self.window, text=index + 1).grid(
                row=index + 1, column=0, padx=10, pady=5
            )
            tk.Entry(master=self.window, textvariable=task_type_name_var).grid(
                row=index + 1, column=1, padx=10, pady=5
            )
