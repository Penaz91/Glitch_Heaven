# Triggerable Platform Component
# Part of the Glitch_Heaven Project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>

import pygame
from libs import platgen


class TriggerablePlatform(pygame.sprite.Sprite):
    """
    Represents a mobile platform that can be triggered
    inherits properties from MobilePlatform
    """
    def __init__(self, x, y, vertical, bpwr, spd, size,
                 active, identifier, *groups, game, bouncy=False, image):
        """
        Default Constructor

        Keyword Arguments:
        - x: The x coord of the top left corner
        - y: The y coord of the top left corner
        - *groups: A collection of sprite groups to add the item to.
        - game: The game istance.

        Returns:
        - Nothing
        """
        super(TriggerablePlatform, self).__init__(*groups)
        self.bouncepwr = bpwr
        if bouncy:
            self.activeimg = platgen.generate(size, 32, image)
        else:
            self.activeimg = platgen.generate(size, 0, image)
        self.inactiveimg = platgen.generate(size, 64, image)
        if active:
            self.image = self.activeimg
        else:
            self.image = self.inactiveimg
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.active = active
        self.bouncy = bouncy
        self.id = identifier
        self.vertical = vertical
        self.speed = spd
        if vertical:
            self.xspeed = 0
            self.yspeed = spd
        else:
            self.yspeed = 0
            self.xspeed = spd
        self.direction = 1
        self.moving = False
        game.plats.add(self)

    def update(self, dt, game):
        """
        Update method

        Keyword Arguments:
        - dt: The unit of time (clock.tick/1000.)
        - game: The game istance

        Returns:
        - Nothing
        """
        self.dt = dt
        self.moving = False
        self.last = self.rect.copy()
        if not game.glitches["timeLapse"] or game.player.x_speed != 0:
            if self.active:
                # Moves the platform
                self.rect.y += self.direction * self.yspeed * dt
                self.rect.x += self.direction * self.xspeed * dt
                self.moving = True
                # Reverses the platform when a "PlatReverse" trigger is touched
                # v-----------------------------------------------------------------v
                for cell in game.tilemap.layers['Triggers'].collide(
                        self.rect, 'PlatReverse'):
                    if self.vertical:
                        if self.last.bottom <= cell.top and\
                                self.rect.bottom > cell.top:
                            self.rect.bottom = cell.top
                        elif self.last.top >= cell.bottom and\
                                self.rect.top < cell.bottom:
                            self.rect.top = cell.bottom
                    else:
                        if self.last.left >= cell.right and\
                                self.rect.left < cell.right:
                            self.rect.left = cell.right
                        elif self.last.right <= cell.left and\
                                self.rect.right > cell.left:
                            self.rect.right = cell.left
                    self.direction *= -1
                # ^------------------------------------------------------------------^
