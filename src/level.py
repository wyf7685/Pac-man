import random
import time
from typing import List, Tuple

import pygame
from pydantic import BaseModel, Field
from pygame.sprite import Group

from src.const import *
from src.maze import generate_maze
from src.sprites import Food, Gate, Ghost, Hero, Wall


class LevelData(BaseModel):
    seq: int = Field(default=999)
    """关卡序号，即关卡在游戏内出现的顺序"""
    name: str = Field(default="DEV")
    """关卡名，显示在游戏界面下方状态栏"""
    hero: List[Position] = Field(default_factory=lambda: [(10, 10)].copy())
    """玩家初始位置，可以是1-2个坐标"""
    blinky: Position = Field(default=(10, 11))
    """Blinky初始位置"""
    clyde: Position = Field(default=(10, 12))
    """Clyde初始位置"""
    inky: Position = Field(default=(10, 13))
    """Inky初始位置"""
    pinky: Position = Field(default=(10, 14))
    """Pinky初始位置"""
    super_food: float = Field(default=0.02)
    """能量豆出现概率"""
    no_food: List[Tuple[int, int, int, int]] = Field(default_factory=list)
    """
    禁止生成食物的区域
    
    (x1, y1, x2, y2)
    """
    gate: List[Tuple[int, int, int, int]] = Field(default_factory=list)
    """
    门坐标

    (x1, y1, x2, y2)
    """
    wall: List[Tuple[int, int, int, int]] = Field(
        default_factory=lambda: [
            (0, 0, 0, 20),
            (0, 0, 20, 0),
            (20, 0, 20, 20),
            (0, 20, 20, 20),
        ].copy()
    )
    """
    墙坐标

    (x1, y1, x2, y2)
    """

    def validate_food(self, x: int, y: int) -> bool:
        for x1, y1, x2, y2 in self.no_food:
            x1, x2 = min(x1, x2), max(x1, x2)
            y1, y2 = min(y1, y2), max(y1, y2)
            if x1 <= x <= x2 and y1 <= y <= y2:
                return False
        return True


class Level(object):
    _font: pygame.font.Font
    _data: LevelData

    name: str
    score: int
    running: bool
    start: float

    maze: List[List[int]]
    walls: "Group[Wall]"
    gates: "Group[Wall]"
    heroes: "Group[Hero]"
    ghosts: "Group[Ghost]"
    foods: "Group[Food]"

    def __init__(self, data: LevelData):
        self._data = data
        self.name = self._data.name

    def setup(self, wall_color: Color = SKYBLUE, gate_color: Color = WHITE):
        self._font = pygame.font.Font(FONTPATH, 18)
        self.score = 0
        self.running = True
        load_images()
        self.setup_wall(wall_color)
        self.setup_gate(gate_color)
        self.setup_player()
        self.setup_food(YELLOW, WHITE)
        self.start = time.time()

    def draw(self, screen: pygame.Surface):
        screen.fill(BLACK)
        self.gates.draw(screen)
        self.walls.draw(screen)
        self.foods.draw(screen)
        # for ghost in self.ghosts:
        #     ghost.draw_path().draw(screen)
        self.ghosts.draw(screen)
        self.heroes.draw(screen)

        name = self._font.render(self.name, True, YELLOW)
        x = screen.blit(name, (10, 610)).right
        score = self._font.render(f"Score: {self.score}", True, RED)
        screen.blit(score, (x + 30, 610))

    def update(self, screen: pygame.Surface):
        eaten = []
        self.heroes.update(self, eaten)
        self.score += len(eaten)
        self.foods.update()
        self.ghosts.update(self)
        self.check_hero_collide()
        Food.update_size()
        self.draw(screen)

    def check_hero_collide(self) -> None:
        for hero in self.heroes:
            if ghosts := pygame.sprite.spritecollide(hero, self.ghosts, False):
                for ghost in ghosts:
                    if ghost.is_worried():
                        if not ghost.is_eaten():
                            ghost.set_eaten(True)
                            self.score += 10
                    else:
                        self.running = False

    @property
    def finished(self):
        return len(self.foods) == 0

    def setup_wall(self, wall_color: Color):
        self.maze = generate_maze(self._data.wall)
        walls = [Wall.create(*wall, wall_color) for wall in self._data.wall]
        self.walls = Group(walls)

    def setup_gate(self, gate_color: Color):
        gates = [Gate.create(*gate, gate_color) for gate in self._data.gate]
        self.gates = Group(gates)

    def setup_player(self):
        self.heroes = Group()
        for pos, frames in zip(self._data.hero, [HERO_FRAMES, HERO2_FRAMES]):
            self.heroes.add(Hero.create(*pos, frames))
        if not len(self.heroes):
            raise ValueError(f"{self.name} 关卡中至少需要有 1 个 Hero")

        Ghost.seq = 0
        self.ghosts = Group(
            Ghost.create(*self._data.blinky, BlinkyPath),
            Ghost.create(*self._data.clyde, ClydePath),
            Ghost.create(*self._data.inky, InkyPath),
            Ghost.create(*self._data.pinky, PinkyPath),
        )

    def setup_food(self, food_color: Color, bg_color: Color):
        foods = []  # type: List[Food]

        for col in range(len(self.maze)):
            for row in range(len(self.maze[col])):
                if self.maze[col][row] == 0 or not self._data.validate_food(col, row):
                    continue

                food = Food.create(col, row, food_color, bg_color)
                if pygame.sprite.spritecollide(food, self.walls, False):
                    continue
                if pygame.sprite.spritecollide(food, self.heroes, False):
                    continue

                foods.append(food)

        count = round(len(foods) * self._data.super_food)
        for food in random.sample(foods, count):
            food.set_super()

        self.foods = Group(foods)


LEVELS = [
    Level(data)
    for data in sorted(
        [
            LevelData.model_validate_json(p.read_text(encoding="utf-8"))
            for p in LEVELPATH.iterdir()
            if p.name.endswith(".json")
        ],
        key=lambda x: x.seq,
    )
]
