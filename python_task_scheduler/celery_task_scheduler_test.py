import unittest
from typing import List
import time
import random

from scheduler import use, task, group


def define_tasks():
    def t1(x):
        time.sleep(random.randint(0, 5))
        if random.random() < 0.5:
            raise Exception('simulated exception')
        return x + 1

    def t2(x):
        time.sleep(random.randint(0, 5))
        if random.random() < 0.5:
            raise Exception('simulated exception')
        return x + 2

    def t3(x: List[int]):
        time.sleep(random.randint(0, 5))
        if random.random() < 0.5:
            raise Exception('simulated exception')
        return sum(x) + 3

    def t4(x):
        time.sleep(random.randint(0, 5))
        if random.random() < 0.5:
            raise Exception('simulated exception')
        return x + 4

    def t5(x: List[int]):
        time.sleep(random.randint(0, 5))
        if random.random() < 0.5:
            raise Exception('simulated exception')
        return sum(x) + 5

    return [t1, t2, t3, t4, t5]


def prepare_celery_tasks():
    for run in define_tasks():
        task(run)


def schedule_tasks():
    t1, t2, t3, t4, t5 = define_tasks()

    # t1: 1 + 1, t2: 2 + 2, t3: sum([t1, t2]) + 3, t4: 4 + 4, t5: sum([t3, t4]) + 5 -> 22
    t__1x2_3 = group(task(t1, 1), task(t2, 2)).next(task(t3))
    t__1x2_3__x4_5 = group(t__1x2_3, task(t4, 4)).next(task(t5))
    t__1x2_3__x4_5.run_async()

    # we must chain a task after a group to aggregate result into one, then group the aggregated tasks, or celery will schedule N x M tasks  # noqa
    group(
        # task(t1, 1).next(group(task(t1), task(t2))),   # don't end with group like this
        # task(t1, 1).next(group(task(t1), task(t2))),   # don't end with group like this
        task(t1, 1).next(group(task(t1), task(t2))).next(task(t3)),
        task(t1, 1).next(group(task(t1), task(t2))).next(task(t3)),
    )\
        .next(task(t3))\
        .run_async()   # result: 23


def config_celery_scheduler():
    from celery_impl import Celery, config, celery_scheduler
    celery_app = Celery('test', broker='pyamqp://admin:admin@localhost:5672/', backend='redis://localhost/2')
    config(celery_app, 'test_task_scheduler')
    use(celery_scheduler)
    return celery_app


class CelerySchedulingTest(unittest.TestCase):

    @unittest.skip('integration test')
    def test_task_scheduling(self):
        # To run this test, we need to start celery worker beforehand.
        # 1. Run command `celery -A celery_app_test worker -Q test_task_scheduler.t1,test_task_scheduler.t2,test_task_scheduler.t3,test_task_scheduler.t4,test_task_scheduler.t5 --loglevel=info`  # noqa
        # 2. Start this test.
        # 3. Check the task execution output in step 1
        config_celery_scheduler()
        schedule_tasks()
