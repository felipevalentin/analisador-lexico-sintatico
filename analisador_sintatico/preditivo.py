import gramatica
import first_follow


def construir_tabela_analise(g: gramatica):
    first = first_follow.first(g)
    follow = first_follow.follow(g)

    tabela_analise = dict()
    for nao_terminal in g.nao_terminais:
        tabela_analise[nao_terminal] = dict()
        for terminal in [*g.terminais, "$"]:
            tabela_analise[nao_terminal][terminal] = "\\"

    for nao_terminal in g.nao_terminais:
        for producao in g.producoes[nao_terminal]:
            first_producao = []
            for simbolo in producao:
                for terminal in first[simbolo]:
                    if terminal not in first_producao:
                        first_producao.append(terminal)
                if "&" not in first_producao:
                    break

            for terminal in first_producao:
                if terminal == "&":
                    for simbolo in follow[nao_terminal]:
                        tabela_analise[nao_terminal][simbolo] = producao

                else:
                    tabela_analise[nao_terminal][terminal] = producao
    return tabela_analise


if __name__ == "__main__":

    g = gramatica.Gramatica("input/gramatica.txt")
    tabela = construir_tabela_analise(g)

    print("      ", end="")
    for terminal in list(g.terminais) + ["$"]:
        print(f"{terminal:<6}", end="")
    print()
    for nao_terminal in g.nao_terminais:
        print(f"{nao_terminal:<2}", end="    ")
        for terminal in list(g.terminais) + ["$"]:
            print(f"{''.join(tabela[nao_terminal][terminal]):<6}", end="")
        print()
