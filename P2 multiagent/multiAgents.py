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
        #find position of cloest ghost
        closestghost = min([manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates])

        if closestghost:
            ghost_dist = -10/closestghost
        else:
            ghost_dist = -1000

        foodList = newFood.asList()
        if foodList:
            closestfood = min([manhattanDistance(newPos, food) for food in foodList])
        else:
            closestfood = 0

        # large weight to number of food left
        return (-2 * closestfood) + ghost_dist - (100*len(foodList))



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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        numAgents = gameState.getNumAgents()
        scores = []

        def _minimax(state, iterCount):
            # if reached depth or win or lose, evaluate state
          if iterCount >= self.depth*numAgents or state.isWin() or state.isLose():
            return self.evaluationFunction(state)
          if iterCount % numAgents != 0: #is Ghost min
            result = 1e10
            for action in state.getLegalActions(iterCount % numAgents):
               #state with iteration count
              successors = state.generateSuccessor(iterCount % numAgents, action)
              result = min(result, _minimax(successors, iterCount+1))
            return result
          else:     #is Pacman max
            result = -1e10
            for action in state.getLegalActions(iterCount % numAgents):
                #state iteration count
              successors = state.generateSuccessor(iterCount % numAgents, action)
              result = max(result, _minimax(successors, iterCount+1))
              if iterCount == 0:
                scores.append(result)
            return result
        result = _minimax(gameState, 0)
        return gameState.getLegalActions(0)[scores.index(max(scores))]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def alphabeta(state):
            value, bestAction = None, None
            #a is the best value that the maximizer currently can guarantee at that level or above.
            #b is the best value that the minimizer currently can guarantee at that level or above.
            a, b = None, None
            for action in state.getLegalActions(0):
                if value is None:
                    value = minValue(state.generateSuccessor(0, action), 1, 1, a, b)
                else:
                    value = max(value, minValue(state.generateSuccessor(0, action), 1, 1, a, b))
                if a is None:
                    a = value
                    bestAction = action
                else:
                    a, bestAction = max(value, a), action if value > a else bestAction
            return bestAction
        #min value
        def minValue(state, agentIdx, depth, a, b):
            #if the last index agent, max value
            if agentIdx == state.getNumAgents():
                return maxValue(state, 0, depth + 1, a, b)
            #else
            value = None
            #calculate score for each possible action by recursively calling min_agent
            for action in state.getLegalActions(agentIdx):
                succ = minValue(state.generateSuccessor(agentIdx, action), agentIdx + 1, depth, a, b)
                if value is None:
                    value = succ
                else:
                    value = min(value, succ)
                if a is not None and value < a:
                    return value
                if b is None:
                    b = value
                else:
                    b = min(b, value)
            if value is not None:
                return value
            else:
                return self.evaluationFunction(state)


        def maxValue(state, agentIdx, depth, a, b):
            #if depth, evaluation state
            if depth > self.depth:
                return self.evaluationFunction(state)
            value = None
            # calculate score for each possible action by recursively calling min_agent
            for action in state.getLegalActions(agentIdx):
                succ = minValue(state.generateSuccessor(agentIdx, action), agentIdx + 1, depth, a, b)
                if value is None:
                    value = succ
                else:
                    value = max(value, succ)
                if b is not None and value > b:
                    return value
                if a is None:
                    a = value
                else:
                    a = max(a, value)
            if value is not None:
                return value
            else:
                return self.evaluationFunction(state)

        action = alphabeta(gameState)

        return action

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
        numAgents = gameState.getNumAgents()
        ActionScore = []
        def _expectMinimax(s, iterCount):
            if iterCount >= self.depth * numAgents or s.isWin() or s.isLose():  # leaf node
                return self.evaluationFunction(s)
            if iterCount % numAgents != 0: #is ghost min
                successorScore = []
                for a in s.getLegalActions(iterCount % numAgents):
                    # state with iteration count
                    new_gameState = s.generateSuccessor(iterCount % numAgents, a)
                    result = _expectMinimax(new_gameState, iterCount + 1)
                    successorScore.append(result)
                averageScore = sum([float(x) / len(successorScore) for x in successorScore])
                return averageScore
            #if iterCount == numAgents, is pacman
            else: #is pacman max
                result = -1e10
                for a in s.getLegalActions(iterCount % numAgents):
                    # state with iteration count
                    new_gameState = s.generateSuccessor(iterCount % numAgents, a)
                    result = max(result, _expectMinimax(new_gameState, iterCount + 1))
                    if iterCount == 0:
                        ActionScore.append(result)
                return result

        result = _expectMinimax(gameState, 0)
        return gameState.getLegalActions(0)[ActionScore.index(max(ActionScore))]

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    #hunting ghosts when eating the wrath.
    def _ghostHunting(gameState):
      score = 0
      #find ghost
      for ghost in gameState.getGhostStates():
        disGhost = manhattanDistance(gameState.getPacmanPosition(), ghost.getPosition())
        #if pacman is fury time
        if ghost.scaredTimer > 0:
          score += pow(max(8 - disGhost, 0), 2)
        else:
          score -= pow(max(7 - disGhost, 0), 2)
      return score

    #search for the nearest food
    def _foodGobbling(gameState):
      disFood = []
      #create list food distance
      for food in gameState.getFood().asList():
        disFood.append(1.0/manhattanDistance(gameState.getPacmanPosition(), food))
      #find min distance food because disFood is list of fractions
      if len(disFood)>0:
        return max(disFood)
      else:
        return 0

    #Find the nearest fury ball
    def _pelletNabbing(gameState):
      score = []
      #create list score
      for Cap in gameState.getCapsules():
        score.append(50.0/manhattanDistance(gameState.getPacmanPosition(), Cap))
    #find max score
      if len(score) > 0:
        return max(score)
      else:
        return 0
    score = currentGameState.getScore()
    return score + _ghostHunting(currentGameState) \
                  + _foodGobbling(currentGameState) \
                    + _pelletNabbing(currentGameState)

# Abbreviation
better = betterEvaluationFunction
