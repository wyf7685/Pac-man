import pathlib as _p
import typing as _t

import pygame
from pygame import Color

type Direction = tuple[float, float]
type Position = tuple[int, int]
type Region = tuple[int, int, int, int]


BLACK = Color(0, 0, 0)
WHITE = Color(255, 255, 255)
BLUE = Color(0, 0, 255)
GREEN = Color(0, 255, 0)
RED = Color(255, 0, 0)
YELLOW = Color(255, 255, 0)
ORANGE = Color(254, 189, 17)
PURPLE = Color(163, 73, 164)
SKYBLUE = Color(0, 191, 255)
PINK = Color(246, 164, 162)

_ASSETS = _p.Path("assets")
_SOUNDS = _ASSETS / "sounds"
_FONT = _ASSETS / "font"
_IMAGES = _ASSETS / "images"
LEVELPATH = _ASSETS / "levels"

BGMPATH = _SOUNDS / "bg.mp3"
FONTPATH = _FONT / "ALGER.TTF"
ICONPATH = _IMAGES / "icon.png"
Hero1Path1 = _IMAGES / "pacman_1_1.png"
Hero1Path2 = _IMAGES / "pacman_1_2.png"
Hero2Path1 = _IMAGES / "pacman_2_1.png"
Hero2Path2 = _IMAGES / "pacman_2_2.png"
BlinkyPath = _IMAGES / "Blinky.png"
ClydePath = _IMAGES / "Clyde.png"
InkyPath = _IMAGES / "Inky.png"
PinkyPath = _IMAGES / "Pinky.png"
GreyPath = _IMAGES / "Grey.png"
EatenPath = _IMAGES / "Eaten.png"


HERO1_KEYMAP: _t.Dict[int, Direction] = {
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0),
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
}
HERO2_KEYMAP: _t.Dict[int, Direction] = {
    pygame.K_a: (-1, 0),
    pygame.K_d: (1, 0),
    pygame.K_w: (0, -1),
    pygame.K_s: (0, 1),
}

HERO_FRAMES: _t.List[_p.Path] = [Hero1Path1, Hero1Path2]
HERO2_FRAMES: _t.List[_p.Path] = [Hero2Path1, Hero2Path2]
GHOST_COLOR: _t.Dict[str, Color] = {
    "Blinky": RED,
    "Clyde": ORANGE,
    "Inky": BLUE,
    "Pinky": PINK,
}

IMAGES: _t.Dict[_p.Path, pygame.Surface] = {}


def load_images():
    """
    从`./assets/`读取图片并写入内存

    避免运行时反复读取
    """
    IMAGES.update(
        {
            p: pygame.image.load(p).convert()
            for p in {
                ICONPATH,
                Hero1Path1,
                Hero1Path2,
                Hero2Path1,
                Hero2Path2,
                BlinkyPath,
                ClydePath,
                InkyPath,
                PinkyPath,
                GreyPath,
                EatenPath,
            }
        }
    )
    for im in IMAGES.values():
        im.set_colorkey(PURPLE)
