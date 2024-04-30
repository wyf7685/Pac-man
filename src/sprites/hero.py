import time
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar, List, Optional, Tuple, override

import pygame
from pygame import Rect, Surface
from pygame.sprite import Sprite

from src.const import *

from .food import Food
from .group import Group

if TYPE_CHECKING:
    from src.level import Level


class Hero(Sprite):
    """Hero"""

    nowframe: float
    allframe: float
    images: List[Surface]
    base_image: Surface
    image: Surface
    rect: Rect
    base_speed: Tuple[int, int]
    speed: Tuple[int, int]
    is_move: bool

    super_food: ClassVar[Optional[float]] = None

    @classmethod
    def create(cls, x: int, y: int, image_path: List[Path]) -> "Hero":
        cls.super_food = None

        self = cls()
        self.nowframe = 0
        self.allframe = 1
        self.images = [IMAGES[p] for p in image_path]
        self.base_image = self.images[0].copy()
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect().copy()
        self.rect.center = x * 30 + 3, y * 30 + 3
        self.base_speed = (3, 3)
        self.speed = (0, 0)
        self.is_move = False
        return self

    @classmethod
    def set_super_food(cls, value: Optional[float] = None):
        cls.super_food = value

    def changeSpeed(self, direction: Direction):
        if direction[0] < 0:
            self.image = pygame.transform.flip(self.base_image, True, False)
        elif direction[0] > 0:
            self.image = self.base_image.copy()
        elif direction[1] < 0:
            self.image = pygame.transform.rotate(self.base_image, 90)
        elif direction[1] > 0:
            self.image = pygame.transform.rotate(self.base_image, -90)

        if any(direction):
            self.speed = (
                round(direction[0] * self.base_speed[0]),
                round(direction[1] * self.base_speed[1]),
            )

        return self.speed

    def check_collide(self, level: "Level") -> None:
        if self.nowframe < self.allframe:
            self.nowframe += 0.05
        else:
            self.nowframe = 0
        self.base_image = self.images[round(self.nowframe)]
        if not self.is_move:
            return

        prev = self.rect.center
        self.rect.centerx += self.speed[0]
        self.rect.centery += self.speed[1]

        collide = pygame.sprite.spritecollide(self, level.walls, False)
        collide += pygame.sprite.spritecollide(self, level.gates, False)

        if collide:
            self.rect.center = prev

    def check_food(self, foods: Group[Food]) -> List["Food"]:
        now = time.time()

        eaten = pygame.sprite.spritecollide(self, foods, True)
        for food in eaten:
            if food.is_super:
                self.set_super_food(now + food.super_duration)

        # Check the expiration time of SuperFood.
        if self.super_food and now >= self.super_food:
            self.set_super_food(None)

        return eaten

    def update(self, level: "Level", eaten: List["Food"], *args, **kwargs) -> None: # type: ignore
        self.check_collide(level)
        eaten.extend(self.check_food(level.foods))
