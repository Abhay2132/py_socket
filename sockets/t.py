from threading import Thread
from time import sleep
class A:
    i = 1
    def __init__(self) -> None:
        thread = Thread(target=self.th)
        thread.start()
        while 1:
            print(self.i)
            sleep(1)

    # @staticmethod
    def th(self):
        while 1:
            self.i += 1
            sleep(0.1)

a = A()