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

def depthFirstSearch(problem):
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
    "*** YOUR CODE HERE ***"
    from util import Stack
    stack = Stack()
    visited = []
    actions = []
    cost = 0

    begin_state = problem.getStartState()
    stack.push((begin_state, actions, cost))

    while not stack.isEmpty():
        cur_state, cur_action, cur_cost = stack.pop()

        # Check if it get to the goal state
        if problem.isGoalState(cur_state):
            return cur_action
            break

        # Check if the node is visited (Find all the adjacents)
        # If not, add it to the stack
        if cur_state not in visited:
            visited.append(cur_state)
            successors = problem.getSuccessors(cur_state)
            for successor in successors:
                if successor[0] not in visited:
                    adjacent, action, _cost = successor
                    path = cur_action + [action]
                    new_cost = cur_cost + _cost
                    stack.push((adjacent, path, new_cost))

    util.raiseNotDefined()


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from util import Queue
    queue = Queue()
    visited = []
    actions = []
    cost = 0

    begin_state = problem.getStartState()
    queue.push((begin_state, actions, cost))

    while not queue.isEmpty():
        cur_state, cur_action, cur_cost = queue.pop()

        # Check if it get to the goal state
        if problem.isGoalState(cur_state):
            return cur_action
            break

        # Check if the node is visited (Find all the adjacents)
        # If not, add it to the queue
        if cur_state not in visited:
            visited.append(cur_state)
            successors = problem.getSuccessors(cur_state)
            for successor in successors:
                if successor[0] not in visited:
                    adjacent, action, _cost = successor
                    path = cur_action + [action]
                    new_cost = cur_cost + _cost
                    queue.push((adjacent, path, new_cost))

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    pri_queue = PriorityQueue()
    visited = []
    actions = []
    cost = 0

    begin_state = problem.getStartState()
    pri_queue.update((begin_state, actions, cost), 0) # Priority queue requires a priority number come up with every node in the graph

    while not pri_queue.isEmpty():
        cur_state, cur_action, cur_cost = pri_queue.pop()

        if problem.isGoalState(cur_state):
            return cur_action
            break

        if cur_state not in visited:
            visited.append(cur_state)
            successors = problem.getSuccessors(cur_state)
            for successor in successors:
                if successor[0] not in visited:
                    adjacent, action, _cost = successor
                    path = cur_action + [action]
                    new_cost = cur_cost + _cost
                    pri_queue.update((adjacent, path, new_cost), new_cost)

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    res = []
    visited = []
    priority_queue = util.PriorityQueue()
    start = (problem.getStartState(), [], 0)
    priority_queue.update(start, 0)

    while not priority_queue.isEmpty():
        state, path, cost = priority_queue.pop()

        if problem.isGoalState(state):
            res = path
            break

        if state not in visited:
            visited.append(state)
            successors = problem.getSuccessors(state)
            for successor in successors:
                adjacent, action, weight = successor
                new_path = path + [action]
                new_cost = cost + weight
                new_node = (adjacent, new_path, new_cost)
                priority_queue.update(new_node, new_cost + heuristic(adjacent, problem))

    return res
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
