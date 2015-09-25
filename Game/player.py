#!/usr/bin/env python3
import pygame
class Player(pygame.sprite.Sprite):
    size=(32,32)
    y_speed=100
    resting=False
    playerspeed=300
    def __init__(self,location,*groups):
        super(Player,self).__init__(*groups)
        self.image=pygame.Surface(self.size)
        self.image.fill((255,255,255))
        self.rect=self.image.get_rect()
        self.rect.x=location[0]
        self.rect.y=location[1]
        #self.screen=game.screen
    def update(self,dt,game):
        last=self.rect.copy()
        key=pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.rect.x-=self.playerspeed*dt
        elif key[pygame.K_RIGHT]:
            self.rect.x+=self.playerspeed*dt
        if key[pygame.K_UP] and self.resting:
            self.y_speed=-500
            self.resting=False
        self.y_speed=(min(400,self.y_speed+40))
        self.rect.y+=self.y_speed*dt
        for cell in game.tilemap.layers['Triggers'].collide(self.rect,'blocker'):
            blockers = cell['blocker']
            #TODO: Implement Collisions
            if 't' in blockers:
                pass
            if 'l' in blockers and last.right<=cell.left and self.rect.right>cell.left:
                self.rect.right=cell.left
            if 'r' in blockers and last.left>=cell.right and self.rect.left<cell.right:
                self.rect.left=cell.right
            if 't' in blockers and last.bottom <= cell.top and self.rect.bottom > cell.top:
                self.resting=True
                self.rect.bottom=cell.top
                self.y_speed=0
            if 'b' in blockers and last.top >= cell.bottom and self.rect.top < cell.bottom:
                self.rect.top=cell.bottom
                self.y_speed=0
        # TODO: Implement a scrolling map to verify this
        game.tilemap.set_focus(self.rect.x,self.rect.y)