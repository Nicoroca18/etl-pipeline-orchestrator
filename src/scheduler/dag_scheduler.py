import asyncio
from typing import Dict, Set
from src.models.dag import DAG
from src.models.task import TaskExecution, TaskStatus
from src.executor.local_executor import LocalExecutor
from src.utils.logger import logger


class DAGScheduler:
    def __init__(self):
        self.executor = LocalExecutor()
        self.dags: Dict[str, DAG] = {}
    
    def register_dag(self, dag: DAG) -> None:
        if not dag.validate():
            raise ValueError(f"DAG {dag.name} is invalid")
        self.dags[dag.dag_id] = dag
    
    async def execute_dag_now(self, dag_id: str):
        dag = self.dags.get(dag_id)
        if not dag:
            raise ValueError(f"DAG {dag_id} not found")
        
        logger.info(f"Starting DAG: {dag.name}")
        
        completed_tasks: Set[str] = set()
        
        while len(completed_tasks) < len(dag.tasks):
            executable_tasks = dag.get_executable_tasks(completed_tasks)
            
            if not executable_tasks:
                break
            
            tasks_to_run = []
            for task in executable_tasks:
                execution = TaskExecution(task_id=task.task_id, dag_id=dag_id)
                tasks_to_run.append(self.executor.execute_task(task, execution))
            
            results = await asyncio.gather(*tasks_to_run)
            
            for i, result in enumerate(results):
                if result.status == TaskStatus.SUCCESS:
                    completed_tasks.add(executable_tasks[i].task_id)
        
        logger.info(f"DAG {dag.name} completed")
