import math
from Layout import *
from DataStructures import PriorityQueue

class Movement:
    def __init__(self, grid):
        self.grid = grid

    def shortest_path(self, src, dest, mode=2):
        src_cell, dest_cell = self.grid.get((src // self.grid.dim, src % self.grid.dim)), self.grid.get(
            (dest // self.grid.dim, dest % self.grid.dim))
        path = dict()
        path[src_cell] = None

        if mode == 0:
            print("Implementing BFS")
            self.__bfs(src_cell, dest_cell, path)
        elif mode == 1:
            print("Implementing DFS")
            self.__dfs(src_cell, dest_cell, path)
        elif mode == 2:
            print("Implementing Djikstra")
            self.__djikstra(src_cell, dest_cell, path)
        elif mode == 3:
            print("Implementing A star")
            self.__a_star(src_cell, dest_cell, path)

    def __bfs(self, src_cell, dest_cell, path):
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
                    path[i] = cell
                    frontier.insert(0, i)  # __bfs if mode = 0 else __dfs

        if flag:
            while cell:
                print(cell)
                cell = path[cell]
        else:
            print("Not Found")

    def __dfs(self, src_cell, dest_cell, path):
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
                    path[i] = cell
                    frontier.insert(-1, i)  # __bfs if mode = 0 else __dfs

        if flag:
            while cell:
                print(cell)
                cell = path[cell]
        else:
            print("Not Found")

    def __djikstra(self, src_cell, dest_cell, path):
        visited, dist = dict(), dict()
        for k in self.grid.items():
            visited[k] = False
            dist[k] = 1e7
        dist[src_cell] = 0
        cell = None
        flag = False

        frontier = PriorityQueue(self.grid.size, lambda x: dist[x], src_cell)
        while frontier:
            cell = frontier.dequeue()
            visited[cell] = True
            if cell == dest_cell:
                flag = True
                break

            for i in self.grid.grid[cell]:
                if not visited[i]:
                    dist[i] = dist[cell] + i.weight
                    frontier.compare_func = lambda x: dist[x]
                    path[i] = cell
                    frontier.enqueue(i)
        if flag:
            while cell:
                print(cell)
                cell = path[cell]
        else:
            print("Not Found")

    def __a_star(self, src_cell, dest_cell, path):
        def manhattan_distance(cell1, cell2):
            return math.fabs(cell1.x - cell2.x) + math.fabs(cell1.y - cell2.y)

        visited = dict()
        for k in self.grid.items():
            visited[k] = False
        cell = None
        flag = False

        frontier = PriorityQueue(self.grid.size, lambda x: x.weight + manhattan_distance(x, dest_cell), src_cell)
        while frontier:
            cell = frontier.dequeue()
            visited[cell] = True
            if cell == dest_cell:
                flag = True
                break

            for i in self.grid.grid[cell]:
                if not visited[i]:
                    path[i] = cell
                    frontier.enqueue(i)
        if flag:
            while cell:
                print(cell)
                cell = path[cell]
        else:
            print("Not Found")


if __name__ == '__main__':
    grid = Grid(10)
    move = Movement(grid)

    move.shortest_path(2, 53, 2)
    # move.shortest_path(2, 53, 3)
