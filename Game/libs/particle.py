# Particle Library
# Part of the Glitch_Heaven Project
# Copyright 2015 Penaz <penazarea@altervista.org>
import pygame
import random


class Particle (pygame.sprite.Sprite):
    """ A Particle """

    def __init__(self, position, colorstart, colorend, speedx, speedy, *groups):
        """
        Default constructor

        :param position: The initial position of the particle
        :param colorstart: A 3-Tuple (RRR,GGG,BBB) representing the initial color of the particle
        :param colorend: A 3-Tuple (RRR,GGG,BBB) representing the final color just before the particle dies
        :param speedx: The horizontal speed of the particle
        :param speedy: The Vertical speed of the particle
        :param *groups: A self-unpacking collection of the spritegroups where the particle should be added

        :return: Nothing
        """
        super(Particle, self).__init__(*groups)
        self.age = 20
        self.color = colorstart
        self.colorsteps = self.colorfade(self.color, colorend, 20)
        self.image = pygame.surface.Surface((2, 2))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = position[0] + random.randint(-5, 5)       # |
        self.rect.y = position[1] + random.randint(-5, 5)       # | Randomises the starting point in a 10x10 pixel square
        self.sx = speedx
        self.sy = speedy

    def update(self):
        """ Update method, called when the sprites get updated """
        self.age -= 1   # Decreases the age of the particle (where 0 is a dead particle)
        if self.age < 100:                                              # |
            self.red = (self.color[0])+(self.colorsteps[0])             # |
            self.green = (self.color[1])+(self.colorsteps[1])           # |
            self.blue = (self.color[2])+(self.colorsteps[2])            # |
            if self.red < 0:                                            # |
                self.red = 0                                            # |
            elif self.red > 255:                                        # | When the particle starts getting old, we start changing its color
                self.red = 255                                          # | With an upper limitation of 255 and a lower
            if self.green < 0:                                          # | Limitation of 0
                self.green = 0                                          # |
            elif self.green > 255:                                      # |
                self.green = 255                                        # |
            if self.blue < 0:                                           # |
                self.blue = 0                                           # |
            elif self.blue > 255:                                       # |
                self.blue = 255                                         # |
            self.color = (self.red, self.green, self.blue)      # I set the new particle color
            self.image.fill(self.color)                         # I Color the particle surface
        if self.age == 0:
            """Alternative? reset the particle color/position to avoid
               useless read/write in memory of new object """
            self.kill()     # When the particle ends its cycle, i kill it
        self.rect.x += self.sx      # |
        self.rect.y += self.sy      # | Setting the new position of the particle


    def colorfade(self, startcolor, finalcolor, steps):
        """
        Function to calculate the color fading steps
    
        :param startcolor: A 3-Tuple (RRR,GGG,BBB) representing the starting color
        :param finalcolor: A 3-Tuple (RRR,GGG,BBB) representing the final color
        :param steps: An integer, representing the number of steps the fading should take
        """
        stepR = (finalcolor[0]-startcolor[0])/steps
        stepG = (finalcolor[1]-startcolor[1])/steps
        stepB = (finalcolor[2]-startcolor[2])/steps
        return (stepR, stepG, stepB)

# Testing Area, used to test the particle system
"""
pygame.init()
screen = pygame.display.set_mode((640, 480))
group = pygame.sprite.Group()
clock = pygame.time.Clock()
player = pygame.Surface((32, 32))
player.fill((255, 255, 255))
x = 320
y = 240
while 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x -= 5
                Particle((x+32, y+32), (255, 0, 0), (0, 255, 0), 1, -1, group)
                Particle((x+32, y+32), (255, 0, 0), (0, 255, 0), 1, -2, group)
                Particle((x+32, y+32), (255, 0, 0), (0, 255, 0), 2, -1, group)
            if event.key == pygame.K_RIGHT:
                x += 5
                Particle((x, y+32), (255, 0, 0), (0, 255, 0), -1, -1, group)
                Particle((x, y+32), (255, 0, 0), (0, 255, 0), -1, -2, group)
                Particle((x, y+32), (255, 0, 0), (0, 255, 0), -2, -1, group)
    screen.fill((0, 0, 0))
    screen.blit(player, (x, y))
    group.draw(screen)
    group.update()
    pygame.display.flip()
"""
