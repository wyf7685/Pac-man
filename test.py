import sys

import pygame

from src.const import *
from src.level import LEVELS

pygame.init()
pygame.display.set_icon(pygame.image.load(ICONPATH))
screen = pygame.display.set_mode((606, 636))
pygame.display.set_caption("Pac-Man - DEBUG")
pygame.font.init()
font = pygame.font.Font(FONTPATH, 18)

level = LEVELS[-1]
level.setup()
pos = (0, 0)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            pos = pos[0] // 30, pos[1] // 30

    level.draw(screen)
    text = font.render(f"Pos: {pos}", True, GREEN)
    w = text.get_rect().width
    screen.blit(text, (600 - w, 610))

    pygame.display.flip()
