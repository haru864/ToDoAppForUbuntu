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
            sql: str = "SELECT * FROM task_type ORDER BY task_type_id"
            cursor.execute(sql)
            return [TaskType(*row) for row in cursor.fetchall()]

    def insertNewTaskType(self, taskTypeName: str) -> None:
        unusedId = self._getUnusedID()
        if unusedId is None:
            raise Exception(
                f"No more registrations (Upper limit of {TaskTypeDAO.MAX_TASK_TYPE_ID})"
            )
        with self.connection as conn:
            cursor = conn.cursor()
            sql: str = "INSERT INTO task_type VALUES (?, ?)"
            data = (unusedId, taskTypeName)
            cursor.execute(sql, data)
            self.connection.commit()

    def updateTaskTypeName(self, currTaskTypeName: str, newTaskTypeName: str) -> None:
        with self.connection as conn:
            cursor = conn.cursor()
            sql: str = (
                "UPDATE task_type SET task_type_name = ? WHERE task_type_name = ?"
            )
            data = (newTaskTypeName, currTaskTypeName)
            cursor.execute(sql, data)
            self.connection.commit()

    def deleteTaskType(self, taskTypeName: str) -> None:
        with self.connection as conn:
            cursor = conn.cursor()
            sql: str = "DELETE FROM task_type WHERE task_type_name = ?"
            data = (taskTypeName,)
            numOfDeletedRows = cursor.execute(sql, data).rowcount
            self.connection.commit()
        if numOfDeletedRows == 0:
            raise Exception("No target to delete")
        elif numOfDeletedRows > 1:
            raise Exception("One or more deleted")

    def _getUnusedID(self) -> Optional[int]:
        with self.connection as conn:
            cursor = conn.cursor()
            sql: str = "SELECT task_type_id FROM task_type"
            cursor.execute(sql)
            usedIdSet = cursor.fetchall()
        if len(usedIdSet) == TaskTypeDAO.MAX_TASK_TYPE_ID:
            return None
        for currId in range(1, TaskTypeDAO.MAX_TASK_TYPE_ID + 1):
            if (currId,) not in usedIdSet:
                return currId
        return None
