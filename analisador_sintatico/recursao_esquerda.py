import gramatica
import copy


def eliminar(g):
    # Algoritmo de eliminar recursão à esquerda indireta, puxamos as produções em há recursão à esquerda indiretamente
    nao_terminais = copy.deepcopy(g.nao_terminais)
    for i in range(len(g.nao_terminais)):
        for j in range(i):
            for producao_i in g.producoes[nao_terminais[i]]:
                if producao_i[0] == nao_terminais[j]:
                    for producao_j in g.producoes[nao_terminais[j]]:
                        nova_producao = producao_j + producao_i[1:] if producao_j != ["&"] else producao_i[1:]
                        g.producoes[nao_terminais[i]].append(nova_producao)
                    g.producoes[nao_terminais[i]].remove(producao_i)
        direta(g, nao_terminais[i])


def direta(g, nao_terminal):
    # Algoritmo de eliminar recursão à esquerda direta, verificamos se há alguma recursão direta, caso não retornamos.
    # Caso haja, criamos num novo estado e adicionamos as produções novas nesse estado, enquanto alteramos as producões
    # do antigo estado para levar a esse novo estado.
    if all(producao[0] != nao_terminal for producao in g.producoes[nao_terminal]):
        return

    novo_nao_terminal = nao_terminal
    while novo_nao_terminal in g.nao_terminais:
        novo_nao_terminal += "'"
    g.nao_terminais.append(novo_nao_terminal)

    producoes_novo_nao_terminal = [["&"]]
    producoes_nao_terminal = copy.deepcopy(g.producoes[nao_terminal])

    for producao in g.producoes[nao_terminal]:
        if producao[0] == nao_terminal:
            producoes_novo_nao_terminal.append(producao[1:] + [novo_nao_terminal])
        else:
            nova_producao = producao + [novo_nao_terminal] if producao != ["&"] else [novo_nao_terminal]
            producoes_nao_terminal.append(nova_producao)
        producoes_nao_terminal.remove(producao)

    g.producoes[novo_nao_terminal] = producoes_novo_nao_terminal
    g.producoes[nao_terminal] = producoes_nao_terminal


if __name__ == "__main__":
    # Há 3 gramaticas para teste: gramatica1.txt, gramatica2.txt e gramatica3.txt
    g = gramatica.Gramatica("testes/recursao_esquerda/gramatica1.txt")
    g.imprimir_gramatica()
    eliminar(g)
    g.imprimir_gramatica()
