#!/usr/bin/env python3
# TODO: Add Copyright Info here
import pygame
from components.player import Player
from libs import tmx
import os
import configparser


class Game(object):
    def toggleGlitch(self, glitch):
        truth = self.glitches.get(glitch)
        if truth:
            truth = False
            print("The {0} glitch has been disabled".format(glitch))
        else:
            truth = True
            print("The {0} glitch has been enabled".format(glitch))
        mydict = {glitch: truth}
        self.glitches.update(mydict)

    def getHelpFlag(self):
        return self.helpflagActive

    def setHelpFlag(self, flag):
        self.helpflagActive = flag

    def setHelpText(self, txt):
        self.currenthelp = txt

    def getHelpText(self):
        return self.currenthelp

    def LoadLevel(self, level, screen):
        levelconfig = configparser.ConfigParser()
        levelconfig.read(os.path.join("data", "maps", level+".conf"))
        self.helpflagActive = False
        self.currenthelp = ""
        self.screen = screen
        self.tempglitches = dict(levelconfig['Glitches'])
        self.tempkeys = self.tempglitches.keys()
        self.tempvalues = self.tempglitches.values()
        self.newvalues = []
        for value in self.tempvalues:
            if value.lower() in ["true", "1", "on", "yes"]:
                self.newvalues.append(True)
            else:
                self.newvalues.append(False)
        self.glitches = dict(zip(self.tempkeys,
                             self.newvalues))
        del self.tempglitches, self.tempkeys, self.tempvalues, self.newvalues
        self.tilemap = tmx.load(os.path.join("data", "maps", level+".tmx"),
                                screen.get_size())
        self.bg = pygame.image.load(
                  os.path.join("resources",
                               "backgrounds",
                               levelconfig["Level_Components"]
                               ["background"])).convert_alpha()
        self.middleback = pygame.image.load(
                          os.path.join("resources",
                                       "backgrounds",
                                       levelconfig["Level_Components"]
                                       ["middle_back1"])).convert_alpha()
        self.middle = pygame.image.load(
                      os.path.join("resources",
                                   "backgrounds",
                                   levelconfig["Level_Components"]
                                   ["middle_back2"])).convert_alpha()
        self.overlay = pygame.image.load(
                       os.path.join("resources",
                                    "overlays",
                                    levelconfig["Level_Components"]
                                    ["overlay"])).convert_alpha()

    """ Main method """
    def main(self, screen, keys):
        """Variables"""
        self.running = True
        self.clock = pygame.time.Clock()
        self.helptxts = pygame.sprite.Group()
        self.LoadLevel("WrapTest", screen)
        self.fps = 30
        self.gravity = 1
        self.deadbodies = pygame.sprite.Group()
        if self.glitches["invertedgravity"]:
            self.gravity = -1
        """Program"""
        pygame.init()
        pygame.display.set_caption("Glitch_Heaven")
        """self.tilemap = tmx.load('data/maps/TestComplete.tmx',
                                screen.get_size())"""
        self.sprites = tmx.SpriteLayer()
        start_cell = self.tilemap.layers['Triggers'].find('playerEntrance')[0]
        self.tilemap.layers.append(self.sprites)
        self.backpos = [0, 0]
        self.middlepos = [0, 0]
        self.player = Player((start_cell.px, start_cell.py),
                             self.sprites, keys=keys)
        print(self.glitches)
        """Game Loop"""
        while self.running:
            dt = self.clock.tick(self.fps)/1000.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                # Glitch Toggles, for testing
                if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                    self.toggleGlitch("wallclimb")
                if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                    self.toggleGlitch("multijump")
                if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                    self.toggleGlitch("highjump")
                if event.type == pygame.KEYDOWN and event.key == pygame.K_4:
                    self.toggleGlitch("featherfalling")
                if event.type == pygame.KEYDOWN and event.key == pygame.K_5:
                    self.toggleGlitch("gravity")
                if event.type == pygame.KEYDOWN and event.key == pygame.K_6:
                    self.toggleGlitch("hover")
                if event.type == pygame.KEYDOWN and event.key == pygame.K_7:
                    self.toggleGlitch("stickyceil")
                if event.type == pygame.KEYDOWN and event.key == pygame.K_8:
                    self.gravity *= -1
                if event.type == pygame.KEYDOWN and event.key == pygame.K_9:
                    self.toggleGlitch("permbodies")
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    self.toggleGlitch("solidhelp")
                if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                    self.toggleGlitch("cliponcommand")
                if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    self.toggleGlitch("hwrapping")
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.toggleGlitch("vwrapping")
            screen.blit(self.bg, (-self.tilemap.viewport.x/6,
                                  -self.tilemap.viewport.y/6))
            screen.blit(self.middleback, (-self.tilemap.viewport.x/4,
                                          -self.tilemap.viewport.y/4))
            self.tilemap.update(dt, self)
            self.helptxts.update(dt, self)
            screen.blit(self.middle, (-self.tilemap.viewport.x/2,
                                      -self.tilemap.viewport.y/2))
            self.tilemap.draw(screen)
            self.player.particles.update()
            self.player.particles.draw(screen)
            screen.blit(self.overlay, (-self.tilemap.viewport.x*1.5,
                                       -self.tilemap.viewport.y*1.5))
            pygame.display.update()
        pygame.quit()
        quit()
