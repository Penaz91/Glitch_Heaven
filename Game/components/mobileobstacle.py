# Mobile Obstacle/Enemy Component
# Part of the Glitch_Heaven Project
# Copyright 2015 Penaz <penazarea@altervista.org>
import pygame
from libs import timedanimation


class Obstacle(pygame.sprite.Sprite):
    """ Represents a mobile enemy that kills the player on touch """

    def __init__(self, location, vertical, spd, image, *groups, preloaded_ani):
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
        self.ani = timedanimation.TimedAnimation([0.5, 0.5, 0.5, 0.5,
                                                 0.5, 0.5, 0.5, 0.5,
                                                 0.5, 0.5, 0.5, 0.5,
                                                 0.5, 0.5, 0.5, 0.5,
                                                 0.5, 0.5, 0.5, 0.5])
        self.preloaded_ani = preloaded_ani
        self.ani.loadFromList(preloaded_ani)
        self.image = self.ani.first()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = location
        if vertical:
            self.xspeed = 0
            self.yspeed = spd
        else:
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
        last = self.rect.copy()
        if not game.glitches["timeLapse"] or game.player.x_speed != 0:
            # Moves the obstacle
            self.rect.x += self.direction * self.xspeed * 0.033
            self.rect.y += self.direction * self.yspeed * 0.033
            self.image = self.ani.rand_next(dt)
            # Reverses the obstacle when a "ObsReverse" trigger is touched
            # v-----------------------------------------------------------------v
            for cell in game.tilemap.layers['Triggers'].collide(self.rect,
                                                                'ObsReverse'):
                if self.vertical:
                    if last.bottom <= cell.top and\
                            self.rect.bottom > cell.top:
                        self.rect.bottom = cell.top
                    elif last.top >= cell.bottom and\
                            self.rect.top < cell.bottom:
                        self.rect.top = cell.bottom
                else:
                    if last.left >= cell.right and\
                            self.rect.left < cell.right:
                        self.rect.left = cell.right
                    elif last.right <= cell.left and\
                            self.rect.right > cell.left:
                        self.rect.right = cell.left
                self.direction *= -1
            # ^------------------------------------------------------------------^
