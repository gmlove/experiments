from typing import Callable, Dict

from celery import Celery, group
from celery.canvas import Signature

from scheduler import Scheduler


_app: Celery = None
_namespace: str = None
_retry_opts: Dict = None

DEFAULT_RETRY_OPTS = {
    'retry_backoff_max': 60,
    'retry_jitter': True,
    'retry_backoff': 1,
    'autoretry_for': (Exception, ),
    'retry_kwargs': {'max_retries': 5},
    'default_retry_delay': 2
}


def config(app: Celery, namespace: str, retry_opts: Dict = None):
    global _app, _namespace, _retry_opts
    _app = app
    _namespace = namespace
    _retry_opts = DEFAULT_RETRY_OPTS if retry_opts is None else retry_opts


class CeleryTask:

    def __init__(self, runnable: Callable, *args, **kwargs):
        task_name = '{}.{}'.format(_namespace, runnable.__name__)
        _task = _app.task(runnable, name=task_name, queue=task_name, **_retry_opts)
        self.task: Signature = _task.s(*args, **kwargs)

    def next(self, task: 'CeleryTask') -> 'CeleryTask':
        self.task = self.task | task.task
        return self

    def run_async(self, *args, **kwargs):
        self.task.apply_async(*args, **kwargs)


class CeleryGroupTask(CeleryTask):

    def __init__(self, *runnables: CeleryTask):
        self.task: Signature = group(runnable.task for runnable in runnables)

    def next(self, task: CeleryTask) -> CeleryTask:
        self.task = self.task | task.task
        return self


class CeleryScheduler(Scheduler):

    def __init__(self):
        super().__init__()
        self.task_impl = CeleryTask
        self.group_task_impl = CeleryGroupTask


celery_scheduler = CeleryScheduler()

__all__ = [
    'Celery', 'celery_scheduler', 'config', 'CeleryTask', 'CeleryGroupTask'
]
