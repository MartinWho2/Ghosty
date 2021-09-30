import pygame

from game import Game
print("done from school")
pygame.init()
w, h = 576, 576
window = pygame.display.set_mode((w, h),pygame.SRCALPHA)
clock = pygame.time.Clock()


def main():
    playing = True
    fps = 60
    game = Game(window)
    before = pygame.time.get_ticks()
    while playing:
        clock.tick(60)
        dt = (pygame.time.get_ticks() - before) * fps / 1000
        game.update(dt)
        before = pygame.time.get_ticks()
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                game.keys[e.key] = True
                if e.key == pygame.K_q:
                    game.moving_character = game.characters[-1 * game.characters.index(game.moving_character) + 1]
                    game.player.fantom.speed = pygame.Vector2(0,0)
                    game.player.image_copy = game.player.image.copy()
                    game.change_character(1)
                elif e.key == pygame.K_SPACE and game.moving_character == "player":
                    game.player.jump()
            if e.type == pygame.KEYUP:
                game.keys[e.key] = False
                if e.key == pygame.K_SPACE:
                    if game.player.is_jumping and game.player.speed.y < 0:
                        game.player.speed.y *= 0.5
                if e.key == pygame.K_p:
                    game.player.pos.y, game.player.rect.y = -1000, -1000
            if e.type == pygame.QUIT:
                pygame.quit()
                playing = False


if __name__ == '__main__':
    main()
