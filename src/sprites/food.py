from typing import Any, Tuple
from typing_extensions import override

import pygame
from pygame import Rect, Surface
from pygame.sprite import Sprite

from src.const import Color


class Food(Sprite):
    """Food"""

    base_x: int
    base_y: int
    base_width: int
    base_height: int
    color: Tuple[int, int, int]
    bg_color: Tuple[int, int, int]

    image: Surface
    rect: Rect
    is_super: bool = False
    super_duration: float = 10.0
    __size: float = 3

    @classmethod
    def create(
        cls, x: int, y: int, width: int, height: int, color: Color, bg_color: Color
    ):
        self = cls()
        self.base_x = x
        self.base_y = y
        self.base_width = width
        self.base_height = height
        self.color = color
        self.bg_color = bg_color

        self.draw()
        return self

    def draw(self):
        x = self.base_x
        y = self.base_y
        width = self.base_width
        height = self.base_height

        if self.is_super:
            size = round(self.__size)
            x -= size
            y -= size
            width += size * 2
            height += size * 2

        self.image = Surface([width, height])
        self.image.fill(self.bg_color)
        self.image.set_colorkey(self.bg_color)
        pygame.draw.ellipse(self.image, self.color, [0, 0, width, height])
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y

    def set_super(self):
        self.is_super = True
        self.draw()

    @override
    def update(self, *args: Any, **kwargs: Any) -> None:
        self.__size += 0.03
        if self.__size >= 3:
            self.__size = 2.0

        self.draw()
