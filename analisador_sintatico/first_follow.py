import gramatica
import copy

# 3 exemplos de cada
# 3 exemplos de programa com tokens


def first(g):
    first_dict = {}

    # first de terminal = terminal
    for simbolo in [*g.nao_terminais, *g.terminais, "&"]:
        first_dict[simbolo] = [simbolo] if simbolo in [*g.terminais, "&"] else []

    # continuar inserindo ate nao conseguir mais
    while True:
        antigo = copy.deepcopy(first_dict)

        for simbolo in g.nao_terminais:
            for producao in g.producoes[simbolo]:
                if producao[0] in [*g.terminais, "&"]:
                    if producao[0] not in first_dict[simbolo]:
                        first_dict[simbolo].append(producao[0])
                else:
                    for simbolo_producao in producao:
                        for terminal in first_dict[simbolo_producao]:
                            if terminal not in [*first_dict[simbolo], "&"]:
                                first_dict[simbolo].append(terminal)

                        if "&" not in first_dict[simbolo_producao]:
                            break

        if antigo == first_dict:
            return first_dict


def follow(g):
    follow_dict = {}
    first_dict = first(g)
    for nao_terminal in g.nao_terminais:
        follow_dict[nao_terminal] = []

    while True:
        antigo = copy.deepcopy(follow_dict)

        for nao_terminal in g.nao_terminais:
            if nao_terminal == g.inicial:
                if "$" not in follow_dict[nao_terminal]:
                    follow_dict[nao_terminal].append("$")

            for producao in g.producoes[nao_terminal]:
                for i, simbolo in enumerate(producao):

                    if simbolo in g.nao_terminais:
                        first_beta = []
                        for j in range(i + 1, len(producao)):
                            for terminal in first_dict[producao[j]]:
                                if terminal not in first_beta:
                                    first_beta.append(terminal)
                            if "&" not in first_beta:
                                break
                        else:
                            for terminal in follow_dict[nao_terminal]:
                                if terminal not in follow_dict[simbolo]:
                                    follow_dict[simbolo].append(terminal)

                        for terminal in first_beta:
                            if terminal not in [*follow_dict[simbolo], "&"]:
                                follow_dict[simbolo].append(terminal)

        if antigo == follow_dict:
            return follow_dict


if __name__ == "__main__":
    gram = gramatica.Gramatica("input/gramatica.txt")
    for k, v in follow(gram).items():
        print(k, v)
