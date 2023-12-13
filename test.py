import sys

import pygame
import pyperclip

from src.const import *
from src.level import Level, LevelData

MODE_TEXT = ["NONE", "WALL", "GATE", "FOOD"]
MODE_KEYMAP = {pygame.K_0: 0, pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3}

pygame.init()
pygame.display.set_icon(pygame.image.load(ICONPATH))
screen = pygame.display.set_mode((606, 636))
pygame.display.set_caption("Pac-Man - DEBUG")
pygame.font.init()
font = pygame.font.Font(FONTPATH, 18)

data_fp = LEVELPATH / "dev.json"
data = LevelData.model_validate_json(data_fp.read_text(encoding="utf-8"))
level = Level(data)
level.setup()
pos = (0, 0)
mode = 0
undo = []


def reload_level():
    level.setup()
    data_fp.write_text(data.model_dump_json(indent=2))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            prev = pos
            pos = pygame.mouse.get_pos()
            pos = pos[0] // 30, pos[1] // 30
            pyperclip.copy(f"{pos[0]}, {pos[1]}")
            t = (prev[0], prev[1], pos[0], pos[1])
            match mode:
                case 1:
                    data.wall.append(t)
                case 2:
                    data.gate.append(t)
                case 3:
                    data.no_food.append(t)
            if mode:
                undo.append(mode)
                mode = 0
                reload_level()
        elif event.type == pygame.KEYDOWN:
            if event.key in MODE_KEYMAP:
                mode = MODE_KEYMAP[event.key]
            elif event.key == pygame.K_z:
                if not undo:
                    continue
                match undo.pop():
                    case 1:
                        data.wall.pop()
                    case 2:
                        data.gate.pop()
                    case 3:
                        data.no_food.pop()
                reload_level()

    level.draw(screen)
    text = font.render(f"Pos: {pos}", True, GREEN)
    x = 600 - text.get_rect().width
    screen.blit(text, (x, 610))
    text = font.render(MODE_TEXT[mode], True, YELLOW)
    x = x - 10 - text.get_rect().width
    screen.blit(text, (x, 610))

    pygame.display.flip()
