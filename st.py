import itertools


class Node:
    def __init__(self, label, id_n=None):
        self.id = id_n
        self.label = label
        self.left = None
        self.right = None
        self.nullable = False
        self.firstpos = set()
        self.lastpos = set()


class Tree:
    def __init__(self, re):
        self.leaves = dict()
        self.id_counter = 1
        self.root = self.make_tree(re)
        self.followpos = [set() for _ in range(self.id_counter - 1)]
        self.postorder_nullable_firstpos_lastpos_followpos(self.root)

    def make_node(self, operator, tree):
        root = Node(operator.pop())
        if root.label != "*":
            root.right = tree.pop()
        root.left = tree.pop()
        tree.append(root)

    def get_next_id(self):
        id_n = self.id_counter
        self.id_counter += 1
        return id_n

    def make_tree(self, s):
        priority = {"(": 1, "|": 2, ".": 3, "*": 4}

        tree = []
        operators = []

        for i in range(len(s)):
            if s[i] == "(":
                operators.append("(")
            elif s[i].isalpha() or s[i] == "#":
                n = Node(s[i], id_n=self.get_next_id())
                self.leaves[n.id] = n.label
                tree.append(n)
            elif s[i] == ")":
                while operators[-1] != "(":
                    self.make_node(operators, tree)
                operators.pop()
            else:
                while len(operators) > 0 and priority[operators[-1]] >= priority[s[i]]:
                    self.make_node(operators, tree)
                operators.append(s[i])

        while len(tree) > 1:
            self.make_node(operators, tree)
        return tree[-1]

    def postorder_nullable_firstpos_lastpos_followpos(self, node):

        if not node:  # Recursion terminator
            return
        # 1. Left
        self.postorder_nullable_firstpos_lastpos_followpos(node.left)
        # 2. Right
        self.postorder_nullable_firstpos_lastpos_followpos(node.right)
        # 3. Root
        if node.label not in [".", "|", "*"]:
            if node.label == "&":  # empty char
                node.nullable = True
            else:
                node.firstpos.add(node.id)
                node.lastpos.add(node.id)
        elif node.label == "|":
            node.nullable = node.left.nullable or node.right.nullable
            node.firstpos = node.left.firstpos.union(node.right.firstpos)
            node.lastpos = node.left.lastpos.union(node.right.lastpos)
        elif node.label == "*":
            node.nullable = True
            node.firstpos = node.left.firstpos
            node.lastpos = node.left.lastpos
            self.compute_follows(
                node
            )  # Follows is only computed for star and cat nodes
        elif node.label == ".":
            node.nullable = node.left.nullable and node.right.nullable
            if node.left.nullable:
                node.firstpos = node.left.firstpos.union(node.right.firstpos)
            else:
                node.firstpos = node.left.firstpos
            if node.right.nullable:
                node.lastpos = node.left.lastpos.union(node.right.lastpos)
            else:
                node.lastpos = node.right.lastpos
            self.compute_follows(
                node
            )  # Follows is only computed for star and cat nodes
        return

    def compute_follows(self, n):
        if n.label == ".":
            for i in n.left.lastpos:
                self.followpos[i] = self.followpos[i].union(n.right.firstpos)
        elif n.label == "*":
            for i in n.left.lastpos:
                self.followpos[i] = self.followpos[i].union(n.left.firstpos)

    def print_tree(self, node=None, level=0):
        node = self.root if level == 0 else node
        if node is not None:
            self.print_tree(node.right, level + 1)
            print(
                " " * 4 * level
                + "-> "
                + node.label
                + " "
                + (str(node.id) if node.id else "")
            )
            self.print_tree(node.left, level + 1)


t = Tree("((a|b)*.a.b.b).#")
t.print_tree()
print(t.followpos)
