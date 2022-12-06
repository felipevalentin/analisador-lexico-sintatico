from collections import defaultdict


class Gramatica:
    def __init__(self, nome_arquivo):
        self.nao_terminais = None
        self.terminais = None
        self.inicial = None
        self.producoes = None
        self.ler_arquivo(nome_arquivo)

    def ler_arquivo(self, nome_arquivo):
        with open(nome_arquivo, "r") as f:
            self.nao_terminais = f.readline().strip().split()
            self.terminais = []
            self.producoes = defaultdict(list)

            for i, line in enumerate(f):
                nao_terminal, producoes = line.split("->", 1)
                nao_terminal = nao_terminal.strip()

                for producao in producoes.split("|"):
                    producao = producao.strip().split()
                    self.producoes[nao_terminal].append(producao)

                    for simbolo in producao:
                        if simbolo not in [*self.nao_terminais, *self.terminais, "&"]:
                            self.terminais.append(simbolo)

                if i == 0:
                    self.inicial = nao_terminal

    def imprimir_gramatica(self):
        print("Não Terminais:", " ".join(self.nao_terminais))
        print("Terminais:", " ".join(self.terminais))
        print("Inicial:", self.inicial)
        print("Produções: ")
        for k, v in self.producoes.items():
            print(f"{k} -> {' | '.join(' '.join(producao) for producao in v)}")
        print()


if __name__ == "__main__":
    g = Gramatica("input/gramatica1.txt")
    g.imprimir_gramatica()
