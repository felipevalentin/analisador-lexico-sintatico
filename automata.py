class Automata:
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
                c = "-".join(str(e) for e in c) + "\n"
                f.write(",".join([str(a), str(b), str(c)]))

    def re2dfa(self, tree):
        unmakerd = [tree.root["firstpos"]]
        marked = []
        finals = []
        trans = []
        while len(unmakerd) > 0:
            S = unmakerd.pop()
            marked.append(S)
            if any(tree.leaves[p] == "#" for p in S):
                finals.append(S)
            for a in self.alfabeto:
                U = set()
                for p in S:
                    if tree.leaves[p] == a:
                        U = U.union(tree.followpos[p])
                if U not in unmakerd and U not in marked:
                    unmakerd.append(U)
                trans.append([S, a, [U]])

        self.make_dfa(marked, finals, trans)

    def make_dfa(self, states, finals, trans):

        self.numero_estados = len(states)
        self.estado_inicial = 0
        self.estados_finais = []
        self.transicoes = []
        for i, state in enumerate(states):
            for j, state2 in enumerate(states):
                for tran in trans:
                    ist, alp, fst = tran
                    if ist == state and fst[0] == state2:
                        ist = i
                        fst = [j]
                        self.transicoes.append([ist, alp, fst])
            if state in finals:
                self.estados_finais.append(i)
