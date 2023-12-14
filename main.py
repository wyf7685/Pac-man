import sys
import time

import pygame

from src.const import *
from src.level import LEVELS, Level


def startLevelGame(level: Level, screen: pygame.Surface):
    clock = pygame.time.Clock()
    level.setup()
    heros = list(level.heroes)

    while level.running and not level.finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    level.start += pause(screen)
                elif event.key in HERO1_KEYMAP:
                    heros[0].changeSpeed(HERO1_KEYMAP[event.key])
                    heros[0].is_move = True
                elif len(heros) > 1 and event.key in HERO2_KEYMAP:
                    heros[1].changeSpeed(HERO2_KEYMAP[event.key])
                    heros[1].is_move = True

            elif event.type == pygame.KEYUP:
                if event.key in HERO1_KEYMAP:
                    heros[0].is_move = False
                elif len(heros) > 1 and event.key in HERO2_KEYMAP:
                    heros[1].is_move = False

        level.update(screen)
        pygame.display.flip()
        clock.tick(60)


def pause(screen: pygame.Surface) -> float:
    centerx = screen.get_rect().centerx
    for t, y, size in zip(
        ["PAUSED", "Press ENTER to continue."],
        [253, 303],
        [30, 24],
    ):
        text = pygame.font.Font(FONTPATH, size).render(t, True, RED)
        x = centerx - text.get_rect().width // 2
        screen.blit(text, (x, y))
    pygame.display.flip()

    start = time.time()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return time.time() - start


def showText(screen: pygame.Surface, is_win: bool, is_end: bool) -> None:
    font = pygame.font.Font(FONTPATH, 24)
    centerx = screen.get_rect().centerx

    texts = [
        "Congratulations, you won!" if is_win else "Game Over!",
        "Press ENTER to continue or play again.",
        "Press ESCAPE to quit.",
    ]
    for t, y in zip(texts, [233, 303, 333]):
        text = font.render(t, True, WHITE)
        x = centerx - text.get_rect().width // 2
        screen.blit(text, (x, y))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if is_win and not is_end:
                        return
                    else:
                        main()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


def main() -> None:
    pygame.init()
    pygame.display.set_icon(pygame.image.load(ICONPATH))
    screen = pygame.display.set_mode((606, 636))
    pygame.display.set_caption("Pac-Man")
    pygame.mixer.init()
    pygame.mixer.music.load(BGMPATH)
    pygame.mixer.music.play(-1, 0.0)
    pygame.font.init()
    pygame.key.set_repeat(1, 1)

    for idx, level in enumerate(LEVELS):
        startLevelGame(level, screen)
        showText(screen, level.finished, idx == len(LEVELS) - 1)


if __name__ == "__main__":
    main()
