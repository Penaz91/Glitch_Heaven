import pygame
import os
pygame.init()
screen = pygame.display.set_mode((800, 240))
# v-----------------------------------------------------------------v
_normal_ = 0
_bouncy_ = 32
_glitched_ = 64
size = 15
type = _normal_
graphics = pygame.image.load("Plats.png").convert_alpha()
lcorner = (0,type,32,32)
center = (32,type,32,32)
rcorner = (64,type,32,32)
loner = (96,type,32,32)
print("The platform size would be: "+str((32*size,32)))
plat = pygame.surface.Surface((32*size,32))
if size == 1:
    plat.blit(graphics, (0,0), loner)
else:
    centrals = size - 2
    plat.blit(graphics, (0,0), lcorner)
    for i in range(centrals):
        i +=1
        plat.blit(graphics, (32*i,0), center)
    plat.blit(graphics, (32*(size-1), 0), rcorner)
# ^-----------------------------------------------------------------^
clock = pygame.time.Clock()
Truth = True
x = 50
while Truth:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Truth = False
    screen.fill ((0,0,0))
    screen.blit(plat, (x, 120))
    x += 1
    pygame.display.update()
pygame.quit()
quit()
