import random

"""
00 01 02
10 11 12
20 21 22

0 1 2
3 4 5
6 7 8
"""


class Cell:
    def __init__(self, x, y, weight, size):
        self.x, self.y, self.weight = x, y, weight
        self.size = size

    def __eq__(self, other):
        return (self.x, self.y, self.weight) == (other.x, other.y, other.weight)

    def __str__(self):
        return f"{self.x * self.size + self.y}"

    def __hash__(self):
        return self.x * self.size + self.y


class Grid:
    def __init__(self, size=3):
        self.grid = dict()
        self.size = size

        for x in range(size):
            for y in range(size):
                self.grid[Cell(x,y, 1, size)] =[]

        for k in self.grid.keys():
            x,y = k.x, k.y
            next = [(x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)]
            self.grid[k] = [self.get(c) for c in next if all(0 <= k < size for k in c)]

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

    def bdfs(self, src, dest, mode=0):
        path = dict()
        visited = dict()
        for k in self.grid.keys():
            visited[k] = False

        src_cell, dest_cell = self.get((src//self.size, src%self.size)), self.get((dest//self.size, dest%self.size))
        path[src_cell] = None
        frontier = [src_cell]
        flag = False

        while frontier:
            cell = frontier.pop(-1)
            visited[cell] = True
            if cell == dest_cell:
                flag = True
                break

            for i in self.grid[cell]:
                if not visited[i]:
                    path[i] = cell
                    frontier.insert(-1*mode, i)  # bfs if mode = 0 else dfs

        if flag:
            while cell:
                print(cell)
                cell = path[cell]
        else:
            print("Not Found")

#
# class Cell:
#     def __init__(self, x, y, weight, size):
#         self.index, self.weight = x*size+y, weight
#         ngb = [(x, y + 1),
#          (x + 1, y),
#          (x, y - 1),
#          (x - 1, y)]
#         self.ngbs = [c[0]*size+c[1] for c in ngb if all(0<=k<size for k in c)]
#
#     def __str__(self):
#         return f"{self.index}, {self.weight}, {self.ngbs}"
#
#     def __eq__(self, other):
#         return self.index == other.index
#
#     def __hash__(self):
#         return self.index
#
#
# class Grid:
#     def __init__(self, size):
#         self.grid = []
#
#         for x in range(size):
#             for y in range(size):
#                 cell = Cell(x,y,1, size)
#                 self.grid.append(cell)
#
#     def bfs(self, src, dest):
#         src_cell, dest_cell = self.grid[src], self.grid[dest]
#         path = dict()
#         path[src_cell] = None
#         frontier = [src_cell]
#
#         while len(frontier) > 0:
#             cell = frontier.pop(-1)
#             if cell.index == dest_cell.index:
#                 print('Found')
#                 break
#
#             for i in cell.ngbs:
#                 if i not in frontier:
#                     path[self.grid[i]] = cell
#                     frontier.append(self.grid[i])
#         print(path)
#
grid = Grid(10)
print(grid)
grid.bdfs(0, 53, 1)

# grid.bfs(0,7)
# # fruits = ['apple', 'banana', 'cherry']
# #
# # x = fruits.pop(1)
# # print(x)