#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the Snowman Puzzle domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

# import os for time functions
import os
from search import * #for search engines
from snowman import SnowmanState, Direction, snowman_goal_state #for snowball specific classes and problems
from test_problems import PROBLEMS #20 test problems

#snowball HEURISTICS
def heur_simple(state):
  '''trivial admissible snowball heuristic'''
  '''INPUT: a snowball state'''
  '''OUTPUT: a numeric value that serves as an estimate of the distance of the state (# of moves required to get) to the goal.'''
  return len(state.snowballs)

def heur_zero(state):
  return 0

def heur_manhattan_distance(state):
    #IMPLEMENT
    '''admissible snowball puzzle heuristic: manhattan distance'''
    '''INPUT: a snowball state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #We want an admissible heuristic, which is an optimistic heuristic.
    #It must always underestimate the cost to get from the current state to the goal.`
    #The sum of the Manhattan distances between the snowballs and the destination for the Snowman is such a heuristic.
    #When calculating distances, assume there are no obstacles on the grid.
    #You should implement this heuristic function exactly, even if it is tempting to improve it.
    #Your function should return a numeric value; this is the estimate of the distance to the goal.

    total_count = 0

    for snow_balls in state.snowballs:
        temp = float("inf")
        if man_distance(snow_balls, state.destination) < temp:
            total_count += man_distance(snow_balls, state.destination)
    return total_count

def man_distance(snow_balls,destination):
    return abs(snow_balls[0] - destination[0]) + abs(snow_balls[1] - destination[1])


def heur_alternate(state):
    #IMPLEMENT
    '''a better heuristic'''
    '''INPUT: a snowball state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #heur_manhattan_distance has flaws.
    #Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    #Your function should return a numeric value for the estimate of the distance to the goal.

    total_count = 0
    for snowball in state.snowballs:
        total_count += count(snowball, state.destination)
    total_count = total_count + robot_count(state.robot, state.destination)
    return total_count


def count(snowball, destination):
    value_1 = abs(snowball[0] - destination[0])
    value_2 = abs(snowball[1] - destination[1])
    return value_1 + value_2

def robot_count(robot, destination):
    value_1 = abs(robot[0] - destination[0])
    value_2 = abs(robot[1] - destination[1])

    return value_1 + value_2

def fval_function(sN, weight):
#IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a SnowballState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """

    #Many searches will explore nodes (or states) that are ordered by their f-value.
    #For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    #You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    #The function must return a numeric f-value.
    #The value will determine your state's position on the Frontier list during a 'custom' search.
    #You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.
    return sN.gval + weight*sN.hval

def anytime_gbfs(initial_state, heur_fn, timebound = 10):
    #IMPLEMENT
    '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
    '''INPUT: a snowball state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    start = os.times()[0]
    eng = SearchEngine(strategy='best_first', cc_level='default')
    eng.init_search(initial_state, heur_fn = heur_manhattan_distance, goal_fn=snowman_goal_state)

    solution = eng.search(timebound)
    holder = True
    while holder:
        time_leftover = timebound - (os.times()[0] - start)
        if time_leftover > 0:
            temp = eng.search(time_leftover, [solution.gval, float("inf"), float("inf")])
            if not temp:
                return solution
            else:
                solution = temp
        else:
            holder = False

    return solution

def anytime_weighted_astar(initial_state, heur_fn, weight=1., timebound = 10):
    #IMPLEMENT
    '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
    '''INPUT: a snowball state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''

    start = os.times()[0]
    time_holder = timebound

    # Search engine & costbound
    wrapped_fval_function = (lambda sN: fval_function(sN, weight))
    eng = SearchEngine(strategy='custom', cc_level='default')
    eng.init_search(initial_state, snowman_goal_state, heur_fn, wrapped_fval_function)
    cost_bound = (float("inf"), float("inf"), float("inf"))
    solution = False
    temp = eng.search(timebound)

    while (os.times()[0] - start) < timebound:

        if temp == False:  # If no result found
            return solution

        start = os.times()[0]
        time_holder = n_timebound(os.times()[0], start, time_holder)

        if (temp.gval <= cost_bound[0]):
            cost_bound = (temp.gval, temp.gval, temp.gval)
            solution = temp
        temp = eng.search(time_holder, cost_bound)

    return solution


def n_timebound(ostime, start, time_holder):

    timedifference = ostime - start
    return time_holder - timedifference


if __name__ == "__main__":
  #TEST CODE
  solved = 0; unsolved = []; counter = 0; percent = 0; timebound = 2; #2 second time limit for each problem
  print("*************************************")
  print("Running A-star")

  for i in range(0, 10): #note that there are 20 problems in the set that has been provided.  We just run through 10 here for illustration.

    print("*************************************")
    print("PROBLEM {}".format(i))

    s0 = PROBLEMS[i] #Problems will get harder as i gets bigger

    se = SearchEngine('astar', 'full')
    se.init_search(s0, goal_fn=snowman_goal_state, heur_fn=heur_simple)
    final = se.search(timebound)

    if final:
      final.print_path()
      solved += 1
    else:
      unsolved.append(i)
    counter += 1

  if counter > 0:
    percent = (solved/counter)*100

  print("*************************************")
  print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))
  print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
  print("*************************************")

  solved = 0; unsolved = []; counter = 0; percent = 0; timebound = 8; #8 second time limit
  print("Running Anytime Weighted A-star")

  for i in range(0, 10):
    print("*************************************")
    print("PROBLEM {}".format(i))

    s0 = PROBLEMS[i] #Problems get harder as i gets bigger
    weight = 10
    final = anytime_weighted_astar(s0, heur_fn=heur_simple, weight=weight, timebound=timebound)

    if final:
      final.print_path()
      solved += 1
    else:
      unsolved.append(i)
    counter += 1

  if counter > 0:
    percent = (solved/counter)*100

  print("*************************************")
  print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))
  print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
  print("*************************************")


