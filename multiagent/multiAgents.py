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

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
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

    def evaluationFunction(self, currentGameState, action):
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

        "*** YOUR CODE HERE ***"
        if successorGameState.isWin(): return successorGameState.getScore()
        if successorGameState.isLose(): return -999999999
        foodList = newFood.asList()
        #distToClosetGhost = min([util.manhattanDistance(newPos, ghost) for ghost in ghostList])
        distToClosetFood = min([util.manhattanDistance(newPos, food) for food in foodList])
        # if len(newGhostStates) > 0: distToClosetGhost = min([util.manhattanDistance(newPos, ghost) for ghost in newGhostStates if ghost.scaredTimer != 0])
        # else: distToClosetGhost = 0
        distToClosetGhost = 999999999
        for ghost in newGhostStates:
            if ghost.scaredTimer == 0: distToClosetGhost = min(distToClosetGhost, util.manhattanDistance(newPos, ghost.getPosition()))
        if distToClosetGhost == 999999999: distToClosetGhost = 0
        return successorGameState.getScore() - distToClosetFood + distToClosetGhost
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
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

    def getAction(self, gameState):
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
        """
        "*** YOUR CODE HERE ***"
        def maxValue(state, depth):
            if state.isWin() or state.isLose() or depth == self.depth: return self.evaluationFunction(state)
            value = -999999999
            actions = state.getLegalActions(0);
            nextAction = Directions.STOP
            for action in actions:
                successorState = state.generateSuccessor(0, action)
                newValue = minValue(successorState, depth, 1)
                if newValue > value:
                    value = newValue
                    nextAction = action
            if depth == 0: return nextAction
            return value

        def minValue(state, depth, ghostIndex):
            if state.isWin() or state.isLose() or depth == self.depth: return self.evaluationFunction(state)
            numAgents = state.getNumAgents()
            if numAgents == 1: return maxValue(state, depth + 1)
            value = 999999999
            actions = state.getLegalActions(ghostIndex)
            for action in actions:
                successorState = state.generateSuccessor(ghostIndex, action)
                if ghostIndex < numAgents - 1: value = min(value, minValue(successorState, depth, ghostIndex + 1))
                else: value = min(value, maxValue(successorState, depth + 1))
            return value
        return maxValue(gameState, 0)
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def maxValue(state, depth, alpha, beta):
            if state.isWin() or state.isLose() or depth == self.depth: return self.evaluationFunction(state)
            actions = state.getLegalActions(0)
            value = -999999999
            nextMove = Directions.STOP
            for action in actions:
                successorState = state.generateSuccessor(0, action)
                newValue = minValue(successorState, depth, alpha, beta, 1)
                if newValue > value:
                    value = newValue
                    nextMove = action
                if value > beta: break
                alpha = max(alpha, value)
            if depth == 0: return nextMove
            else: return value

        def minValue(state, depth, alpha, beta, index):
            if state.isWin() or state.isLose() or depth == self.depth: return self.evaluationFunction(state)
            numAgents = state.getNumAgents()
            value = 999999999
            actions = state.getLegalActions(index)
            for action in actions:
                successorState = state.generateSuccessor(index, action)
                if numAgents - 1 ==  index: newValue = maxValue(successorState, depth + 1, alpha, beta)
                else: newValue = minValue(successorState, depth, alpha, beta, index + 1)
                value = min(value, newValue)
                beta = min(beta, value)
                if value < alpha: break
            return value

        return maxValue(gameState, 0, -999999999, 999999999)
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        def maxValue(state, depth):
            if state.isWin() or state.isLose() or depth == self.depth: return self.evaluationFunction(state)
            actions = state.getLegalActions(0)
            value = -999999999
            move = ""
            for action in actions:
                successorState = state.generateSuccessor(0, action)
                newValue = expValue(successorState, depth, 1)
                if newValue > value:
                    value = newValue
                    move = action
            if depth == 0: return move
            else: return value

        def expValue(state, depth, index):
            if state.isWin() or state.isLose() or depth == self.depth: return self.evaluationFunction(state)
            value = 0
            actions = state.getLegalActions(index)
            num = len(actions)
            numAgents = state.getNumAgents()
            for action in actions:
                successorState = state.generateSuccessor(index, action)
                if numAgents - 1 == index: value = value + maxValue(successorState, depth + 1)
                else: value = value + expValue(successorState, depth, index + 1)
            return float(value) / num
        move = maxValue(gameState, 0)
        #print move
        return move
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    if currentGameState.isWin(): return currentGameState.getScore()
    if currentGameState.isLose(): return -999999999
    position = currentGameState.getPacmanPosition()
    foodList = currentGameState.getFood().asList()
    distToClosetFood = min([util.manhattanDistance(position, food) for food in foodList])
    return currentGameState.getScore() - (distToClosetFood + len(foodList))
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
