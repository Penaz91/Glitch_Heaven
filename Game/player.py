#!/usr/bin/env python3
import pygame
import os
class Player(pygame.sprite.Sprite):
    size=(32,32)

    playerspeed=300
    def __init__(self,location,*groups):
        super(Player,self).__init__(*groups)
        self.image=pygame.image.load(os.path.join("resources","sprites","player.png"))
        self.rect=pygame.rect.Rect(location,self.image.get_size())
        self.rect.x=location[0]
        self.rect.y=location[1]
        self.resting=False
        self.y_speed=0
        self.jump_speed=-500
    def update(self,dt,game):
        last=self.rect.copy()
        key=pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.rect.x-=self.playerspeed*dt
        elif key[pygame.K_RIGHT]:
            self.rect.x+=self.playerspeed*dt
        if game.glitches["multiJump"]:
            if key[pygame.K_UP]:
                if game.glitches["gravity"]:
                    game.gravity*=-1
                else:
                    if game.glitches["highJump"]:
                        self.y_speed=self.jump_speed*2
                    else:
                        self.y_speed=self.jump_speed
        else:
            if key[pygame.K_UP] and self.resting:
                if game.glitches["gravity"]:
                    game.gravity*=-1
                else:
                    if game.glitches["highJump"]:
                        self.y_speed=self.jump_speed*2
                    else:
                        self.y_speed=self.jump_speed
                self.resting=False
        if game.glitches["featherFalling"]:
            self.y_speed=(min(200,abs(self.y_speed)+20))*game.gravity
        else:
            self.y_speed=(min(400,abs(self.y_speed)+40))*game.gravity
        self.rect.y+=self.y_speed*dt
        self.resting=False
        for cell in game.tilemap.layers['Triggers'].collide(self.rect,'blocker'):
            blockers = cell['blocker']
            if 't' in blockers:
                pass
            if 'l' in blockers and last.right<=cell.left and self.rect.right>cell.left:
                self.rect.right=cell.left
                if game.glitches["wallClimb"]:
                    self.y_speed=-200
            if 'r' in blockers and last.left>=cell.right and self.rect.left<cell.right:
                self.rect.left=cell.right
                if game.glitches["wallClimb"]:
                    self.y_speed=-200
            if 't' in blockers and last.bottom <= cell.top and self.rect.bottom > cell.top:
                if game.gravity==1:
                    self.resting=True
                self.rect.bottom=cell.top
                self.y_speed=0
            if 'b' in blockers and last.top >= cell.bottom and self.rect.top < cell.bottom:
                self.rect.top=cell.bottom
                self.y_speed=0
                if game.gravity==-1:
                    self.resting=True
        game.tilemap.set_focus(self.rect.x,self.rect.y)
        game.backpos[0]=-game.tilemap.view_x
