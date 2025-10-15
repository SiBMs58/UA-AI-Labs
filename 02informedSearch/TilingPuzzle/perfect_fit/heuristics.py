def heuristic(state, problem) -> float:
    """
    Admissible heuristic for the tiling problem.

    h(s) = max( fewest_placements_by_area(s), number_of_empty_components(s) )

    - fewest_placements_by_area: minimal k such that the sum of the k largest
      remaining piece areas >= number of remaining empty cells (ignoring geometry).
    - number_of_empty_components: count connected components (4-neighborhood) of
      currently empty, non-blocked cells; each component needs at least one placement.
    """
    grid, counts = state

    # ----- count remaining empty cells -----
    H, W = problem.H, problem.W
    blocked = problem.blocked
    rem_empty = 0
    for r in range(H):
        row = grid[r]
        for c in range(W):
            if (r, c) in blocked:
                continue
            if row[c] == 0:
                rem_empty += 1

    if rem_empty == 0:
        return 0.0

    # ----- build multiset of available piece sizes -----
    sizes = []
    for i, pid in enumerate(problem.piece_catalog_order):
        cnt = counts[i]
        if cnt <= 0:
            continue
        s = problem.piece_sizes[pid]
        # append with multiplicity
        sizes.extend([s] * cnt)

    # If no pieces left but cells remain, search will discover dead-end;
    # return a small heuristic (admissible) so A* remains correct.
    if not sizes:
        # Component bound still helps a bit
        comp_lb = _count_empty_components(grid, blocked)
        return float(comp_lb)

    # ----- (1) Area bound: minimal k pieces to cover all remaining empty cells -----
    sizes.sort(reverse=True)               # greedy take largest areas first
    covered, k = 0, 0
    for s in sizes:
        k += 1
        covered += s
        if covered >= rem_empty:
            area_lb = k
            break
    else:
        # Even all remaining pieces don't cover the empties -> dead state w.r.t. counts.
        # Still safe to use k (= all pieces) as a (weak) lower bound.
        area_lb = len(sizes)

    # ----- (2) Component bound: number of disconnected empty regions -----
    comp_lb = _count_empty_components(grid, blocked)

    return float(max(area_lb, comp_lb))


def _count_empty_components(grid, blocked) -> int:
    """Count 4-connected components of (grid[r][c] == 0 and not blocked)."""
    H, W = len(grid), len(grid[0]) if grid else 0
    seen = [[False]*W for _ in range(H)]

    def is_empty(r, c):
        return (0 <= r < H and 0 <= c < W and
                (r, c) not in blocked and grid[r][c] == 0)

    comps = 0
    for r in range(H):
        for c in range(W):
            if not is_empty(r, c) or seen[r][c]:
                continue
            # BFS/DFS
            comps += 1
            stack = [(r, c)]
            seen[r][c] = True
            while stack:
                rr, cc = stack.pop()
                for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
                    nr, nc = rr+dr, cc+dc
                    if is_empty(nr, nc) and not seen[nr][nc]:
                        seen[nr][nc] = True
                        stack.append((nr, nc))
    return comps
