# Mobile Obstacle/Enemy Component
# Part of the Glitch_Heaven Project
# Copyright 2015 Penaz <penazarea@altervista.org>
import pygame
import os
from libs import emitter
from libs import tmx


class Obstacle(pygame.sprite.Sprite):
    """ Represents a mobile enemy that kills the player on touch """

    def __init__(self, location, vertical, spd, image, game, *groups):
        """
        Default constructor

        Keyword Arguments:
        - location: A 2-tuple (x,y) representing the item location
        - vertical: Boolean representing if the item moves vertically
        - spd: The movement speed
        - image: A surface representing the image of the item
        - *groups: A collection of sprite groups to add the item to

        Returns:
        - Nothing
        """
        super(Obstacle, self).__init__(*groups)
        self.image = pygame.image.load(os.path.join("resources",
                                                    "sprites",
                                                    "player.png"))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = location
        self.partlayer = tmx.SpriteLayer()
        self.game = game
        if vertical:
            if game.config.getboolean("Video", "obstacleparticles"):
                self.upperemitter = emitter.Emitter(self.rect.midtop, (255, 0, 0),
                                               (0, 0, 0), 0, 1,
                                               self.partlayer)
                self.loweremitter = emitter.Emitter(self.rect.midbottom, (255, 0, 0),
                                               (0, 0, 0), 0, -1,
                                               self.partlayer)
                game.tilemap.layers.append(self.partlayer)
            self.xspeed = 0
            self.yspeed = spd
        else:
            if game.config.getboolean("Video", "obstacleparticles"):
                self.leftemitter = emitter.Emitter(self.rect.midleft, (255, 0, 0),
                                               (0, 0, 0), -1, 0,
                                               self.partlayer)
                self.rightemitter = emitter.Emitter(self.rect.midright, (255, 0, 0),
                                               (0, 0, 0), 1, 0,
                                               self.partlayer)
                game.tilemap.layers.append(self.partlayer)
            self.yspeed = 0
            self.xspeed = spd
        self.direction = 1
        self.vertical = vertical

    def update(self, dt, game):
        """
        Update method, moves and updates the obstacle status

        Keyword Arguments:
        - dt: The time slice (clock.tick())
        - game: The game instance.
        """
        self.rect.x += self.direction * self.xspeed * dt    # |
        self.rect.y += self.direction * self.yspeed * dt    # | Moves obstacle
        if self.direction > 0 and game.config.getboolean("Video", "obstacleparticles"):
            if self.vertical:
                self.upperemitter.move(self.rect.midtop)
                self.upperemitter.emit(1)
            else:
                self.leftemitter.move(self.rect.midleft)
                self.leftemitter.emit(1)
        if self.direction < 0 and game.config.getboolean("Video", "obstacleparticles"):
            if self.vertical:
                self.loweremitter.move(self.rect.midbottom)
                self.loweremitter.emit(1)
            else:
                self.rightemitter.move(self.rect.midright)
                self.rightemitter.emit(1)
        # Reverses the obstacle when a "ObsReverse" trigger is touched
        # v-----------------------------------------------------------------v
        for cell in game.tilemap.layers['Triggers'].collide(self.rect,
                                                            'ObsReverse'):
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
        # ^------------------------------------------------------------------^
        if self.rect.colliderect(game.player.rect):
            game.player.respawn(game)
