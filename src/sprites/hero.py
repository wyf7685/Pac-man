import time
from typing import TYPE_CHECKING, ClassVar, List, Optional, Tuple
from typing_extensions import override

import pygame
from pygame import Rect, Surface
from pygame.sprite import Group, Sprite

from src.const import *

if TYPE_CHECKING:
    from src.level import Level

    from .food import Food
    from .wall import Wall


class Hero(Sprite):
    """Hero"""

    nowframe: float
    allframe: float
    images: List[Surface]
    base_image: Surface
    image: Surface
    rect: Rect
    pre_x: int
    pre_y: int
    base_speed: Tuple[int, int]
    speed: Tuple[int, int]
    is_move: bool

    super_food: ClassVar[Optional[float]] = None

    @classmethod
    def create(cls, x: int, y: int, image_path: List[str]) -> "Hero":
        cls.super_food = None
        x = x * 30 + 3
        y = y * 30 + 3

        self = cls()
        self.nowframe = 0
        self.allframe = 1
        self.images = [IMAGES[p] for p in image_path]
        self.base_image = self.images[0].copy()
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect().copy()
        self.rect.centerx = x
        self.rect.centery = y
        self.pre_x = x
        self.pre_y = y
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

    def check_collide(self, walls: "Group[Wall]", gates: "Group[Wall]") -> bool:
        if self.nowframe < self.allframe:
            self.nowframe += 0.05
        else:
            self.nowframe = 0
        self.base_image = self.images[round(self.nowframe)].copy()
        self.changeSpeed((0, 0))
        if not self.is_move:
            return False

        x_pre = self.rect.centerx
        y_pre = self.rect.centery
        self.rect.centerx += self.speed[0]
        self.rect.centery += self.speed[1]

        collide = pygame.sprite.spritecollide(self, walls, False)
        if gates:
            collide.extend(pygame.sprite.spritecollide(self, gates, False))

        if collide:
            self.rect.centerx = x_pre
            self.rect.centery = y_pre
            return False

        return True

    def check_food(self, foods: "Group[Food]") -> List["Food"]:
        now = time.time()

        eaten = pygame.sprite.spritecollide(self, foods, True)
        for food in eaten:
            if food.is_super:
                self.set_super_food(now + food.super_duration)

        # Check the expiration time of SuperFood.
        if self.super_food and now >= self.super_food:
            self.set_super_food(None)

        return eaten

    @override
    def update(self, level: "Level", eaten: List["Food"], *args, **kwargs) -> None:
        self.check_collide(level.walls, level.gates)
        eaten.extend(self.check_food(level.foods))
