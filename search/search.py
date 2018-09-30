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
import time

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

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """

    # use stack as structure and initialize
    stack = util.Stack()
    stack.push((problem.getStartState(), []))  # insert state and action as a tuple
    visited_list = []

    while not stack.isEmpty():
        current_state, path = stack.pop()
        if problem.isGoalState(current_state):
            return path
        elif current_state not in visited_list:
            visited_list.append(current_state)
            for successor in problem.getSuccessors(current_state):  # get the leaf node
                next_state, next_action, step_cost = successor
                if next_state not in visited_list:  # if the leaf node unexpanded, add to stack
                    stack.push((next_state, path + [next_action]))
    return []


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    # use queue as structure and initialize
    queue = util.Queue()
    queue.push((problem.getStartState(), []))  # insert state and action as a tuple
    visited_list = []

    while not queue.isEmpty():
        current_state, path = queue.pop()
        # print "current_state", current_state

        if problem.isGoalState(current_state):
            return path
        elif current_state not in visited_list:  # check if expanded
            visited_list.append(current_state)
            for successor in problem.getSuccessors(current_state):
                next_state, next_action, step_cost = successor
                if next_state not in visited_list:  # if the leaf node unexpanded, add to queue
                    queue.push((next_state, path + [next_action]))
    return []


def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    # this algorithms use priority queue as data structure
    priority_queue = util.PriorityQueue()
    priority_queue.push((problem.getStartState(), []), 0)
    # add a cost as the priority of the nodes
    visited_list = []

    while not priority_queue.isEmpty():
        current_state, path = priority_queue.pop()
        if problem.isGoalState(current_state):  # if is goal, return current path right away
            return path
        elif current_state not in visited_list:
            visited_list.append(current_state)
            for successor in problem.getSuccessors(current_state):
                next_state, next_action, step_cost = successor
                if next_state not in visited_list:  # check leaf node if already visited
                    new_path = path + [next_action]
                    new_cost = problem.getCostOfActions(new_path)  # calculate total cost of the path from begin point.
                    priority_queue.push((next_state, new_path), new_cost)
    return []


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    # similar to Dijikstra above, except calculation of cost.
    priority_queue = util.PriorityQueue()
    priority_queue.push((problem.getStartState(), []), 0)
    visited_list = []

    while not priority_queue.isEmpty():
        current_state, path = priority_queue.pop()

        if problem.isGoalState(current_state):  # first check if is goal
            return path
        elif current_state not in visited_list:  # then check if is already visited
            visited_list.append(current_state)
            for successor in problem.getSuccessors(current_state):  # expand all leafnodes
                next_state, next_action, step_cost = successor
                if next_state not in visited_list:
                    new_path = path + [next_action]
                    new_cost = problem.getCostOfActions(new_path) + heuristic(next_state, problem)
                    # add a heuristic to the cost calculation
                    priority_queue.push((next_state, new_path), new_cost)
    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
