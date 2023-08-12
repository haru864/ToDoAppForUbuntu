from typing import Optional
from Task import Task
import json
import copy


class TasksJson:
    def __init__(self) -> None:
        self.registeredTasksList: list[Task] = []
        self.isSynchronizedWithTasksJsonFile: bool = False
        self.loadTasksJson()

    def getNumOfTasksRegisteredInJson(self) -> int:
        return len(self.registeredTasksList)

    def isRegisteredTaskName(self, taskName: str) -> bool:
        for task in self.registeredTasksList:
            if taskName == task.taskName:
                return True
        return False

    def addTaskToTasksJson(self, task: Optional[Task | None]) -> None:
        if task is None:
            return
        self.registeredTasksList.append(task)
        self.saveRegisteredTasks()
        self.loadTasksJson()

    def updateTaskList(self, newtasklist: Optional[list[Task] | None]):
        if newtasklist is None:
            return
        self.registeredTasksList = copy.copy(newtasklist)
        self.saveRegisteredTasks()

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
        try:
            taskInfoDictList: list[dict] = []
            for cueeTask in self.registeredTasksList:
                taskInfoDict: dict = {}
                taskInfoDict["taskName"] = cueeTask.taskName
                taskInfoDict["leftSeconds"] = cueeTask.leftSeconds
                taskInfoDictList.append(taskInfoDict)
            if len(taskInfoDictList) == 0:
                return
            with open("setting/tasks.json", "w") as taskJson:
                json.dump(taskInfoDictList, taskJson)
            self.isSynchronizedWithTasksJsonFile = True
        except Exception as e:
            print(f"TasksJson.saveRegisteredTasks() -> {e}")
            raise e

    def __str__(self) -> str:
        return str(self.registeredTasksList)
