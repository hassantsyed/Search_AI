import argparse
import ast
from unidecode import unidecode
from PathPlanning import PathPlan, CityNode
from WaterJug import WaterJug, JugNode
from TilePuzzle import TilePuzzle, TileNode

def parsePuzzle(config):
	with open(config) as file:
		lines = file.read().splitlines()
	if lines[0] == "cities":
		return cityParseTwo(lines[1], lines[2], lines[3], lines[4:])
	elif lines[0] == "jugs":
		return jugParse(lines[1], lines[2], lines[3])
	elif lines[0] == "tiles":
		return tileParse(unidecode(lines[1]), unidecode(lines[2]), unidecode(lines[3]))

def tileParse(N, start, end):
	N = ast.literal_eval(N)
	start = ast.literal_eval(start)
	end = ast.literal_eval(end)
	starting = nestedTiles(start, N)
	goal = nestedTiles(end, N)
	t = TilePuzzle(goal)
	initial = TileNode(starting)
	#print(starting)
	#print(goal)
	return t, initial

def nestedTiles(board, N):
	i = 0
	newBoard = []
	while i < len(board):
		newBoard.append(board[i:i+N])
		i+=N
	return newBoard


def jugParse(sizes, start, end):
	capacities = ast.literal_eval(sizes)
	start = ast.literal_eval(start)
	end = ast.literal_eval(end)
	start = list(start)
	end = list(end)

	w = WaterJug(end)
	j = JugNode(start, capacities)
	return w, j

def cityParseTwo(cities, start, dest, roads):
	cities = ast.literal_eval(cities)
	start = start.replace('"', '')
	dest = dest.replace('"', '')
	roads = [ast.literal_eval(r) for r in roads]

	neighbs = {}
	for city in cities:
		neighbs[city[0]] = [(city[1], city[2])]
		if city[0] == start:
			sNode = CityNode(start, city[1], city[2])
		if city[0] == dest:
			x = city[1]
			y = city[2]
	p = PathPlan(dest, x, y)
	
	for r in roads:
		neighbs[r[0]].append((r[1],r[2]))
		neighbs[r[1]].append((r[0],r[2]))
	sNode.neighbs = neighbs
	return p, sNode

def cityParse(cities, start, dest, roads):
	cities = ast.literal_eval(cities)
	start = start.replace('"', '')
	dest = dest.replace('"', '')
	roads = [ast.literal_eval(r) for r in roads]

	nodes = []
	for city in cities:
		if city[0] == dest:
			x = city[1]
			y = city[2]
	p = PathPlan(dest, x, y)

	for city in cities:
		nodes.append(CityNode(*city))
	for road in roads:
		for n in nodes:
			if n.name == road[0]:
				orig = n
			if n.name == road[1]:
				goal = n
		orig.addUndirectedNeighbor(goal, road[2])

	for n in nodes:
		if n.name == start:
			startNode = n
	return p, startNode

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("config", help = "puzzle config file")
	parser.add_argument("algo", help = "desired search algorithm")
	parser.add_argument("-f", "--function", help="desired heuristic function")
	args = parser.parse_args()
	
	config = args.config
	searchAlgo = args.algo
	if args.function:
		function = args.function
	else:
		function = None
	
	#config = "test_cities.config"
	#searchAlgo = "astar"
	#function = "euclid"
	puzzle, start = parsePuzzle(config)
	puzzle.setH(function)
	puzzle.run(start, searchAlgo)
	