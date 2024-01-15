import pygame
from typing import Tuple


class GridCanvas:
    __CORE__ : "pygame" = pygame
    __DEFAULT_GRID_WH : Tuple[int] = (40, 40)
    __DEFAULT_GRID_SIZE : int = 30

    def __init__(self : "GraphCanvas") -> None:
        self.cells = set()

    def paint_cell(self : "GraphCanvas", color : str, pos : Tuple[int], surface : "pygame.surface.Surface") -> None:
        col = (pos[0]) // GridCanvas.__DEFAULT_GRID_SIZE
        row = (pos[1]) // GridCanvas.__DEFAULT_GRID_SIZE
        entry = (col, row, color)

        if entry not in self.cells:
            self.cells.add(entry)

        topLeft = (((col * GridCanvas.__DEFAULT_GRID_SIZE) - 10), row * GridCanvas.__DEFAULT_GRID_SIZE)
        if (200 <= topLeft[0] <= 1250 and 60 <= topLeft[1] <= 750):
            GridCanvas.__CORE__.draw.rect(surface, color, (*topLeft, GridCanvas.__DEFAULT_GRID_SIZE, GridCanvas.__DEFAULT_GRID_SIZE))

        self.draw_in(surface)

    def clear_cell(self : "GraphCanvas", pos : Tuple[int], eraseColor : Tuple[int], surface : "pygame.surface.Surface") -> None:
        col = (pos[0]) // GridCanvas.__DEFAULT_GRID_SIZE
        row = (pos[1]) // GridCanvas.__DEFAULT_GRID_SIZE
        
        for __col, __row, color in self.cells:
            if __row == row and __col == col:
                topLeft = (((col * GridCanvas.__DEFAULT_GRID_SIZE) - 10), row * GridCanvas.__DEFAULT_GRID_SIZE)
                GridCanvas.__CORE__.draw.rect(surface, eraseColor, (*topLeft, GridCanvas.__DEFAULT_GRID_SIZE, GridCanvas.__DEFAULT_GRID_SIZE))
                self.cells.remove((__col, __row, color))
                break

        self.draw_in(surface)

    def draw_in(self : "GraphCanvas", surface : "pygame.surface.Surface") -> None:
        for row in range(2, GridCanvas.__DEFAULT_GRID_WH[1] + 2):
            startPoint = (200, row * GridCanvas.__DEFAULT_GRID_SIZE)
            endPoint = (1250, row * GridCanvas.__DEFAULT_GRID_SIZE)
            GridCanvas.__CORE__.draw.line(surface, "black", startPoint, endPoint)

        for col in range(GridCanvas.__DEFAULT_GRID_WH[1]):
            startPoint = (200 + (col * GridCanvas.__DEFAULT_GRID_SIZE), 60)
            endPoint = (200 + (col * GridCanvas.__DEFAULT_GRID_SIZE), 750)
            GridCanvas.__CORE__.draw.line(surface, "black", startPoint, endPoint)