from abc import ABC, abstractmethod

class Node(ABC):
	def __init__(self):
		self.edges = []
		self.parent = None

	@abstractmethod
	def getChildren(self):
		pass

	@abstractmethod
	def getState(self):
		pass

	def addDirectedNeighbor(self, node, weight):
		self.edges.append(Edge(self, node, weight))

	def addUndirectedNeighbor(self, node, weight):
		self.edges.append(Edge(self, node, weight))
		node.edges.append(Edge(node, self, weight))

	def getEdge(self, node):
		for edge in self.edges:
			if node == edge.dest:
				return edge

	@abstractmethod
	def __lt__(self, other):
		pass

class Edge(ABC):
	def __init__(self, origin, dest, weight):
		self.origin = origin
		self.dest = dest
		self.weight = weight