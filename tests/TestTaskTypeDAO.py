import unittest
import sys

sys.path.append("/home/haru/project/ToDoApp")
sys.path.append("/home/haru/project/ToDoApp/src")

from src.TaskType import TaskType
from src.TaskTypeDAO import TaskTypeDAO


class TestTaskTypeDAO(unittest.TestCase):
    DB_PATH = "db/todo.db"

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    def test_1_insertNewTaskType(self):
        taskTypeDAO = TaskTypeDAO(TestTaskTypeDAO.DB_PATH)
        self.assertTrue(taskTypeDAO.insertNewTaskType("task_type_01"))

    def test_2_selectAll(self):
        taskTypeDAO = TaskTypeDAO(TestTaskTypeDAO.DB_PATH)
        self.assertTrue(taskTypeDAO.selectAll())

    def test_3_updateTaskTypeName(self):
        taskTypeDAO = TaskTypeDAO(TestTaskTypeDAO.DB_PATH)
        insertedTaskType = TaskType(1, "task_type_01")
        self.assertTrue(
            taskTypeDAO.updateTaskTypeName(insertedTaskType, "task_type_01_updated")
        )

    def test_4_deleteTaskType(self):
        taskTypeDAO = TaskTypeDAO(TestTaskTypeDAO.DB_PATH)
        updatedTaskType = TaskType(1, "task_type_01_updated")
        self.assertTrue(taskTypeDAO.deleteTaskType(updatedTaskType))


if __name__ == "__main__":
    unittest.main()
