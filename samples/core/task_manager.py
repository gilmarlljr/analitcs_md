import abc
import asyncio
import sched
import threading
import time


class Task(threading.Thread, metaclass=abc.ABCMeta):
    def __init__(self):
        super(Task, self).__init__()

    @abc.abstractmethod
    def interval(self):
        return 1.0

    @abc.abstractmethod
    def execute(self):
        return

    def run(self):
        ticker = threading.Event()
        running = True
        while running:
            self.execute()
            running = not ticker.wait(self.interval())


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
            task.start()

        self.ioloop.run_forever()
