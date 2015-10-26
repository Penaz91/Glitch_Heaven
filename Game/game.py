# Game Component
# Part of the Glitch_Heaven Project
# Copyright 2015 Penaz <penazarea@altervista.org>
import pygame
from components.player import Player
from libs import tmx
import os
import configparser
from components.mobileobstacle import Obstacle
from escmenu import pauseMenu
import shelve


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
        self.obstacles = tmx.SpriteLayer()
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
        for obstacle in self.tilemap.layers['Triggers'].find('Obstacle'):
            obs = obstacle['Obstacle']
            speed = obstacle['ObsSpeed']
            if "v" in obs:
                Obstacle((obstacle.px, obstacle.py), True, speed, None,
                         self.obstacles)
            else:
                Obstacle((obstacle.px, obstacle.py), False, speed, None,
                         self.obstacles)
        self.tilemap.layers.append(self.obstacles)

    def loadNextLevel(self, campaign, screen):
        self.campaignIndex += 1
        print("LoadNextLevel: "+str(campaign))
        print(self.campaignIndex)
        self.LoadLevel(campaign[self.campaignIndex], screen)

    def loadCampaign(self, campaignfile):
        with open(os.path.join("data", "campaigns", campaignfile+".cmp"),
                  "r") as campfile:
            x = campfile.readlines()
            y = []
            for element in x:
                y.append(element.strip())
            return y

    def eraseCurrentLevel(self):
        self.tilemap = None
        self.player.kill()
        self.sprites.empty()
        self.player = None

    def loadLevelPart2(self, keys):
        self.sprites = tmx.SpriteLayer()
        start_cell = self.tilemap.layers['Triggers'].find('playerEntrance')[0]
        self.tilemap.layers.append(self.sprites)
        self.backpos = [0, 0]
        self.middlepos = [0, 0]
        self.player = Player((start_cell.px, start_cell.py),
                             self.sprites, keys=keys)

    def saveGame(self):
        shelf = shelve.open("SaveGame.dat")
        shelf["currentcampaign"] = self.currentcampaign
        shelf["campaignfile"] = self.campaignFile
        shelf["campaignIndex"] = self.campaignIndex - 1
        shelf.close()

    def loadGame(self):
        shelf = shelve.open("SaveGame.dat")
        self.currentcampaign = shelf["currentcampaign"]
        self.campaignFile = shelf["campaignfile"]
        self.campaignIndex = shelf["campaignIndex"]
        shelf.close()
        print("Loadgame: "+str(self.currentcampaign))
        print(self.campaignIndex)

    """ Main method """
    def main(self, screen, keys, mode):
        """Variables"""
        self.running = True
        self.clock = pygame.time.Clock()
        self.screen = screen
        self.keys = keys
        self.helptxts = pygame.sprite.Group()
        if mode.lower() == "load":
            self.loadGame()
            self.loadNextLevel(self.currentcampaign, screen)
        else:
            self.campaignFile = "TestCampaign"
            self.currentcampaign = self.loadCampaign(self.campaignFile)
            self.campaignIndex = -1
            self.loadNextLevel(self.currentcampaign, screen)
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
        self.loadLevelPart2(self.keys)
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
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    pauseMenu().main(screen, keys, self)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    self.saveGame()
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
