import asyncio
from src.models.dag import DAG
from src.models.task import Task
from src.scheduler.dag_scheduler import DAGScheduler
from src.utils.logger import logger


def extract_data(**kwargs):
    logger.info("Extracting data...")
    return {"records": 1000}


async def transform_data(**kwargs):
    logger.info("Transforming data...")
    await asyncio.sleep(1)
    return {"transformed": 950}


def load_data(**kwargs):
    logger.info("Loading data...")
    return {"loaded": True}


async def main():
    dag = DAG(name="etl_pipeline", description="Basic ETL example")
    
    extract_task = Task(name="extract", callable_func=extract_data)
    transform_task = Task(name="transform", callable_func=transform_data, dependencies=[extract_task.task_id])
    load_task = Task(name="load", callable_func=load_data, dependencies=[transform_task.task_id])
    
    dag.add_task(extract_task)
    dag.add_task(transform_task)
    dag.add_task(load_task)
    
    scheduler = DAGScheduler()
    scheduler.register_dag(dag)
    
    await scheduler.execute_dag_now(dag.dag_id)
    print("\n✅ Pipeline completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())
