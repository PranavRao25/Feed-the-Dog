class Cell:
    def __init__(self, x, y, weight, dim):
        self.x, self.y, self.weight = x, y, weight
        self.dim = dim

    def __eq__(self, other):
        return (self.x, self.y, self.weight) == (other.x, other.y, other.weight)

    def __str__(self):
        return f"{self.x * self.dim + self.y}"

    def __hash__(self):
        return self.x * self.dim + self.y


class Grid:
    def __init__(self, dim=3):
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

    def __str__(self):
        s = ""
        for k in self.grid.keys():
            s += f"{k}: "
            for l in self.grid[k]:
                s += f"{l}; "
            s += '\n'
        return s

    def get(self, item):
        return [k for k in self.grid.keys() if k.x == item[0] and k.y == item[1]][0]

    def items(self):
        return list(self.grid.keys())
