import random
from typing import Type

import pygame
from pygame.sprite import Group

from Maze import generate_maze
from Sprites import *
from Const import *


class Level(object):
    info: str
    maze: list[list[int]]
    wall_sprites: "Group[Wall]"
    gate_sprites: "Group[Wall]"
    hero_sprites: "Group[Hero]"
    ghost_sprites: "Group[Ghost]"
    food_sprites: "Group[Food]"

    def __init__(self):
        raise NotImplemented

    def setupWalls(self, wall_color) -> "Group[Wall]":
        raise NotImplemented

    def setupGate(self, gate_color) -> "Group[Wall]":
        raise NotImplemented

    def setupPlayers(self) -> tuple["Group[Hero]", "Group[Ghost]"]:
        raise NotImplemented

    def setupFood(self, food_color, bg_color) -> "Group[Food]":
        raise NotImplemented


class Level1(Level):
    """Level1"""

    def __init__(self):
        self.info = "Level-1"

    def setupWalls(self, wall_color):
        """Create Walls"""
        self.wall_sprites = pygame.sprite.Group()
        wall_positions = [
            [0, 0, 6, 600],
            [0, 0, 600, 6],
            [0, 600, 606, 6],
            [600, 0, 6, 606],
            [300, 0, 6, 66],
            [60, 60, 186, 6],
            [360, 60, 186, 6],
            [60, 120, 66, 6],
            [60, 120, 6, 126],
            [180, 120, 246, 6],
            [300, 120, 6, 66],
            [480, 120, 66, 6],
            [540, 120, 6, 126],
            [120, 180, 126, 6],
            [120, 180, 6, 126],
            [360, 180, 126, 6],
            [480, 180, 6, 126],
            [180, 240, 6, 126],
            [180, 360, 246, 6],
            [420, 240, 6, 126],
            # [240, 240, 42, 6],  # Gate左侧
            # [324, 240, 42, 6],  # Gate右侧
            [240, 240, 6, 66],
            [240, 300, 126, 6],
            [360, 240, 6, 66],
            [0, 300, 66, 6],
            [540, 300, 66, 6],
            [60, 360, 66, 6],
            [60, 360, 6, 186],
            [480, 360, 66, 6],
            [540, 360, 6, 186],
            [120, 420, 366, 6],
            [120, 420, 6, 66],
            [480, 420, 6, 66],
            [180, 480, 246, 6],
            [300, 480, 6, 66],
            [120, 540, 126, 6],
            [360, 540, 126, 6],
        ]

        self.maze = generate_maze(wall_positions)

        for wall_position in wall_positions:
            wall = Wall.create(*[*wall_position, wall_color])
            self.wall_sprites.add(wall)
        return self.wall_sprites

    def setupGate(self, gate_color):
        """Create Gate"""
        self.gate_sprites = pygame.sprite.Group()
        self.gate_sprites.add(Wall.create(282, 242, 42, 2, gate_color))
        self.gate_sprites.add(Wall.create(240, 242, 42, 2, gate_color))  # Gate左侧
        self.gate_sprites.add(Wall.create(324, 242, 42, 2, gate_color))  # Gate右侧
        return self.gate_sprites

    def setupPlayers(self):
        """Create Players(Including ghosts and hero)"""
        self.hero_sprites = pygame.sprite.Group()
        self.hero_sprites.add(Hero.create(287, 439, HEROPATH, HEROPATH2))

        self.ghost_sprites = pygame.sprite.Group()
        self.ghost_sprites.add(Ghost.create(287, 199, BlinkyPATH))
        self.ghost_sprites.add(Ghost.create(319, 259, ClydePATH))
        self.ghost_sprites.add(Ghost.create(255, 259, InkyPATH))
        self.ghost_sprites.add(Ghost.create(287, 259, PinkyPATH))

        return self.hero_sprites, self.ghost_sprites

    def setupFood(self, food_color, bg_color):
        """Create Food"""
        self.food_sprites = pygame.sprite.Group()
        foods = []  # type: List[Food]

        for row in range(19):
            for col in range(19):
                if (row == 7 or row == 8) and (col == 8 or col == 9 or col == 10):
                    continue
                else:
                    fcol = 30 * col + 32
                    frow = 30 * row + 32
                    food = Food.create(fcol, frow, 4, 4, food_color, bg_color)
                    if pygame.sprite.spritecollide(food, self.wall_sprites, False):
                        continue
                    if pygame.sprite.spritecollide(food, self.hero_sprites, False):
                        continue
                    foods.append(food)

        for food in random.sample(foods, round(len(foods) / 50)):
            food.set_super()

        self.food_sprites.add(*foods)
        return self.food_sprites


LEVELS = [Level1]  # type: List[Type[Level]]
