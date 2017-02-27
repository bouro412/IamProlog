from data import *
from lexer import get_token, get_token_from_string
from reader import Reader
from itertools import takewhile
import os

class Parser:
    def __init__(self, reader):
        self.reader = reader.__iter__()

    def __iter__(self):
        return self

    def __next__(self):
        exp = list(takewhile(lambda x: x != "period",
                             self.reader))
        if exp == []:
            raise StopIteration()
        return parse1(exp)
       
def parse_test():
    path_name = os.path.normpath(os.path.join(os.path.abspath('test.pl'),''))
    for x in Parser(Reader(get_token(path_name))):
        print(x)
def str_parse(string):
    return list(Parser(Reader(get_token_from_string(string))))
def str_read(string):
    return list(Reader(get_token_from_string(string)))
