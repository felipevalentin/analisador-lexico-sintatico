import automata
import regularexpression


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
        is_id = False
        for c in re:
            if c == "\\":
                is_id = True
            elif c == "(" and not is_id:
                operators.append("(")
            elif c == ")" and not is_id:
                while operators[-1] != "(":
                    self.make_node(operators.pop(), tree)
                operators.pop()
            elif c in ["|", ".", "*"] and not is_id:
                while len(operators) > 0 and priority[operators[-1]] >= priority[c]:
                    self.make_node(operators.pop(), tree)
                operators.append(c)
            else:
                self.make_node(c, tree, True, leaf_id)
                self.followpos.append(set())
                self.leaves[leaf_id] = c
                leaf_id += 1
                is_id = False

        while len(tree) > 1:
            self.make_node(operators.pop(), tree)

        return tree[-1]

    def make_node(self, label, tree, is_id=False, leaf_id=None):
        root = {
            "leaf_id": leaf_id,
            "is_id": True if is_id else False,
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

        if node["label"] == "|" and not node["is_id"]:
            node["nullable"] = node["left"]["nullable"] or node["right"]["nullable"]
            node["firstpos"] = node["left"]["firstpos"].union(node["right"]["firstpos"])
            node["lastpos"] = node["left"]["lastpos"].union(node["right"]["lastpos"])
        elif node["label"] == "*" and not node["is_id"]:
            node["nullable"] = True
            node["firstpos"] = node["left"]["firstpos"]
            node["lastpos"] = node["left"]["lastpos"]
            self.compute_follows(node)
        elif node["label"] == "." and not node["is_id"]:
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


def regex_from_read_file(name):
    res = []
    with open(name) as f:
        for line in f:
            def_re, raw_re = line.split(":")
            res.append(regularexpression.Regex(def_re, raw_re, res))
    return res


"""regexs = regex_from_read_file("input/er.txt")
for regex in regexs:
    print(regex.re, regex.alphabet)
    tree = Tree(regex.add_end_of_regex_symbol(regex.re))
    dfa = automata.Automata(alfabeto=regex.alphabet)
    dfa.re2dfa(tree)
    dfa.def_re = regex.re
    dfa.imprimir_atributos()"""
