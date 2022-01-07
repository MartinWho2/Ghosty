import time
import pygame
pygame.init()
w, h = 576, 576
window = pygame.display.set_mode((w, h), pygame.SRCALPHA)
clock = pygame.time.Clock()

# measure the smallest time delta by spinning until the time changes
def main():
    times = []
    for i in range(100):
        t0 = pygame.time.get_ticks()
        print(t0)
        t1 = pygame.time.get_ticks()
        while t1 == t0:
            t1 = pygame.time.get_ticks()
        times.append(t1 - t0)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit(main)
    return times

times = main()
for s in times:
    print(f'time delta: {s} seconds')