from typing import Optional, List


class Cell:
	def __init__(self, x:int, y:int, weight:float, dim:int):
		self.x, self.y, self.weight = x, y, weight
		self.dim = dim

	def __eq__(self, other)->bool:
		return (self.x, self.y, self.weight) == (other.x, other.y, other.weight)

	def __str__(self)->str:
		return f"{self.x, self.y}"

	def __hash__(self)->int:
		return self.x * self.dim + self.y


class Grid:
	def __init__(self, dim:int=3):
		self.grid = dict()
		self.dim =  dim
		self.size = dim ** 2

		for x in range(dim):
			for y in range(dim):
				self.grid[Cell(x,y, 1, dim)] =[]

		for k in self.grid.keys():
			x,y = k.x, k.y
			next = [(x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)]
			self.grid[k] = [self.get(c) for c in next if all(0 <= k < dim for k in c)]

	def __str__(self)->int:
		s = ""
		for k in self.grid.keys():
			s += f"{k}: "
			for l in self.grid[k]:
				s += f"{l}; "
			s += '\n'
		return s

	def get(self, item: tuple)->Optional[Cell]:
		for k in self.grid.keys():
			if k.x == item[0] and k.y == item[1]:
				return k
		else:
			return None

	def items(self)->List[Cell]:
		return list(self.grid.keys())
