import sys
import time

import pygame

from src.const import *
from src.level import LEVELS, Level


def startLevelGame(level: Level, screen: pygame.Surface):
    clock = pygame.time.Clock()
    level.setup()
    running = True

    start_time = time.time()
    start_ghost = list(level.ghosts)
    heros = list(level.heroes)

    while running:
        if time.time() - start_time <= 13:
            idx = min(round((time.time() - start_time) / 3), 3)
            start_ghost[idx].is_move = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_time = time.time()
                    pause(screen)
                    start_time += time.time() - pause_time
                elif event.key in list(HERO_KEYMAP):
                    heros[0].changeSpeed(HERO_KEYMAP[event.key])
                    heros[0].is_move = True
                elif len(heros) > 1 and event.key in HERO2_KEYMAP:
                    heros[1].changeSpeed(HERO2_KEYMAP[event.key])
                    heros[1].is_move = True

            elif event.type == pygame.KEYUP:
                if event.key in list(HERO_KEYMAP):
                    heros[0].is_move = False
                elif len(heros) > 1 and event.key in HERO2_KEYMAP:
                    heros[1].is_move = False

        # Update
        level.update(screen)

        # Check game status
        if level.finished:
            break

        # Check if hero crashed into ghosts
        if collide := pygame.sprite.groupcollide(
            level.heroes, level.ghosts, False, False
        ):
            for ghosts in collide.values():
                for ghost in ghosts:
                    if ghost.is_worried():
                        # If ghost is worried, check is_eaten
                        if not ghost.is_eaten():
                            # Not eaten yet, eat it
                            ghost.set_eaten(True)
                            level.score += 10
                    # Otherwise, stop the game
                    else:
                        running = False

        pygame.display.flip()
        clock.tick(60)

    return level.finished


def pause(screen: pygame.Surface):
    texts = [
        pygame.font.Font(FONTPATH, 30).render("PAUSED", True, RED),
        pygame.font.Font(FONTPATH, 24).render("Press ENTER to continue.", True, RED),
    ]
    center = screen.get_rect().center[0]
    positions = [
        (center - texts[0].get_rect().width // 2, 253),
        (center - texts[1].get_rect().width // 2, 303),
    ]

    for text, position in zip(texts, positions):
        screen.blit(text, position)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return


def showText(screen: pygame.Surface, is_win: bool, is_end: bool):
    font = pygame.font.Font(FONTPATH, 24)
    msg = "Congratulations, you won!" if is_win else "Game Over!"
    positions = [(145, 233) if is_win else (235, 233), (65, 303), (170, 333)]
    surface = pygame.Surface((400, 200))
    surface.set_alpha(10)
    surface.fill(Color(128, 128, 128))
    screen.blit(surface, (100, 200))
    texts = [
        font.render(msg, True, WHITE),
        font.render("Press ENTER to continue or play again.", True, WHITE),
        font.render("Press ESCAPE to quit.", True, WHITE),
    ]

    for text, position in zip(texts, positions):
        screen.blit(text, position)
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


def main():
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
        is_win = startLevelGame(level, screen)
        showText(screen, is_win, idx == len(LEVELS) - 1)


if __name__ == "__main__":
    main()
