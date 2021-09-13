# -*- encoding=utf-8 -*-

import psutil

from task import AsyncTask, Task
from queue import ThreadSafeQueue
import threading

class ProcessThread(threading.Thread):
    def __init__(self, task_queue, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        # 线程停止标记，用set()方法进行停止标记
        self.dismiss_flag = threading.Event()
        # 任务队列（处理线程不断从队列取出元素处理）
        self.task_queue = task_queue
        self.args = args
        self.kwargs = kwargs

    # 重写了threading.thread里的run方法，在start()时候会调用
    def run(self):

        while True:
            # 判断线程是否被要求停止
            if self.dismiss_flag.is_set():
                break
            task = self.task_queue.pop()
            # 如果任务队列中弹出来的不是任务对象Task，不是的话继续弹出下一个任务
            if not isinstance(task, Task):
                continue
            # 执行task的实际逻辑（通过函数调用引进来的）
            result = task.callable(*task.args, **task.kwargs)
            # 如果是异步任务就将结果传入set_result中，之后可以用get_result取出
            if isinstance(task, AsyncTask):
                task.set_result(result)

    def dismiss(self):
        self.dismiss_flag.set()
    
    def stop(self):
        self.dismiss()


# 线程池
class ThreadPool:
    def __init__(self, size=0) -> None:
        if not size:
            # 约定线程池大小为CPU核数的两倍（最佳实践）
            size = psutil.cpu_count()*2
        # 用线程安全的queue建立一个线程池（现在只是一个线程安全的队列，还没有传入线程）
        self.pool = ThreadSafeQueue(size)
        # 用线程安全的queue建立一个任务队列实例
        self.task_queue = ThreadSafeQueue()

        # 将任务队列绑定线程实例传入到线程池内
        for i in range(size):
            self.pool.put(ProcessThread(self.task_queue))

    # 开启线程池内所有线程
    def start(self):
        for i in range(self.pool.size()):
            thread = self.pool.get(i)
            thread.start()

    # 停止线程池内所有线程
    def join(self):
        for i in range(self.pool.size()):
            thread = self.pool.get(i)
            thread.stop()
        # 线程不为空时，将线程POP出来，等待线程真正的停止
        while self.pool.size():
            thread = self.pool.pop()
            thread.join()
        
    # 往线程池提交任务
    def put(self, item):
        if not isinstance(item, Task):
            raise TaskTypeErrorException("任务提交失败")
        self.task_queue.put(item)
        

    def batch_put(self, li):
        if not isinstance(li, list):
            raise TaskTypeErrorException("任务批量提交失败")
        for item in li:
            self.put(item)

    def size(self):
        # pool是线程安全的队列，所以不需要互斥锁
        return self.pool.size()

class TaskTypeErrorException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.args = args

    def __str__(self) -> str:
        print("操作异常，",self.args)