import gramatica


def eliminar(g):
    for i in range(len(g.nao_terminais)):
        for j in range(i):
            for producao_i in g.producoes[g.nao_terminais[i]]:
                if producao_i[0] == g.nao_terminais[j]:
                    for producao_j in g.producoes[g.nao_terminais[j]]:
                        nova_producao = (
                            producao_j + producao_i[1:]
                            if producao_j != ["&"]
                            else producao_i[1:]
                        )
                        g.producoes[g.nao_terminais[i]].append(nova_producao)
                    g.producoes[g.nao_terminais[i]].remove(producao_i)
        direta(g, g.nao_terminais[i])


def direta(g, nao_terminal):
    if all(producao[0] != nao_terminal for producao in g.producoes[nao_terminal]):
        return

    novo_nao_terminal = nao_terminal
    while novo_nao_terminal in g.nao_terminais:
        novo_nao_terminal += "'"
    g.nao_terminais.append(novo_nao_terminal)

    producoes_novo_nao_terminal = [["&"]]
    producoes_nao_terminal = g.producoes[nao_terminal].copy()

    for producao in g.producoes[nao_terminal]:
        if producao[0] == nao_terminal:
            producoes_novo_nao_terminal.append(producao[1:] + [novo_nao_terminal])
        else:
            nova_producao = (
                producao + [novo_nao_terminal]
                if producao != ["&"]
                else [novo_nao_terminal]
            )
            producoes_nao_terminal.append(nova_producao)
        producoes_nao_terminal.remove(producao)

    g.producoes[novo_nao_terminal] = producoes_novo_nao_terminal
    g.producoes[nao_terminal] = producoes_nao_terminal


if __name__ == "__main__":
    g = gramatica.Gramatica("input/recursao_esquerda/gramatica1.txt")
    eliminar(g)
    for k, v in g.producoes.items():
        print(k, v)
