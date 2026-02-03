from datetime import datetime
from typing import Optional, Dict, List
from pydantic import BaseModel, Field
import uuid
from src.models.task import Task


class DAG(BaseModel):
    dag_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: Optional[str] = None
    tasks: Dict[str, Task] = Field(default_factory=dict)
    schedule_interval: Optional[str] = None
    
    def add_task(self, task: Task) -> None:
        self.tasks[task.task_id] = task
    
    def get_task(self, task_id: str) -> Optional[Task]:
        return self.tasks.get(task_id)
    
    def get_executable_tasks(self, completed_tasks: set[str]) -> List[Task]:
        executable = []
        for task in self.tasks.values():
            if task.task_id not in completed_tasks:
                deps_met = all(dep in completed_tasks for dep in task.dependencies)
                if deps_met:
                    executable.append(task)
        return executable
    
    def validate(self) -> bool:
        visited = set()
        rec_stack = set()
        
        def has_cycle(task_id: str) -> bool:
            visited.add(task_id)
            rec_stack.add(task_id)
            task = self.tasks.get(task_id)
            if not task:
                return False
            for dep in task.dependencies:
                if dep not in visited:
                    if has_cycle(dep):
                        return True
                elif dep in rec_stack:
                    return True
            rec_stack.remove(task_id)
            return False
        
        for task_id in self.tasks:
            if task_id not in visited:
                if has_cycle(task_id):
                    return False
        return True
    
    class Config:
        arbitrary_types_allowed = True
