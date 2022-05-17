import time

import pygame
import sys
from game import Game

pygame.init()
w, h = 576, 576
window = pygame.display.set_mode((0,0), pygame.SRCALPHA)
clock = pygame.time.Clock()
font = pygame.font.Font("media/fonts/pixel-font.ttf", 15)


def display_fps(dt):
    fps_text = font.render(str(round(60 / dt, 3)), False, (0, 0, 0))
    window.blit(fps_text, (0, 0))


def main():
    playing = True
    fps = 60
    game = Game(window)
    before = time.time()
    time.sleep(0.02)
    while playing:
        #clock.tick()
        dt = (time.time() - before) * fps
        while dt == 0:
            print("WTF DUDE")
            dt = (time.time() - before) * fps
        before = time.time()
        dt = round(dt,4)
        # Compensate not to skip too much frames
        if dt > 5:
            dt = 5
            # game.update_pressed_keys()
        if not game.game_not_started:
            if not game.pause_menu:
                game.update(dt)
            else:
                # pause menu
                pass
        else:
            game.menu(dt)

        display_fps(dt)
        pygame.display.flip()
        for e in pygame.event.get():
            if not game.game_not_started and not game.pause_menu:
                if e.type == pygame.KEYDOWN:
                    game.keys[e.key] = True
                    if e.key == pygame.K_q:
                        # Change Character
                        game.characters_class[game.moving_character].image = game.characters_class[
                            game.moving_character].image_copy
                        game.moving_character = game.characters[-1 * game.characters.index(game.moving_character) + 1]
                        game.player.fantom.speed = pygame.Vector2(0, 0)
                        game.player.image_copy = game.player.image.copy()
                        game.change_character(dt)
                        game.buttons_pushable = dict.fromkeys(game.buttons_pushable.keys(), False)
                        for button in game.object_sprites:
                            button.change_image(game.moving_character)
                        for door in game.doors_sprites:
                            door.change_image(game.moving_character)
                        for platform in game.platform_sprites:
                            platform.change_image(game.moving_character)
                    if e.key == pygame.K_w and game.moving_character == "player":
                        # Jump
                        game.player.jump(dt)
                elif e.type == pygame.KEYUP:
                    game.keys[e.key] = False
                    if e.key == pygame.K_w and game.moving_character == "player":
                        if game.player.is_jumping and game.player.speed.y < 0:
                            game.player.speed.y *= 0.5
                    elif e.key == pygame.K_SPACE:
                        if game.moving_character == "player":
                            game.player.shoot([game.bullets], [game.doors_sprites, game.object_sprites, game.enemies])
                            game.shot = 1
                        if game.moving_character == "fantom" and game.can_push_button and \
                                game.buttons_pushable[game.can_push_button]:
                            game.can_push_button.activate(game.moving_character)
                elif e.type == pygame.MOUSEWHEEL:
                    game.zoom_coeff += e.y/5
                    if game.zoom_coeff < 1:
                        game.zoom_coeff = 1
            elif game.game_not_started:
                if e.type == pygame.KEYUP:
                    if e.key == pygame.K_SPACE:
                        game.game_not_started = False
            if e.type == pygame.QUIT:
                pygame.quit()
                playing = False
                sys.exit()


if __name__ == '__main__':
    main()
