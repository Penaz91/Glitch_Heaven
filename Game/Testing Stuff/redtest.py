import pygame
import math
import random
from animation import Animation
pygame.init()
size = (1024, 768)
y = - size[1]
secs = 15
screen = pygame.display.set_mode(size)
tileani = Animation()
tileani.loadFromDir("noise")
tilesurf = tileani.next()
redsurf = pygame.surface.Surface(size, pygame.SRCALPHA)
whitesurf = pygame.surface.Surface((200, 200))
whitesurf.fill((255, 255, 255))
linesize = 3
overlay = None
oy=0.
# v-----------------------------------------------------------------v
# ^-----------------------------------------------------------------^
clock = pygame.time.Clock()
Truth = True
time = 0.
x = 50
while Truth:
    dt = clock.tick(30)/1000.
    time += dt
    y = -size[1] + (size[1] * time) / secs
    if y > 0:
        y = - size[1]
        time = 0.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Truth = False
    redsurf.fill((255, 0, 0, 127))
    for y2 in range(0,math.ceil(redsurf.get_rect().height / 240)):
        for x2 in range (0, math.ceil(redsurf.get_rect().width / 320)):
            redsurf.blit(tilesurf, (x2*320, y2*240))
    if not overlay:
        putoverlay = random.randint(0,100)
        if putoverlay <=45:
            overlay = pygame.surface.Surface((int(redsurf.get_rect().width),(random.randint(10,150))),pygame.SRCALPHA)
            overlay.fill(random.choice([(150,150,150,50), (0,0,0,50)]))
    if overlay:
        oy += 1000*dt
        redsurf.blit(overlay, (0,oy))
        if oy > redsurf.get_rect().height:
            oy=-overlay.get_rect().height
            overlay = None
    redsurf.fill((255,255,255,255), pygame.rect.Rect(redsurf.get_rect().left,
                                                     redsurf.get_rect().bottom - linesize,
                                                     redsurf.get_rect().width,
                                                     linesize))
    tilesurf = tileani.next()
    screen.fill((0, 0, 0))
    screen.blit(whitesurf, (100, 100))
    screen.blit(redsurf, (0, y))
    pygame.display.update()
pygame.quit()
quit()
