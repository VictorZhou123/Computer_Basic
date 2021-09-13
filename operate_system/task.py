# -*- encoding=utf-8 -*-

from threading import Thread
import threading
import uuid

class Task:
    def __init__(self, func, *args, **kwargs) -> None:
        # 任务的具体逻辑，通过函数引用传递进来
        self.id = uuid.uuid4()
        self.callable = func
        self.args = args
        self.kwargs = kwargs

    def __str__(self) -> str:
        return 'Task id:' + str(self.id)

class AsyncTask(Task):
    def __init__(self, func, *args, **kwargs) -> None:
        super().__init__(func, *args, **kwargs)
        self.result = None
        self.condition = threading.Condition()

    def set_result(self, result):
        self.condition.acquire()
        self.result = result
        self.condition.notify()
        self.condition.release()

    def get_result(self):
        self.condition.acquire()
        if not self.result:
            self.condition.wait()
        result = self.result
        self.condition.release()
        return result

def my_fuction():
    print("this is function test information...")

if __name__ == '__main__':
    task = Task(my_fuction)
    print(task)