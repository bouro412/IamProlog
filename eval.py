from parser import Parser
from data import Predicate

## table
def empty_table():
    return dict()
def has_table(key, table):
    return table.get(key) != None
# 破壊的変更
def add_table(name, rule, table):
    if has_table(name, table):
        table[name].append(rule)
    else:
        table[name] = [rule]
    return table
def look_table(name, table):
    return table[name]

## Env
def empty_emv():
    return dict()
# 非破壊的(浅いコピーを返す)
def extend_env(name, value, env):
    newenv = env.copy()
    newenv[name] = value
    return newenv
def look_env(name, env):
    return env[name]

def record_fact(exp, table):
    if not (type(exp) == Predicate):
        raise Exception("Fact must be a Predicate")
    add_table(exp.name, exp, table)
    return
def record_rule(exp, table):
    if not (type(exp) == Operator and exp.name == ":-"):
        raise Exception("rule must be a :- Operator.")
    add_table(exp.args[0].name, exp, table)
    return

def eval_toplevel(parser, table):
    for exp in parser:
        if type(exp) == Predicate:
            record_fact(exp, table)
        elif type(exp) == Operator and exp.name == ":-":
            record_rule(exp, table)
        else:
            raise Exception("Top form is only fact or rule.")
    return table

def eval_test():
    path_name = os.path.normpath(os.path.join(os.path.abspath('test.pl'),''))
    parser = Parser(Reader(get_token(path_name)))
    return eval_toplevel (parser, empty_table())
 
