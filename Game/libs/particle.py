# Particle Library
# Part of the Glitch_Heaven Project
# Copyright 2015 Penaz <penaz@altervista.org>
import pygame
import random


class Particle (pygame.sprite.Sprite):
    def __init__(self, position, *groups):
        super(Particle, self).__init__(*groups)
        self.age = 10
        self.color = (255, 0, 0)
        self.colorsteps = self.colorfade(self.color, (0, 255, 0), 10)
        self.image = pygame.surface.Surface((3, 3))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = position[0] + random.randint(-5, 5)
        self.rect.y = position[1] + random.randint(-5, 5)

    def update(self):
        self.age -= 1
        if self.age < 100:
            self.color = (
                (self.color[0])+(self.colorsteps[0]),
                (self.color[1])+(self.colorsteps[1]),
                (self.color[2])+(self.colorsteps[2]))
            self.image.fill(self.color)
        if self.age == 0:
            self.kill()

    def colorfade(self, startcolor, finalcolor, steps):
        stepR = (finalcolor[0]-startcolor[0])/steps
        stepG = (finalcolor[1]-startcolor[1])/steps
        stepB = (finalcolor[2]-startcolor[2])/steps
        return (stepR, stepG, stepB)
pygame.init()
screen = pygame.display.set_mode((640, 480))
group = pygame.sprite.Group()
clock = pygame.time.Clock()
while 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            particle = Particle(pygame.mouse.get_pos(), group)
            particle = Particle(pygame.mouse.get_pos(), group)
            particle = Particle(pygame.mouse.get_pos(), group)
            particle = Particle(pygame.mouse.get_pos(), group)
    screen.fill((0, 0, 0))
    group.draw(screen)
    group.update()
    pygame.display.flip()

"""
Particle class example i found online:


class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, vx, vy, ax, ay, size, colorstructure, *groups):
        pygame.sprite.Sprite.__init__(self, groups)
        self.vx, self.vy, self.ax, self.ay = vx, vy, ax, ay
        self.images = []
        for x in colorstructure:
            start, end, duration = x
            startr, startg, startb = start
            endr, endg, endb = end
            def f(s, e, t):
                return s   int((e - s)*(t/float(duration)))
            for t in range(duration):
                image = pygame.Surface((size, size)).convert()
                image.fill((f(startr, endr, t),
                            f(startg, endg, t),
                            f(startb, endb, t)))
                self.images.append(image)
        self.image = self.images[0]
        self.rect = self.image.get_rect(center = pos)
    def update(self):
        self.rect.move_ip(self.vx, self.vy)
        self.vx = self.vx   self.ax
        self.vy = self.vy   self.ay
        if not self.images:
            self.kill()
        else:
            self.image = self.images.pop(0)
"""
