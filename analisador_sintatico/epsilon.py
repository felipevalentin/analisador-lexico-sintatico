import gramatica
import utils
import copy


def eliminar(g):
    # Calculamos o conjunto epsilon e montamos as novas produções com base no powerset de uma produção, ignorando
    # todas as produções que não incluem os simbolos que não estão no conjunto epsilon
    conjunto_epsilon = construir_conjunto_epsilon(g)
    nao_terminais = copy.deepcopy(g.nao_terminais)
    for nao_terminal in nao_terminais:
        novas_producoes_nao_terminal = []
        for producao in g.producoes[nao_terminal]:
            conjunto_nao_epsilon = {
                item: producao.count(item)
                for item in producao
                if item not in conjunto_epsilon
            }
            if nao_terminal == g.inicial and not conjunto_nao_epsilon:
                novo_inicial = nao_terminal
                while novo_inicial in g.nao_terminais:
                    novo_inicial += "'"
                g.producoes[novo_inicial] = [[g.inicial], ["&"]]
                g.nao_terminais.insert(0, novo_inicial)
                g.inicial = novo_inicial

            novas_producoes = powerset(producao)
            for nova_producao in novas_producoes:
                if all(
                    nova_producao.count(k) >= v for k, v in conjunto_nao_epsilon.items()
                ):
                    utils.add(novas_producoes_nao_terminal, nova_producao)
        utils.union(g.producoes[nao_terminal], novas_producoes_nao_terminal)
        utils.discard(g.producoes[nao_terminal], ["&"])


def construir_conjunto_epsilon(g):
    conjunto_epsilon = []
    while True:
        antigo = copy.deepcopy(conjunto_epsilon)
        for nao_terminal in g.nao_terminais:
            for producao in g.producoes[nao_terminal]:
                if producao == ["&"]:
                    utils.add(conjunto_epsilon, nao_terminal)
                for simbolo in producao:
                    if simbolo not in conjunto_epsilon:
                        break
                else:
                    utils.add(conjunto_epsilon, nao_terminal)
        if conjunto_epsilon == antigo:
            break
    return conjunto_epsilon


def powerset(seq):
    ans = [[]]

    for n in seq:
        ans += [a + [n] for a in ans]
    ans.remove([])
    return ans


if __name__ == "__main__":
    # Há 3 gramaticas para teste: gramatica1.txt, gramatica2.txt e gramatica3.txt
    g = gramatica.Gramatica("testes/epsilon/gramatica3.txt")
    g.imprimir_gramatica()
    eliminar(g)
    g.imprimir_gramatica()
