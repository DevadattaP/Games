import ast
import operator
import re

variables = ['A','B','C','D','E','F','G','H','I']
digits = [20,8,72,48,11,18,9,5,13]

equations = [
    ("A+B+C", 41),
    ("D+E*F", 312),
    ("G-H+I", 16),
    ("A-D/G", 9),
    ("B/E+H", 15),
    ("C*F-I", 375),
]


# -------------------------------------------------------
# Safe expression evaluator
# -------------------------------------------------------

OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
}


def eval_ast(node):
    if isinstance(node, ast.Constant):
        return node.value

    if isinstance(node, ast.Name):
        return assignment[node.id]

    if isinstance(node, ast.UnaryOp):
        return OPS[type(node.op)](eval_ast(node.operand))

    if isinstance(node, ast.BinOp):
        left = eval_ast(node.left)
        right = eval_ast(node.right)

        # avoid division by zero
        if isinstance(node.op, ast.Div) and right == 0:
            raise ZeroDivisionError

        return OPS[type(node.op)](left, right)

    raise ValueError(node)


def evaluate(expr):
    tree = ast.parse(expr, mode="eval")
    return eval_ast(tree.body)


# -------------------------------------------------------
# Parse variables used in each equation
# -------------------------------------------------------

compiled = []

for expr, target in equations:
    vars_used = set(re.findall(r"[A-Z]", expr))
    compiled.append((expr, target, vars_used))


# -------------------------------------------------------
# Check completed equations
# -------------------------------------------------------

def constraints_ok():

    for expr, target, vars_used in compiled:

        # not all variables assigned yet
        if not vars_used.issubset(assignment.keys()):
            continue

        try:
            value = evaluate(expr)
        except ZeroDivisionError:
            return False

        if abs(value - target) > 1e-9:
            return False

    return True


# -------------------------------------------------------
# Backtracking
# -------------------------------------------------------

assignment = {}


def solve(index, remaining_digits):

    if index == len(variables):
        return True

    var = variables[index]

    for d in remaining_digits:

        assignment[var] = d

        if constraints_ok():

            new_remaining = remaining_digits.copy()
            new_remaining.remove(d)

            if solve(index + 1, new_remaining):
                return True

        del assignment[var]

    return False


# -------------------------------------------------------

if solve(0, digits.copy()):

    print("Solution\n")

    for v in variables:
        print(f"{v} = {assignment[v]}")

else:
    print("No solution")