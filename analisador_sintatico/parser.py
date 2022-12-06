import preditivo
import gramatica
import fatoracao
import recursao_esquerda
import first_follow
import epsilon
import utils


def parser(g, tabela_analise, tokens):
    indice_tokens = 0
    pilha = ["$", g.inicial]

    with open("output/pilha.txt", "w") as f:
        f.write(" ".join(pilha) + "\n")
        while pilha[-1] != "$":
            topo = pilha.pop()

            if topo == tokens[indice_tokens]:
                indice_tokens += 1
            elif topo in g.terminais:
                raise SyntaxError("Invalido: Erro Sintático")
            elif tabela_analise[topo][tokens[indice_tokens]] == "\\":
                raise SyntaxError("Invalido: Erro Sintático")
            else:
                for simbolo in reversed(tabela_analise[topo][tokens[indice_tokens]]):
                    if simbolo != "&":
                        pilha.append(simbolo)

            f.write(" ".join(pilha) + "\n")
        print("Valido")


def eh_ll1(g, first, follow):
    for nao_terminal in g.nao_terminais:
        if "&" in first[nao_terminal]:
            if utils.intersection(first[nao_terminal], follow[nao_terminal]):
                return False
    return True

if __name__ == "__main__":
    # Há 3 gramaticas para teste: gramatica1.txt, gramatica2.txt e gramatica3.txt
    g = gramatica.Gramatica("input/gramatica3.txt")
    tokens = utils.ler_tokens("/Users/felipe/Desktop/UFSC/formais_trab/lista_tokens.txt")
    g.imprimir_gramatica()
    print(tokens)

    fatoracao.fatorar(g)
    # epsilon.eliminar(g) # Tirar a epsilon produção pode tornar a gramatica não deterministica.
    recursao_esquerda.eliminar(g)
    first = first_follow.first(g)
    follow = first_follow.follow(g)
    eh_ll1(g, first, follow)
    tabela_analise = preditivo.construir_tabela_analise(g, first, follow)
    utils.salvar_tabela(g, tabela_analise)

    parser(g, tabela_analise, tokens)
