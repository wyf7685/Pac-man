import os
import typing as _t

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
SKYBLUE = (0, 191, 255)

_cwd = os.getcwd()

BGMPATH = os.path.join(_cwd, "assets/sounds/bg.mp3")
ICONPATH = os.path.join(_cwd, "assets/images/icon.png")
FONTPATH = os.path.join(_cwd, "assets/font/ALGER.TTF")
HEROPATH = os.path.join(_cwd, "assets/images/pacman.png")
HEROPATH2 = os.path.join(_cwd, "assets/images/pacman2.png")
BlinkyPATH = os.path.join(_cwd, "assets/images/Blinky.png")
ClydePATH = os.path.join(_cwd, "assets/images/Clyde.png")
InkyPATH = os.path.join(_cwd, "assets/images/Inky.png")
PinkyPATH = os.path.join(_cwd, "assets/images/Pinky.png")
GreyPATH = os.path.join(_cwd, "assets/images/Grey.png")
EatenPATH = os.path.join(_cwd, "assets/images/Eaten.png")

Color: _t.TypeAlias = _t.Tuple[int, int, int]
Direction: _t.TypeAlias = _t.Tuple[float, float]
Position: _t.TypeAlias = _t.Tuple[int, int]
