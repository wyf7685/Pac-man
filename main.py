# Import the required modules.
import sys
import time
from typing import List

import pygame

from src.const import *
from src.levels import LEVELS, Level
from src.sprites import Food


def startLevelGame(level: Level, screen: pygame.Surface, font: pygame.font.Font):
    clock = pygame.time.Clock()
    SCORE = 0
    level_name_text = font.render(level.info, True, YELLOW)

    wall_sprites = level.setupWalls(SKYBLUE)
    gate_sprites = level.setupGate(WHITE)
    hero_sprites, ghost_sprites = level.setupPlayers()
    food_sprites = level.setupFood(YELLOW, WHITE)
    is_win = False

    start_time = time.time()
    start_ghost = list(ghost_sprites)

    def renderStatusBar():
        nonlocal SCORE

        # Render level name
        screen.blit(level_name_text, (10, 610))

        # Update score and render
        SCORE += len(food_eaten)
        score_text = font.render(f"Score: {SCORE}", True, RED)
        screen.blit(score_text, (level_name_text.get_rect().right + 40, 610))

    while True:
        if time.time() - start_time < 12:
            idx = round((time.time() - start_time) / 3)
            if idx < 4:
                start_ghost[idx].is_move = True

        pygame.key.set_repeat(1, 1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    for hero in hero_sprites:
                        hero.changeSpeed((-1, 0))
                        hero.is_move = True
                elif event.key == pygame.K_RIGHT:
                    for hero in hero_sprites:
                        hero.changeSpeed((1, 0))
                        hero.is_move = True
                elif event.key == pygame.K_UP:
                    for hero in hero_sprites:
                        hero.changeSpeed((0, -1))
                        hero.is_move = True
                elif event.key == pygame.K_DOWN:
                    for hero in hero_sprites:
                        hero.changeSpeed((0, 1))
                        hero.is_move = True

            if event.type == pygame.KEYUP:
                if (
                    (event.key == pygame.K_LEFT)
                    or (event.key == pygame.K_RIGHT)
                    or (event.key == pygame.K_UP)
                    or (event.key == pygame.K_DOWN)
                ):
                    for hero in hero_sprites:
                        hero.is_move = False

        # Reset screen
        screen.fill(BLACK)
        wall_sprites.draw(screen)
        gate_sprites.draw(screen)

        # Validate hero's movement
        for hero in hero_sprites:
            hero.check_collide(wall_sprites, gate_sprites)
        hero_sprites.draw(screen)

        # Check hero's collision with food
        food_eaten = []  # type: List[Food]
        for hero in hero_sprites:
            eaten = hero.check_food(food_sprites)
            food_eaten.extend(eaten)

        # Update food display
        food_sprites.update()
        food_sprites.draw(screen)

        # Update ghosts
        for ghost in ghost_sprites:
            for hero in hero_sprites:
                ghost.update_position(hero, wall_sprites, level.maze)
        ghost_sprites.draw(screen)

        # Check game status
        if len(food_sprites) == 0:
            is_win = True
            renderStatusBar()
            break

        # Check if hero crashed into ghosts
        do_break = False
        if collide := pygame.sprite.groupcollide(
            hero_sprites, ghost_sprites, False, False
        ):
            # collide: Dict[Hero, List[Ghost]]
            for hero, ghosts in collide.items():
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
    is_clearance: bool,
    flag: bool = False,
):
    clock = pygame.time.Clock()
    msg = "Game Over!" if not is_clearance else "Congratulations, you won!"
    positions = (
        [[235, 233], [65, 303], [170, 333]]
        if not is_clearance
        else [[145, 233], [65, 303], [170, 333]]
    )
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
                    if is_clearance and not flag:
                        return
                    else:
                        main(initialize())
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        for text, position in zip(texts, positions):
            screen.blit(text, position)
        pygame.display.flip()
        clock.tick(10)


def initialize():
    pygame.init()
    icon_image = pygame.image.load(ICONPATH)
    pygame.display.set_icon(icon_image)
    screen = pygame.display.set_mode([606, 636])
    pygame.display.set_caption("Pac-Man")
    return screen


def main(screen: pygame.Surface):
    pygame.mixer.init()
    pygame.mixer.music.load(BGMPATH)
    pygame.mixer.music.play(-1, 0.0)
    pygame.font.init()
    font_small = pygame.font.Font(FONTPATH, 18)
    font_big = pygame.font.Font(FONTPATH, 24)

    for idx, Level in enumerate(LEVELS):
        level = Level()
        is_clearance = startLevelGame(level, screen, font_small)
        showText(screen, font_big, is_clearance, idx == len(LEVELS) - 1)


if __name__ == "__main__":
    main(initialize())
