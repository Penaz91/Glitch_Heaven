#!/usr/bin/env python3
import pygame
import os
from deadbody import DeadBody


class Player(pygame.sprite.Sprite):
    size = (32, 32)
    playerspeed = 300

    def __init__(self, location, *groups):
        super(Player, self).__init__(*groups)
        self.image = pygame.image.load(os.path.join("resources",
                                                    "sprites",
                                                    "player.png"))
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        self.rect.x = location[0]
        self.rect.y = location[1]
        self.resting = False
        self.y_speed = 0
        self.jump_speed = -500

    def update(self, dt, game):
        last = self.rect.copy()
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            if key[pygame.K_z]:
                self.rect.x -= self.playerspeed*dt*1.5
            else:
                self.rect.x -= self.playerspeed*dt
        elif key[pygame.K_RIGHT]:
            if key[pygame.K_z]:
                self.rect.x += self.playerspeed*dt*1.5
            else:
                self.rect.x += self.playerspeed*dt
        if game.glitches["multiJump"]:
            if key[pygame.K_UP]:
                if game.glitches["gravity"]:
                    game.gravity *= -1
                else:
                    if game.glitches["highJump"]:
                        if self.y_speed > -(self.jump_speed/2) or self.resting:
                            self.y_speed = self.jump_speed*2*game.gravity
                    else:
                        if self.y_speed > -(self.jump_speed/2) or self.resting:
                            self.y_speed = self.jump_speed*game.gravity
        elif game.glitches["hover"]:
            if key[pygame.K_UP]:
                self.y_speed = self.jump_speed*game.gravity*0.8
        else:
            if key[pygame.K_UP] and self.resting:
                if game.glitches["gravity"]:
                    game.gravity *= -1
                else:
                    if game.glitches["highJump"]:
                        self.y_speed = self.jump_speed*2*game.gravity
                    else:
                        self.y_speed = self.jump_speed*game.gravity
                self.resting = False
        if game.glitches["featherFalling"]:
            if game.gravity == 1:
                self.y_speed = (min(200, self.y_speed+20))
            elif game.gravity == -1:
                self.y_speed = -(min(200, abs(self.y_speed)+20))
            elif game.gravity == 0:
                self.y_speed = 0
        else:
            if game.gravity == 1:
                self.y_speed = (min(400, self.y_speed+40))
            elif game.gravity == -1:
                self.y_speed = (max(-400, self.y_speed-40))
            elif game.gravity == 0:
                self.y_speed = 0
        self.rect.y += self.y_speed*dt
        self.resting = False
        for cell in game.tilemap.layers['Triggers'].collide(self.rect,
                                                            'blocker'):
            blockers = cell['blocker']
            if 'l' in blockers and last.right <= cell.left and\
                    self.rect.right > cell.left:
                self.rect.right = cell.left
                if game.glitches["wallClimb"]:
                    self.y_speed = -200
            if 'r' in blockers and last.left >= cell.right and\
                    self.rect.left < cell.right:
                self.rect.left = cell.right
                if game.glitches["wallClimb"]:
                    self.y_speed = -200
            if 't' in blockers and last.bottom <= cell.top and\
                    self.rect.bottom > cell.top:
                self.rect.bottom = cell.top
                if game.glitches["stickyCeil"]:
                    self.y_speed = 3/dt
                else:
                    self.y_speed = 0
                if game.gravity == 1:
                    self.resting = True
            if 'b' in blockers and last.top >= cell.bottom and\
                    self.rect.top < cell.bottom:
                self.rect.top = cell.bottom
                if game.glitches["stickyCeil"]:
                    self.y_speed = -5/dt
                else:
                    self.y_speed = 0
                if game.gravity == -1:
                    self.resting = True
        for cell in game.tilemap.layers["Triggers"].collide(self.rect,
                                                            'bouncy'):
            bouncy = cell["bouncy"]
            # FIXME: Touching a bouncer that should push you further down/up,
            # makes you go out of bounds
            if 't' in bouncy and last.bottom <= cell.top and\
                    self.rect.bottom > cell.top:
                self.rect.bottom = cell.top
                if game.gravity == 1:
                    self.y_speed = self.jump_speed*game.gravity*2
                elif game.gravity == -1:
                    self.y_speed = self.jump_speed*game.gravity*-2
            if 'b' in bouncy and last.top >= cell.bottom and\
                    self.rect.top < cell.bottom:
                self.rect.top = cell.bottom
                if game.gravity == -1:
                    self.y_speed = self.jump_speed*game.gravity*2
                elif game.gravity == 1:
                    self.y_speed = self.jump_speed*game.gravity*-2
        for cell in game.tilemap.layers["Triggers"].collide(self.rect,
                                                            'deadly'):
            deadly = cell["deadly"]
            if 't' in deadly and last.bottom <= cell.top and\
                    self.rect.bottom > cell.top:
                self.rect.bottom = cell.top
                if game.glitches["permBodies"]:
                    x, y = game.tilemap.pixel_from_screen(self.rect.x,
                                                          self.rect.y)
                    body = DeadBody(x, y, game.sprites, game=game)
                    game.deadbodies.add(body)
                self.kill()
                start_cell = game.tilemap.layers['Triggers']\
                    .find('player')[0]
                game.player = Player((start_cell.px, start_cell.py),
                                     game.sprites)
            if 'b' in deadly and last.top >= cell.bottom and\
                    self.rect.top < cell.bottom:
                self.rect.top = cell.bottom
                if game.glitches["permBodies"]:
                    x, y = game.tilemap.pixel_from_screen(self.rect.x,
                                                          self.rect.y)
                    body = DeadBody(x, y, game.sprites, game=game)
                    game.deadbodies.add(body)
                self.kill()
                start_cell = game.tilemap.layers['Triggers']\
                    .find('player')[0]
                game.player = Player((start_cell.px, start_cell.py),
                                     game.sprites)
                # FIXME: Can cross dead bodies horizontally
        collision = pygame.sprite.spritecollide(self, game.deadbodies, False)
        for block in collision:
            if self.y_speed == 0:
                self.resting = True
            elif self.y_speed > 0:
                self.rect.bottom = block.rect.top
                self.resting = True
                self.y_speed = 0
            elif self.y_speed < 0:
                self.rect.top = block.rect.bottom
                self.resting = False
                self.y_speed = 0
        game.tilemap.set_focus(self.rect.x, self.rect.y)
        game.backpos[0] = -game.tilemap.view_x
