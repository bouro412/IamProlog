
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
        def in_predicate_parse(exp):
            if len(exp) == 1:
                return exp[0].parse()
            else:
                stack = []
                predOp = None
                it = iter(exp)
                for x in it:
                    if type(x) == Operator:
                        if predOp == None:
                            predOp = x
                            stack.append(x)
                        else:
                            n = next(it)
                            if x.getPower() > predOp.getPower():
                                x.args = [stack.pop(), n]
                                stack.append(x)
                            else:
                                prev = stack.pop()
                                preop = stack.pop()
                                pprev = stack.pop()
                                preop.args = [prev, pprev]
                                stack.append(preop)
                                stack.append(x)
                                predOp = x
                    else:
                        stack.append(x.parse())
                if len(stack) == 1:
                    return stack[0]
                elif predOp != None:
                    predOp.args = [stack[0], stack[2]]
                    return predOp
                else:
                    raise Exception("parse error: {}".format(exp))
        self.args = [in_predicate_parse(x) for x in self.args]
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
        def in_predicate_parse(exp):
            if len(exp) == 0:
                return []
            else:
                stack = []
                predOp = None
                it = iter(exp)
                for x in exp:
                    if type(x) == Operator:
                        if predOp == None:
                            predOp = x
                            stack.append(x)
                        else:
                            n = next(it)
                            if x.getPower() > predOp.getPower():
                                x.args = [stack.pop(), n]
                                stack.append(x)
                            else:
                                prev = stack.pop()
                                preop = stack.pop()
                                pprev = stack.pop()
                                preop.args = [prev, pprev]
                                stack.append(preop)
                                stack.append(x)
                                predOp = x
                    else:
                        stack.append(x.parse())
                if len(stack) == 1:
                    return stack[0]
                elif predOp != None:
                    predOp.args = [stack[0], stack[2]]
                    return predOp
                else:
                    raise Exception("parse error: {}".format(exp))
        self.list = [in_predicate_parse(x) for x in self.list]
        return self
