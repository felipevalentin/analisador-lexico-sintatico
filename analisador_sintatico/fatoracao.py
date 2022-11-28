import gramatica


def fatorar(gramatica):
    for _ in range(10):
        indireta(gramatica)
        # direta(gramatica)


def indireta(gramatica):
    for nao_terminal in gramatica.nao_terminais:
        novas_producoes = []
        for producao in gramatica.producoes[nao_terminal]:
            if producao[0] in gramatica.nao_terminais:
                for producao_indireta in gramatica.producoes[producao[0]]:
                    novas_producoes.append(producao_indireta + producao[1:])
            else:
                novas_producoes.append(producao)
        gramatica.producoes[nao_terminal] = novas_producoes


def direta(gramatica):
    for nao_terminal in gramatica.nao_terminais:
        producoes_novo_nao_terminal = []
        producoes_nao_terminal = gramatica.producoes[nao_terminal].copy()

        if not any(
            producao_i[0] == producao_j[0]
            for producao_i in gramatica.producoes[nao_terminal]
            for producao_j in gramatica.producoes[nao_terminal]
            and producao_i != producao_j
        ):
            continue

        for producao_i in gramatica.producoes[nao_terminal]:
            for producao_j in gramatica.producoes[nao_terminal]:
                if producao_i[0] == producao_j[0] and producao_i != producao_j:
                    producoes_novo_nao_terminal.append(producao_j[1:])
                    producoes_nao_terminal.remove(producao_j)
            producoes_nao_terminal.r
            producoes_novo_nao_terminal.append(producao_i[1:])


g = gramatica.Gramatica("input/gramatica.txt")
fatorar(g)
print(g.producoes)
