import math


class Node:
    def __init__(self, children=None, score=None):
        self.children = children
        self.score = score


def score(node):
    return node.score


def minimax(node, depth, player):
    if depth == 0:
        return score(node)

    if player == "min":
        value = math.inf
        for child in node.children:
            value = min(value, minimax(child, depth - 1, "max"))
        return value

    elif player == "max":
        value = -math.inf
        for child in node.children:
            value = max(value, minimax(child, depth - 1, "min"))
        return value


root = Node()
max1 = Node()
max2 = Node()
min1_1 = Node(score=1)
min1_2 = Node(score=2)
min2_1 = Node(score=3)
min2_2 = Node(score=4)

max1.children = [min1_1, min1_2]
max2.children = [min2_1, min2_2]
root.children = [max1, max2]

print(minimax(root, 2, "max"))