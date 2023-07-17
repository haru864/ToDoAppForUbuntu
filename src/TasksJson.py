from typing import Optional
from Task import Task
import json


class TasksJson:
    def __init__(self) -> None:
        self.registeredTasksList: list[Task] = []
        self.isSynchronizedWithTasksJsonFile: bool = False

    def addTask(self, task: Optional[Task | None]) -> None:
        if task is None:
            return
        self.registeredTasksList.append(task)

    def loadTasksJson(self) -> None:
        data = None
        with open("setting/tasks.json", "r") as taskJson:
            data = json.load(taskJson)
        if data is None or isinstance(data, list) == False:
            self.registeredTasksList = []
            self.isSynchronizedWithTasksJsonFile = False
            return
        for currDict in data:
            try:
                task = Task(
                    taskName=currDict["taskName"],
                    leftSeconds=int(currDict["leftSeconds"]),
                )
                self.registeredTasksList.append(task)
            except Exception as e:
                print(f"TasksJson.loadTasksJson() -> {e}")
                self.registeredTasksList = []
                self.isSynchronizedWithTasksJsonFile = False
                return
        self.isSynchronizedWithTasksJsonFile = True

    def saveRegisteredTasks(self) -> None:
        taskInfoList: list[dict] = []
        for i in len(self.registeredTasksList):
            task: Task = self.registeredTasksList[i]
            taskInfo: dict = {}
            taskInfoList["taskName"] = task.taskName
            taskInfoList["leftSeconds"] = task.leftSeconds
            taskInfoList.append(taskInfo)
        if len(taskInfoList) == 0:
            return
        with open("setting/tasks.json", "w") as taskJson:
            json.dump(taskInfoList, TasksJson)
        self.isSynchronizedWithTasksJsonFile = True

    def __str__(self) -> str:
        return str(self.registeredTasksList)
