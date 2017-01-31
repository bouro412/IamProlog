from lexer import get_token
from data import *

class Reader:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer.__iter__()
        self.stack = []

    def getnext(self):
        try:
            return self.state.__next__()
        except StopIteration:
            return None
    def __iter__(self):
        return self

    def __next__(self):
        def match(token, tag):
            if tag == "lparen":
                return self.readparen(tag)
            elif tag == "lbracket":
                return List(self.readparen(tag))
            elif tag == "atom":
                try:
                    (ntoken, ntag) = self.tokenizer.__next__()
                    if ntag == "lparen":
                        return Predicate(token, self.readparen(ntag))
                    else:
                        self.stack.append((ntoken, ntag))
                        return Atom(token)
                except StopIteration:
                    return Atom(token)
            elif tag == "period":
                return "period"
            elif tag == "comma":
                return Operator(",")
            elif tag == "semicolon":
                return Operator(";")
            elif tag == "pipe":
                return Operator("|")
            elif tag == "variable" or tag == "number" or tag == "operator":
                return self.makevalue(token, tag)
            else:
                raise Exception("prolog: read error")
        if len(self.stack) != 0:
            token, tag = self.stack.pop()
            return match(token, tag)
        for (token, tag) in self.tokenizer:
            return match(token, tag)
        raise StopIteration()

    def readparen(self, paren_tag):
        lis = []
        term = []
        lp = 0
        lb = 0
        rtag = "r" + paren_tag[1:]
        for (token, tag) in self.tokenizer:
            if tag == "comma" and lp == lb == 0:
                lis.append(list(Reader(term)))
                term = []
            elif tag == rtag and lp == lb == 0:
                lis.append(list(Reader(term)))
                return lis
            elif tag == "lparen":
                lp += 1
                term.append((token, tag))
                
            elif tag == "lbracket":
                lb += 1
                term.append((token, tag))
            elif tag == "rparen":
                lp -= 1
                term.append((token, tag))
            elif tag == "rbracket":
                lb -= 1
                term.append((token, tag))
            else:
                term.append((token, tag))


    def makevalue(self, token, tag):
        if tag == "number":
            return Number(token)
        elif tag == "atom":
            return Atom(token)
        elif tag == "variable":
            return Variable(token)
        elif tag == "operator":
            return Operator(token)
        else:
            raise Exception(tag + " can't make value.")

def read_test():
    for x in Reader(get_token("/home/keita/Documents/prolog/gomi.pl")):
        print(x)
