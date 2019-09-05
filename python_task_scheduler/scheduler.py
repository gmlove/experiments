from typing import Callable, List, Union, ClassVar


class Task(object):

    def __init__(self, runnable: Callable, *args):
        pass

    def next(self, task: 'Task') -> 'Task':
        raise NotImplemented()

    def run_async(self, *args, **kwargs):
        raise NotImplemented()


class GroupTask(Task):

    def __init__(self, *runnables: Task):
        super().__init__(None)


def task(runnable: Callable, *args, **kwargs) -> Task:
    return _impl.task_impl(runnable, *args, **kwargs)


def group(*runnables: Task) -> Task:
    return _impl.group_task_impl(*runnables)


class Scheduler(object):

    def __init__(self):
        self.task_impl: ClassVar[Task] = None
        self.group_task_impl: ClassVar[GroupTask] = None


_impl: Scheduler = None


def use(impl: Scheduler):
    global _impl
    _impl = impl


__all__ = [
    'use', 'task', 'group'
]
