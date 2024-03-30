import threading
import time

dic = {"n":1}

def func(d):
    print(d)
    time.sleep(2)
    d["n"] += 1
    print(d["n"])

thread = threading.Thread(target=func, args=(dic,), daemon=True)
thread.start()
print("WAITING FOR THREAD")
print("EXITING")
thread.join()

print(repr(dic))
