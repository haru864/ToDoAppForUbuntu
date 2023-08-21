class TaskType:
    def __init__(self, task_type_id: int, task_type_name: str) -> None:
        self.task_type_id = task_type_id
        self.task_type_name = task_type_name

    def __str__(self) -> str:
        return f"{{(task_type_id){self.task_type_id}, (task_type_name){self.task_type_name}}}"

    def __repr__(self) -> str:
        return f"TaskType({self.task_type_id}, {self.task_type_name})"
