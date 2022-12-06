import copy

import gramatica
import first_follow
from collections import defaultdict
import utils


def fatorar(g):
    for _ in range(10):
        indireta(g)
        direta(g)


def indireta(g):
    # Remove o não determinismo indireto, Fazendo a derivação sucessiva sempre que identifica um não determinismo .
    # Para identificar o não determinismo utiliza do first, pois se duas produções, sendo uma delas iniciando com um
    # não terminal possuem o mesmo first, há um não determinismo e necessita de derivação. Esse processo de derivação é
    # reiniciado toda vez que um derivação acontece, pois a produção ao derivar pode conter um outro não determinismo.
    # o máximo que pode acontecer de derivações sem entrar em um loop é o somatório do tamanho da maior produção de cada
    # não terminal.
    first = first_follow.first(g)
    for nao_terminal in g.nao_terminais:
        maximo_tentativas = sum(
            max([len(producao) for producao in g.producoes[nao_terminal]])
            + len(g.producoes[nao_terminal])
            for nao_terminal in g.nao_terminais
        )
        while maximo_tentativas:
            producoes_nao_terminal = copy.deepcopy(g.producoes[nao_terminal])
            for producao_i in producoes_nao_terminal:
                if producao_i[0] in g.nao_terminais and producao_i[0] != nao_terminal:
                    first_sequencia_i = []
                    for simbolo in producao_i:
                        utils.union(first_sequencia_i, first[simbolo])
                        if "&" not in first_sequencia_i:
                            break

                    for producao_j in producoes_nao_terminal:
                        first_sequencia_j = []
                        if producao_i != producao_j:
                            for simbolo in producao_j:
                                utils.union(first_sequencia_j, first[simbolo])
                                if "&" not in first_sequencia_j:
                                    break

                        for terminal in first_sequencia_i:
                            if terminal != "&" and terminal in first_sequencia_j:
                                for producao_k in g.producoes[producao_i[0]]:
                                    if producao_k != ["&"]:
                                        utils.add(
                                            g.producoes[nao_terminal],
                                            producao_k + producao_i[1:],
                                        )
                                    else:
                                        if len(producao_i) == 1:
                                            utils.add(g.producoes[nao_terminal], ["&"])
                                        else:
                                            utils.add(
                                                g.producoes[nao_terminal],
                                                producao_i[1:],
                                            )
                                break
                        else:
                            continue
                        break
                    else:
                        continue
                    g.producoes[nao_terminal].remove(producao_i)
                    break
            maximo_tentativas -= 1


def direta(g):
    # remove o não determinismo direto criando um novo não terminal e adicionando produções em que identifica o não
    # determinismo. Para identificar o não determinismo direto é feito um agrupamento das produções que iniciam com o
    # mesmo simbolo. Se um simbolo tem mais que uma produção há um não determinismo.
    pos = 0
    size = len(g.nao_terminais)
    while pos < size:
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
                        utils.add(g.producoes[novo_nao_terminal], producao[1:])
                    else:
                        utils.add(g.producoes[novo_nao_terminal], ["&"])
                else:
                    utils.add(
                        g.producoes[nao_terminal], producao[:1] + [novo_nao_terminal]
                    )

        pos += 1


if __name__ == "__main__":
    # Há 3 gramaticas para teste: gramatica1.txt, gramatica2.txt e gramatica3.txt
    g = gramatica.Gramatica("testes/fatoracao/gramatica3.txt")
    g.imprimir_gramatica()
    fatorar(g)
    g.imprimir_gramatica()
