# ETL Pipeline Orchestrator

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Production-ready task orchestrator for ETL pipelines with DAG support, async execution, and retry logic.

## Features

- **DAG-based workflows** - Define complex task dependencies
- **Async execution** - Parallel task execution with asyncio
- **Retry logic** - Automatic retries for failed tasks
- **Type safety** - Full Pydantic validation
- **Cycle detection** - Validates DAGs before execution

## Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Run example
python examples/basic_dag.py
```

## Example
```python
from src.models.dag import DAG
from src.models.task import Task
from src.scheduler.dag_scheduler import DAGScheduler

def my_task(**kwargs):
    return {"result": "success"}

dag = DAG(name="my_pipeline")
task = Task(name="my_task", callable_func=my_task)
dag.add_task(task)

scheduler = DAGScheduler()
scheduler.register_dag(dag)
await scheduler.execute_dag_now(dag.dag_id)
```

## Architecture

- **DAG**: Directed Acyclic Graph with cycle detection
- **Task**: Executable unit with retry/timeout config
- **Executor**: Runs tasks with error handling
- **Scheduler**: Orchestrates DAG execution

## License

MIT License
