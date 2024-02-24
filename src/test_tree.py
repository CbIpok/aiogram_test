import json
from copy import deepcopy

from treelib import Node, Tree
from src.test_types import TestMessage




def from_root_iterator(path: [str], tree_in: Tree):
    # print('tree_in', tree_in)
    last = path[-1]
    if len(tree_in.children(last)) == 0:
        yield path
    for node in tree_in.children(path[-1]):
        new_path = deepcopy(path)
        new_path.append(node.identifier)
        sub_tree = tree_in.subtree(new_path[-1])
        yield from from_root_iterator(new_path, sub_tree)


def iterate(tree_in):
    for i in from_root_iterator(['root'], tree_in):
        print(i)


def commands_list(tree: Tree):
    tests_commands = []
    for command in from_root_iterator(['root'], tree):
        tests_commands.append(command)
    print(tests_commands)
    lists = []
    i = 0
    for command_nodes in tests_commands:
        lists.append([])
        for command in command_nodes:
            node = tree.get_node(command)
            node_val = json.loads(node.tag)
            lists[i].extend(node_val)
        i += 1
    return lists
