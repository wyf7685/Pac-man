# Import the required modules.
import sys
import time
from typing import List

import pygame

from src.const import *
from src.level import LEVELS, Level
from src.sprites import Food


def startLevelGame(level: Level, screen: pygame.Surface, font: pygame.font.Font):
    clock = pygame.time.Clock()
    SCORE = 0
    level_name_text = font.render(level.name, True, YELLOW)

    level.setup()
    is_win = False

    start_time = time.time()
    start_ghost = list(level.ghosts)
    heros = list(level.heroes)
    food_eaten = []  # type: List[Food]

    def renderStatusBar():
        nonlocal SCORE

        # Render level name
        rect = screen.blit(level_name_text, (10, 610))

        # Update score and render
        SCORE += len(food_eaten)
        food_eaten.clear()
        score_text = font.render(f"Score: {SCORE}", True, RED)
        screen.blit(score_text, (rect.right + 40, 610))

    while True:
        if time.time() - start_time <= 13:
            idx = min(round((time.time() - start_time) / 3), 3)
            start_ghost[idx].is_move = True

        pygame.key.set_repeat(1, 1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key in list(HERO_KEYMAP):
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

        # Reset screen
        screen.fill(BLACK)

        # Update sprites
        level.heroes.update(level, food_eaten)
        level.foods.update()
        level.ghosts.update(level)

        # Draw all sprites
        level.draw(screen)

        # Check game status
        if len(level.foods) == 0:
            is_win = True
            renderStatusBar()
            break

        # Check if hero crashed into ghosts
        do_break = False
        if collide := pygame.sprite.groupcollide(
            level.heroes, level.ghosts, False, False
        ):
            # collide: Dict[Hero, List[Ghost]]
            for ghosts in collide.values():
                for ghost in ghosts:
                    # If ghost is worried, check is_eaten
                    if ghost.is_worried():
                        # Not eaten yet, eat it
                        if not ghost.is_eaten():
                            ghost.set_eaten(True)
                            SCORE += 10
                    # Otherwise, stop the game
                    else:
                        is_win = False
                        do_break = True
                        break

        renderStatusBar()

        if do_break:
            break

        pygame.display.flip()
        clock.tick(60)

    return is_win


def showText(
    screen: pygame.Surface,
    font: pygame.font.Font,
    is_win: bool,
    is_end: bool = False,
):
    clock = pygame.time.Clock()
    msg = "Congratulations, you won!" if is_win else "Game Over!"
    positions = ((145, 233) if is_win else (235, 233), (65, 303), (170, 333))
    surface = pygame.Surface((400, 200))
    surface.set_alpha(10)
    surface.fill((128, 128, 128))
    screen.blit(surface, (100, 200))
    texts = [
        font.render(msg, True, WHITE),
        font.render("Press ENTER to continue or play again.", True, WHITE),
        font.render("Press ESCAPE to quit.", True, WHITE),
    ]
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
        for text, position in zip(texts, positions):
            screen.blit(text, position)
        pygame.display.flip()
        clock.tick(10)


def main():
    pygame.init()
    pygame.display.set_icon(pygame.image.load(ICONPATH))
    screen = pygame.display.set_mode((606, 636))
    pygame.display.set_caption("Pac-Man")
    pygame.mixer.init()
    pygame.mixer.music.load(BGMPATH)
    pygame.mixer.music.play(-1, 0.0)
    pygame.font.init()
    font_small = pygame.font.Font(FONTPATH, 18)
    font_big = pygame.font.Font(FONTPATH, 24)

    for idx, level in enumerate(LEVELS):
        is_win = startLevelGame(level, screen, font_small)
        showText(screen, font_big, is_win, idx == len(LEVELS) - 1)


if __name__ == "__main__":
    main()
