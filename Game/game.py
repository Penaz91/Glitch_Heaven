#!/usr/bin/env python3
# TODO: Add Copyright Info here
import pygame
from player import Player
from libs import tmx
import os


class Game(object):
    """ Main method """
    def main(self, screen):
        """Variables"""
        self.running = True
        self.clock = pygame.time.Clock()
        self.glitches = {"wallClimb": False,
                         "multiJump": False,
                         "highJump": False,
                         "featherFalling": False,
                         "gravity": False,
                         "hover": False,
                         "stickyCeil": False,
                         "invertedGravity": False,
                         "permBodies": True}
        self.fps = 30
        self.gravity = 1
        self.deadbodies = pygame.sprite.Group()
        if self.glitches["invertedGravity"]:
            self.gravity = -1
        """Program"""
        pygame.init()
        pygame.display.set_caption("Glitch_Heaven")
        bg = pygame.image.load(os.path.join("resources",
                                            "backgrounds",
                                            "Back1.png"))
        middle = pygame.image.load(os.path.join("resources",
                                                "backgrounds",
                                                "Back2.png"))
        middleback = pygame.image.load(os.path.join("resources",
                                                    "backgrounds",
                                                    "Back3.png"))
        self.tilemap = tmx.load('data/maps/TestComplete.tmx',
                                screen.get_size())
        self.sprites = tmx.SpriteLayer()
        start_cell = self.tilemap.layers['Triggers'].find('player')[0]
        self.player = Player((start_cell.px, start_cell.py), self.sprites)
        self.tilemap.layers.append(self.sprites)
        self.backpos = [0, 0]
        self.middlepos = [0, 0]
        print(self.glitches)
        """Game Loop"""
        while self.running:
            dt = self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            screen.blit(bg, (-self.tilemap.viewport.x/6,
                             -self.tilemap.viewport.y/6))
            screen.blit(middleback, (-self.tilemap.viewport.x/4,
                                     -self.tilemap.viewport.y/4))
            self.tilemap.update(dt/1000., self)
            screen.blit(middle, (-self.tilemap.viewport.x/2,
                                 -self.tilemap.viewport.y/2))
            self.tilemap.draw(screen)
            #  self.deadbodies.draw(screen)
            pygame.display.flip()
        pygame.quit()
        quit()
