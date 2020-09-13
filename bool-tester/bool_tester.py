import string
import itertools as it

ALLOWED_CHARACTERS = "()10^|*>-="

def check_valid_expression(expression):
    # works 99% of the time!
    open_parens = 0
    for i in expression:
        if i == "(":
            open_parens += 1
        elif i == ")":
            open_parens -= 1
        elif i not in string.ascii_letters and i not in ALLOWED_CHARACTERS:
            return False
    return open_parens == 0

def get_variables(expression):
    s = set(); d = {}
    for i in expression:
        if i in string.ascii_letters:
            s.add(i)
    l = sorted(s)
    for c, el in enumerate(l):
        d[el] = c
    return d

def replace_variables(expression, variable_dict, boolean_combo):
    for i in range(len(expression)):
        if expression[i] in variable_dict:
            expression[i] = "1" if boolean_combo[variable_dict[expression[i]]] else "0"

def list_find(l, x, start = 0):
    try:
        return l.index(x, start)
    except ValueError:
        return -1

def remove_nots_from_expression(expression):
    # this function will correctly handle "--A". (not not A)
    start = 0
    while True:
        not_idx = list_find(expression, "-", start)
        if not_idx == -1:
            return 
        expression.pop(not_idx)
        if expression[not_idx] == "0":
            expression[not_idx] = "1"
        elif expression[not_idx] == "1":
            expression[not_idx] = "0"
        elif expression[not_idx] == "-":
            expression.pop(not_idx)
        start = not_idx
        
gate_expressions = {
    "AND" : ["^", lambda a, b : a == "1" and b == "1"],
    "OR" : ["|", lambda a, b : a == "1" or b == "1"],
    "XOR" : ["*", lambda a, b : a != b],
    "COND" : [">", lambda a, b : not a == "1" or b == "1"],
    "BICOND" : ["=", lambda a, b : a == b],
}

def remove_sub_expression(expression, gate_name):
    start = 0
    gate_char, gate_func = gate_expressions[gate_name]
    while True:
        next_idx = list_find(expression, gate_char, start)
        if next_idx == -1:
            return
        first_char = expression.pop(next_idx - 1)
        second_char = expression.pop(next_idx)
        if gate_func(first_char, second_char):
            expression[next_idx - 1] = "1"
        else:
            expression[next_idx - 1] = "0"
        start = next_idx

def calculate_expression_without_parenthesis(expression):
    #print(expression)
    remove_nots_from_expression(expression)
    remove_sub_expression(expression, "AND")
    remove_sub_expression(expression, "XOR")
    remove_sub_expression(expression, "OR")
    remove_sub_expression(expression, "COND")
    remove_sub_expression(expression, "BICOND")
    return expression[0]    # should only be 1 character left, 0 or 1.

def calculate_expression(expression):
    while True:
        new_expression = []
        close_paren_idx = list_find(expression, ")")
        if close_paren_idx == -1:
            if len(expression) == 1:
                return expression[0]
            return calculate_expression_without_parenthesis(expression)
        else:
            for i in range(close_paren_idx - 1, -1, -1):
                if expression[i] == "(":
                    break
            open_paren_idx = i
            res = calculate_expression_without_parenthesis(expression[open_paren_idx + 1 : close_paren_idx])
            #print("yeah", res, expression, new_expression)
            for j in range(open_paren_idx):
                new_expression.append(expression[j])
            new_expression.append(res)
            for k in range(close_paren_idx + 1, len(expression)):
                new_expression.append(expression[k])
            expression = new_expression

def print_result(combo, result):
    bool_letters = ["F", "T"]
    #print(combo, end = " ")
    for i in range(len(combo)):
        print(" " + bool_letters[combo[i]] + " |", end = "")
    print(" " + bool_letters[int(result)])

def explore_expression(expression):
    if not check_valid_expression(expression):
        print("Invalid expression!")
        return
    variables = get_variables(expression)
    num_variables = len(variables)
    combos = it.product([True, False], repeat = num_variables)
    print(" ", end = "")
    for c, variable in enumerate(variables):
        print(variable, end = "")
        if c != num_variables - 1:
            print(" | ", end = "")
    print(" | * ")
    print("-" * (4 * (num_variables + 1) - 1))
    for combo in combos:
        expression_list = list(expression)
        replace_variables(expression_list, variables, combo)
        res = calculate_expression(expression_list)
        print_result(combo, res)

while True:
    inp = input()
    if inp == "quit":
        break
    explore_expression(inp)
