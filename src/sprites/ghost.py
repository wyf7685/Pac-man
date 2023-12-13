import math
import random
import time
from typing import TYPE_CHECKING, List, Optional, Set, Tuple
from typing_extensions import override

import pygame
from pygame import Rect, Surface
from pygame.sprite import Group, Sprite

from src.const import *
from src.maze import Maze, MazePath, get_path

if TYPE_CHECKING:
    from .wall import Wall
    from src.level import Level

from .hero import Hero

CORNER_POS: Set[Position] = {
    (x * 30, y * 30) for x, y in {(1, 1), (1, 19), (19, 1), (19, 19)}
}


def distance(pos1: Position, pos2: Position):
    return math.sqrt(math.pow(pos1[0] - pos2[0], 2) + math.pow(pos1[1] - pos2[1], 2))


def direction_preset(this: Rect, wall: Rect):
    return [
        # 1
        (distance(this.topleft, wall.topright), (0.5, -0.5), (0.5, 0.5)),
        (distance(this.topright, wall.topleft), (-0.5, -0.5), (-0.5, 0.5)),
        (distance(this.bottomleft, wall.bottomright), (0.5, 0.5), (0.5, -0.5)),
        (distance(this.bottomright, wall.bottomleft), (-0.5, 0.5), (-0.5, -0.5)),
        # 2
        (distance(this.topleft, wall.bottomright), (0.5, 0.5), (0.5, 0.0)),
        (distance(this.topright, wall.bottomleft), (-0.5, 0.5), (-0.5, 0.0)),
        (distance(this.bottomleft, wall.topright), (0.5, -0.5), (0.5, 0.0)),
        (distance(this.bottomright, wall.topleft), (-0.5, -0.5), (-0.5, 0.0)),
        # 3
        (distance(this.topleft, wall.bottomleft), (-0.5, 0.5), (0.0, 0.5)),
        (distance(this.topright, wall.bottomright), (0.5, 0.5), (0.0, 0.5)),
        (distance(this.bottomleft, wall.topleft), (-0.5, -0.5), (0.0, -0.5)),
        (distance(this.bottomright, wall.topright), (0.5, -0.5), (0.0, -0.5)),
    ]


