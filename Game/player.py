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
                        if self.y_speed>-(self.jump_speed/2) or self.resting:
                            self.y_speed=self.jump_speed*2*game.gravity
                    else:
                        if self.y_speed>-(self.jump_speed/2) or self.resting:
                            self.y_speed=self.jump_speed*game.gravity
        elif game.glitches["hover"]:
            if key[pygame.K_UP]:
                self.y_speed=self.jump_speed*game.gravity*0.8
        else:
            if key[pygame.K_UP] and self.resting:
                if game.glitches["gravity"]:
                    game.gravity*=-1
                else:
                    if game.glitches["highJump"]:
                        self.y_speed=self.jump_speed*2*grame.gravity
                    else:
                        self.y_speed=self.jump_speed*game.gravity
                self.resting=False
        if game.glitches["featherFalling"]:
            if game.gravity==1:
                self.y_speed=(min(200,self.y_speed+20))
            elif game.gravity==-1:
                self.y_speed=-(min(200,abs(self.y_speed)+20))
            elif game.gravity==0:
                self.y_speed=0
        else:
            if game.gravity==1:
                self.y_speed=(min(400,self.y_speed+40))
            elif game.gravity==-1:
                self.y_speed=(max(-400,self.y_speed-40))
            elif game.gravity==0:
                self.y_speed=0
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
                self.rect.bottom=cell.top
                self.y_speed=0
                if game.gravity==1:
                    self.resting=True
            if 'b' in blockers and last.top >= cell.bottom and self.rect.top < cell.bottom:
                self.rect.top=cell.bottom
                if game.glitches["stickyCeil"]:
                    self.y_speed=-2/dt
                else:
                    self.y_speed=0
                if game.gravity==-1:
                    self.resting=True
        game.tilemap.set_focus(self.rect.x,self.rect.y)
        game.backpos[0]=-game.tilemap.view_x