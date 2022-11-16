class Automato:
    def __init__(
        self,
        numero_estados=None,
        estado_inicial=None,
        estados_finais=None,
        alfabeto=None,
        transicoes=None,
    ):
        self.numero_estados = numero_estados
        self.estado_inicial = estado_inicial
        self.estados_finais = estados_finais
        self.alfabeto = alfabeto
        self.transicoes = transicoes

    def ler_arquivo(self, nome):
        with open(nome) as f:
            self.numero_estados = f.readline().strip()
            self.estado_inicial = f.readline().strip()
            self.estados_finais = f.readline().strip().split(",")
            self.alfabeto = f.readline().strip().split(",")
            self.transicoes = []
            for line in f:
                a, b, c = line.strip().split(",")
                c = c.split("-")
                self.transicoes.append([a, b, c])

    def escrever_arquivo(self, nome):
        with open(nome, "w") as f:
            f.write(str(self.numero_estados) + "\n")
            f.write(str(self.estado_inicial) + "\n")
            f.write(",".join(str(e) for e in self.estados_finais) + "\n")
            f.write(",".join(self.alfabeto) + "\n")
            for line in self.transicoes:
                a, b, c = line
                c = "-".join(c) + "\n"
                f.write(",".join([a, b, c]))


if __name__ == "__main__":
    automato = Automato()
    automato.ler_arquivo("entrada_automato.txt")
    automato.escrever_arquivo("saida_automato.txt")
