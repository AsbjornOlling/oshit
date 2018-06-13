
import threading
# import queue
import time


def f(n, threads):
    print("starting thread " + str(n))
    tcopy = threads[:]
    threads.append(threading.current_thread())

    print("threads: " + str(len(threads)))
    print("copy: " + str(len(tcopy)))

    time.sleep(n)

    for t in tcopy:
        print("thread " + str(n) + " joining thread")
        t.join()

    print("ending thread " + str(n))
    # print("THREAD NAME=" + str(threading.current_thread()))


threads = []
t = threading.Thread(target=f, args=(5, threads))
t.start()

t = threading.Thread(target=f, args=(4, threads))
t.start()

t = threading.Thread(target=f, args=(3, threads))
t.start()

# print("THREADS " + str(len(threads)))

t = threading.Thread(target=f, args=(2, threads))
t.start()

t = threading.Thread(target=f, args=(1, threads))
t.start()
