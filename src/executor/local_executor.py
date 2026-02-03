import asyncio
from datetime import datetime
from src.executor.base import BaseExecutor
from src.models.task import Task, TaskExecution, TaskStatus
from src.utils.logger import logger


class LocalExecutor(BaseExecutor):
    async def execute_task(self, task: Task, execution: TaskExecution) -> TaskExecution:
        execution.status = TaskStatus.RUNNING
        execution.start_time = datetime.now()
        execution.attempt += 1
        
        logger.info(f"Executing task {task.name}")
        
        try:
            if task.timeout:
                result = await asyncio.wait_for(
                    self._run_callable(task),
                    timeout=task.timeout
                )
            else:
                result = await self._run_callable(task)
            
            execution.status = TaskStatus.SUCCESS
            execution.result = result
            execution.end_time = datetime.now()
            logger.info(f"Task {task.name} completed")
            
        except Exception as e:
            execution.status = TaskStatus.FAILED
            execution.error_message = str(e)
            execution.end_time = datetime.now()
            logger.error(f"Task {task.name} failed: {e}")
        
        return execution
    
    async def _run_callable(self, task: Task):
        if asyncio.iscoroutinefunction(task.callable_func):
            return await task.callable_func(**task.kwargs)
        else:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, lambda: task.callable_func(**task.kwargs))
