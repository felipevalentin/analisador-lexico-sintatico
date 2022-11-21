class Tree:
    def __init__(self, re):
        self.leaves = dict()
        self.followpos = []
        self.root = self.make_tree(re)
        self.make_syntax_tree(self.root)

    def make_tree(self, re):
        priority = {"(": 1, "|": 2, ".": 3, "*": 4}
        tree = []
        operators = []
        leaf_id = 0

        for c in re:
            if c == "(":
                operators.append("(")
            elif c == ")":
                while operators[-1] != "(":
                    self.make_node(operators.pop(), tree)
                operators.pop()
            elif c in ["|", ".", "*"]:
                while len(operators) > 0 and priority[operators[-1]] >= priority[c]:
                    self.make_node(operators.pop(), tree)
                operators.append(c)
            else:
                self.make_node(c, tree, leaf_id)
                self.followpos.append(set())
                self.leaves[leaf_id] = c
                leaf_id += 1

        while len(tree) > 1:
            self.make_node(operators.pop(), tree)

        return tree[-1]

    def make_node(self, label, tree, leaf_id=None):
        root = {
            "leaf_id": leaf_id,
            "label": label,
            "left": None,
            "right": None,
            "nullable": False,
            "firstpos": set(),
            "lastpos": set(),
        }
        if leaf_id is None:
            if root["label"] != "*":
                root["right"] = tree.pop()
            root["left"] = tree.pop()
        tree.append(root)

    def make_syntax_tree(self, node):
        if not node:
            return

        self.make_syntax_tree(node["left"])
        self.make_syntax_tree(node["right"])

        if node["label"] == "|":
            node["nullable"] = node["left"]["nullable"] or node["right"]["nullable"]
            node["firstpos"] = node["left"]["firstpos"].union(node["right"]["firstpos"])
            node["lastpos"] = node["left"]["lastpos"].union(node["right"]["lastpos"])
        elif node["label"] == "*":
            node["nullable"] = True
            node["firstpos"] = node["left"]["firstpos"]
            node["lastpos"] = node["left"]["lastpos"]
            self.compute_follows(node)
        elif node["label"] == ".":
            node["nullable"] = node["left"]["nullable"] and node["right"]["nullable"]
            if node["left"]["nullable"]:
                node["firstpos"] = node["left"]["firstpos"].union(
                    node["right"]["firstpos"]
                )
            else:
                node["firstpos"] = node["left"]["firstpos"]

            if node["right"]["nullable"]:
                node["lastpos"] = node["left"]["lastpos"].union(
                    node["right"]["lastpos"]
                )
            else:
                node["lastpos"] = node["right"]["lastpos"]
            self.compute_follows(node)

        else:
            if node["label"] == "&":
                node["nullable"] = True
            else:
                node["firstpos"].add(node["leaf_id"])
                node["lastpos"].add(node["leaf_id"])

    def compute_follows(self, node):
        if node["label"] == ".":
            for i in node["left"]["lastpos"]:
                self.followpos[i] = self.followpos[i].union(node["right"]["firstpos"])
        elif node["label"] == "*":
            for i in node["left"]["lastpos"]:
                self.followpos[i] = self.followpos[i].union(node["left"]["firstpos"])

    def print_tree(self, node=None, level=0):
        node = self.root if level == 0 else node
        if node is not None:
            self.print_tree(node["right"], level + 1)
            print(
                " " * 4 * level
                + "-> "
                + node["label"]
                + " "
                + (str(node["leaf_id"]) if node["leaf_id"] is not None else "")
                # + " "
                # + str(node["firstpos"])
                # + " "
                # + str(node["lastpos"])
            )
            self.print_tree(node["left"], level + 1)