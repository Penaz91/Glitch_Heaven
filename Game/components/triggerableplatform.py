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
                 active, id, *groups, game, bouncy=False, image):
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
        # self.activeimg = pygame.image.load(os.path.join("resources",
        # "tiles",
        # "platx3.png"))
        self.inactiveimg = platgen.generate(size, 64, image)
        # self.inactiveimg = pygame.image.load(os.path.join(
        # "resources",
        # "tiles",
        # "platx3_glitched.png"))
        if active:
            self.image = self.activeimg
        else:
            self.image = self.inactiveimg
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.active = active
        self.bouncy = bouncy
        self.id = id
        self.vertical = vertical
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
        if not game.glitches["timeLapse"] or game.player.x_speed != 0:
            if self.active:
                self.last = self.rect.copy()
                # Moves the platform
                self.rect.x += self.direction * self.xspeed * dt
                self.rect.y += self.direction * self.yspeed * dt
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
