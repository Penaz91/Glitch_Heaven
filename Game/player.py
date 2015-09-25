#!/usr/bin/env python3
import pygame
class Player(pygame.sprite.Sprite):
    size=(32,32)
    x_speed=0
    y_speed=0
    x=400
    y=300
    resting=False
    def __init__(self,game):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface(self.size)
        self.image.fill((255,255,255))
        self.rect=self.image.get_rect()
        self.screen=game.screen
    def update(self,dt):
        self.x+=self.x_speed*dt/1000.
        self.y+=self.y_speed*dt/1000.
        for cell in game.tilemap.layers['Triggers'].collide(self.rect,'blocker'):
            blockers = cell['blocker']
            #TODO: Implement Collisions
            if 't' in blockers:
                pass
        # TODO: Implement a scrolling map to verify this
        game.tilemap.set_focus(self.rect.x,self.rect.y)