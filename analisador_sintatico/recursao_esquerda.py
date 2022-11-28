import gramatica


def eliminar(gramatica):
    ordenado = gramatica.nao_terminais

    for i in range(len(ordenado)):
        for j in range(i):
            for producao_i in gramatica.producoes[ordenado[i]]:
                if producao_i[0] == ordenado[j]:
                    for producao_j in gramatica.producoes[ordenado[j]]:
                        nova_producao = (
                            producao_j + producao_i[1:]
                            if producao_j != "&"
                            else producao_i[1:]
                        )
                        gramatica.producoes[ordenado[i]].append(nova_producao)
                    gramatica.producoes[ordenado[i]].remove(producao_i)
        direta(gramatica, ordenado[i])


def direta(gramatica, nao_terminal):
    novo_nao_terminal = nao_terminal + "'"
    gramatica.nao_terminais.append(novo_nao_terminal)

    producoes_novo_nao_terminal = ["&"]
    producoes_nao_terminal = gramatica.producoes[nao_terminal].copy()

    if all(
        producao[0] != nao_terminal for producao in gramatica.producoes[nao_terminal]
    ):
        return

    for producao in gramatica.producoes[nao_terminal]:
        if producao[0] == nao_terminal:
            producoes_novo_nao_terminal.append(producao[1:] + novo_nao_terminal)
        else:
            nova_producao = (
                producao + novo_nao_terminal if producao != "&" else novo_nao_terminal
            )
            producoes_nao_terminal.append(nova_producao)
        producoes_nao_terminal.remove(producao)

    gramatica.producoes[novo_nao_terminal] = producoes_novo_nao_terminal
    gramatica.producoes[nao_terminal] = producoes_nao_terminal


g = gramatica.Gramatica("input/gramatica.txt")
eliminar(g)
print(g.producoes)
