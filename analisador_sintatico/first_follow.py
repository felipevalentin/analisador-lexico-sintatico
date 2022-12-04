import gramatica
import copy
import utils


def first(g):
    first_dict = {}

    # first de terminal = terminal
    for simbolo in [*g.nao_terminais, *g.terminais, "&"]:
        first_dict[simbolo] = [simbolo] if simbolo in [*g.terminais, "&"] else []

    # continuar inserindo ate não ter diferença
    # o algoritmo usado é o do livro do aho
    while True:
        antigo = copy.deepcopy(first_dict)

        for simbolo in g.nao_terminais:
            for producao in g.producoes[simbolo]:
                if producao[0] in [*g.terminais, "&"]:
                    utils.add(first_dict[simbolo], producao[0])
                else:
                    for simbolo_producao in producao:
                        for terminal in first_dict[simbolo_producao]:
                            if terminal != "&":
                                utils.add(first_dict[simbolo], terminal)

                        if "&" not in first_dict[simbolo_producao]:
                            break
                    else:
                        utils.add(first_dict[simbolo], "&")

        if antigo == first_dict:
            return first_dict


def follow(g):
    follow_dict = {}
    first_dict = first(g)
    for nao_terminal in g.nao_terminais:
        follow_dict[nao_terminal] = []

    # continuar inserindo ate não ter diferença
    # algoritmo usado do livro do aho
    utils.add(follow_dict[g.inicial], "$")
    while True:
        antigo = copy.deepcopy(follow_dict)
        for nao_terminal in g.nao_terminais:
            for producao in g.producoes[nao_terminal]:
                for i, simbolo in enumerate(producao):

                    if simbolo in g.nao_terminais:
                        first_beta = []
                        for j in range(i + 1, len(producao)):
                            utils.union(first_beta, first_dict[producao[j]])
                            if "&" not in first_beta:
                                break
                        else:
                            utils.union(follow_dict[simbolo], follow_dict[nao_terminal])

                        for terminal in first_beta:
                            if terminal != "&":
                                utils.add(follow_dict[simbolo], terminal)

        if antigo == follow_dict:
            return follow_dict


if __name__ == "__main__":
    # Há 3 gramaticas para teste: gramatica1.txt, gramatica2.txt e gramatica3.txt
    g = gramatica.Gramatica("testes/first_follow/gramatica2.txt")
    print("FIRST")
    for k, v in first(g).items():
        print(k, v)
    print()
    print("FOLLOW")
    for k, v in follow(g).items():
        print(k, v)
