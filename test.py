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

level = LEVELS.pop()
level.setup()
level_name_text = font.render(level.name, True, YELLOW)
score_text = font.render("Score: 0", True, RED)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    screen.fill(BLACK)
    level.draw(screen)
    screen.blit(level_name_text, (10, 610))
    screen.blit(score_text, (level_name_text.get_rect().right + 40, 610))
    pygame.display.flip()

