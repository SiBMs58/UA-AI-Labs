# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        newCapsules = successorGameState.getCapsules()

        # Start from the game’s internal score (captures things like food eaten)
        score = successorGameState.getScore()

        # --- Food: approach it
        for foodPos in newFood.asList():
            score += 1 / manhattanDistance(newPos, foodPos)

        # --- Capsules: approach it
        for pelletPos in newCapsules:
            score += 1 / manhattanDistance(newPos, pelletPos)

        # --- Ghosts: avoid when dangerous, approach when scared
        for ghostState in newGhostStates:
            ghostPos = ghostState.getPosition()
            gdist = manhattanDistance(newPos, ghostPos)

            if ghostState.scaredTimer > 0:
                # Ghost is scared: approach it
                score += 10.0 / (gdist + 1.0)
            else:
                # Ghost is not scared: avoid it
                if gdist == 0:
                    return float('-inf')  # suicide
                score -= 10.0 / (gdist + 1.0)

        return score



def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        numAgents = gameState.getNumAgents()

        def minimax(agentIndex, depth, state):
            # Terminal / cutoff
            if depth == self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            actions = state.getLegalActions(agentIndex)
            if not actions:  # no legal actions → evaluate leaf
                return self.evaluationFunction(state)

            nextAgent = (agentIndex + 1) % numAgents
            nextDepth = depth + 1 if nextAgent == 0 else depth

            if agentIndex == 0:  # Pacman (max)
                value = float('-inf')
                for a in actions:
                    succ = state.generateSuccessor(agentIndex, a)
                    value = max(value, minimax(nextAgent, nextDepth, succ))
                return value
            else:  # Ghosts (min)
                value =float('inf')
                for a in actions:
                    succ = state.generateSuccessor(agentIndex, a)
                    value = min(value, minimax(nextAgent, nextDepth, succ))
                return value

        # Choose the maximizing action at the root (Pacman)
        bestScore = float('-inf')
        bestAction = Directions.STOP
        for a in gameState.getLegalActions(0):
            succ = gameState.generateSuccessor(0, a)
            score = minimax(1, 0, succ)
            if score > bestScore:
                bestScore = score
                bestAction = a

        return bestAction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        numAgents = gameState.getNumAgents()

        def maxValue(state, alpha, beta, depth):
            # Terminal test
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state), None

            v = -float("inf")
            bestAction = None

            for action in state.getLegalActions(0):  # Pacman
                successor = state.generateSuccessor(0, action)
                score = minValue(successor, 1, alpha, beta, depth)
                if score > v:
                    v, bestAction = score, action
                if v > beta:   # Beta cutoff
                    return v, bestAction
                alpha = max(alpha, v)

            return v, bestAction

        def minValue(state, agentIndex, alpha, beta, depth):
            # Terminal test
            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            v = float("inf")
            nextAgent = (agentIndex + 1) % numAgents

            for action in state.getLegalActions(agentIndex):
                successor = state.generateSuccessor(agentIndex, action)
                # Next agent wraps to Pacman → increase depth
                if nextAgent == 0:
                    score, _ = maxValue(successor, alpha, beta, depth + 1)
                else:
                    score = minValue(successor, nextAgent, alpha, beta, depth)
                v = min(v, score)
                if v < alpha:  # Alpha cutoff
                    return v
                beta = min(beta, v)

            return v

        _, action = maxValue(gameState, -float("inf"), float("inf"), 0)
        return action


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        numAgents = gameState.getNumAgents()

        def value(state, agentIndex, depth):
            # Terminal test
            if depth == self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            # Pseudocode: if the next agent is MAX → max-value; if EXP → exp-value
            if agentIndex == 0:
                return max_value(state, depth)
            else:
                return exp_value(state, agentIndex, depth)

        def max_value(state, depth):
            # def max-value(state): v = -∞; for each successor: v = max(v, value(successor))
            actions = state.getLegalActions(0)
            if not actions:
                return self.evaluationFunction(state)

            v = -float("inf")
            for a in actions:
                succ = state.generateSuccessor(0, a)
                v = max(v, value(succ, 1, depth))   # next agent is first ghost, same ply
            return v

        def exp_value(state, agentIndex, depth):
            # def exp-value(state): v = 0; for each successor: v += p * value(successor); return v
            actions = state.getLegalActions(agentIndex)
            if not actions:
                return self.evaluationFunction(state)

            p = 1.0 / len(actions)  # uniform randomness
            v = 0.0
            nextAgent = (agentIndex + 1) % numAgents
            nextDepth = depth + 1 if nextAgent == 0 else depth  # increase depth after last ghost

            for a in actions:
                succ = state.generateSuccessor(agentIndex, a)
                v += p * value(succ, nextAgent, nextDepth)
            return v

        # Choose the maximizing action at the root
        bestScore = -float("inf")
        bestAction = None
        for a in gameState.getLegalActions(0):
            succ = gameState.generateSuccessor(0, a)
            score = value(succ, 1, 0)  # first ghost moves next, depth still 0
            if score > bestScore or bestAction is None:
                bestScore, bestAction = score, a

        return bestAction

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
