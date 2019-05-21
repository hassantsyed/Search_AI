# README / Report

## Setup:
* Python 3.6
* Ubuntu 18
* i7 CPU
* 16 gb RAM

##### Packages:
Installation Required:
* unidecode

Used but already in Python distribution:
* argparse
* ast
* heapq
* abc (abstract base class)
* math
* itertools

## How to run:
##### without heuristic:

python puzzlesolver.py <config_file> <search_algo>

##### with heuristic:

python puzzlesolver.py <config_file> <search_algo> [-f heuristic_function]

search algo options:
* bfs
* dfs
* unicost
* greedy
* astar

heuristic functions:
(description of each function is in puzzle's heuristic section)
* Path Planning:
  * euclid
* Water Jug:
  * dist
* Tile Puzzle:
  * manhattan
  * misplaced

For more information on how to run:

python puzzlesolver.py -h

## Path Puzzle:
##### Actions:
The only action possible is to visit the neighboring cities.

PLEASE NOTE: The expansion order follows the order of the roads in the config.

##### Heuristic Function:
euclid
* This will calculate the Euclidean distance between the current node city and the goal node city (discussed in class)

##### Transcript:
path_transcript
 * contains transcript of unicost, greedy (euclid), astar (euclid) searches ran on test_cities.config

##### Discussion Points:

1. What do you think is the best search strategy, and why? You should take all four factors into considerations (completeness, optimality, time complexity, space complexity).

I think astar with the euclid heuristic is the best search strategy because it returned a correct path with the minimum space and time costs. Greedy with the euclid heuristic returned a path with a much higher cost than the one returned by unicost and astar. Since greedy resulted in a sub optimal solution, I do not think it can be the best.

| test_cities.config |  Space (frontier + explored)  | Time |
|:------------------:|:-----------------------------:|:----:|
|       unicost      |              296              | 1074 |
|   greedy & euclid  |               25              |  28  |
|   astar & euclid   |              249              |  879 |

As the table shows, astar with the euclid heuristic needed to do less exploring and took up less memory than unicost. Therefore, I think astar with the euclid heuristic is the best for this puzzle to find the optimal path. 

However, if we devalue being optimal, greedy could be a good algorithm to use, as the amount of space and the time is took was significantly less than the other algorithms since it only cares about being as close to the goal as possible.

## Water Jug Puzzle:
##### Actions:
There are three possible types of actions at any state:
1. Empty a jug 
  * ex. (1,0) -> (0, 0)
2. Fill a jug
  * ex. (0,0) -> (4, 0) (if (4,5) is the specified jug capacity)
3. Pour from one jug to another
  * ex. (3,4) -> (2,5) (if (4,5) is the specified jug capacity)


PLEASE NOTE: this is the order the actions are expanded in.

If two jugs are specified there is a maximum of 6 possible actions.

##### Heuristic Function:
dist
* This will calculate the distance of the current state to the goal state.
  * ex. cur: (2,3), goal: (0,5): abs(2-0) + abs(3-5) = 4

```
totalDist = 0
for i in range(len(goal)):
	totalDist += int(math.fabs(goal[i] - cur[i]))
return totalDist
```
This represents the absolute distance from the current state to the goal state. In theory, the smaller this value is the better state we are in because we are closer to the goal state.

Note: This heuristic function is not admissible, as it is not always optimistic.

ex. capacities: (2,5), goal: (0,5), current: (2,3)
In this case the heuristic would say 4, since the distance between our current state and the goal state is 4. In reality, we would only need one move, pouring jug one into jug two. This would result in (0, 5), our goal state.

##### Transcript:
jug_transcript
 * contains transcript of bfs, dfs, greedy (dist) searches ran on test_jugs.config

##### Discussion Points:

1. What do you think is the best search strategy, and why? You should take all four factors into considerations (completeness, optimality, time complexity, space complexity).

I do not think dfs is a good strategy for this puzzle. In this puzzle it is easy to get into loops where we go back to a jug state that we have already been in. We also rely on luck in expanding the correct branch to arrive at the optimal solution. In this case, we did not arrive at an optimal solution, rather we arrived at a sub optimal solution. The space is better, since we don't keep an explored list. I think iterative deepening would be a good option here.

That leaves us with bfs and greedy with the dist heuristic. I think we have to eliminate greedy here since it is neither complete nor optimal, meaning it has the same issue of potentially arriving at a sub optimal solution to the problem or never finding a solution. However, with a sufficiently good heuristic we could minimize this issue.

I think bfs is the best strategy of the ones we ran for this puzzle. While its space and time is not the best, we are guranteed of it finding the optimal solution if it exists. This is why I lean to iterative deepening, we can reduce our memory complexity with this algorithm as well as being optimal.

| test_jugs.config |  Space (frontier + explored)  | Time |
|:----------------:|:-----------------------------:|:----:|
|        bfs       |               19              |  91  |
|        dfs       |               5               |  61  |
|   greedy & dist  |               16              |  43  |


2. For the water jugs problem, is your heuristic admissible and consistent? Explain.

My heuristic is not admissible, but it is consistent. Since my heuristic is the sum of the distance of the current state to the goal state, we can get a higher heuristic value than the amount of steps to the solution since a single step can take us several 'pints' to the goal. 
* ex. capacities: (2,5), goal: (0,5), current: (2,3)

In this case the heuristic would say 4, since the distance between our current state and the goal state is 4. In reality, we would only need one move, pouring jug one into jug two. This would result in (0, 5), our goal state.
However, this heuristic is consistent. Since this is the absolute distance from our goal, each step we take will bring us that amount closer or away from the goal each time.
* ex. capacities: (5,5), goal: (0,5), current: (2,3). Heuristic((2,3)) = 4

If our next step were to pour out jug one resulting in (0,3) our heuristic would be 2. We have lost the water in jug one as desired and only need to gain 2 in jug two. 

If instead, our next step were to fill up jug one resulting in (5,3) our heuristic would be 7. We have gained 3 in jug one. So the distance for jug one is 5 and we remain deficient in jug two by 2 so our total distance is 7. Our heuristic's change is directly dependent on the resulting volumes of water from our next step.

However, it is not a good measure of how far we are from our goal state.

## Tile Puzzle:
##### Actions:
There are four possible configurations that can be generated:
1. Move the blank tile up
2. Move the blank tile down
3. Move the blank tile right
4. Move the blank tile left
  * All of these are dependent on the move being valid (not going out of bounds)


PLEASE NOTE: this is the order the actions are expanded in.

##### Heuristic Function:
manhattan
* This will calculate the distance of each tile to its goal state in the amount of moves up or down and left or right (discussed in class)

misplaced
* This will count the amount of tiles that are not in their goal state (discussed in class)


##### Transcript:
tile_transcript
 * contains transcript of bfs, astar (misplaced), astar (manhattan) on test_tiles.config & astar (manhattan) on tiles.config
astar (misplaced) on tiles.config was not able to finish in the alloted 30 minutes.


bfs on tiles.config was not able to finish in the alloted 30 minutes. However, I did run it overnight and I did get a solution path after over 8 hours of running. 

Note: The first two lines after every run of the program is the starting configuration and the goal configuration. I forgot to comment it out when I took the transcript.

##### Discussion Points:

1. What do you think is the best search strategy, and why? You should take all four factors into considerations (completeness, optimality, time complexity, space complexity).

For the tiles puzzle, I think astar with the manhattan distance heuristic is the best search strategy. Perhaps, the most important reason for this is the fact that it is the only optimal & complete search which worked on both the test_tiles.config & tiles.config. A solution is better than no solution. 

(Note. astar with misplace & bfs are both technically optimal & complete but they failed to finish in the alloted time.)

| test_tiles.config |  Space (frontier + explored)  |  Time |
|:-----------------:|:-----------------------------:|:-----:|
|         bfs       |             56870             | 37274 |
| astar & manhattan |               30              |   43  |
| astar & misplaced |              102              |  150  |

In terms of time and space, astar with the manhattan heuristic proved to be the best. It was took less than 1/3 the time of astar with the misplaced heuristic and was much faster than bfs. This is because the manhattan heuristic is much better than the misplaced heuristic. The manhattan heuristic gives an approximation of the amount of moves to get every tile back into place, while the misplaced heuristic only counts misplaced tiles. The misplaced heuristic could have two puzzles where one is much harder than the other but the amount of misplaced tiles are equal. It is much better than bfs because bfs explores everything, level by level until it finds a solution. This is why bfs takes so long and uses so much space. Both astars are relatively efficient in space since they explore so many fewer nodes compared to bfs, but the manhattan heuristic helps again here as it requires less of the graph to be explored.


## Additional Discussion Points:

* Did all the outcomes make sense (e.g., do the time/space comlexities of different search strategies match your expectation based on our class discussions? What about optimality and completeness?)

All of the outcomes do make sense. DFS uses less memory but doesn't always result in the optimal path as expected. BFS & unicost will use lots of memory but will result in optimal paths. They are identical if no weights. Greedy doesn't always result in the optimal path but astar will.

I was orginally confused when bfs & astar with the misplaced heuristic did not return solutions in a reasonable amount of time when ran on tiles.config, but I realised that they were expanding tons of nodes. Eventually I would expect them to come to a solution, but they would take a long time as the search space is 8!.

Both the attributed I associated with the searches and the expected complexities seemed to align with what we discussed in class.


* You may also include additional discussions on any observations that you find surprising and/or interesting. / Was there anything that surprised you? if so, elaborate.

I found it interesting that astar and unicost do not necessarily result in the shortest path if there are multiple paths with the minimum weight.

I also think I have a better understanding of how important the heuristic is to astar. I didn't expect the misplaced heuristic to result in so much worse performance than the manhatten heuristic.


## Bugs:
Astar & Unicost sometimes return different paths, but they are both the minimum weight. It does not prioritize smaller length path if equal weight.

## Discussed With:
Alessio Mazzone: String/tuple/state representation

## Additional References:
1. https://docs.python.org/3/library/abc.html
  * abstract base class documentation
2. https://docs.python.org/3.7/library/heapq.html
  * heapq documentation

