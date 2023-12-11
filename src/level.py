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
    hero: List[Position]
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
    maze: List[List[int]]
    walls: "Group[Wall]"
    gates: "Group[Wall]"
    heroes: "Group[Hero]"
    ghosts: "Group[Ghost]"
    foods: "Group[Food]"

    def __init__(self, data: _LevelData):
        self._data = data
        self.name = data.name

    def setup_wall(self, wall_color: Color):
        self.maze = generate_maze(self._data.wall)
        walls = [Wall.create(*[*wall, wall_color]) for wall in self._data.wall]
        self.walls = Group(walls)
        return self.walls

    def setup_gate(self, gate_color: Color):
        gates = [Wall.create(*[*gate, gate_color]) for gate in self._data.gate]
        self.gates = Group(gates)
        return self.gates

    def setup_player(self):
        self.heroes = Group()
        for pos, frames in zip(self._data.hero, [HERO_FRAMES, HERO2_FRAMES]):
            self.heroes.add(Hero.create(*pos, frames))
        self.ghosts = Group([
            Ghost.create(*self._data.blinky, BlinkyPATH),
            Ghost.create(*self._data.clyde, ClydePATH),
            Ghost.create(*self._data.inky, InkyPATH),
            Ghost.create(*self._data.pinky, PinkyPATH),
        ])
        return self.heroes, self.ghosts

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
                if pygame.sprite.spritecollide(food, self.walls, False):
                    continue
                if pygame.sprite.spritecollide(food, self.heroes, False):
                    continue

                foods.append(food)

        for food in random.sample(foods, round(len(foods) / 50)):
            food.set_super()

        self.foods = Group(foods)
        return self.foods


_LEVEL_DATA = sorted(
    [
        _LevelData.model_validate_json(p.read_text(encoding="utf-8"))
        for p in LEVELPATH.iterdir()
        if p.name.endswith(".json")
    ],
    key=lambda x: x.seq,
)
LEVELS = [Level(i) for i in _LEVEL_DATA]
