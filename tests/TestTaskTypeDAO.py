import unittest
import sys

sys.path.append("/home/haru/project/ToDoApp")
sys.path.append("/home/haru/project/ToDoApp/src")

from src.TaskType import TaskType
from src.TaskTypeDAO import TaskTypeDAO


class TestTaskTypeDAO(unittest.TestCase):
    DB_PATH = "db/todo.db"
    REGISTRATION_NUMBER = 10

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.taskTypeDAO = TaskTypeDAO(TestTaskTypeDAO.DB_PATH)

    def test_1_insertNewTaskType(self):
        for n in range(1, TestTaskTypeDAO.REGISTRATION_NUMBER + 1):
            self.taskTypeDAO.insertNewTaskType(f"task_type_{str(n).zfill(2)}")

    def test_2_selectAll(self):
        selectedData = self.taskTypeDAO.selectAll()
        if len(selectedData) != TestTaskTypeDAO.REGISTRATION_NUMBER:
            raise Exception("num of selectedData is not enough")

    def test_3_updateTaskTypeName(self):
        for n in range(1, TestTaskTypeDAO.REGISTRATION_NUMBER + 1):
            self.taskTypeDAO.updateTaskTypeName(
                f"task_type_{str(n).zfill(2)}",
                f"task_type_{str(n).zfill(2)}_updated",
            )

    def test_4_deleteTaskType(self):
        for n in range(1, TestTaskTypeDAO.REGISTRATION_NUMBER + 1):
            self.taskTypeDAO.deleteTaskType(f"task_type_{str(n).zfill(2)}_updated")


if __name__ == "__main__":
    unittest.main()
