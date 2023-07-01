from typing import Final


class Task:
    MAX_NUM_OF_TASKS: Final[int] = 10
    NUM_OF_USED_TASK_ID: int = 0
    TASK_ID_POOL: bool = [False for i in range(MAX_NUM_OF_TASKS)]

    def __init__(self, taskName: str, leftSeconds: int) -> None:
        self.taskId: int = self.getTaskID()
        print(f"taskId: {self.taskId}")
        if self.taskId is None:
            raise Exception("Cannot register any more tasks")
        self.taskName: str = taskName
        self.leftSeconds: int = leftSeconds

    def getTaskID(self) -> int:
        if Task.NUM_OF_USED_TASK_ID >= Task.MAX_NUM_OF_TASKS:
            return None
        for i in range(Task.MAX_NUM_OF_TASKS):
            newTaskID: int = i
            if Task.TASK_ID_POOL[newTaskID] == False:
                Task.TASK_ID_POOL[newTaskID] = True
                Task.NUM_OF_USED_TASK_ID += 1
                print(f"newTaskID: {newTaskID}")
                return newTaskID
        return None

    def rename(self, newTaskName: str):
        self.taskName = newTaskName

    def delete(self):
        Task.NUM_OF_USED_TASK_ID -= 1
        Task.TASK_ID_POOL[self.taskId] = False
