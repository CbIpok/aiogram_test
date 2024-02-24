import json
import time
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
        self.command_cases: [[TestMessage]] = []
        self.server: Server = server

    @staticmethod
    def get_test_message(message: Message) -> TestMessage:
        return {'type': 'bot' if message.from_user.is_bot else 'user', 'text': str(message.text)}

    def run_test(self, commands):
        thread = Thread(target=self.server.start)
        thread.start()
        # nmain.run_tread()
        time.sleep(10)
        SendMessage(commands)
        print("commands", commands)
        time.sleep(1)
        ans = list(map(Action.get_test_message, self.server.msgs))
        self.server.stop()
        # self.command_cases.append(ans)
        return ans

    def record_steps(self, commands):
        self.command_cases.append(self.run_test(commands))

    def save(self):
        with open("cash", 'w') as f:
            json.dump(self.command_cases, f)

    def load(self):
        with open("cash", 'r') as f:
            self.command_cases = json.load(f)

    def test(self):
        for case_id, case in enumerate(self.command_cases):
            commands = [None if command['type'] == 'bot' else command['text'] for command in case]
            commands = list(filter(lambda item: item is not None, commands))
            ans = self.run_test(commands)
            print(ans == self.command_cases[case_id])

    # list1 = [1, 2, 3]
# list2 = [2, 1, 3]
# list3 = [1, 2, 3]
# set_l = {tuple(i) for i in [list1, list2, list3]}
# print(set_l)
