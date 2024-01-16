import sys
import pygame
from typing import *

from drawComponents import ColorPlate, GridCanvas


class App():
    __CORE__ : "pygame" = pygame
    __DEFAULT_WINDOW_SIZE : Tuple[int] = (1280, 780)
    __DEFAULT_WINDOW_COLOR : Tuple[int] = (205, 205, 205)

    def __init__(self : "App") -> None:
        App.__CORE__.init()
        self.activeDrawSate = False
        self.activeEraseState = False
        self.__WINDOW : "pygame.display"
        self.__MAIN_SURFACE : "pygame.surface.Surface"
        self.__currentSize : Tuple[int] = App.__DEFAULT_WINDOW_SIZE
        self.colorPlate : ColorPlate = ColorPlate()
        self.gridCanvas : GridCanvas = GridCanvas()
        self.__set_render_components()
        self.__set_tools()

    def __set_tools(self : "App") -> None:
        self.drawButtonSurface = App.__CORE__.image.load("assets/pencile.png").convert_alpha()
        self.drawButtonSurface = App.__CORE__.transform.scale(self.drawButtonSurface, (60, 60))
        self.drawButtonPosRect = self.drawButtonSurface.get_rect(topleft=(1100, 5))

        self.eraserButtonSurface = App.__CORE__.image.load("assets/eraser.png").convert_alpha()
        self.eraserButtonSurface = App.__CORE__.transform.scale(self.eraserButtonSurface, (40, 40))
        self.eraserButtonPosRect = self.eraserButtonSurface.get_rect(topleft=(1155, 15))

        self.saveButtonSurface = App.__CORE__.image.load("assets/save.png").convert_alpha()
        self.saveButtonSurface = App.__CORE__.transform.scale(self.saveButtonSurface, (40, 40))
        self.saveButtonPosRect = self.drawButtonSurface.get_rect(topleft=(1210, 15))

    def __set_render_components(self : "App") -> None:
        self.__WINDOW = App.__CORE__.display
        self.__WINDOW.set_caption("PYPAINT")
        self.__WINDOW.set_mode(self.__currentSize)
        self.__MAIN_SURFACE = self.__WINDOW.get_surface()
        self.__MAIN_SURFACE.fill(App.__DEFAULT_WINDOW_COLOR)

        self.colorPlate.draw_in(self.__MAIN_SURFACE)
        self.colorPlate.mark_selected_color(self.__MAIN_SURFACE)
        self.gridCanvas.draw_in(self.__MAIN_SURFACE)

    def __check_for_tool_selection(self : "App", pos : Tuple[int]) -> None:
        if self.saveButtonPosRect.collidepoint(pos):
            self.gridCanvas.export_png()
        
        if self.drawButtonPosRect.collidepoint(pos):
            self.activeDrawSate = not self.activeDrawSate
            if self.activeDrawSate:
                self.activeEraseState = False
                App.__CORE__.draw.circle(self.__MAIN_SURFACE, App.__CORE__.Color(App.__DEFAULT_WINDOW_COLOR), self.eraserButtonPosRect.center, 20)
                App.__CORE__.draw.circle(self.__MAIN_SURFACE, "Yellow", self.drawButtonPosRect.center, 20)
            else:
                App.__CORE__.draw.circle(self.__MAIN_SURFACE, App.__CORE__.Color(App.__DEFAULT_WINDOW_COLOR), self.drawButtonPosRect.center, 20)

        if self.eraserButtonPosRect.collidepoint(pos):
            self.activeEraseState = not self.activeEraseState

            if self.activeEraseState:
                self.activeDrawSate = False
                App.__CORE__.draw.circle(self.__MAIN_SURFACE, App.__CORE__.Color(App.__DEFAULT_WINDOW_COLOR), self.drawButtonPosRect.center, 20)
                App.__CORE__.draw.circle(self.__MAIN_SURFACE, "Yellow", self.eraserButtonPosRect.center, 20)
            else:
                App.__CORE__.draw.circle(self.__MAIN_SURFACE, App.__CORE__.Color(App.__DEFAULT_WINDOW_COLOR), self.eraserButtonPosRect.center, 20)

    def __execute_action(self : "App", event : "pygame.event.Event") -> None:
        color = self.colorPlate.get_selected_color()
        if color and self.activeDrawSate:
            color[1].center = event.dict["pos"]
            self.gridCanvas.paint_cell(color[0], event.dict["pos"], self.__MAIN_SURFACE)

        if self.activeEraseState:
            self.gridCanvas.clear_cell(event.dict["pos"], App.__DEFAULT_WINDOW_COLOR, self.__MAIN_SURFACE)

    def __handle_event(self : "App", event : "pygame.event.Event") -> None:
        if event.type == App.__CORE__.QUIT:
            App.__CORE__.quit()
            sys.exit()

        if event.type == App.__CORE__.MOUSEBUTTONDOWN:
            self.__check_for_tool_selection(event.dict["pos"])
            self.colorPlate.mark_selected_color(self.__MAIN_SURFACE)
            self.colorPlate.draw_in(self.__MAIN_SURFACE)
            selected = self.colorPlate.check_for_color_selection(event.dict["pos"], self.__MAIN_SURFACE)
            self.__execute_action(event)

        if event.type == App.__CORE__.MOUSEMOTION and event.buttons[0]:
            self.__execute_action(event)

    def run(self : "App") -> None:
        while True:
            for event in App.__CORE__.event.get():
                self.__handle_event(event)

            self.__MAIN_SURFACE.blit(self.eraserButtonSurface, self.eraserButtonPosRect)
            self.__MAIN_SURFACE.blit(self.drawButtonSurface, self.drawButtonPosRect)
            self.__MAIN_SURFACE.blit(self.saveButtonSurface, self.saveButtonPosRect)
            self.__WINDOW.flip()


if __name__ == "__main__":
    App().run()