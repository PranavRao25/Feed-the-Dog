import math
from typing import Dict, List
from app.Layout import *
from app.DataStructures import PriorityQueue

class Movement:
	def __init__(self, grid:Grid):
		self.grid = grid

	def shortest_path(self, src: tuple, dest: tuple, mode:int=3):
		src_cell, dest_cell = self.grid.get(src), self.grid.get(dest)
		print(src_cell, dest_cell)
		path = []
		pred = dict()
		pred[src_cell] = None

		if mode == 0:
			print("Implementing BFS")
			path = self.__bfs(src_cell, dest_cell, pred)
		elif mode == 1:
			print("Implementing DFS")
			path = self.__dfs(src_cell, dest_cell, pred)
		elif mode == 2:
			print("Implementing Djikstra")
			path = self.__djikstra(src_cell, dest_cell, pred)
		elif mode == 3:
			print("Implementing A star")
			path = self.__a_star(src_cell, dest_cell, pred)

		for cell in path[::-1]:
			yield cell

	def __bfs(self, src_cell: Cell, dest_cell: Cell, pred: Dict[Cell, Cell]):
		visited = dict()
		for k in self.grid.items():
			visited[k] = False
		cell = None
		frontier = [src_cell]
		flag = False

		while frontier:
			cell = frontier.pop(-1)
			visited[cell] = True
			if cell == dest_cell:
				flag = True
				break

			for i in self.grid.grid[cell]:
				if not visited[i]:
					pred[i] = cell
					frontier.insert(0, i)  # __bfs if mode = 0 else __dfs

		path = []
		if flag:
			while cell:
				path.append(cell)
				cell = pred[cell]
		else:
			print("Not Found")
		return path

	def __dfs(self, src_cell: Cell, dest_cell: Cell, pred: Dict[Cell, Cell]):
		visited = dict()
		for k in self.grid.items():
			visited[k] = False
		cell = None
		frontier = [src_cell]
		flag = False

		while frontier:
			cell = frontier.pop(-1)
			visited[cell] = True
			if cell == dest_cell:
				flag = True
				break

			for i in self.grid.grid[cell]:
				if not visited[i]:
					pred[i] = cell
					frontier.insert(-1, i)  # __bfs if mode = 0 else __dfs

		path = []
		if flag:
			while cell:
				path.append(cell)
				cell = pred[cell]
		else:
			print("Not Found")
		return path

	def __djikstra(self, src_cell: Cell, dest_cell: Cell, pred: Dict[Cell, Cell]):
		visited, dist = dict(), dict()
		for k in self.grid.items():
			visited[k] = False
			dist[k] = 1e7
		dist[src_cell] = 0
		cell = None
		flag = False

		frontier = PriorityQueue()
		frontier.enqueue(dist[src_cell], src_cell)
		# print(len(frontier)>0)
		while len(frontier)>0:
			_, cell = frontier.dequeue()
			# print(cell)
			visited[cell] = True
			if cell == dest_cell:
				flag = True
				break

			for ngb in self.grid.grid[cell]:
				if not visited[ngb] and dist[ngb] > dist[cell] + ngb.weight:
					# print(ngb)
					dist[ngb] = dist[cell] + ngb.weight
					frontier.compare_func = dist
					pred[ngb] = cell
					frontier.enqueue(dist[ngb], ngb)
		path = []
		if flag:
			while cell:
				path.append(cell)
				cell = pred[cell]
		else:
			print("Not Found")
		return path

	def __a_star(self, src_cell: Cell, dest_cell: Cell, pred: Dict[Cell, Cell]):
		def cost_function(cell1):
			return dist[cell1] + manhattan_distance(cell1, dest_cell)

		def manhattan_distance(cell1, cell2):
			return math.fabs(cell1.x - cell2.x) + math.fabs(cell1.y - cell2.y)

		visited, dist = dict(), dict()
		for k in self.grid.items():
			visited[k] = False
			dist[k] = 1e7
		dist[src_cell] = 0
		cell = None
		flag = False

		frontier = PriorityQueue()
		frontier.enqueue(cost_function(src_cell), src_cell)
		while frontier:
			_,cell = frontier.dequeue()
			visited[cell] = True
			if cell == dest_cell:
				flag = True
				break

			for ngb in self.grid.grid[cell]:
				if not visited[ngb] and dist[ngb] > dist[cell] + ngb.weight:
					dist[ngb] = dist[cell] + ngb.weight
					pred[ngb] = cell
					frontier.enqueue(cost_function(ngb), ngb)
		path = []
		if flag:
			while cell:
				path.append(cell)
				cell = pred[cell]
		else:
			print("Not Found")
		return path


# if __name__ == '__main__':
# 	grid = Grid(10)
# 	move = Movement(grid)
#
# 	for i in move.shortest_path((0,2), (5, 3), 3):
# 		print(i)
# 	# move.shortest_path(2, 53, 3)
