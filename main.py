import time

import pygame
import sys
from game import Game

pygame.init()
w, h = 576, 576
window = pygame.display.set_mode((w, h), pygame.SRCALPHA)
clock = pygame.time.Clock()
font = pygame.font.Font("pixel-font.ttf", 15)


def main():
    playing = True
    fps = 60
    game = Game(window)
    before = time.time()
    while playing:
        clock.tick(60)
        ips = str(clock.get_fps())
        text = font.render(ips, False, (0, 0, 0))
        dt = (time.time() - before) * fps
        while dt == 0.0:
            dt = (time.time() - before) * fps
        game.update(dt)
        before = time.time()
        window.blit(text, (0, 0))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                game.keys[e.key] = True
                if e.key == pygame.K_q:
                    # Change Character
                    game.characters_class[game.moving_character].image = game.characters_class[game.moving_character].image_copy
                    game.moving_character = game.characters[-1 * game.characters.index(game.moving_character) + 1]
                    game.player.fantom.speed = pygame.Vector2(0, 0)
                    game.player.image_copy = game.player.image.copy()
                    game.change_character(dt)
                    game.can_push_button = False
                    for button in game.object_sprites:
                        button.change_image(game.moving_character)
                    for door in game.doors_sprites:
                        door.change_image(game.moving_character)
                if e.key == pygame.K_a:
                    if game.moving_character == "fantom" and game.can_push_button:
                        game.can_push_button.activate(game.moving_character)
                elif e.key == pygame.K_SPACE and game.moving_character == "player":
                    # Jump
                    game.player.jump()
            elif e.type == pygame.KEYUP:
                game.keys[e.key] = False
                if e.key == pygame.K_SPACE:
                    if game.player.is_jumping and game.player.speed.y < 0:
                        game.player.speed.y *= 0.5
                elif e.key == pygame.K_w and game.moving_character == "player":
                    game.player.shoot([game.bullets],[game.doors_sprites,game.object_sprites,game.enemies])
            elif e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                playing = False

if __name__ == '__main__':
    main()
