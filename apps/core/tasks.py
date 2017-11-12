import logging
from celery.task import task
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

@task
def test_task():
    logger.info("I'm a task!")
