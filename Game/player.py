#!/usr/bin/env python3
import pygame
class Player(pygame.sprite.Sprite):
    size=(32,32)
    x_speed=0
    y_speed=0
    x=400
    y=300
    resting=False
    def __init__(self,screen):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface(self.size)
        self.image.fill((255,255,255))
        self.rect=self.image.get_rect()
        self.screen=screen
    def update(self,dt):
        self.x+=self.x_speed*dt/1000.
        self.y+=self.y_speed*dt/1000.
        self.screen.blit(self.image,(self.x,self.y))
