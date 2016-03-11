import pygame
import math
import random
from timedanimation import TimedAnimation
import os
pygame.init()
size = (800, 600)
y = - size[1]
secs = 60
screen = pygame.display.set_mode(size)
ani = TimedAnimation([0.2,0.2,0.2,0.2])
ani.loadFromDir(os.path.join("noise2/"))
tiles = []
redsurf = pygame.surface.Surface(size, pygame.SRCALPHA)
whitesurf = pygame.surface.Surface((200, 200))
whitesurf.fill((255, 255, 255))
linesize = 3
overlay = None
oy = 0.
i=-1
# v-----------------------------------------------------------------v
# ^-----------------------------------------------------------------^
clock = pygame.time.Clock()
Truth = True
time = 0.
tm = 0.
x = 50
while Truth:
    dt = clock.tick(30)/1000.
    time += dt
    tm += dt
    screen.fill((0,0,0))
    redsurf.fill((0,0,0,0))
    yy = -size[1] + (size[1] * time) / secs
    if yy > 0:
        yy = - size[1]
        time = 0.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Truth = False
    image = ani.next(dt).convert_alpha()
    for y in range(0,600,64):
        for x in range(0,800,64):
            redsurf.blit(image, (x,y))
    screen.blit(whitesurf, (100, 100))
    screen.blit(redsurf, (0, yy))
    pygame.display.update()
pygame.quit()
quit()
