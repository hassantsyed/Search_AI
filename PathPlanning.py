from search import Search
from graph import Node, Edge
import math

class PathPlan(Search):
	def __init__(self, goal, x, y):
		self.goal = goal
		self.x = x
		self.y = y

	def setH(self, hAlgo):
		self.hAlgo = hAlgo

	def goalTest(self, node):
		return node.name == self.goal

	def euclid(self, node):
		curPos = (node.x, node.y)
		goalPos = (self.x, self.y)
		estimatedW = math.sqrt((goalPos[0] - curPos[0])**2 + (goalPos[1] - curPos[1])**2)
		return estimatedW

	def heuristic(self, node):
		weights = {"euclid": self.euclid}
		return weights[self.hAlgo](node)

class CityNode(Node):
	def __init__(self, name, x, y):
		Node.__init__(self)
		self.name = name
		self.x = x
		self.y = y

	def getState(self):
		return self.name

	def getChildren(self):
		neighbs = self.neighbs[self.name][1:]
		children = [CityNode(n[0], self.neighbs[n[0]][0][0], self.neighbs[n[0]][0][1]) for n in neighbs]
		for i in range(len(neighbs)):
			self.addUndirectedNeighbor(children[i], neighbs[i][1])
			children[i].neighbs = self.neighbs
		return children
		#return [e.dest for e in self.edges]

	def __lt__(self, other):
		return self.name < other.name

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		return self.name
