# -*- encoding=utf-8 -*-

import threading

import random, time

class ThreadSafeQueueException:
    pass

# 线程安全的队列
class ThreadSafeQueue:
    def __init__(self, max_size = 0) -> None:
        self.max_size = max_size
        self.queue = []
        self.lock = threading.Lock()
        self.condition = threading.Condition()
        
    # 当前队列元素的数量
    def size(self):
        self.lock.acquire()
        size = len(self.queue)
        self.lock.release()
        return size

    # 往队列里面放入元素
    def put(self, item):
        if self.size != 0 and self.size() > self.max_size:
            return ThreadSafeQueueException()
        else:
            self.lock.acquire()
            self.queue.append(item)
            self.lock.release()
            # 通知在等待（阻塞状态）的进程
            self.condition.acquire()
            self.condition.notify()
            self.condition.release()

    # 往队列里面批量添加元素
    def batch_put(self, item_list):
        if not isinstance(item_list, list):
            item_list = list(item_list)
        for item in item_list:
            self.put(item)

    # 取出队列元素
    def pop(self, block=False, timeout=0):
        if self.size() == 0:
            # 是否阻塞
            if block:
                self.condition.acquire()
                self.condition.wait(timeout = timeout)
                self.condition.release()
            else:
                return None

        self.lock.acquire()
        item = None
        if len(self.queue) > 0:
            item = self.queue.pop()
        self.lock.release()
        return item

    # 按下标查询元素
    def get(self, index):
        self.lock.acquire()
        if index >= len(self.queue):
            item = None
        else:
            item = self.queue[index]
        self.lock.release()
        return item

if __name__ == "__main__":
    q = ThreadSafeQueue(max_size=100)

    def write():
        while True:
            q.put(random.randint(0,100))
            time.sleep(3)

    def read():
        while True:
            num = q.pop(block=True, timeout=2)
            time.sleep(2)
            print("the number from queue is ",num)


    thread1 = threading.Thread(target=write)
    thread2 = threading.Thread(target=read)

    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()