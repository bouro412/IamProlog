import os

operators = ["+", "-", "*", "/", ":-", "=", "==", "===", "<", ">", ".", "(", ")", ",", "[", "]", "|"]
def get_atom(line):
    def is_atom_char(char):
        return char.islower() \
            or char.isupper() \
            or char == '_' \
            or char.isdigit()
    for i in range(len(line)):
        if not(is_atom_char(line[i])):
            return line[:i], line[i:]
    return line, ""
    
def get_sp_atom(line):
    for i in range(1, len(line)):
        if(line[i] == "'"):
            return line[:i+1], line[i+1:]
def get_var(line):
    def is_var_char(char):
        return char.islower() \
            or char.isupper() \
            or char == '_' \
            or char.isdigit()
    for i in range(1, len(line)):
        if not(is_var_char(line[i])):
            return line[:i], line[i:]
    return line, ""
def get_number(line):
    haspoint = False
    for i in range(len(line)):
        if line[i] == '.':
            if not(i + 1 < len(line) and line[i+1].isdigit()):
                return line[:i], line[i:]
            elif haspoint:
                raise Exception("number can't has two \".\"!")
            else:
                haspoint = True
        elif not(line[i].isdigit()):
            return line[:i], line[i:]
    return line, ""
def get_operator(line):
    for ope in operators:
        if line.find(ope) == 0:
            i = len(ope)
            return line[:i], line[i:]
    
def atomInfo(atom):
    if atom == "is":
        return "operator"
    else:
        return "atom"
    
def opInfo(op):
    special_op_list = [("(", "lparen"), (")", "rparen"), (",", "comma"), (".", "period"),
                       ("|", "pipe"), ("[" , "lbracket"), ("]", "rbracket"), (";", "semicolon")]
    for pair in special_op_list:
        if op == pair[0]:
            return pair[1]
    return "operator"

def get_token_from_string(string):
    line = string.strip() 
    while(line):
        head = line[0]
        if head.islower():
            atom, line = get_atom(line)
            yield atom, atomInfo(atom)
        elif head == "'":
            atom, line = get_sp_atom(line)
            yield atom, "atom"
        elif head.isupper() or head == "_":
            var, line = get_var(line)
            yield var, "variable"
        elif head.isdigit():
            num, line = get_number(line)
            yield num, "number"
        elif any((line.find(x) == 0 for x in operators)):
            operator, line = get_operator(line)
            yield operator, opInfo(operator)
        else:
            raise Exception("read error: {}".format(line))
        line = line.strip()

def get_token(path):
    for line in open(path, 'r'):
        for x in get_token_from_string(line):
            yield x

def lexer_test():
    path_name = os.path.normpath(os.path.join(os.path.abspath('test.pl'),''))
    p = get_token(path_name)
    for token in p:
        print(token)
