# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
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

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
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

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    # Border case where start state is the goal state
    if problem.isGoalState(problem.getStartState()):
        return problem.getStartState()

    # General case of finiding optimal path
    fringe = util.PriorityQueue()  # Keep track of the fringe in the case of breadthfrist we use a queue
    fringe.push((problem.getStartState(), [], 0), 0)  # Add the initials start, and its path, and the cost so far. Then for the priority arg we pass 0 for now, it will be the cosqt patgh
    visited = {}  # Keep thrack of the already visited states along witht their costs, to avoid deadlokc, infinite loops

    while not fringe.isEmpty():
        state, path, cost_so_far = fringe.pop()

        if state in visited and visited[state] <= cost_so_far:# If we already visited with a lower cost, skip
            continue
        visited[state] = cost_so_far

        if problem.isGoalState(state):
            return path

        for successor, action, step_cost in problem.getSuccessors(state):
            new_cost = cost_so_far + step_cost
            fringe.push((successor, path + [action], new_cost), new_cost)

    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
