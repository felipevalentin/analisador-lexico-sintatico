import preditivo
import gramatica


def parser(g, tokens):
    tabela_analise = preditivo.construir_tabela_analise(g)
    with open("output/tabela_analise.txt", "w") as f:
        f.write(f"{'':>2}")
        for terminal in list(g.terminais) + ["$"]:
            f.write(f"{terminal:>7}")
        f.write("\n")
        for nao_terminal in g.nao_terminais:
            f.write(f"{nao_terminal:<2}")
            for terminal in [*g.terminais, "$"]:
                f.write(f"{''.join(tabela_analise[nao_terminal][terminal]):>7}")
            f.write("\n")

    indice_tokens = 0
    pilha = ["$", g.inicial]
    with open("output/pilha.txt", "w") as f:
        f.write(" ".join(pilha) + "\n")
        while pilha[-1] != "$":
            topo = pilha.pop()

            if topo == tokens[indice_tokens]:
                indice_tokens += 1
            elif topo in g.terminais:
                raise "Error"
            elif tabela_analise[topo][tokens[indice_tokens]] == "\\":
                raise "Error"
            else:
                for simbolo in reversed(tabela_analise[topo][tokens[indice_tokens]]):
                    if simbolo != "&":
                        pilha.append(simbolo)

            f.write(" ".join(pilha) + "\n")
        print("Ok")


g = gramatica.Gramatica("input/gramatica.txt")
lista_t = ["id", "+", "id", "*", "id", "$"]
parser(g, lista_t)
