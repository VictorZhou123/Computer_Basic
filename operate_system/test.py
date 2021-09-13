# -*- encoding=utf-8 -*-

from pool import ThreadPool
from task import Task, AsyncTask
import time

class SimpleTask(Task):
    def __init__(self, callable) -> None:
        super().__init__(callable)

def process():
    print('this is a SimpleTask callable function')
    time.sleep(1)

def test():
    # 初始化一个线程池
    test_pool = ThreadPool()
    test_pool.start()
    # 生成一系列的任务
    for i in range(10):
        simpletask = SimpleTask(process)
        # 往线程池提交任务执行
        test_pool.put(simpletask)
    test_pool.join()

def async_task():
    def async_process():
        num = 0
        for i in range(100):
            num += i
        time.sleep(1)
        return num

    # 初始化一个线程池
    test_pool = ThreadPool()
    test_pool.start()
    # 生成一系列的任务
    for i in range(10):
        async_task = AsyncTask(func = async_process)
        # 往线程池提交任务执行
        test_pool.put(async_task)
        result = async_task.get_result()
        print("Get result:%d" %result)
    test_pool.join()



if __name__ == "__main__":
    async_task()