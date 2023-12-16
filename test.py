import pygame
from pygame.locals import QUIT

screen = pygame.display.set_mode((300, 300))

t = pygame.image.load("tf.png").convert()
t.set_colorkey((0, 0, 0))
t = pygame.mask.from_surface(t)
t.invert()
t = t.to_surface(setcolor=(0, 0, 0), unsetcolor=(255,255, 255, 0))


screen.fill((0, 255, 255))
screen.blit(t, (0, 0))
pygame.display.flip()

run = True
while run:
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

pygame.quit()