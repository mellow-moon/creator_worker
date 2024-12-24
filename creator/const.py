from dataclasses import dataclass


@dataclass(frozen=True)
class Queue:
    CREATE: str = "create_queue"
    START: str = "start_queue"
    ONE_TASK: str = "one_task_queue"
    ALL_TASK: str = "all_task_queue"
