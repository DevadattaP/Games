from fractions import Fraction

board = [
    ['8','-','4','/','8','/'],
    ['/','1','/','1','/','2'],
    ['8','+','7','+','2','*'],
    ['-','6','+','8','/','4'],
    ['1','+','1','/','1','+'],
    ['*','2','/','5','+','9']
]

target = Fraction(33)

N = len(board)

dirs = [
    (1,0),
    (-1,0),
    (0,1),
    (0,-1)
]


def apply(a, op, b):
    if op == '+':
        return a + b
    elif op == '-':
        return a - b
    elif op == '*':
        return a * b
    elif op == '/':
        if b == 0:
            return None
        return a / b


def dfs(r, c, value, pending_op, expr, visited, path):

    # Reached destination
    if (r, c) == (N-1, N-1):

        if pending_op is None and value == target:
            return path.copy(), expr, value

        return None

    for dr, dc in dirs:

        nr = r + dr
        nc = c + dc

        if not (0 <= nr < N and 0 <= nc < N):
            continue

        if (nr, nc) in visited:
            continue

        token = board[nr][nc]

        visited.add((nr, nc))
        path.append((nr, nc))

        if pending_op is None:

            # Expecting an operator
            if token in "+-*/":

                ans = dfs(
                    nr,
                    nc,
                    value,
                    token,
                    expr + token,
                    visited,
                    path
                )

                if ans:
                    return ans

        else:

            # Expecting a number
            if token.isdigit():

                number = Fraction(int(token))
                new_value = apply(value, pending_op, number)

                if new_value is not None:

                    ans = dfs(
                        nr,
                        nc,
                        new_value,
                        None,
                        expr + token,
                        visited,
                        path
                    )

                    if ans:
                        return ans

        path.pop()
        visited.remove((nr, nc))

    return None


start = Fraction(int(board[0][0]))

result = dfs(
    0,
    0,
    start,
    None,
    board[0][0],       # expression starts with first number
    {(0,0)},
    [(0,0)]
)

if result:
    path, expression, value = result

    print("Expression :", expression)
    print("Value      :", value)
    print("Path:")
    for p in path:
        print(p)
else:
    print("No solution found.")
