from search import Search
from graph import Node, Edge
import itertools
import math

class WaterJug(Search):
	def __init__(self, goal):
		self.goal = goal

	def goalTest(self, node):
		return node.getState() == self.goal

	def dist(self, node):
		goal = self.goal
		cur = node.getState()
		totalDist = 0
		for i in range(len(goal)):
			totalDist += int(math.fabs(goal[i] - cur[i]))
		return totalDist

	def heuristic(self, node):
		weigths = {"dist" : self.dist}
		return weigths[self.hAlgo](node)

	def setH(self, hAlgo):
		self.hAlgo = hAlgo

class JugNode(Node):
	def __init__(self, jugs, capacities):
		Node.__init__(self)
		self.jugs = jugs
		self.capacities = capacities

	def getState(self):
		return self.jugs

	def getChildren(self):
		children = []
		#empties
		for i in range(len(self.jugs)):
			jEmpty= list(self.jugs)
			jEmpty[i] = 0
			children.append(jEmpty)
		#fills
		for i in range(len(self.jugs)):
			jFill = list(self.jugs)
			jFill[i] = self.capacities[i]
			children.append(jFill)
		#from one to another
		pours = list(itertools.permutations([i for i in range(len(self.jugs))], 2))
		for pour in pours:
			jPour = list(self.jugs)
			source = pour[0]
			dest = pour[1]
			while jPour[source] > 0 and not jPour[dest] == self.capacities[dest]:
				jPour[source] -= 1
				jPour[dest] += 1
			children.append(jPour)
		childNodes = [JugNode(child, self.capacities) for child in children]
		for c in childNodes:
			self.addUndirectedNeighbor(c, 1)
		return childNodes

	def __lt__(self, other):
		return self.jugs < other.jugs

	def __repr__(self):
		return str(self.getState())