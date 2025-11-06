# === constraints.py ===
# Fill in add_constraints(model, X, parsed) using OR-Tools.
# You must enforce:
#   1) Row and column AllDifferent
#   2) Givens (prefilled digits)
#   3) Inequalities:
#        - Horizontal dictionary parsed["horiz"] maps (r,c) -> "<" or ">"
#          and relates X[r][c] ? X[r][c+1].
#        - Vertical dictionary parsed["vert"] maps (r,c) -> "^" or "v"
#          and relates X[r][c] ? X[r+1][c].
#          Here '^' means TOP < BOTTOM (arrow points to larger value),
#               'v' means TOP > BOTTOM.
#
# The CSV format is (2N-1)x(2N-1)   Counting from row 0 and col 0:
#  - Even-even cells contain digits or blank.
#  - Even-odd cells may contain '<' or '>' between horizontal neighbors.
#  - Odd-even cells may contain '^' or 'v' between vertical neighbors.
#
# Example:
#   - parsed["N"] -> size N
#   - parsed["givens"][r][c] is either None or an int in 1..N
#   - parsed["horiz"] and parsed["vert"] as described above.

from ortools.sat.python import cp_model

def add_constraints(model: "cp_model.CpModel", X, parsed):
    N = parsed["N"]
    givens = parsed["givens"]
    horiz  = parsed["horiz"]
    vert   = parsed["vert"]

    # 1) Row and column AllDifferent
    for r in range(N):
        model.AddAllDifferent(X[r])

    for c in range(N):
        col_vars = [X[r][c] for r in range(N)]
        model.AddAllDifferent(col_vars)

    # 2) Givens (prefilled digits)
    for r in range(N):
        for c in range(N):
            if givens[r][c] is not None:
                model.Add(X[r][c] == givens[r][c])

    # 3) Inequalities: Horizontal inequalities
    # horiz[(r, c)] relates X[r][c] ? X[r][c+1]
    for (r, c), sign in horiz.items():
        if sign == "<":
            model.Add(X[r][c] < X[r][c + 1])
        elif sign == ">":
            model.Add(X[r][c] > X[r][c + 1])
        else:
            raise ValueError(f"Unknown horizontal sign {sign} at {(r, c)}")

    # 3) Inequalities: Vertical inequalities
    # vert[(r, c)] relates X[r][c] ? X[r+1][c]
    # '^' means TOP < BOTTOM
    # 'v' means TOP > BOTTOM
    for (r, c), sign in vert.items():
        if sign == "^":
            model.Add(X[r][c] < X[r + 1][c])
        elif sign == "v":
            model.Add(X[r][c] > X[r + 1][c])
        else:
            raise ValueError(f"Unknown vertical sign {sign} at {(r, c)}")