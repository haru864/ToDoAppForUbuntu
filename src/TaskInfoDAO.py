import sqlite3
from TaskInfo import TaskInfo


class TaskInfoDAO:
    def __init__(self, dbPath: str) -> None:
        self.connection = sqlite3.connect(database=dbPath)

    def getIncompleteTaskInfo(self):
        with self.connection as conn:
            cursor = conn.cursor()
            sql: str = "SELECT * FROM task_info WHERE is_completed = 0"
            cursor.execute(sql)
            return [TaskInfo(*row) for row in cursor.fetchall()]
