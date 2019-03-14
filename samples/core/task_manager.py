import abc
import asyncio
import sched
import time


class Task(metaclass=abc.ABCMeta):
    def __init__(self):
        self.scheduler = sched.scheduler(time.time, time.sleep)

    @abc.abstractmethod
    def interval(self):
        return 1.0

    @abc.abstractmethod
    def execute(self):
        return

    @asyncio.coroutine
    def run_task(self):
        self.execute()
        yield from asyncio.sleep(self.interval())


class TaskManager:
    def __init__(self, task_list=None):
        if task_list is None:
            task_list = []
        self.task_list = task_list
        self.ioloop = asyncio.get_event_loop()  # Event Loop

    def append(self, task: Task):
        self.task_list.append(task)

    def execute(self):
        async_task = []
        for task in self.task_list:
            async_task.append(self.ioloop.create_task(task.run_task()))
        wait_tasks = asyncio.wait(async_task)
        self.ioloop.run_until_complete(wait_tasks)
        self.execute()
        self.ioloop.close()
