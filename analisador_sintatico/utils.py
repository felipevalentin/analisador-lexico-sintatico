def salvar_tabela(g, tabela_analise):
    with open("output/tabela_analise.txt", "w") as f:
        largura_para_terminal = {}
        largura_nao_terminais = max(len(nao_terminal) for nao_terminal in g.nao_terminais) + 4
        for terminal in ["$", *g.terminais]:
            largura = 0
            for nao_terminal in g.nao_terminais:
                largura_producao = len(" ".join(tabela_analise[nao_terminal][terminal]))
                largura = max(largura, largura_producao)
            largura = max(largura, len(terminal))
            largura_para_terminal[terminal] = largura + 4
        f.write(f"{'':<{largura_nao_terminais}}")
        for terminal in ["$", *g.terminais]:
            f.write(f"{terminal:^{largura_para_terminal[terminal]}}")
        f.write("\n")

        for nao_terminal in g.nao_terminais:
            f.write(f"{nao_terminal:<{largura_nao_terminais}}")
            for terminal in ["$", *g.terminais]:
                f.write(f"{' '.join(tabela_analise[nao_terminal][terminal]):^{largura_para_terminal[terminal]}}")
            f.write("\n")


def ler_tokens(nome_arquivo):
    tokens = []
    with open(nome_arquivo, "r") as f:
        for line in f:
            lexema, padrao = line.strip().split()
            if padrao == "p_r":
                tokens.append(lexema)
            else:
                tokens.append(padrao)
    tokens.append("$")
    return tokens


def union(lista1, lista2):
    for elemento in lista2:
        if elemento not in lista1:
            lista1.append(elemento)


def add(lista, elemento):
    if elemento not in lista:
        lista.append(elemento)


def discard(lista, elemento):
    if elemento in lista:
        lista.remove(elemento)
