import threading
import time
from multiprocessing import Queue

share=Queue()
thread_num=3

class Mythread(threading.Thread):
    def __init__(self,func):
        super().__init__()
        self.func=func

    def run(self):
        self.func()

def worker():
    global share
    while not share.empty():
        item=share.get()
        print("processing: ",item)
        time.sleep(1)

def main():
    global share
    threads=[]
    for task in range(5):
        share.put(task)

    thread=Mythread(worker)
    thread.start()
    threads.append(thread)
    #for thread in threads:
     #   thread.join()

if __name__=='__main__':
    main()