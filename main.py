# hw1/main.py
# CMPE326 HW1 - Minimum Spanning Tree
# Reads:  udg.dat (from current working directory)
# Writes: mst.dat (to current working directory)
# Prints: minimum spanning weight (to stdout)

from typing import List, Tuple


INF = 10**18


def read_matrix(filename: str) -> List[List[int]]:
    with open(filename, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f.readlines() if ln.strip()]

    matrix: List[List[int]] = []
    for ln in lines:
        row = list(map(int, ln.split()))
        matrix.append(row)

    if not matrix:
        raise ValueError("Input file is empty or unreadable.")

    n = len(matrix)
    for i, row in enumerate(matrix):
        if len(row) != n:
            raise ValueError(f"Matrix is not square: row {i} has {len(row)} cols, expected {n}.")

    # Basic sanity checks for undirected adjacency matrix
    for i in range(n):
        if matrix[i][i] != 0:
            # Not fatal, but usually adjacency matrix diagonal is 0 in this assignment
            pass
        for j in range(i + 1, n):
            if matrix[i][j] != matrix[j][i]:
                raise ValueError(f"Matrix is not symmetric at ({i},{j}) and ({j},{i}).")

    return matrix


def prim_mst(matrix: List[List[int]]) -> Tuple[int, List[int]]:
    """
    Returns:
      total_weight: int
      parent: list where parent[v] is the MST parent of v (parent[root] = -1)
    """
    n = len(matrix)
    in_mst = [False] * n
    key = [INF] * n
    parent = [-1] * n

    root = 0
    key[root] = 0

    for _ in range(n):
        # Pick the non-MST vertex with the smallest key
        u = -1
        best = INF
        for v in range(n):
            if not in_mst[v] and key[v] < best:
                best = key[v]
                u = v

        if u == -1:
            # Graph disconnected (should not happen since it's complete per assignment)
            break

        in_mst[u] = True

        # Relax edges from u to all v
        row_u = matrix[u]
        for v in range(n):
            if not in_mst[v]:
                w = row_u[v]
                if v != u and w < key[v]:
                    key[v] = w
                    parent[v] = u

    total_weight = sum(key)
    return total_weight, parent


def build_mst_matrix(matrix: List[List[int]], parent: List[int]) -> List[List[int]]:
    n = len(matrix)
    mst = [[0] * n for _ in range(n)]
    for v in range(n):
        u = parent[v]
        if u != -1:
            w = matrix[u][v]
            mst[u][v] = w
            mst[v][u] = w
    return mst


def write_matrix(filename: str, mat: List[List[int]]) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        for row in mat:
            f.write(" ".join(map(str, row)) + "\n")


def main() -> None:
    matrix = read_matrix("udg.dat")
    total_weight, parent = prim_mst(matrix)
    mst_mat = build_mst_matrix(matrix, parent)

    # Print minimum spanning weight
    print(total_weight)

    # Save MST matrix
    write_matrix("mst.dat", mst_mat)


if __name__ == "__main__":
    main()