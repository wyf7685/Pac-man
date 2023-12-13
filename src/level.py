import random
from typing import List, Tuple

import pygame
from pydantic import BaseModel
from pygame.sprite import Group

from src.const import *
from src.maze import generate_maze
from src.sprites import Food, Gate, Ghost, Hero, Wall


class _LevelData_no_food(BaseModel):
    """
    指定禁止生成食物的区域

    以下范围均为闭区间
    """

    row: Tuple[int, int]
    """行范围"""
    col: Tuple[int, int]
    """列范围"""


class _LevelData(BaseModel):
    seq: int
    """关卡序号，即关卡在游戏内出现的顺序"""
    name: str
    """关卡名，显示在游戏界面下方状态栏"""
    hero: List[Position]
    """玩家初始位置，可以是1-2个坐标"""
    blinky: Position
    """Blinky初始位置"""
    clyde: Position
    """Clyde初始位置"""
    inky: Position
    """Inky初始位置"""
    pinky: Position
    """Pinky初始位置"""
    super_food: float
    """能量豆出现概率"""
    no_food: List[_LevelData_no_food]
    """
    禁止生成食物的区域
    
    [{"row": [7, 9], "col": [10, 12]}]
    """
    gate: List[Tuple[int, int, int, int]]
    """
    门坐标

    (x1, y1, x2, y2)
    """
    wall: List[Tuple[int, int, int, int]]
    """
    墙坐标

    (x1, y1, x2, y2)
    """


class Level(object):
    _font: pygame.font.Font
    _data: _LevelData
    name: str
    score: int
    maze: List[List[int]]
    walls: "Group[Wall]"
    gates: "Group[Wall]"
    heroes: "Group[Hero]"
    ghosts: "Group[Ghost]"
    foods: "Group[Food]"

    def __init__(self, data: _LevelData):
        self._data = data
        self.name = self._data.name

    def setup(self, wall_color: Color = SKYBLUE, gate_color: Color = WHITE):
        self.score = 0
        self._font = pygame.font.Font(FONTPATH, 18)
        load_images()
        self.setup_wall(wall_color)
        self.setup_gate(gate_color)
        self.setup_player()
        self.setup_food(YELLOW, WHITE)

    def draw(self, screen: pygame.Surface):
        screen.fill(BLACK)
        self.gates.draw(screen)
        self.walls.draw(screen)
        self.heroes.draw(screen)
        self.foods.draw(screen)
        self.ghosts.draw(screen)

        level_name = self._font.render(self.name, True, YELLOW)
        rect = screen.blit(level_name, (10, 610))
        score = self._font.render(f"Score: {self.score}", True, RED)
        screen.blit(score, (rect.right + 40, 610))

    def update(self, screen: pygame.Surface):
        eaten = []
        self.heroes.update(self, eaten)
        self.score += len(eaten)
        Food.update_size()
        self.foods.update()
        self.ghosts.update(self)
        self.draw(screen)

    @property
    def finished(self):
        return len(self.foods) == 0

    def setup_wall(self, wall_color: Color):
        self.maze = generate_maze(self._data.wall)
        walls = [Wall.create(*wall, wall_color) for wall in self._data.wall]
        self.walls = Group(walls)
        return self.walls

    def setup_gate(self, gate_color: Color):
        gates = [Gate.create(*gate, gate_color) for gate in self._data.gate]
        self.gates = Group(gates)
        return self.gates

    def setup_player(self):
        self.heroes = Group()
        for pos, frames in zip(self._data.hero, [HERO_FRAMES, HERO2_FRAMES]):
            self.heroes.add(Hero.create(*pos, frames))
        self.ghosts = Group(
            Ghost.create(*self._data.blinky, BlinkyPATH),
            Ghost.create(*self._data.clyde, ClydePATH),
            Ghost.create(*self._data.inky, InkyPATH),
            Ghost.create(*self._data.pinky, PinkyPATH),
        )
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

                food = Food.create(col, row, food_color, bg_color)
                if pygame.sprite.spritecollide(food, self.walls, False):
                    continue
                if pygame.sprite.spritecollide(food, self.heroes, False):
                    continue

                foods.append(food)

        for food in random.sample(foods, round(len(foods) * self._data.super_food)):
            food.set_super()

        self.foods = Group(foods)
        return self.foods


LEVELS = [
    Level(data)
    for data in sorted(
        [
            _LevelData.model_validate_json(p.read_text(encoding="utf-8"))
            for p in LEVELPATH.iterdir()
            if p.name.endswith(".json")
        ],
        key=lambda x: x.seq,
    )
]
