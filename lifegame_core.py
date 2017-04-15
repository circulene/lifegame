import random
import time

class Cells:
    UNDEFINED = 0
    DEAD = 1
    ALIVE = 2

    def __init__(self, nx, ny):
        self.nx = nx
        self.ny = ny
        self._cells = [[Cells.UNDEFINED for y in range(ny)] for x in range(nx)]
        self._nextCells = [[Cells.UNDEFINED for y in range(ny)] for x in range(nx)]
        for x in range(nx):
            for y in range(ny):
                status = random.choice((Cells.DEAD, Cells.ALIVE))
                self._cells[x][y] = status

    def cell(self, x, y):
        if x < 0 or x >= self.nx or y < 0 or y >= self.ny:
            return Cells.DEAD
        return self._cells[x][y]
#        return self._cells[x % self.nx][y % self.ny]

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
                elif self._cells[x][y] == Cells.DEAD and aliveNeighbours == 3:
                    self._nextCells[x][y] = Cells.ALIVE
                else:
                    self._nextCells[x][y] = self._cells[x][y]
        self._cells = self._nextCells[:]

