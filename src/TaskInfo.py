class TaskInfo:
    def __init__(
        self,
        task_name: str,
        registered_at: str,
        task_type_id: int,
        is_completed: bool,
        difficulty: int,
        total_elapsed_time_seconds: int,
        remaining_time_seconds: int,
    ) -> None:
        self.task_name = task_name
        self.registered_at = registered_at
        self.task_type_id = task_type_id
        self.is_completed = is_completed
        self.difficulty = difficulty
        self.total_elapsed_time_seconds = total_elapsed_time_seconds
        self.remaining_time_seconds = remaining_time_seconds
