from pygame import Rect, Surface
from pygame.sprite import Sprite

from src.const import *


class Wall(Sprite):
    """Wall"""

    image: Surface
    rect: Rect

    @classmethod
    def create(cls, x: int, y: int, width: int, height: int, color: Color):
        self = cls()
        self.image = Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        return self
