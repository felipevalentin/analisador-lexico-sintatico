class RegularExpression:
    def __init__(self, re={}):
        self.re = re

    def read_file(self, name):
        with open(name) as f:
            for line in f:
                def_re, raw_re = line.split(":")
                self.re[def_re] = "".join(self.parse(raw_re))

    def parse(self, raw_re):
        re = raw_re.strip().replace(" ", "")
        re = self.parse_groups(re)
        re = self.expand_extension(re)
        re = self.add_and_symbol(re)
        return re

    def parse_groups(self, raw_re):
        re = raw_re
        for k, v in self.re.items():
            re = re.replace(k, v)
        lower = "|".join(chr(c) for c in range(ord("a"), ord("z") + 1))
        upper = "|".join(chr(c) for c in range(ord("A"), ord("Z") + 1))
        digit = "|".join(chr(c) for c in range(ord("0"), ord("9") + 1))
        re = re.replace("[a-z]", lower)
        re = re.replace("[a-zA-Z]", lower + "|" + upper)
        re = re.replace("[A-Z]", upper)
        re = re.replace("[0-9]", digit)
        return re

    def expand_extension(self, raw_er):
        re = []
        for i in range(len(raw_er)):
            if raw_er[i] == "?":
                if raw_er[i - 1] == ")":
                    re.insert("".join(re).rindex("("), "(")
                else:
                    re.insert(len(re) - 2, "(")
                re += ["|", "&", ")"]
            elif raw_er[i] == "+":
                if raw_er[i - 1] == ")":
                    re += re["".join(re).rindex("(") :]
                else:
                    re.append(re[-1])
                re.append("*")
            else:
                re.append(raw_er[i])
        return re

    def add_and_symbol(self, raw_re):
        re = []
        for i in range(len(raw_re)):
            if (
                i > 1
                and raw_re[i] not in ["|", ")", ".", "*"]
                and raw_re[i - 1] not in ["|", "(", "."]
            ):
                re.append(".")
            re.append(raw_re[i])
        return re


if __name__ == "__main__":
    re = RegularExpression()
    re.read_file("entrada_er.txt")
    for k, v in re.re.items():
        print(f"{k}: {''.join(v)}")
