# celery_worker.py
from celery import Celery
from llmMessenger import predict
import logging
from celery import signals

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = Celery('tasks')
app.config_from_object('celery_config')


@app.task
def process_files_task(course_path, saved_files):
    if course_path is None or saved_files is None:
        logger.error("Received None values for course_path or saved_files")
        return "Error: Invalid input"
    try:
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
        predict(course_path, saved_files)
        return "Processing completed"
    except Exception as e:
        logger.exception(f"Error processing files: {str(e)}")
        return f"Error: {str(e)}"


@signals.task_prerun.connect
def task_prerun_handler(task_id, task, *args, **kwargs):
    print(f"Task {task_id} is about to run with args: {args} and kwargs: {kwargs}")


@signals.task_postrun.connect
def task_postrun_handler(task_id, task, *args, **retval):
    print(f"Task {task_id} completed with result: {retval}")
