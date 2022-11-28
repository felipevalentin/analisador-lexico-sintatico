import preditivo
import gramatica


def parser(g, lista_tokens):
    tabela_analise = preditivo.construir_tabela_analise(g)

    indice_tokens = 0
    stack = ["$", g.inicial]
    while stack[-1] != "$":
        if stack[-1] == lista_tokens[indice_tokens]:
            stack.pop()
            indice_tokens += 1
        elif stack[-1] in g.terminais:
            raise "Error"
        elif tabela_analise[stack[-1]][lista_tokens[indice_tokens]] == "\\":
            raise "Error"
        else:
            temp = stack.pop()
            for simbolo in tabela_analise[temp][lista_tokens[indice_tokens]][::-1]:
                if simbolo != "&":
                    stack.append(simbolo)
    print("Ok")


g = gramatica.Gramatica("input/gramatica.txt")
lista_t = ["i", "+", "i", "*", "i", "$"]
parser(g, lista_t)
