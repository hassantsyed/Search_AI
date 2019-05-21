from search	import Search
from graph import Node, Edge
import math

class TilePuzzle(Search):
	def __init__(self, goal):
		self.goal = goal

	def goalTest(self, node):
		return node.getState() == self.goal

	def manhattan(self, node):
		goal = self.goal
		cur = node.getState()
		nums = {}
		for r in range(len(goal)):
			for c in range(len(goal[0])):
				if goal[r][c] == 'b':
					continue
				nums[goal[r][c]] = [(r,c)]
		for r in range(len(cur)):
			for c in range(len(cur[0])):
				if cur[r][c] == 'b':
					continue
				nums[cur[r][c]].append((r,c))
		totalDist = 0
		for _, cors in nums.items():
			dist = math.fabs(cors[0][0] - cors[1][0]) + math.fabs(cors[0][1] - cors[1][1])
			totalDist += dist
		totalDist = int(totalDist)
		return totalDist

	def misplaced(self, node):
		goal = self.goal
		cur = node.getState()
		misplacedCount = 0
		for r in range(len(goal)):
			for c in range(len(goal[0])):
				if goal[r][c] == 'b':
					continue
				if not goal[r][c] == cur[r][c]:
					misplacedCount += 1
		return misplacedCount

	def heuristic(self, node):
		weights = {"manhattan" : self.manhattan, "misplaced" : self.misplaced}
		return weights[self.hAlgo](node)

	def setH(self, hAlgo):
		self.hAlgo = hAlgo

class TileNode(Node):
	def __init__(self, state):
		Node.__init__(self)
		self.state = state

	def getState(self):
		return self.state

	def getChildren(self):
		state = self.state
		blankPos = self.getBlankPos(state)
		moves = []
		#generating possible moves
		if not blankPos[0] == 0:
			up = [blankPos[0]-1, blankPos[1]]
			moves.append(up)
		if not blankPos[0] == len(state)-1:
			down = [blankPos[0]+1, blankPos[1]]
			moves.append(down)
		if not blankPos[1] == 0:
			left = [blankPos[0], blankPos[1] - 1]
			moves.append(left)
		if not blankPos[1] == len(state[0])-1:
			right = [blankPos[0], blankPos[1] + 1]
			moves.append(right)
		#swapping
		states = []
		for move in moves:
			swap = [s[:] for s in state]
			swap[blankPos[0]][blankPos[1]], swap[move[0]][move[1]] = swap[move[0]][move[1]], swap[blankPos[0]][blankPos[1]]
			states.append(swap)
		#returning children states
		childNodes = [TileNode(s) for s in states]
		for c in childNodes:
			self.addUndirectedNeighbor(c, 1)
		return childNodes

	def getBlankPos(self, state):
		for r, row in enumerate(state):
			for c, col in enumerate(row):
				if col == 'b':
					return [r,c]

	def __lt__(self, other):
		return self.state

	def __repr__(self):
		board = ""
		for row in self.state:
			board += str(row)
			board += "\n"
		return board
		#return str(self.getState())