import gramatica
import first_follow


def construir_tabela_analise(gram: gramatica):
    tabela_analise = dict()
    for nao_terminal in gram.nao_terminais:
        tabela_analise[nao_terminal] = dict()
        for terminal in gram.terminais + ["$"]:
            tabela_analise[nao_terminal][terminal] = "\\"

    for nao_terminal in gram.nao_terminais:
        for producao in gram.producoes[nao_terminal]:
            first = set()
            for simbolo in producao:
                temp_first = first_follow.first(gram, simbolo)
                first = first.union(temp_first)
                if "&" not in temp_first:
                    break

            for terminal in first:
                if terminal == "&":
                    follow = first_follow.follow(gram, nao_terminal)
                    for simbolo in follow:
                        tabela_analise[nao_terminal][simbolo] = producao

                else:
                    tabela_analise[nao_terminal][terminal] = producao
    return tabela_analise


g = gramatica.Gramatica("input/gramatica.txt")
tabela = construir_tabela_analise(g)
print(g.terminais)
print("    ", end="")
for terminal in g.terminais + ["$"]:
    print(terminal, "   ", end="")
print()
for nao_terminal in g.nao_terminais:
    print(nao_terminal, end="   ")
    for terminal in g.terminais + ["$"]:
        print(f"{tabela[nao_terminal][terminal]:<5}", end="")
    print()
