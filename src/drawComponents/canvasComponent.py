import os
import pygame
from typing import Tuple, Set
from datetime import datetime
from plyer import notification


class GridCanvas:
    __CORE__ : "pygame" = pygame
    __DEFAULT_GRID_WH : Tuple[int] = (32, 32)
    __DEFAULT_GRID_SIZE : int = 23
    __XOFFSET : int = 300
    __YOFFSET : int = 20

    def __init__(self : "GraphCanvas") -> None:
        self.cells : Set[Tuple[int, int, str]] = set()

    def paint_cell(self : "GraphCanvas", color : str, pos : Tuple[int], surface : "pygame.surface.Surface") -> None:
        col, row = self.get_coord(pos)
        entry = (col, row, color)
        
        if col == -1 or row == -1:
            return

        if entry not in self.cells:
            self.cells.add(entry)

        topLeft = (GridCanvas.__XOFFSET + (col * GridCanvas.__DEFAULT_GRID_SIZE), GridCanvas.__YOFFSET + (row * GridCanvas.__DEFAULT_GRID_SIZE))

        if (GridCanvas.__XOFFSET <= topLeft[0] < ((GridCanvas.__DEFAULT_GRID_WH[0] * GridCanvas.__DEFAULT_GRID_SIZE) + GridCanvas.__XOFFSET)
                    and (GridCanvas.__YOFFSET) <= topLeft[1] <= (GridCanvas.__DEFAULT_GRID_WH[1] * GridCanvas.__DEFAULT_GRID_SIZE)):
            GridCanvas.__CORE__.draw.rect(surface, color, (*topLeft, GridCanvas.__DEFAULT_GRID_SIZE, GridCanvas.__DEFAULT_GRID_SIZE))

        self.draw_in(surface)

    def clear_cell(self : "GraphCanvas", pos : Tuple[int], eraseColor : Tuple[int], surface : "pygame.surface.Surface") -> None:
        col, row = self.get_coord(pos)

        if col == -1 or row == -1:
            return
        
        for __col, __row, color in self.cells:
            if __row == row and __col == col:
                topLeft = (GridCanvas.__XOFFSET + (col * GridCanvas.__DEFAULT_GRID_SIZE), GridCanvas.__YOFFSET + (row * GridCanvas.__DEFAULT_GRID_SIZE))
                GridCanvas.__CORE__.draw.rect(surface, eraseColor, (*topLeft, GridCanvas.__DEFAULT_GRID_SIZE, GridCanvas.__DEFAULT_GRID_SIZE))
                self.cells.remove((__col, __row, color))
                break

        self.draw_in(surface)

    def draw_in(self : "GraphCanvas", surface : "pygame.surface.Surface") -> None:
        #Horizontal line
        for row in range(GridCanvas.__DEFAULT_GRID_WH[1] + 1):
            startPoint = (GridCanvas.__XOFFSET, GridCanvas.__YOFFSET + (row * GridCanvas.__DEFAULT_GRID_SIZE))
            endPoint = (GridCanvas.__XOFFSET + (GridCanvas.__DEFAULT_GRID_WH[0] * GridCanvas.__DEFAULT_GRID_SIZE), GridCanvas.__YOFFSET + (row * GridCanvas.__DEFAULT_GRID_SIZE))
            GridCanvas.__CORE__.draw.line(surface, "black", startPoint, endPoint)

        #Vertical line
        for col in range(GridCanvas.__DEFAULT_GRID_WH[1] + 1):
           startPoint = (GridCanvas.__XOFFSET + (col * GridCanvas.__DEFAULT_GRID_SIZE), GridCanvas.__YOFFSET)
           endPoint = (GridCanvas.__XOFFSET + (col * GridCanvas.__DEFAULT_GRID_SIZE), GridCanvas.__YOFFSET + (GridCanvas.__DEFAULT_GRID_WH[1] * GridCanvas.__DEFAULT_GRID_SIZE))
           GridCanvas.__CORE__.draw.line(surface, "black", startPoint, endPoint)

    def __send_notification(self : "GraphCanvas", fileInfo : str) -> None:
        notification.notify(
            title="PYPAINT : Drawing saved !",
            message=f"File saved at : {fileInfo}",
            app_name="PYPAINT",
            timeout=30,  # Display duration in seconds
        )

    def __get_drawing_for_export(self: "GraphCanvas", scale : int) -> "pygame.surface.Surface":
        canvas_size = (GridCanvas.__DEFAULT_GRID_WH[0] * scale, GridCanvas.__DEFAULT_GRID_WH[1] * scale)
        canvas = GridCanvas.__CORE__.surface.Surface(canvas_size)

        # Enable anti-aliasing
        canvas.set_alpha(None)

        for row in range(GridCanvas.__DEFAULT_GRID_WH[0]):
            for col in range(GridCanvas.__DEFAULT_GRID_WH[1]):
                pixel_size = scale * 1
                pixel_color = "white"
                pixel_rect = (col * pixel_size, row * pixel_size, pixel_size, pixel_size)
                GridCanvas.__CORE__.draw.rect(canvas, pixel_color, pixel_rect, 0)  # Set the third argument to 0 for no anti-aliasing

        for col, row, color in self.cells:
            pixel_size = scale * 1
            pixel_rect = (col * pixel_size, row * pixel_size, pixel_size, pixel_size)
            GridCanvas.__CORE__.draw.rect(canvas, color, pixel_rect, 0)  # Set the third argument to 0 for no anti-aliasing

        return canvas

    def get_coord(self : "GraphCanvas", pos : Tuple[int]) -> Tuple[int]:
        coord = (-1, -1)
        if not (GridCanvas.__XOFFSET <= pos[0] < ((GridCanvas.__DEFAULT_GRID_WH[0] * GridCanvas.__DEFAULT_GRID_SIZE) + GridCanvas.__XOFFSET)
            and (GridCanvas.__YOFFSET) <= pos[1] <= (GridCanvas.__DEFAULT_GRID_WH[1] * GridCanvas.__DEFAULT_GRID_SIZE) + (GridCanvas.__YOFFSET + 12)):
                    return coord

        col = ((pos[0]) // GridCanvas.__DEFAULT_GRID_SIZE) - (GridCanvas.__XOFFSET // GridCanvas.__DEFAULT_GRID_SIZE)
        row = ((pos[1]) // GridCanvas.__DEFAULT_GRID_SIZE) - ((GridCanvas.__YOFFSET + 12) // GridCanvas.__DEFAULT_GRID_SIZE)

        coord = (col, row)

        return coord

    def export_png(self) -> None:
        file1Name : str = f"pypaint_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}s_50.png"
        file2Name : str = f"pypaint_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}s_1.png"
        
        GridCanvas.__CORE__.image.save_extended(self.__get_drawing_for_export(scale=50), file1Name)
        GridCanvas.__CORE__.image.save_extended(self.__get_drawing_for_export(scale=1), file2Name)
        
        self.__send_notification(os.path.join(os.getcwd(), file1Name))
        self.__send_notification(os.path.join(os.getcwd(), file2Name))