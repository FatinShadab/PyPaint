import pygame
from typing import Tuple, Dict, List, Optional

class ColorPlate:
    __CORE__ : "pygame" = pygame
    SQR_SIZE : int = 30
    DEFAULT_ROW_QUANTITY = 26

    def __init__(self : "ColorPlate") -> None:
        self.maxRow = ColorPlate.DEFAULT_ROW_QUANTITY
        self.selectedColor : str = None
        self.colors : Dict[str, "pygame.Rect"] = dict({})
        self.make_colors()

    def make_colors(self : "ColorPlate", maxRow = None) -> None:
        self.maxRow = maxRow if maxRow else self.maxRow
        row, col = (0, 0)
        for idx, color in enumerate(( color for color in ColorPlate.__CORE__.colordict.THECOLORS if color[-1] not in "0123456789")):
            row = idx % self.maxRow
            if row == 0 and idx != 0:
                col += 1
            self.colors[color] = ColorPlate.__CORE__.Rect(ColorPlate.SQR_SIZE * col, ColorPlate.SQR_SIZE * row, ColorPlate.SQR_SIZE, ColorPlate.SQR_SIZE)

    def check_for_color_selection(self : "ColorPlate", pos : Tuple[int], surface : "pygame.surface.Surface") -> bool:
        found = False
        for colorName, colorRect in self.colors.items():
            if colorRect.colliderect(ColorPlate.__CORE__.Rect(pos[0], pos[1], ColorPlate.SQR_SIZE, ColorPlate.SQR_SIZE)):
                self.selectedColor = colorName
                found = True
                break

        self.mark_selected_color(surface)

        return found

    def mark_selected_color(self : "ColorPlate", surface : "pygame.surface.Surface") -> None:
        if self.selectedColor:
            _, selectedRect = self.get_selected_color()
            selectedRect.width -= 20
            selectedRect.height -= 20
            ColorPlate.__CORE__.draw.rect(surface, "black", selectedRect)

    def get_selected_color(self : "ColorPlate") -> Optional[Tuple[str, "pygame.Rect"]]:
        if self.selectedColor:
            return (self.selectedColor, self.colors[self.selectedColor].copy())

    def draw_in(self : "ColorPlate", surface : "pygame.surface.Surface") -> None:
        for colorName, colorRect in self.colors.items():
            ColorPlate.__CORE__.draw.rect(surface, colorName, colorRect)