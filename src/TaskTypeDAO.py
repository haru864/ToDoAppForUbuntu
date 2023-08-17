from typing import Optional
import sqlite3
from TaskType import TaskType


class TaskTypeDAO:
    MAX_TASK_TYPE_ID = 20

    def __init__(self, dbPath: str) -> None:
        self.connection = sqlite3.connect(database=dbPath)

    def selectAll(self) -> list[TaskType]:
        with self.connection as conn:
            cursor = conn.cursor()
            sql: str = "SELECT * FROM task_type"
            cursor.execute(sql)
            return [TaskType(*row) for row in cursor.fetchall()]

    def insertNewTaskType(self, taskTypeName: str) -> bool:
        unusedId = self._getUnusedID()
        if not unusedId:
            return False
        with self.connection as conn:
            cursor = conn.cursor()
            sql: str = "INSERT INTO task_type VALUES (?, ?)"
            data = [unusedId, taskTypeName]
            cursor.execute(sql, data)
            self.connection.commit()
        return True

    def updateTaskTypeName(
        self, currTaskType: TaskType, newTaskTypeName: str
    ) -> Optional[TaskType]:
        with self.connection as conn:
            cursor = conn.cursor()
            sql: str = (
                "UPDATE task_type SET task_type_name = ? WHERE task_type_id = ?"
            )
            data = [newTaskTypeName, currTaskType.task_type_id]
            cursor.execute(sql, data)
            self.connection.commit()
        updatedTaskType = TaskType(currTaskType.task_type_id, newTaskTypeName)
        return updatedTaskType

    def deleteTaskType(self, taskType: TaskType) -> bool:
        deletedRows = 0
        with self.connection as conn:
            cursor = conn.cursor()
            sql: str = "DELETE FROM task_type WHERE task_type_id = ?"
            data = [taskType.task_type_id]
            deletedRows = cursor.execute(sql, data).rowcount
            self.connection.commit()
        if deletedRows != 1:
            return False
        return True

    def _getUnusedID(self) -> Optional[int]:
        with self.connection as conn:
            cursor = conn.cursor()
            sql: str = "SELECT task_type_id FROM task_type"
            cursor.execute(sql)
            usedIdSet: set[int] = set([id for id in cursor.fetchall()])
        if len(usedIdSet) == TaskTypeDAO.MAX_TASK_TYPE_ID:
            return None
        for currId in range(1, TaskTypeDAO.MAX_TASK_TYPE_ID + 1):
            if currId not in usedIdSet:
                return currId
        return None
