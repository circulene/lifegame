import random
import time

class Cells:
    UNDEFINED = 0
    DEAD = 1
    ALIVE = 2

    def __init__(self, nx, ny, density = 5):
        self.nx = nx
        self.ny = ny
        self._cells = [[Cells.UNDEFINED for y in range(ny)] for x in range(nx)]
        self._nextCells = [[Cells.UNDEFINED for y in range(ny)] for x in range(nx)]
        self._gen = [[0 for y in range(ny)] for x in range(nx)]
        for x in range(nx):
            for y in range(ny):
#                status = random.choice((Cells.DEAD, Cells.ALIVE))
                status = Cells.ALIVE if random.randint(0, 100) < density else Cells.DEAD
                self._cells[x][y] = status
                self._gen[x][y] = status - 1

    def cell(self, x, y):
        if x < 0 or x >= self.nx or y < 0 or y >= self.ny:
            return Cells.DEAD
        return self._cells[x][y]
#        return self._cells[x % self.nx][y % self.ny]

    def gen(self, x, y):
        if x < 0 or x >= self.nx or y < 0 or y >= self.ny:
            return 0
        return self._gen[x][y]

    def _countAliveNeighbours(self, x, y):
        aliveNeighbours = 0
        neighbours = ((-1, -1), (0, -1), ( 1, -1),
                      (-1,  0),          ( 1,  0),
                      (-1,  1), (0,  1), ( 1,  1))
        for (ix, iy) in neighbours:
            neighbour = self.cell(x + ix, y + iy)
            if neighbour == Cells.ALIVE:
                aliveNeighbours += 1
        return aliveNeighbours

    def survive(self):
        for x in range(self.nx):
            for y in range(self.ny):
                aliveNeighbours = self._countAliveNeighbours(x, y)
                if self._cells[x][y] == Cells.ALIVE and (aliveNeighbours <= 1 or aliveNeighbours >= 4):
                    self._nextCells[x][y] = Cells.DEAD
                    self._gen[x][y] = 0
                elif self._cells[x][y] == Cells.DEAD and aliveNeighbours == 3:
                    self._nextCells[x][y] = Cells.ALIVE
                    self._gen[x][y] = 1
                else:
                    self._nextCells[x][y] = self._cells[x][y]
                    self._gen[x][y] += 1
        self._cells = self._nextCells[:]

