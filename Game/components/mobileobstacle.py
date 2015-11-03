# Mobile Obstacle/Enemy Component
# Part of the Glitch_Heaven Project
# Copyright 2015 Penaz <penazarea@altervista.org>
import pygame
import os


class Obstacle(pygame.sprite.Sprite):
    """ Represents a mobile enemy that kills the player on touch """

    def __init__(self, location, vertical, spd, image, *groups):
        """
        Default constructor

        :param location: A 2-tuple (x,y) representing the item location
        :param vertical: Boolean representing if the item moves vertically
        :param spd: The movement speed
        :param image: A surface representing the image of the item
        :param *groups: A collection of sprite groups to add the item to

        :return: Nothing
        """
        super(Obstacle, self).__init__(*groups)
        self.image = pygame.image.load(os.path.join("resources",
                                                    "sprites",
                                                    "player.png"))
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
        
        :param dt: The time slice (clock.tick())
        :param game: The game instance.
        """
        self.rect.x += self.direction * self.xspeed * dt    # |
        self.rect.y += self.direction * self.yspeed * dt    # | Moves the obstacle
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
