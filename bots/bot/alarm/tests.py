from threading import Thread

import pyautogui
from src.test_types import Server
import time
import nmain

print("Запуск сделан!")




def SendMessage(tasks):
    # message = input("Введите сообщение:")
    amount = 30

    for i in range(amount):
        pass

    for task in tasks:
        pyautogui.typewrite(task.strip())
        time.sleep(1)
        pyautogui.press('enter')


def asd():
    print(123)


def method_name(tasks):
    # thread = multiprocessing.Process(target=nmain.main_sync, args=())
    thread = Thread(target=nmain.server.start)
    thread.start()
    # nmain.run_tread()
    time.sleep(10)
    SendMessage(tasks)
    time.sleep(1)
    nmain.server.stop()
    return [[msg.text, msg.from_user.id] for msg in nmain.msgs]


def get_test_msgs(tasks):
    res = method_name(tasks)
    nmain.msgs = []
    return res


tasks_1 = ["/jobs", "/start", "/jobs"]
tasks_2 = ["/jobs", "/start", "/start"]
test_out = [get_test_msgs(tasks_1), get_test_msgs(tasks_2)]

print(*test_out, sep='\n')
