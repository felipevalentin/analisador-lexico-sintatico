class Node:
    def __init__(self, label):
        self.id = 0
        self.label = label
        self.left = None
        self.right = None
        self.nullable = False
        self.firstpos = set()
        self.lastpos = set()


def make_node(operator, tree):
    root = Node(operator.pop())
    if root.label != "*":
        root.right = tree.pop()
    root.left = tree.pop()
    tree.append(root)


def make_tree(s):
    priority = {"(": 1, "|": 2, ".": 3, "*": 4}

    tree = []
    operators = []

    for i in range(len(s)):
        if s[i] == "(":
            operators.append("(")
        elif s[i].isalpha() or s[i] == "#":
            n = Node(s[i])
            tree.append(n)
        elif s[i] == ")":
            while operators[-1] != "(":
                make_node(operators, tree)
            operators.pop()
        else:
            while len(operators) > 0 and priority[operators[-1]] >= priority[s[i]]:
                make_node(operators, tree)
            operators.append(s[i])

    while len(tree) > 1:
        make_node(operators, tree)

    return tree[-1]


def print_tree(node, level=0):
    if node is not None:
        print_tree(node.right, level + 1)
        print(" " * 4 * level + "-> " + node.label)
        print_tree(node.left, level + 1)


root = make_tree("((a|b)*.a.b.b).#")
print_tree(root)
