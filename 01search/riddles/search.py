from typing import List
import util

def depthFirstSearch(problem) :
    """Place your DFS algorithm from pacman here"""
    # Border case where start state is the goal state
    if problem.isGoalState(problem.getStartState()):
        return problem.getStartState()

    # General case of finiding optimal path
    fringe = util.Stack() # Keep track the fringe in the case of depthfirst its of a stack containing (state, path)
    fringe.push((problem.getStartState(), [])) # Start withe pushing the start staete to the fringe
    visited = [] # Keep a list of visited stated else we could have a deadlock/infite loop
    while not fringe.isEmpty():
        state, path = fringe.pop()

        if state in visited: # Check if we already visited
            continue
        visited.append(state)

        if problem.isGoalState(state): # If this state is the goal state we get the path corrresponding tot the state
            return path

        for successor, action, step_cost in problem.getSuccessors(state): # Then we have a look at its successors, along wiht tther cost and actions
            if successor not in visited: # check if we already visited the succesoor
                fringe.push((successor, path + [action])) # if not, we push the tuple to the frigne

    return []



def breadthFirstSearch(problem):
    """Place your BFS algorithm from pacman here"""
    # Border case where start state is the goal state
    if problem.isGoalState(problem.getStartState()):
        return problem.getStartState()

    # General case of finiding optimal path
    fringe = util.Queue() # Keep track of the fringe in the case of breadthfrist we use a queue
    fringe.push((problem.getStartState(), [])) # Add the initials start, and its path
    visited = [] # Keep thrack of the already visited states, to avoid deadlokc, infinite loops

    while not fringe.isEmpty():
        state, path = fringe.pop()
        if state in visited:
            continue
        visited.append(state)

        if problem.isGoalState(state):
            return path

        for successor, action, step_cost in problem.getSuccessors(state):
            if successor not in visited:
                fringe.push((successor, path + [action]))

    return []

