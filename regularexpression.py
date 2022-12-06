class Regex:
    def __init__(self, def_re=None, re=None, parsed=[]):
        self.def_re = def_re
        self.alphabet = []
        self.re = self.parse(re, parsed)

    def parse(self, raw_re, parsed):
        re = raw_re.strip().replace(" ", "")
        re = self.parse_groups(re, parsed)
        re = self.create_regex_list(re)
        re = self.expand_extension(re)
        return "".join(re)

    def parse_groups(self, raw_re, parsed={}):
        re = raw_re
        for parsed_re in parsed:
            temp = "(" + parsed_re.re + ")"
            re = re.replace(parsed_re.def_re, temp)
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
                    re.insert(len(re) - 1, "(")
                re += ["|", "&", ")"]
            elif raw_er[i] == "+":
                if raw_er[i - 1] == ")":
                    re.append(".")
                    re += re["".join(re).rindex("(") : -1]
                else:
                    re.append(re[-1])
                re.append("*")
            else:
                re.append(raw_er[i])
        return re

    def add_end_of_regex_symbol(self, raw_re):
        re = list(raw_re)
        re.insert(0, "(")
        re = re + [")", ".", "#"]
        return re

    def create_regex_list(self, raw_re):
        re = [*raw_re]
        is_id = False
        for c in raw_re:
            if c == "\\" and not is_id:
                is_id = True
            elif c not in ["(", ")", ".", "*", "|", "+", "?"] or is_id:
                if c not in self.alphabet:
                    self.alphabet.append(c)
                is_id = False
        return re