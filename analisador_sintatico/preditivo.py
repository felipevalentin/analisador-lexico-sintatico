import gramatica


def construir_tabela_analise(g: gramatica, first, follow):
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
