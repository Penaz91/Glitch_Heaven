# Particle Library
# Part of the Glitch_Heaven Project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
import pygame
import random


class Particle (pygame.sprite.Sprite):
    """ A Particle """

    def __init__(self, position, colorstart, colorend,
                 speedx, speedy, tilemap, *groups):
        """
        Default constructor

        Keyword Arguments:
        - position: The initial position of the particle
        - colorstart: A 3-Tuple (RRR,GGG,BBB) representing the initial color
                      of the particle
        - colorend: A 3-Tuple (RRR,GGG,BBB) representing the final color just
                    before the particle dies
        - speedx: The horizontal speed of the particle
        - speedy: The Vertical speed of the particle
        - tilemap: The tilemap the particle reacts to
        - *groups: A collection of the spritegroups to add the particle to

        Returns:
        - Nothing
        """
        super(Particle, self).__init__(*groups)
        self.age = 30
        # self.color = colorstart
        startcolor = pygame.Color(*colorstart)
        endcolor = pygame.Color(*colorend)
        self.color = startcolor
        # self.colorsteps = self.colorfade(self.color, colorend, 30)
        self.colorsteps = (startcolor - endcolor) // pygame.Color(30, 30, 30)
        self.image = pygame.surface.Surface((2, 2))
        self.image.fill(self.color)
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        # Randomises the starting point in a 10x10 pixel square
        # v------------------------------------------------------v
        self.rect.x = position[0] + random.randint(-5, 5)
        self.rect.y = position[1] + random.randint(-5, 5)
        # ^------------------------------------------------------^
        self.sx = speedx
        self.sy = speedy
        self.tilemap = tilemap

    def update(self):
        """ Update method, called when the sprites get updated """
        # Decreases the age of the particle (where 0 is a dead particle)
        last = self.rect.copy()
        self.age -= 1
        # When the particle starts getting old, we start changing
        # color with an upper limitation of 255 and a lower of 0
        if self.age < 100:
            # self.red = min(max((self.color[0])+(self.colorsteps[0]), 0), 255)
            # self.green = min(max((self.color[1])+(self.colorsteps[1]), 0), 255)
            # self.blue = min(max((self.color[2])+(self.colorsteps[2]), 0), 255)
            self.color -= self.colorsteps
            """
            if self.red < 0:
                self.red = 0
            elif self.red > 255:
                self.red = 255
            if self.green < 0:
                self.green = 0
            elif self.green > 255:
                self.green = 255
            if self.blue < 0:
                self.blue = 0
            elif self.blue > 255:
                self.blue = 255
            """
            # Set the new particle color and paint the surface
            # v----------------------------------------------v
            # self.color = (self.red, self.green, self.blue)
            self.image.fill(self.color)
            # ^----------------------------------------------^
        if self.age == 0:
            """Alternative? reset the particle color/position to avoid
               useless read/write in memory of new object """
            self.kill()     # When the particle ends its cycle, i kill it
        self.rect.x += self.sx     # |
        self.rect.y += self.sy     # | Setting the new position of the particle
        for cell in self.tilemap.layers["Triggers"].collide(self.rect,
                                                            'blocker'):
            blockers = cell['blocker']
            if 'l' in blockers and last.right <= cell.left and\
                    self.rect.right > cell.left:
                self.rect.right = cell.left
                self.sx *= -1
            if 'r' in blockers and last.left >= cell.right and\
                    self.rect.left < cell.right:
                self.rect.left = cell.right
                self.sx *= -1
            if 't' in blockers and last.bottom <= cell.top and\
                    self.rect.bottom > cell.top:
                self.rect.bottom = cell.top
                self.sy *= -1
            if 'b' in blockers and last.top >= cell.bottom and\
                    self.rect.top < cell.bottom:
                self.rect.top = cell.bottom
                self.sy *= -1

    """def colorfade(self, startcolor, finalcolor, steps):
        Function to calculate the color fading steps

        Keyword Arguments:
        - startcolor: A 3-Tuple (RRR,GGG,BBB) representing the starting color
        - finalcolor: A 3-Tuple (RRR,GGG,BBB) representing the final color
        - steps: An integer, representing the number of steps the
                 fading should take

        Returns:
        - The color steps to add to the color to complete the fade
        stepR = (finalcolor[0]-startcolor[0])/steps
        stepG = (finalcolor[1]-startcolor[1])/steps
        stepB = (finalcolor[2]-startcolor[2])/steps
        return (stepR, stepG, stepB)
        """
