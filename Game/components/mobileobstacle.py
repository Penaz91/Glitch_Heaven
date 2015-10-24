# Mobile Obstacle/Enemy Component
# Part of the Glitch_Heaven Project
# Copyright 2015 Penaz <penazarea@altervista.org>
import pygame
import os

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, location, vertical, image, *groups):
        super(Obstacle, self).__init__(*groups)
        self.image = pygame.image.load(os.path.join("resources", "sprites", "player.png"))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = location
        if vertical:
            self.xspeed = 0
            self.yspeed = 50
        else:
            self.yspeed = 0
            self.xspeed = 50
        self.direction = 1
        self.vertical = vertical

    def update(self, dt, game):
        self.rect.x += self.direction * self.xspeed * dt
        self.rect.y += self.direction * self.yspeed * dt
        for cell in game.tilemap.layers['Triggers'].collide(self.rect, 'ObsReverse'):
            if self.vertical:
                if self.direction > 0:
                    self.rect.bottom = cell.top
                else:
                    self.rect.top = cell.bottom
            else:
                if self.direction > 0:
                    self.rect.right = cell.left
                else:
                    self.rect.left = cell.right
            self.direction *= -1
        if self.rect.colliderect(game.player.rect):
            game.player.respawn(game)