from abc import ABC, abstractmethod
from src.models.task import Task, TaskExecution


class BaseExecutor(ABC):
    @abstractmethod
    async def execute_task(self, task: Task, execution: TaskExecution) -> TaskExecution:
        pass
