import sys

import pygame

from src.const import *
from src.level import Level, LevelData


pygame.init()
pygame.display.set_icon(pygame.image.load(ICONPATH))
screen = pygame.display.set_mode((606, 636))
pygame.display.set_caption("Pac-Man - DEBUG")
pygame.font.init()
font = pygame.font.Font(FONTPATH, 18)
clock = pygame.time.Clock()

MODE_TEXT = ["NONE", "WALL", "GATE", "FOOD"]
data_fp = LEVELPATH / "dev.json"
data = LevelData.model_validate_json(data_fp.read_text(encoding="utf-8"))
level = Level(data)
level.setup()
prev = pos = (0, 0)
mode = 0
undo = []  # type: list[int]


def reload_level():
    level.setup()
    data_fp.write_text(data.model_dump_json())


def container(id: int):
    match id:
        case 1:
            return data.wall
        case 2:
            return data.gate
        case 3:
            return data.no_food
        case _:
            raise


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                prev = pos
                pos = pygame.mouse.get_pos()
                pos = pos[0] // 30, pos[1] // 30
                if mode:
                    container(mode).append((prev[0], prev[1], pos[0], pos[1]))
                    undo.append(mode)
                    mode = 0
                    reload_level()
            elif event.button == pygame.BUTTON_RIGHT:
                if undo:
                    container(undo.pop()).pop()
                    reload_level()
            elif event.button == pygame.BUTTON_WHEELDOWN:
                mode = (mode + 1) % len(MODE_TEXT)
            elif event.button == pygame.BUTTON_WHEELUP:
                mode = (mode - 1) % len(MODE_TEXT)

    level.draw(screen)
    text = font.render(f"Pos: {pos}", True, GREEN)
    x = 600 - text.get_rect().width
    screen.blit(text, (x, 610))
    text = font.render(MODE_TEXT[mode], True, YELLOW)
    x = x - 10 - text.get_rect().width
    screen.blit(text, (x, 610))
    pygame.display.flip()
    clock.tick(30)
