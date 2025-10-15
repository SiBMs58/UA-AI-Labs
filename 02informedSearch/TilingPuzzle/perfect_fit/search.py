from util import PriorityQueue


def reconstruct_path(came_from, goal_state):
    path = []
    s = goal_state
    while s in came_from:
        s, move = came_from[s]
        path.append(move)
    path.reverse()
    return path

def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def astar(problem, heuristic= nullHeuristic):
    start = problem.getStartState()
    if problem.isGoalState(start):
        return []

    fringe = PriorityQueue()
    fringe.push((start, [], 0), heuristic(start, problem))  # (state, path, g)

    best_g = {start: 0}

    while not fringe.isEmpty():
        state, path, g = fringe.pop()

        if problem.isGoalState(state):
            return path

        # Explore successors
        for succ, action, step_cost in problem.getSuccessors(state):
            new_g = g + step_cost
            if succ not in best_g or new_g < best_g[succ]:
                best_g[succ] = new_g
                f = new_g + heuristic(succ, problem)
                fringe.push((succ, path + [action], new_g), f)

    return []

def ucs(problem):
    """Search the node of least total cost first."""
    # Border case where start state is the goal state
    if problem.isGoalState(problem.getStartState()):
        return problem.getStartState()

    # General case of finiding optimal path
    fringe = PriorityQueue()  # Keep track of the fringe in the case of breadthfrist we use a queue
    fringe.push((problem.getStartState(), [], 0), 0)  # Add the initials start, and its path, and the cost so far. Then for the priority arg we pass 0 for now, it will be the cosqt patgh
    visited = {}  # Keep thrack of the already visited states along witht their costs, to avoid deadlokc, infinite loops

    while not fringe.isEmpty():
        state, path, cost_so_far = fringe.pop()

        if state in visited and visited[state] <= cost_so_far:# If we already visited with a lower cost, skip
            continue
        visited[state] = cost_so_far

        if problem.isGoalState(state): # This is the one, so end
            return path

        for successor, action, step_cost in problem.getSuccessors(state):
            new_cost = cost_so_far + step_cost # push the new cost to the quueue
            fringe.push((successor, path + [action], new_cost), new_cost)

    return []