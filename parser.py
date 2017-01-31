from data import *
from lexer import get_token, get_token_from_string
from reader import Reader
from itertools import takewhile

class Parser:
    def __init__(self, reader):
        self.reader = reader.__iter__()

    def __iter__(self):
        return self

    def __next__(self):
        stack = []
        preOps = []
        def push(obj):
            stack.append(obj)
            if type(obj) == Operator:
                preOps.append(obj)
            return
        for term in self.reader:
            if type(term) != str:
                term = term.parse()
            if term == "period":
                if preOp != []:
                   pre = stack[0]
                   op = stack[1]
                   n = stack[2]
                   op.args = [pre, n]
                   return op
                elif len(stack) == 1:
                    return stack[0]
                else:
                    raise Exception("Parse Error.")
            elif type(term) == Operator:
                if preOp == None:
                    stack.append(term)
                    preOp = term
                else:
                    if preOp.getPower() < term.getPower():
                        n = next(self.reader)
                        pre = stack.pop()
                        term.args = [pre, n]
                        stack.append(term)
                    else:
                        pre = stack.pop()
                        op = stack.pop()
                        ppre = stack.pop()
                        op.args = [ppre, pre]
                        stack.append(op)
                        stack.append(term)
                        preOp = term
            else:
                stack.append(term)
        raise StopIteration()


def parse_test():
    for x in Parser(Reader(get_token("/home/keita/Documents/prolog/gomi.pl"))):
        print(x)
def str_parse(string):
    return list(Parser(Reader(get_token_from_string(string))))
def str_read(string):
    return list(Reader(get_token_from_string(string)))
