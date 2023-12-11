import time
from typing import TYPE_CHECKING, List, Optional, Tuple

import pygame
from pygame import Rect, Surface
from pygame.sprite import Group, Sprite

from src.const import *

if TYPE_CHECKING:
    from .food import Food
    from .wall import Wall


class Hero(Sprite):
    """Hero"""

    nowframe: float
    allframe: float
    images: List[str]
    role_name: str
    base_image: Surface
    image: Surface
    rect: Rect
    pre_x: int
    pre_y: int
    base_speed: Tuple[int, int]
    speed: Tuple[int, int]
    is_move: bool

    super_food: Optional[float]

    @classmethod
    def create(cls, x: int, y: int, images: List[str]) -> "Hero":
        cls.super_food = None

        self = cls()
        self.nowframe = 0
        self.allframe = 1
        self.images = images
        self.role_name = self.images[0].split("/")[-1].split(".")[0]
        self.base_image = pygame.image.load(self.images[0]).convert()
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
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

    def check_collide(
        self, wall_sprites: "Group[Wall]", gate_sprites: "Group[Wall]"
    ) -> bool:
        if self.nowframe < self.allframe:
            self.nowframe += 0.05
        else:
            self.nowframe = 0
        self.base_image = pygame.image.load(self.images[round(self.nowframe)]).convert()
        self.changeSpeed((0, 0))
        if not self.is_move:
            return False
        x_pre = self.rect.left
        y_pre = self.rect.top
        self.rect.left += self.speed[0]
        self.rect.top += self.speed[1]
        collide = pygame.sprite.spritecollide(self, wall_sprites, False)
        if gate_sprites is not None:
            if not collide:
                collide = pygame.sprite.spritecollide(self, gate_sprites, False)
        if collide:
            self.rect.left = x_pre
            self.rect.top = y_pre
            return False
        return True

    def check_food(self, food_sprites: "Group[Food]") -> List["Food"]:
        now = time.time()

        eaten = pygame.sprite.spritecollide(self, food_sprites, True)
        for food in eaten:
            if food.is_super:
                self.set_super_food(now + food.super_duration)

        # Check the expiration time of SuperFood.
        if self.super_food and now >= self.super_food:
            self.set_super_food(None)

        return eaten