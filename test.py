import os
import signal
import subprocess
import time
from threading import Thread

from action import raiseTimeoutError


def function1():
    print("hey")
    signal.signal(signal.SIGALRM, raiseTimeoutError)
    time.sleep(2)
    print("exit function1")


# def function2():
#     print("Oh")
#     time.sleep(2)
#     print("exit function2")


thread1 = Thread(target=function1, args=())
thread1.start()
# if os.name == 'nt':
#     subprocess.Popen(r"cmd", creationflags=subprocess.CREATE_NEW_CONSOLE)
# else:
#     os.system(os.environ['SHELL'])

# thread2 = Thread(target=function2, args=())
# thread2.start()
# thread2.join()
thread1.join()
