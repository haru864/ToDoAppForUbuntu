from typing import Optional
from Task import Task
import json
import copy


class TasksJson:
    def __init__(self) -> None:
        self.registeredTasksList: list[Task] = []

    def addTask(self, task: Optional[Task]) -> None:
        if task is None:
            return
        self.registeredTasksList.append(task)

    def loadTasksJson(self) -> None:
        data = None
        with open("setting/tasks.json", "r") as taskJson:
            data = json.load(taskJson)
        if data is None or isinstance(data, list) == False:
            self.registeredTasksList = []
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
                return

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

    def __str__(self) -> str:
        retval: str = "["
        retval += "]"
        print(type(self.registeredTasksList[0]))
        print(self.registeredTasksList[0])
        return str(self.registeredTasksList)
