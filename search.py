from abc import ABC, abstractmethod
import heapq

class Search(ABC):
	def run(self, startNode, algo):
		algos = {"bfs" : self.bfs, "dfs" : self.dfs, "unicost" : self.unicost, "astar" : self.astar, "greedy" : self.greedy}
		algos[algo](startNode)

	def dfs(self, startNode):
		frontier = [startNode]
		curNode = None
		nodeCount = 1
		maxFrontierCount = len(frontier)
		while frontier:
			parent = curNode
			curNode = frontier.pop()
			curNode.parent = parent
			if self.goalTest(curNode):
				self.printPath(curNode, nodeCount, maxFrontierCount)
				return curNode
			children = curNode.getChildren()
			for child in children:
				nodeCount += 1
				if not child in frontier and not self.checkParents(curNode, child):
					frontier.append(child)
			maxFrontierCount = max([len(frontier), maxFrontierCount])
		self.printPath(curNode, nodeCount, maxFrontierCount)
		return None

	def checkParents(self, curNode, childNode):
		parents = [curNode.getState()]
		while curNode:
			if curNode.parent == None:
				break
			parents.append(curNode.parent.getState())
			curNode = curNode.parent
		if childNode.getState() in parents:
			return True
		else:
			return False

	#neither bfs nor dfs use weights
	def bfs(self, startNode):
		explored = []
		frontier = [startNode]
		maxFrontierCount = len(frontier)
		maxExploredCount = len(explored)
		nodeCount = 1
		while frontier:
			curNode = frontier.pop(0)
			explored.append(curNode.getState())
			if self.goalTest(curNode):
				self.printPath(curNode, nodeCount, maxFrontierCount, maxExploredCount)
				return curNode
			children = curNode.getChildren()
			for child in children:
				nodeCount += 1
				if not child.getState() in explored and not child in frontier:
					frontier.append(child)
					child.parent = curNode
			maxFrontierCount = max([len(frontier), maxFrontierCount])
			maxExploredCount = max([len(explored), maxExploredCount])
		self.printPath(None, nodeCount, maxFrontierCount, maxExploredCount)
		return None

	def unicost(self, startNode):
		explored = []
		frontier = [(0, startNode)]
		maxFrontierCount = len(frontier)
		maxExploredCount = len(explored)
		nodeCount = 1
		while frontier:
			nodeWeight = heapq.heappop(frontier)
			weight = nodeWeight[0]
			curNode = nodeWeight[-1]
			explored.append(curNode.getState())
			if self.goalTest(curNode):
				#print(weight)
				self.printPath(curNode, nodeCount, maxFrontierCount, maxExploredCount)
				return curNode
			children = curNode.getChildren()
			for child in children:
				nodeCount += 1
				if not child.getState() in explored:
					potential = (curNode.getEdge(child).weight + weight, child)
					child.parent = curNode
					heapq.heappush(frontier, potential)
			maxFrontierCount = max([len(frontier), maxFrontierCount])
			maxExploredCount = max([len(explored), maxExploredCount])
		self.printPath(None, nodeCount, maxFrontierCount, maxExploredCount)
		return None

	def greedy(self, startNode):
		frontier = [(self.heuristic(startNode), startNode)]
		explored = []
		maxFrontierCount = len(frontier)
		maxExploredCount = len(explored)
		nodeCount = 1
		while frontier:
			node_weight = heapq.heappop(frontier)
			weight = node_weight[0]
			curNode = node_weight[1]
			explored.append(curNode.getState())
			if self.goalTest(curNode):
				self.printPath(curNode, nodeCount, maxFrontierCount, maxExploredCount)
				return curNode
			children = curNode.getChildren()
			for child in children:
				nodeCount+=1
				if not child.getState() in explored:
					potential = (self.heuristic(child), child) #replace 0 with result from heuristic function
					child.parent = curNode
					heapq.heappush(frontier, potential)
			maxFrontierCount = max([len(frontier), maxFrontierCount])
			maxExploredCount = max([len(explored), maxExploredCount])
		self.printPath(None, nodeCount, maxFrontierCount, maxExploredCount)
		return None

	def astar(self, startNode):
		frontier = [(self.heuristic(startNode), startNode, 0)]
		explored = []
		maxFrontierCount = len(frontier)
		maxExploredCount = len(explored)
		nodeCount = 1
		while frontier:
			node_weight = heapq.heappop(frontier)
			hWeight = node_weight[0]
			curNode = node_weight[1]
			pWeight = node_weight[2]
			explored.append(curNode.getState())
			if self.goalTest(curNode):
				#print(pWeight)
				self.printPath(curNode, nodeCount, maxFrontierCount, maxExploredCount)
				return curNode
			children = curNode.getChildren()
			#print(curNode)
			for child in children:
				nodeCount+=1
				if not child.getState() in explored:
					#print(child)
					#print(f"heur {self.heuristic(child)}  cur: {pWeight} next: {curNode.getEdge(child).weight}")
					#same = False
					potential = (self.heuristic(child) + pWeight + curNode.getEdge(child).weight, child, pWeight + curNode.getEdge(child).weight)
					#for n in frontier:
					#	if n[0] == potential[0] and n[1].getState() == potential[1].getState():
					#		same = True
					#if same:
					#	continue
					child.parent = curNode
					heapq.heappush(frontier, potential)
			maxFrontierCount = max([len(frontier), maxFrontierCount])
			maxExploredCount = max([len(explored), maxExploredCount])
		self.printPath(None, nodeCount, maxFrontierCount, maxExploredCount)
		return None

	def betterNode(self, frontier, potential):
		for i in range(len(frontier)):
			node = frontier[i]
			if potential[1].getState() == node[1].getState() and potential[0] < node[0]:
				return i
		return None

	def printPath(self, node, nodeCount, frontierCount, exploredCount = None):
		path = []
		if node == None:
			print("No solution found.")
		else:
			while node:
				path.insert(0, node)
				#if node == start:
				#	break
				node = node.parent
			for p in path:
				print(p)
		print(f"Time: {nodeCount}")
		if exploredCount:
			print(f"Space: frontier: {frontierCount}, explored: {exploredCount}")
		else:
			print(f"Space: frontier: {frontierCount}")

	@abstractmethod
	def goalTest(self, node):
		pass

	@abstractmethod
	def heuristic(self, node):
		pass