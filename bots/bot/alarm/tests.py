import json
from threading import Thread

import pyautogui
from treelib import Tree

from src.test_types import Server, TestMessage, Action
import src.test_tree
import time
import nmain

print("Запуск сделан!")

tree = Tree()

commands_root = ["/start", "/jobs"]
commands_left = ["/jobs", '/jobs']
commands_right = ["/jobs", '/jobs']
commands_right_right = ["/start", "/start"]

# node_j = json.dumps(node)
tree.create_node(json.dumps(commands_root), "root")  # No parent means its the root node
tree.create_node(json.dumps(commands_left), "left", parent="root")
tree.create_node(json.dumps(commands_right), "right", parent="root")
tree.create_node(json.dumps(commands_right_right), "right-right", parent="right")
# tree.create_node(node_j, "diane", parent="jane")
# tree.create_node(node_j, "mary", parent="diane")
# tree.create_node(node_j, "mark", parent="jane")


print(tree)


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


action = Action(server=nmain.server)


def get_test_msgs(tasks):
    res = action.record_steps(tasks)
    return res


# tasks_1 = ["/jobs", "/start", "/jobs"]
# tasks_2 = ["/jobs", "/start", "/start"]
# print(get_test_msgs(tasks_1))
# print(get_test_msgs(tasks_2))

# commands_list = src.test_tree.commands_list(tree)
# test_out = []
# for commands in commands_list:
#     test_out.append(get_test_msgs(commands))
# action.save()
# print(*test_out, sep="\n")

action.load()
action.test()