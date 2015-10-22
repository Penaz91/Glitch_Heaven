# Particle Library
# Part of the Glitch_Heaven Project
# Copyright 2015 Penaz <penazarea@altervista.org>
import pygame
import random


class Particle (pygame.sprite.Sprite):
    def __init__(self, position, colorstart, colorend,
                 speedx, speedy, *groups):
        super(Particle, self).__init__(*groups)
        self.age = 20
        self.color = colorstart
        self.colorsteps = self.colorfade(self.color, colorend, 20)
        self.image = pygame.surface.Surface((2, 2))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = position[0] + random.randint(-5, 5)
        self.rect.y = position[1] + random.randint(-5, 5)
        self.sx = speedx
        self.sy = speedy

    def update(self):
        self.age -= 1
        if self.age < 100:
            self.red = (self.color[0])+(self.colorsteps[0])
            self.green = (self.color[1])+(self.colorsteps[1])
            self.blue = (self.color[2])+(self.colorsteps[2])
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
            self.color = (self.red, self.green, self.blue)
            self.image.fill(self.color)
        if self.age == 0:
            # Alternative: reset the particle color/position to avoid
            # useless read/write in memory of new object
            self.kill()
        self.rect.x += self.sx
        self.rect.y += self.sy

    def colorfade(self, startcolor, finalcolor, steps):
        stepR = (finalcolor[0]-startcolor[0])/steps
        stepG = (finalcolor[1]-startcolor[1])/steps
        stepB = (finalcolor[2]-startcolor[2])/steps
        return (stepR, stepG, stepB)

"""Test Area
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
