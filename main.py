import syntaxtree
import automata
import regularexpression


def regex_from_read_file(name):
    res = []
    with open(name) as f:
        for line in f:
            def_re, raw_re = line.split(":")
            res.append(regularexpression.Regex(def_re, raw_re, res))
    return res


def main():
    regexs = regex_from_read_file("input/er.txt")
    automatos = {}
    for regex in regexs:
        tree = syntaxtree.Tree(regex.add_end_of_regex_symbol(regex.re))
        dfa = automata.Automata(alfabeto=regex.alphabet)
        dfa.re2dfa(tree)
        automatos[regex.def_re] = dfa
    for k, v in automatos.items():
        v.escrever_arquivo("output/" + str(k) + ".txt")


if __name__ == "__main__":
    main()
