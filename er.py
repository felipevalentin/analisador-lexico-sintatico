class ExpressaoRegular:
    def __init__(self, expressao=None):
        self.expressao = expressao

    def ler_arquivo(self, nome):
        with open(nome) as f:
            for line in f:
                head, tail = line.split(":")

                if head == "er":
                    self.er_normal(tail)
                else:
                    self.er_grupos(head, tail)

    def er_normal(self, tail):
        er = tail.strip()
        er = self.add_and(er)
        er = self.add_parenteses(er)
        er = self.expandir_extensoes(er)
        self.expressao = er

    def expandir_extensoes(self, tail):
        er = []
        ps = []
        lp = None
        for i, char in enumerate(tail):
            last = len(er) - 1
            if char == "(":
                er.append("(")
                ps.append(last + 1)
            elif char == ")":
                er.append(")")
                lp = ps.pop()
            elif char == "+":
                er.append(".")
                if lp is not None:
                    er += er[lp : last + 1]
                else:
                    er.append(er[last])
                er.append("*")
            elif char == "?":
                er.append("|")
                er.append("&")
            else:
                er.append(char)
        return er

    def add_parenteses(self, tail):
        er = []
        ps = []
        lp = None
        for i, char in enumerate(tail):
            last = len(er) - 1
            if char == "(":
                er.append("(")
                ps.append(last + 1)
            elif char == ")":
                er.append(")")
                lp = ps.pop()
            elif char == "+":
                if lp is not None:
                    er.insert(lp, "(")
                    er.append("+")
                    er.append(")")
                    lp = None
                else:
                    er.insert(last, "(")
                    er.append("+")
                    er.append(")")
            elif char == "?":
                if lp:
                    er.insert(lp, "(")
                    er.append("?")
                    er.append(")")
                    lp = None
                else:
                    er.insert(last, "(")
                    er.append("?")
                    er.append(")")
            else:
                er.append(char)
        return er

    def add_and(self, tail):
        er = []
        for i in range(len(tail)):
            if (
                i > 0
                and tail[i] not in ["|", "+", "?", ")"]
                and tail[i - 1] not in ["|", "("]
            ):
                er.insert(len(er), ".")
                er.append(tail[i])
            else:
                er.append(tail[i])
        return er

    def er_grupos(self, head, tail):
        start = None
        finish = None
        group = False
        lower = "|".join(chr(c) for c in range(ord("a"), ord("z") + 1))
        upper = "|".join(chr(c) for c in range(ord("A"), ord("Z") + 1))
        digit = "|".join(chr(c) for c in range(ord("0"), ord("9") + 1))
        er = tail.replace("[a-z]", lower)
        er = er.replace("[a-zA-Z]", lower + "|" + upper)
        er = er.replace("[A-Z]", upper)
        er = er.replace("[0-9]", digit)
        self.expressao = er


if __name__ == "__main__":
    er = ExpressaoRegular()
    er.ler_arquivo("entrada_er.txt")
    print("".join(er.expressao))
