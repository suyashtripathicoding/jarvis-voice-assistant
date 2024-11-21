import multiprocessing
import subprocess
import time
import os

# To run Jarvis
def startJarvis():
    # Code for process 1
    print("Process 1 is running.")
    from main import start
    start()
    time.sleep(10)  # Run for 10 seconds

# To run hotword
def listenHotword():
    # Code for process 2
    print("Process 2 is running.")
    from engine.features import hotword
    hotword()
    time.sleep(10)  # Run for 10 seconds

# Start both processes
if __name__ == '__main__':
    p1 = multiprocessing.Process(target=startJarvis)
    p2 = multiprocessing.Process(target=listenHotword)
    p1.start()
    subprocess.call([r'device.bat'])
    p2.start()
    p1.join()

    if p2.is_alive():
        p2.terminate()
        p2.join()

    print("system stop")