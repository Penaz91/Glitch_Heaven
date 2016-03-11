from timedanimation import TimedAnimation
import pygame
import os

pygame.init()
screen = pygame.display.set_mode((640,480))

clock = pygame.time.Clock()
running = True
ani = TimedAnimation([0.2,0.2,0.2,0.2])
ani.loadFromDir(os.path.join("noise2/"))
while running:
    screen.fill((255,0,0))
    dt = clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
    image = ani.next(dt).convert_alpha()
    for y in range(0,480,64):
        for x in range(0,640,64):
            screen.blit(image, (x,y))
    pygame.display.update()
