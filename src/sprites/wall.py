from pygame import Rect, Surface
from pygame.sprite import Sprite
from typing_extensions import override

from src.const import *


class Wall(Sprite):
    """Wall"""

    image: Surface
    rect: Rect

    @classmethod
    def _create(cls, x: int, y: int, width: int, height: int, color: Color):
        self = cls()
        self.image = Surface([width, height])
        self.image.fill(color)
        for p in {(0, 0), (0, height-1), (width-1, 0), (width-1, height-1)}:
            self.image.set_at(p, BLACK)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        return self

    @classmethod
    def create(cls, x1: int, y1: int, x2: int, y2: int, color: Color) -> "Wall":
        x, y = min(x1, x2) * 30, min(y1, y2) * 30
        w, h = abs(x1 - x2) * 30 + 6, abs(y1 - y2) * 30 + 6
        return cls._create(x, y, w, h, color)


class Gate(Wall):
    """Gate"""

    @override
    @classmethod
    def create(cls, x1: int, y1: int, x2: int, y2: int, color: Color) -> "Gate":
        x, y = min(x1, x2) * 30 + 2, min(y1, y2) * 30 + 2
        w, h = abs(x1 - x2) * 30 + 3, abs(y1 - y2) * 30 + 3
        return cls._create(x, y, w, h, color)
