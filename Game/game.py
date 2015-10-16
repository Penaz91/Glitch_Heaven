#!/usr/bin/env python3
# TODO: Add Copyright Info here
import pygame
from components.player import Player
from libs import tmx
import os


class Game(object):
    def toggleGlitch(game, glitch):
        truth = game.glitches.get(glitch)
        if truth:
            truth = False
            print("The {0} glitch has been disabled".format(glitch))
        else:
            truth = True
            print("The {0} glitch has been enabled".format(glitch))
        mydict = {glitch: truth}
        game.glitches.update(mydict)

    def getHelpFlag(self):
        return self.helpflagActive

    def setHelpFlag(self, flag):
        self.helpflagActive = flag
    """ Main method """
    def main(self, screen):
        """Variables"""
        self.running = True
        self.helpflagActive = False
        self.clock = pygame.time.Clock()
        self.glitches = {"wallClimb": False,
                         "multiJump": False,
                         "highJump": False,
                         "featherFalling": False,
                         "gravity": False,
                         "hover": False,
                         "stickyCeil": False,
                         "invertedGravity": False,
                         "permBodies": False}
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
        overlay = pygame.image.load(os.path.join("resources",
                                                 "overlays",
                                                 "overlay1.png"))
        self.tilemap = tmx.load('data/maps/TestComplete.tmx',
                                screen.get_size())
        self.sprites = tmx.SpriteLayer()
        start_cell = self.tilemap.layers['Triggers'].find('playerEntrance')[0]
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
                # Glitch Toggles, for testing
                if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                    self.toggleGlitch("wallClimb")
                if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                    self.toggleGlitch("multiJump")
                if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                    self.toggleGlitch("highJump")
                if event.type == pygame.KEYDOWN and event.key == pygame.K_4:
                    self.toggleGlitch("featherFalling")
                if event.type == pygame.KEYDOWN and event.key == pygame.K_5:
                    self.toggleGlitch("gravity")
                if event.type == pygame.KEYDOWN and event.key == pygame.K_6:
                    self.toggleGlitch("hover")
                if event.type == pygame.KEYDOWN and event.key == pygame.K_7:
                    self.toggleGlitch("stickyCeil")
                if event.type == pygame.KEYDOWN and event.key == pygame.K_8:
                    self.gravity *= -1
                if event.type == pygame.KEYDOWN and event.key == pygame.K_9:
                    self.toggleGlitch("permBodies")
            screen.blit(bg, (-self.tilemap.viewport.x/6,
                             -self.tilemap.viewport.y/6))
            screen.blit(middleback, (-self.tilemap.viewport.x/4,
                                     -self.tilemap.viewport.y/4))
            self.tilemap.update(dt/1000., self)
            screen.blit(middle, (-self.tilemap.viewport.x/2,
                                 -self.tilemap.viewport.y/2))
            self.tilemap.draw(screen)
            screen.blit(overlay, (-self.tilemap.viewport.x*1.5,
                                  -self.tilemap.viewport.y*1.5))
            pygame.display.flip()
        pygame.quit()
        quit()
