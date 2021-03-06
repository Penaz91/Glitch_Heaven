import pygame
import math
import random
import numpy
from animation import Animation
pygame.init()
size = (800, 600)
y = - size[1]
secs = 60
screen = pygame.display.set_mode(size)
tileani = Animation()
tileani.loadFromDir("noise")
tiles = []
for x in range(len(tileani.frames)):
    tile = tileani.frames[x]
    y = pygame.surface.Surface(size, pygame.SRCALPHA)
    for y2 in range(0, math.ceil(size[1] / 240)):
        for x2 in range(0, math.ceil(size[0] / 320)):
            y.blit(tile, (x2*320, y2*240))
    tiles.append(y)
realtileani = Animation()
realtileani.loadFromList(tiles)
redsurf = pygame.surface.Surface(size, pygame.SRCALPHA)
whitesurf = pygame.surface.Surface((200, 200))
whitesurf.fill((255, 255, 255))
for x in range(4):
    redsurf.fill((255, 0, 0, 127))
    rs = pygame.surfarray.array3d(redsurf)
    noise_small = numpy.random.random((200, 150)) * 0.2 + 0.4
    noise_big = noise_small.repeat(4, 0).repeat(4, 1)
    rs = (rs.astype(noise_big.dtype) * noise_big[:, :, numpy.newaxis]).astype(rs.dtype)
    redsurf = pygame.surfarray.make_surface(rs).convert_alpha()
    os = pygame.surfarray.pixels_alpha(redsurf)
    os[:] = 127
    del rs
    del os
    tiles[x] = redsurf
linesize = 3
tilesurf = realtileani.next()
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
    y = -size[1] + (size[1] * time) / secs
    rcopy = None
    if y > 0:
        y = - size[1]
        time = 0.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Truth = False
    if tm > 0.2:
        i = (i+1)%4
        todisplay = tiles[i]
        tm = 0.
    """
    if not overlay:
        putoverlay = random.randint(0,100)
        if putoverlay <= 45:
            ospeed = random.randrange(500, 2000, 100)
            overlay = pygame.surface.Surface((int(redsurf.get_rect().width),(random.randint(10,250))),pygame.SRCALPHA)
            overlay.fill(random.choice([(150,150,150,50), (0,0,0,50), (121,121,121,50), (56,56,56,50), (200,200,200,50)]))
    if overlay:
        oy += ospeed*dt
        redsurf.blit(overlay, (0, oy))
        if oy > redsurf.get_rect().height:
            oy=-overlay.get_rect().height
            overlay = None
    """
    #redsurf.blit(tilesurf, (0,0))
    todisplay.fill((255,255,255,255), pygame.rect.Rect(redsurf.get_rect().left,
                                                     redsurf.get_rect().bottom - linesize,
                                                     redsurf.get_rect().width,
                                                     linesize))
    #tilesurf = realtileani.next()
    screen.fill((0, 0, 0))
    screen.blit(whitesurf, (100, 100))
    screen.blit(todisplay, (0, y))
    pygame.display.update()
pygame.quit()
quit()
