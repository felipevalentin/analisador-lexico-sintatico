import gramatica as gram


# melhor retornar o dicionário em vez do first do simbolo

def first(gramatica, simbolo_entrada):
    if simbolo_entrada == "&":
        return set("&")
    if simbolo_entrada in gramatica.terminais:
        return set(simbolo_entrada)

    conjunto_first = set()

    for producao in gramatica.producoes[simbolo_entrada]:
        if producao[0] in gramatica.terminais:
            conjunto_first.add(producao[0])
        elif producao == "&":
            conjunto_first.add("&")
        else:
            for simbolo in producao:
                first_simbolo = first(gramatica, simbolo)

                if "&" not in first_simbolo:
                    conjunto_first = conjunto_first.union(first_simbolo)
                    break

                first_simbolo.remove("&")
                conjunto_first = conjunto_first.union(first_simbolo)

    return conjunto_first


def follow(gramatica, simbolo_entrada):
    dicionario_follow = dict()
    for nao_terminal in gramatica.nao_terminais:
        dicionario_follow[nao_terminal] = set()

    acrescentou = True
    while acrescentou:
        antigo = dicionario_follow.copy()
        for nao_terminal in gramatica.nao_terminais:
            if nao_terminal == gramatica.inicial:
                dicionario_follow[nao_terminal].add("$")

            for producao in gramatica.producoes[nao_terminal]:
                for i, simbolo in enumerate(producao):
                    if simbolo in gramatica.nao_terminais:
                        first_beta = set()
                        empty_beta = True
                        for j in range(i + 1, len(producao)):
                            temp_first = first(gramatica, producao[j])
                            first_beta = first_beta.union(temp_first)
                            if "&" not in temp_first:
                                empty_beta = False
                                break

                        if "&" in first_beta:
                            first_beta.remove("&")
                        dicionario_follow[simbolo] = dicionario_follow[simbolo].union(first_beta)

                        if empty_beta:
                            dicionario_follow[simbolo] = dicionario_follow[simbolo].union(dicionario_follow[nao_terminal])
        if antigo == dicionario_follow:
            acrescentou = False
    return dicionario_follow[simbolo_entrada]


g = gram.Gramatica("input/gramatica.txt")
d = follow(g, "A'")
print(d)
