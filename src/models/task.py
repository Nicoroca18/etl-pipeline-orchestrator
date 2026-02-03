from enum import Enum
from datetime import datetime
from typing import Optional, Callable, Any, Dict
from pydantic import BaseModel, Field
import uuid


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    RETRYING = "retrying"


class Task(BaseModel):
    task_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    callable_func: Callable
    dependencies: list[str] = Field(default_factory=list)
    max_retries: int = 3
    retry_delay: int = 60
    timeout: Optional[int] = None
    kwargs: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        arbitrary_types_allowed = True


class TaskExecution(BaseModel):
    execution_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    task_id: str
    dag_id: str
    status: TaskStatus = TaskStatus.PENDING
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    error_message: Optional[str] = None
    result: Optional[Any] = None
    attempt: int = 0
    
    class Config:
        arbitrary_types_allowed = True
