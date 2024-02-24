from datetime import time
from threading import Thread

import pyautogui

bot_id = 6618135740
from typing import TypedDict
from aiogram.types import Message


class Server:
    def __init__(self, start, stop, msgs):
        self.start = start
        self.stop = stop
        self.msgs = msgs


class TestMessage(TypedDict):
    text: str
    type: str

def SendMessage(tasks):
    # message = input("Введите сообщение:")
    amount = 30

    for i in range(amount):
        pass

    for task in tasks:
        pyautogui.typewrite(task.strip())
        time.sleep(1)
        pyautogui.press('enter')

class Action:
    def __init__(self, server: Server):
        self.command_cases = None
        self.ans_cases = None
        self.server: Server = server

    @staticmethod
    def get_test_message(message: Message) -> TestMessage:
        return {'type': 'bot' if message.from_user.is_bot else 'user', 'text': str(message.text)}

    def record_steps(self, commands):
        thread = Thread(target=self.server.start)
        thread.start()
        # nmain.run_tread()
        time.sleep(10)
        SendMessage(commands)
        time.sleep(1)
        self.server.stop()
        return [[msg.text, msg.from_user.id] for msg in self.server.msgs]


    # list1 = [1, 2, 3]
# list2 = [2, 1, 3]
# list3 = [1, 2, 3]
# set_l = {tuple(i) for i in [list1, list2, list3]}
# print(set_l)
