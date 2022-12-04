import gramatica
import recursao_esquerda
from collections import defaultdict


def fatorar(g):
    for _ in range(10):
        indireta(g)
        direta(g)


def indireta(gramatica):
    for nao_terminal in gramatica.nao_terminais:
        while True:
            for producao in gramatica.producoes[nao_terminal]:
                if producao[0] in g.nao_terminais:
                    for producao_j in gramatica.producoes[producao[0]]:
                        if producao_j != ["&"]:
                            if producao_j + producao[1:] not in gramatica.producoes[nao_terminal]:
                                gramatica.producoes[nao_terminal].append(producao_j + producao[1:])
                        else:
                            if len(producao) == 1:
                                if ["&"] not in gramatica.producoes[nao_terminal]:
                                    gramatica.producoes[nao_terminal].append(["&"])
                            else:
                                if producao[1:] not in gramatica.producoes[nao_terminal]:
                                    gramatica.producoes[nao_terminal].append(producao[1:])
                    gramatica.producoes[nao_terminal].remove(producao)
                    break
            else:
                break


def direta(g):
    pos = 0
    while pos < len(g.nao_terminais):
        nao_terminal = g.nao_terminais[pos]
        agrupamento_producoes = defaultdict(list)
        for producao in g.producoes[nao_terminal]:
            agrupamento_producoes[producao[0]].append(producao)

        for simbolo, producoes in agrupamento_producoes.items():
            if len(producoes) > 1:
                novo_nao_terminal = nao_terminal
                while novo_nao_terminal in g.nao_terminais:
                    novo_nao_terminal += "'"
                g.nao_terminais.append(novo_nao_terminal)
                for producao in producoes:
                    g.producoes[nao_terminal].remove(producao)
                    if len(producao) > 1:
                        if producao[1:] not in g.producoes[novo_nao_terminal]:
                            g.producoes[novo_nao_terminal].append(producao[1:])
                    else:
                        if ["&"] not in g.producoes[novo_nao_terminal]:
                            g.producoes[novo_nao_terminal].append(["&"])
                else:
                    if producao[:1] + [novo_nao_terminal] not in g.producoes[novo_nao_terminal]:
                        g.producoes[nao_terminal].append(producao[:1] + [novo_nao_terminal])

        pos += 1


if __name__ == "__main__":
    g = gramatica.Gramatica("input/fatoracao/gramatica3.txt")
    fatorar(g)
    for k, v in g.producoes.items():
        print(k, v)
