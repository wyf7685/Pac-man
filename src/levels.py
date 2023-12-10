import random

import pygame
from pydantic import BaseModel
from pygame.sprite import Group

from src.const import *
from src.maze import generate_maze
from src.sprites import *


class _LevelData_no_food(BaseModel):
    row: Tuple[int, int]
    col: Tuple[int, int]


class _LevelData(BaseModel):
    seq: int
    name: str
    hero: Position
    blinky: Position
    clyde: Position
    inky: Position
    pinky: Position
    no_food: List[_LevelData_no_food]
    gate: List[Tuple[int, int, int, int]]
    wall: List[Tuple[int, int, int, int]]


class Level(object):
    _data: _LevelData
    name: str
    maze: list[list[int]]
    wall_sprites: "Group[Wall]"
    gate_sprites: "Group[Wall]"
    hero_sprites: "Group[Hero]"
    ghost_sprites: "Group[Ghost]"
    food_sprites: "Group[Food]"

    def __init__(self, data: _LevelData):
        self._data = data
        self.name = data.name

    def setup_wall(self, wall_color: Color):
        self.maze = generate_maze(self._data.wall)
        walls = [Wall.create(*[*wall, wall_color]) for wall in self._data.wall]
        self.wall_sprites = Group(walls)
        return self.wall_sprites

    def setup_gate(self, gate_color: Color):
        gates = [Wall.create(*[*gate, gate_color]) for gate in self._data.gate]
        self.gate_sprites = Group(gates)
        return self.gate_sprites

    def setup_player(self):
        self.hero_sprites = Group(Hero.create(*self._data.hero))
        ghosts = [
            Ghost.create(*self._data.blinky, BlinkyPATH),
            Ghost.create(*self._data.clyde, ClydePATH),
            Ghost.create(*self._data.inky, InkyPATH),
            Ghost.create(*self._data.pinky, PinkyPATH),
        ]
        self.ghost_sprites = Group(*ghosts)
        return self.hero_sprites, self.ghost_sprites

    def setup_food(self, food_color: Color, bg_color: Color):
        foods = []  # type: List[Food]

        def invalid(row: int, col: int):
            for item in self._data.no_food:
                if (
                    item.row[0] <= row <= item.row[1]
                    and item.col[0] <= col <= item.col[1]
                ):
                    return True
            return False

        for col in range(len(self.maze)):
            for row in range(len(self.maze[col])):
                if self.maze[col][row] == 0 or invalid(row, col):
                    continue

                fcol = 30 * col + 2
                frow = 30 * row + 2
                food = Food.create(fcol, frow, 4, 4, food_color, bg_color)
                if pygame.sprite.spritecollide(food, self.wall_sprites, False):
                    continue
                if pygame.sprite.spritecollide(food, self.hero_sprites, False):
                    continue

                foods.append(food)

        for food in random.sample(foods, round(len(foods) / 50)):
            food.set_super()

        self.food_sprites = Group(foods)
        return self.food_sprites


_LEVEL_DATA = sorted(
    [
        _LevelData.model_validate_json(p.read_text(encoding="utf-8"))
        for p in LEVELPATH.iterdir()
        if p.name.endswith(".json")
    ],
    key=lambda x: x.seq,
)
LEVELS = [Level(i) for i in _LEVEL_DATA]
