from typing import Optional
from Task import Task
import json
import copy


class TasksJson:
    def __init__(self) -> None:
        self.registeredTasksList: list[Task] = []
        self.isSynchronizedWithTasksJsonFile: bool = False
        self._loadTasksJson()

    def getNumOfTasksRegisteredInJson(self) -> int:
        return len(self.registeredTasksList)

    def isRegisteredTaskName(self, taskName: str) -> bool:
        for task in self.registeredTasksList:
            if taskName == task.taskName:
                return True
        return False

    def deleteTaskFromTasksJson(self, taskName: str) -> bool:
        self._loadTasksJson()
        for i in range(len(self.registeredTasksList)):
            if self.registeredTasksList[i].taskName == taskName:
                del self.registeredTasksList[i]
                break
        self._saveRegisteredTasks()

    def renameTask(self, currTaskName: str, newTaskName: str) -> None:
        self._loadTasksJson()
        for task in self.registeredTasksList:
            if task.taskName == currTaskName:
                task.rename(newTaskName)
                break
        self._saveRegisteredTasks()

    def updateTaskTime(self, targetTaskName: str, newTaskTimeSeconds: int) -> None:
        self._loadTasksJson()
        for task in self.registeredTasksList:
            if task.taskName == targetTaskName:
                task.leftSeconds = newTaskTimeSeconds
                break
        self._saveRegisteredTasks()

    def addTaskToTasksJson(self, task: Optional[Task | None]) -> None:
        if task is None:
            return
        self.registeredTasksList.append(task)
        self._saveRegisteredTasks()
        self._loadTasksJson()

    def updateTaskList(self, newtasklist: Optional[list[Task] | None]):
        if newtasklist is None:
            return
        self.registeredTasksList = copy.copy(newtasklist)
        self._saveRegisteredTasks()

    def _loadTasksJson(self) -> None:
        self.registeredTasksList.clear()
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
                print(f"TasksJson._loadTasksJson() -> {e}")
                self.registeredTasksList = []
                self.isSynchronizedWithTasksJsonFile = False
                return
        self.isSynchronizedWithTasksJsonFile = True

    def _saveRegisteredTasks(self) -> None:
        try:
            taskInfoDictList: list[dict] = []
            for task in self.registeredTasksList:
                taskInfoDict: dict = {}
                taskInfoDict["taskName"] = task.taskName
                taskInfoDict["leftSeconds"] = task.leftSeconds
                taskInfoDictList.append(taskInfoDict)
            with open("setting/tasks.json", "w") as taskJson:
                json.dump(taskInfoDictList, taskJson)
            self.isSynchronizedWithTasksJsonFile = True
        except Exception as e:
            print(f"TasksJson._saveRegisteredTasks() -> {e}")
            raise e

    def __str__(self) -> str:
        return str(self.registeredTasksList)
