class PrologValue:
    def parse(self):
        return self

class Predicate(PrologValue):
    def __init__(self, name, args):
        self.name = name
        self.args = args
    def __repr__(self):
        return "Predicate({0}: {1})".format(self.name, self.args)
    def parse(self):
        self.args = [parse1(x) for x in self.args]
        return self
                        
class Number(PrologValue):
    def __init__(self, number):
        if number.find(".") > -1:
            self.number = float(number)
        else:
            self.number = int(number)
    def __repr__(self):
        return "Number(" + str(self.number) + ")"

class Atom(PrologValue):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return "Atom(" + self.name + ")"

class Variable(PrologValue):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return "Variable({})".format(self.name)

class Operator(PrologValue):
    Power = {":-" : 0, "," : 200, ";" : 200, "|" : 300,
             "is" : 500, "+" : 900, "-" : 900,
             "*" : 800, "/" : 800}
    def __init__(self, name):
        self.name = name
        self.args = []
    def __repr__(self):
        return "Operator({}, {})".format(self.name, self.args)
    def getPower(self):
        return self.Power[self.name]
    
class List(PrologValue):
    def __init__(self, lis):
        self.list = lis
    def __repr__(self):
        return "List({})".format(self.list)
    def parse(self):
        self.list = [parse1(x) for x in self.list]
        return self

def parse1(explist):
    if len(explist) == 1:
        return explist[0].parse()
    else:
        objs = []
        ops = []
        i = (x.parse() if type(x) != str else x for x in explist)
        for x in i:
            if type(x) == Operator:
                while(len(ops) > 0 and ops[-1].getPower() > x.getPower()):
                    op = ops.pop()
                    arg2 = objs.pop()
                    arg1 = objs.pop()
                    op.args = [arg2, arg1]
                    objs.append(op)
                ops.append(x)
            elif type(x) == list:
                objs.append(parse1(x))
            else:
                objs.append(x)
        while(len(ops) > 0):
            op = ops.pop()
            arg1 = objs.pop()
            arg2 = objs.pop()
            op.args = [arg2, arg1]
            objs.append(op)
        return objs[0]
