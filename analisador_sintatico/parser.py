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
                print("Invalido")
                raise ValueError
            elif tabela_analise[topo][tokens[indice_tokens]] == "\\":
                print("Invalido")
                raise ValueError
            else:
                for simbolo in reversed(tabela_analise[topo][tokens[indice_tokens]]):
                    if simbolo != "&":
                        pilha.append(simbolo)

            f.write(" ".join(pilha) + "\n")
        print("Valido")


if __name__ == "__main__":
    # Há 3 gramaticas para teste: gramatica1.txt, gramatica2.txt e gramatica3.txt
    g = gramatica.Gramatica("input/gramatica1.txt")
    tokens = utils.ler_tokens("input/tokens1.txt")
    g.imprimir_gramatica()
    print(tokens)

    fatoracao.fatorar(g)
    # epsilon.eliminar(g) # Tirar a epsilon produção pode tornar a gramatica não deterministica.
    recursao_esquerda.eliminar(g)
    first = first_follow.first(g)
    follow = first_follow.follow(g)
    tabela_analise = preditivo.construir_tabela_analise(g, first, follow)
    utils.salvar_tabela(g, tabela_analise)

    parser(g, tabela_analise, tokens)
