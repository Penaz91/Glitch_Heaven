# Particle Library
# Part of the Glitch_Heaven Project
# Copyright 2015 Penaz <penaz@altervista.org>
import pygame


class Particle (pygame.sprite.Sprite):
    def __init__(self,x,y,*groups):
        super(Particle,self).__init__(*groups)
        self.age=500
        self.color=(255,255,255)
        self.image=pygame.surface.Surface((3,3))
        self.image.fill(self.color)
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
    def update(self):
        self.age-=1
        if self.age==0:
            self.kill()
            
pygame.init()
screen=pygame.display.set_mode((640,480))
group=pygame.sprite.Group()
while 1:
    for event in pygame.event.get():
        if event.type==pygame.MOUSEMOTION:
            particle = Particle(*(pygame.mouse.get_pos()),group)
    screen.fill((0,0,0))
    group.draw(screen)
    group.update()
    pygame.display.flip()
