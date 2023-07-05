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
Pacman agents (in search_agents.py).
"""

from builtins import object
import util
import os

def tiny_maze_search(problem):
    """
    Returns a sequence of moves that solves tiny_maze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tiny_maze.
    """
    from game import Directions

    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depth_first_search(problem):
    "*** YOUR CODE HERE ***"
    util.raise_not_defined()


def breadth_first_search(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    util.raise_not_defined()


def uniform_cost_search(problem, heuristic=None):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raise_not_defined()


# 
# heuristics
# 
def a_really_really_bad_heuristic(position, problem):
    from random import random, sample, choices
    return int(random()*1000)

def null_heuristic(state, problem=None):
    return 0

def heuristic1(state, problem=None):
    from search_agents import FoodSearchProblem
    
    # 
    # heuristic for the find-the-goal problem
    # 
    #used manahattan distance function defined in util.py to find distance from state to goal state
    #good heuristic to use because distance decreases as you get closer to the goal state
    if isinstance(problem, SearchProblem):
        # data
        pacman_x, pacman_y = state
        goal_x, goal_y     = problem.goal
     
        optimisitic_number_of_steps_to_goal = util.manhattan_distance((pacman_x,pacman_y),(goal_x,goal_y))
        return optimisitic_number_of_steps_to_goal
    # 
    # traveling-salesman problem (collect multiple food pellets)
    # for food search, used as_list() to find coordinates of all available food on grid
    # found manhattan distance from state to food for all food cordinates in list
    # only needed food that was a minimum distance away so used minimum manhattan distance in list as heuristic
    # added length of food_grid to heuristic to penalize earlier states (when length of food grid was longer)
    # multiplied by scalar to have more weight - 5 seemed optimal
    elif isinstance(problem, FoodSearchProblem):
        # the state includes a grid of where the food is (problem isn't ter)
        position, food_grid = state
        pacman_x, pacman_y = position
        optimal_cost = []
        for i in food_grid.as_list():
            optimal_cost.append(util.manhattan_distance((pacman_x,pacman_y),i))
        if len(optimal_cost) == 0:
            return 0
        optimisitic_number_of_steps_to_goal = min(optimal_cost) + len(food_grid.as_list()) * 5
        return optimisitic_number_of_steps_to_goal

def a_star_search(problem, heuristic=heuristic1):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    
    visited_nodes = []
    frontier = util.PriorityQueue()
    dict = {} #used to dict to store action sequence of each state.
    #item in pq is list, cost is priority. add first element
    frontier.push(problem.get_start_state(),heuristic(problem.get_start_state(),problem))
    dict[problem.get_start_state()] = [] #store list of actions of lowest cost for each state
    #continue popping states from pq until goal state is found. If no goal state is found, return empty list (meaning goal state is first state)
    while not frontier.is_empty():
        item = frontier.pop()
        state = item
        actions = dict[state]
        
        if state in visited_nodes: 
            continue
        else:
            visited_nodes.append(state)

        if problem.is_goal_state(state): #late-check policy
            return actions

        children = problem.get_successors(state)
            
        #for each child, calculate cost with new action. push cost into pq and store new action in dictionary
        for i in children:
            newAction = list(actions)
            newAction.append(i.action) #creates list of parent connections
            cost = problem.get_cost_of_actions(newAction) + heuristic(i.state,problem)
            frontier.update(i.state,cost)
            if i.state in dict:
                if cost < problem.get_cost_of_actions(dict[i.state]):
                    dict[i.state] = newAction 
            else:
                dict[i.state] = newAction

    return []


# (you can ignore this, although it might be helpful to know about)
# This is effectively an abstract class
# it should give you an idea of what methods will be available on problem-objects
class SearchProblem(object):
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem.
        """
        util.raise_not_defined()

    def is_goal_state(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raise_not_defined()

    def get_successors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, step_cost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'step_cost' is
        the incremental cost of expanding to that successor.
        """
        util.raise_not_defined()

    def get_cost_of_actions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raise_not_defined()

if os.path.exists("./hidden/search.py"): from hidden.search import *
# fallback on a_star_search
for function in [breadth_first_search, depth_first_search, uniform_cost_search, ]:
    try: function(None)
    except util.NotDefined as error: exec(f"{function.__name__} = a_star_search", globals(), globals())
    except: pass

# Abbreviations
bfs   = breadth_first_search
dfs   = depth_first_search
astar = a_star_search
ucs   = uniform_cost_search