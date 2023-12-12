import os
import typing as _t
import pathlib as _p
import pygame
from pygame import Color

Direction: _t.TypeAlias = _t.Tuple[float, float]
Position: _t.TypeAlias = _t.Tuple[int, int]

BLACK = Color(0, 0, 0)
WHITE = Color(255, 255, 255)
BLUE = Color(0, 0, 255)
GREEN = Color(0, 255, 0)
RED = Color(255, 0, 0)
YELLOW = Color(255, 255, 0)
PURPLE = Color(255, 0, 255)
SKYBLUE = Color(0, 191, 255)

_cwd = os.getcwd()

BGMPATH = os.path.join(_cwd, "assets/sounds/bg.mp3")
FONTPATH = os.path.join(_cwd, "assets/font/ALGER.TTF")
ICONPATH = os.path.join(_cwd, "assets/images/icon.png")
HEROPATH_1_1 = os.path.join(_cwd, "assets/images/pacman_1_1.png")
HEROPATH_1_2 = os.path.join(_cwd, "assets/images/pacman_1_2.png")
HEROPATH_2_1 = os.path.join(_cwd, "assets/images/pacman_2_1.png")
HEROPATH_2_2 = os.path.join(_cwd, "assets/images/pacman_2_2.png")
BlinkyPATH = os.path.join(_cwd, "assets/images/Blinky.png")
ClydePATH = os.path.join(_cwd, "assets/images/Clyde.png")
InkyPATH = os.path.join(_cwd, "assets/images/Inky.png")
PinkyPATH = os.path.join(_cwd, "assets/images/Pinky.png")
GreyPATH = os.path.join(_cwd, "assets/images/Grey.png")
EatenPATH = os.path.join(_cwd, "assets/images/Eaten.png")

LEVELPATH = _p.Path("assets/levels")

HERO_KEYMAP: _t.Dict[int, Direction] = {
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

HERO_FRAMES: _t.List[str] = [HEROPATH_1_1, HEROPATH_1_2]
HERO2_FRAMES: _t.List[str] = [HEROPATH_2_1, HEROPATH_2_2]

IMAGES: _t.Dict[str, pygame.Surface] = {}


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
                HEROPATH_1_1,
                HEROPATH_1_2,
                HEROPATH_2_1,
                HEROPATH_2_2,
                BlinkyPATH,
                ClydePATH,
                InkyPATH,
                PinkyPATH,
                GreyPATH,
                EatenPATH,
            }
        }
    )
