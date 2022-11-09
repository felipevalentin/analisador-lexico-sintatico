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
        for char in tail:
            if char == "?":
                pass
            elif char == "+":
                pass

    def er_grupos(self, head, tail):
        pass


if __name__ == "__main__":
    er = ExpressaoRegular()
    er.ler_arquivo("entrada_er.txt")