class Ghost(Sprite):
    """Ghost"""

    role_name: str
    base_image: Surface
    image: Surface
    rect: Rect
    prev: Position
    basic_speed: Tuple[float, float]
    speed: Tuple[int, int]
    is_move: bool

    destination: Tuple[int, int]
    route: MazePath
    __route_update: float
    """Update time when searching the path"""
    __route_update_interval: float = 1.0
    """Update interval of the searching the path"""

    __worried: bool = False
    """Mark as alarmed state."""
    __worry_time: float
    __image_path: str
    """Image path."""

    __eaten: bool = False
    """Mark as eaten state."""
    __start_pos: Tuple[int, int]
    """Birthplace coordinates."""

    __direction_update: float
    __last_direction: Direction

    @classmethod
    def create(cls, x: int, y: int, image_path: str):
        self = cls()
        self.role_name = image_path.split("/")[-1].split(".")[0]
        self.base_image = IMAGES[image_path].copy()
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = x * 30 + 3, y * 30 + 3
        self.prev = self.rect.center
        self.basic_speed = (3.5, 3.5)
        self.speed = (0, 0)
        self.is_move = False

        self.destination = self.rect.center
        self.route = []
        self.__route_update = 0.0

        self.__image_path = image_path
        self.__start_pos = (x, y)
        self.__worry_time = -1
        self.set_worried(False)
        self.set_eaten(False)

        self.__direction_update = 0.0
        self.__last_direction = (0.0, 0.0)

        return self

    def changeSpeed(self, direction: Direction):
        """Change Direction"""
        if not self.is_move:
            return

        if direction[0] < 0:
            self.image = pygame.transform.flip(self.base_image, True, False)
        elif direction[0] > 0:
            self.image = self.base_image.copy()
        elif direction[1] < 0:
            self.image = pygame.transform.rotate(self.base_image, 90)
        elif direction[1] > 0:
            self.image = pygame.transform.rotate(self.base_image, -90)
        self.speed = (
            round(direction[0] * self.basic_speed[0]),
            round(direction[1] * self.basic_speed[1]),
        )
        return self.speed

    def randomDirection(self) -> Direction:
        """Random Direction"""
        return random.choice([(-0.5, 0), (0.5, 0), (0, 0.5), (0, -0.5)])

    def check_collide(
        self,
        wall_sprites: "Group[Wall]",
        gate_sprites: Optional["Group[Wall]"],
    ) -> tuple[bool, List["Wall"]]:
        self.prev = self.rect.center
        self.rect.centerx += self.speed[0]
        self.rect.centery += self.speed[1]
        collide = pygame.sprite.spritecollide(self, wall_sprites, False)

        if gate_sprites is not None and not collide:
            collide = pygame.sprite.spritecollide(self, gate_sprites, False)

        if collide:
            self.rect.center = self.prev
            return False, collide

        return True, collide

    def update_destination(
        self,
        maze: Maze,
        destination: Tuple[int, int],
        *,
        instant: bool = False,
        inplace: bool = True
    ):
        now = time.time()
        dest = self.destination
        route = self.route
        if now - self.__route_update >= self.__route_update_interval or instant:
            dest = destination
            route = get_path(maze, self.rect.center, destination)
            if inplace:
                self.__route_update = now
                self.destination = dest
                self.route = route

        return dest, route

    def next_direction(self, level: "Level") -> Direction:
        self.set_worried(Hero.super_food is not None)
        self.__worry_time = (
            Hero.super_food - time.time() if Hero.super_food is not None else 0.0
        )

        # Return to the birthplace coordinates after being eaten.
        if self.is_eaten():
            self.update_destination(level.maze, self.__start_pos)
        # Escape from the player when in an alarmed state.
        # TODO: Optimize the escape algorithm.
        elif self.is_worried():
            arr = []
            for hero in level.heroes:
                arr.extend((distance(hero.rect.center, i), i) for i in CORNER_POS)
            arr.sort(key=lambda x: x[0], reverse=True)
            self.update_destination(level.maze, arr[0][1])
        # Chase the player without any special conditions.
        # TODO: Execute different pursuit strategies based on the role_name.
        else:
            arr = []
            for hero in level.heroes:
                dest, path = self.update_destination(
                    level.maze,
                    hero.rect.center,
                    instant=True,
                    inplace=False,
                )
                arr.append((len(path), dest))
            arr.sort()
            self.update_destination(level.maze, arr[0][1])

        # Find the next target point in the path.
        x, y = [i // 30 for i in self.rect.center]
        for i in range(len(self.route)):
            pos = self.route[i]
            if pos.x == x and pos.y == y:
                self.route = self.route[i:]
                break
        else:
            return self.randomDirection()

        if len(self.route) == 1:
            return self.randomDirection()

        n = self.route[1]
        return ((n.x - pos.x) / 2, (n.y - pos.y) / 2)

    @override
    def update(self, level: "Level", *args, **kwargs) -> None:
        if time.time() - self.__direction_update < 0.2:
            direction = self.__last_direction
        else:
            direction = self.next_direction(level)
            self.__direction_update = time.time()

        preset = 0

        while True:
            self.changeSpeed(direction)  # type: ignore
            success, collide = self.check_collide(level.walls, None)
            if success:
                self.__last_direction = direction  # type: ignore
                return

            arr: List[Tuple[float, Direction, Direction]] = []

            for wall in collide:
                arr.extend(direction_preset(self.rect, wall.rect))
            arr.sort(key=lambda x: x[0])
            direction = arr[0][1 + preset]
            preset = (preset + 1) % 2

    def set_worried(self, worried: bool) -> None:
        self.__worried = worried

        if not self.__worried:
            self.set_eaten(False)

        self.update_image()

    def is_worried(self) -> bool:
        return self.__worried

    def set_eaten(self, eaten: bool = True) -> None:
        self.__eaten = eaten

        self.update_image()

    def is_eaten(self) -> bool:
        return self.__eaten

    def update_image(self) -> None:
        img = self.__image_path
        if round(min(self.__worry_time, 3.0) * 10 // 4) % 2:
            if self.is_eaten():
                img = EatenPATH
            elif self.is_worried():
                img = GreyPATH

        self.base_image = IMAGES[img].copy()
