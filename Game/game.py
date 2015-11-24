# Game Component
# Part of the Glitch_Heaven Project
# Copyright 2015 Penaz <penazarea@altervista.org>
#
# ------------------------------------------------
# TODO Area
# - Add a game HUD
# - Add Joypad support
# - Make the program not crash when the end of the campaign is reached.
# - If custom campaign/level support will be added
#   add support for multiple savefiles.
# ------------------------------------------------
import pygame
from components.player import Player
from libs import tmx
import os
import configparser
from components.mobileobstacle import Obstacle
from escmenu import pauseMenu
from components.triggerableplatform import TriggerablePlatform
import shelve


class Game(object):
    """ The Main Game """

    def toggleGlitch(self, glitch):
        """
        Debug method for toggling glitches

        Works only with glitches in the "Glitches" dictionary

        Keyword Arguments:
        - Glitch: String key which identifies the glitch to toggle

        Retuns:
        - Nothing
        """
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
        """
        Getter method for helpflagactive
        MIGHT NEED DEPRECATION

        Returns:
        - self.helpflagActive
        """
        return self.helpflagActive

    def setHelpFlag(self, flag):
        """
        Setter method for helpflagactive
        MIGHT NEED DEPRECATION

        Keyword Arguments:
        - flag: The flag to set
        """
        self.helpflagActive = flag

    def setHelpText(self, txt):
        """
        Setter Method for currenthelp
        MIGHT NEED DEPRECATION

        Keyword Arguments:
        - txt: The text to set
        """
        self.currenthelp = txt

    def getHelpText(self):
        """
        Getter Method for currenthelp
        MIGHT NEED DEPRECATION

        Returns:
        - self.currenthelp
        """
        return self.currenthelp

    def LoadLevel(self, level, screen):
        """
        Method to load the defined level

        Keyword Arguments:
        - level: The level name, without the file extension.
        - screen: The surface to draw the level to

        Returns:
        - Nothing
        """
        # Loads the level configuration and the control keys
        # v--------------------------------------------------------------v
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
        # Will this stop the automatic Garbage collector from working?
        # v--------v
        del self.tempglitches, self.tempkeys, self.tempvalues, self.newvalues
        # ^--------^
        # ^--------------------------------------------------------------^
        # Loads the level map, triggers, obstacles
        # v--------------------------------------------------------------v
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
        if levelconfig["Level_Components"]["overlay"].lower() != "none":
            self.hasOverlay = True
            self.overlay = pygame.image.load(
                           os.path.join("resources",
                                        "overlays",
                                        levelconfig["Level_Components"]
                                        ["overlay"])).convert_alpha()
        else:
            self.hasOverlay = False
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
        for platform in self.tilemap.layers['Triggers'].find('Platform'):
            plat = platform['Platform']
            if "v" in plat:
                TriggerablePlatform(platform.px, platform.py, True, 100,
                                    False, platform['id'], self.plats, game=self)
            else:
                TriggerablePlatform(platform.px, platform.py, False, 100,
                                    False, platform['id'], self.plats, game=self)
        self.tilemap.layers.append(self.plats)
        # ^--------------------------------------------------------------^

    def loadNextLevel(self, campaign, screen):
        """
        Loads the next level in the current campaign

        Keyword Arguments:
        - campaign: The loaded list of levels composing the campaign
        - screen: the surface to draw the level on.

        Returns:
        - Nothing
        """
        # TODO: Make the program not crash when the end of the campaign
        #       is reached.
        self.campaignIndex += 1
        # Debug Area
        # v--------------------------------------------------------------v
        print("LoadNextLevel: "+str(campaign))
        print(self.campaignIndex)
        # ^--------------------------------------------------------------^
        self.LoadLevel(campaign[self.campaignIndex], screen)

    def loadCampaign(self, campaignfile):
        """
        Loads the levels of the campaign defined in the argument

        Keyword Arguments:
        - campaignFile: The file (Without extension) defining the campaign
        """
        with open(os.path.join("data", "campaigns", campaignfile+".cmp"),
                  "r") as campfile:
            x = campfile.readlines()
            y = []
            for element in x:
                y.append(element.strip())   # Strips levelname from "\n" chars
            return y

    def eraseCurrentLevel(self):
        """
        Erases the whole level, tilemap, kills the player and
        prepares for a new load
        """
        self.tilemap = None
        self.player.kill()
        self.plats.empty()
        self.sprites.empty()
        self.player = None

    def loadLevelPart2(self, keys):
        """
        Terminates the level loading by defining the sprite layer,
        and spawning the player.
        """
        self.sprites = tmx.SpriteLayer()
        start_cell = self.tilemap.layers['Triggers'].find('playerEntrance')[0]
        self.tilemap.layers.append(self.sprites)
        self.backpos = [0, 0]       # DEPRECATED??
        self.middlepos = [0, 0]     # DEPRECATED??
        self.player = Player((start_cell.px, start_cell.py),
                             self.sprites, keys=keys, game=self)
        self.particlesurf = pygame.surface.Surface((self.tilemap.px_width,
                                                    self.tilemap.px_height),
                                                   pygame.SRCALPHA,
                                                   32).convert_alpha()

    def saveGame(self):
        """
        Saves the game level/campaign in a shelf file.
        """
        # TODO: If custom campaign support will be added
        #       add support for multiple savefiles.
        shelf = shelve.open("SaveGame")
        shelf["currentcampaign"] = self.currentcampaign
        shelf["campaignfile"] = self.campaignFile
        # When loadNextLevel will be called, it will be the right one
        # v--------v
        shelf["campaignIndex"] = self.campaignIndex - 1
        # ^--------^
        shelf.close()

    def loadGame(self):
        """
        Opens the game from a shelf file
        """
        # TODO: If custom campaign support will be added
        #       add support for multiple savefiles.
        shelf = shelve.open("SaveGame")
        self.currentcampaign = shelf["currentcampaign"]
        self.campaignFile = shelf["campaignfile"]
        self.campaignIndex = shelf["campaignIndex"]
        shelf.close()
        # Debug Area
        # v--------------------------------------------------------------v
        print("Loadgame: "+str(self.currentcampaign))
        print(self.campaignIndex)
        # ^--------------------------------------------------------------^

    def main(self, screen, keys, mode, config):
        """
        Main Game method

        Keyword Arguments:
        - Screen: The surface to draw the game to.
        - keys: The control keys to use.
        - Mode: This can be "load" or "newgame", to trigger load mode
                or new game mode

        Returns:
        - Nothing
        """
        self.running = True
        self.clock = pygame.time.Clock()
        self.screen = screen
        self.keys = keys
        self.config = config
        self.helptxts = pygame.sprite.Group()
        self.plats = tmx.SpriteLayer()
        # Defines if a level should be loaded or a
        # new campaign should be started.
        # v--------------------------------------------------------------v
        if mode.lower() == "load":
            self.loadGame()
            self.loadNextLevel(self.currentcampaign, screen)
        else:
            self.campaignFile = "TestCampaign"
            self.currentcampaign = self.loadCampaign(self.campaignFile)
            self.campaignIndex = -1
            self.loadNextLevel(self.currentcampaign, screen)
        # ^--------------------------------------------------------------^
        self.fps = 30
        self.gravity = 1
        self.deadbodies = pygame.sprite.Group()
        # In case the invertedgravity glitch is up, invert gravity
        # v--------v
        if self.glitches["invertedgravity"]:
            self.gravity = -1
        # ^--------^
        pygame.init()
        pygame.display.set_caption("Glitch_Heaven")
        self.loadLevelPart2(self.keys)
        print(self.glitches)
        """Game Loop"""
        while self.running:
            dt = self.clock.tick(self.fps)/1000.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                # Debug Area - Glitch Toggles
                # v----------------------------------------------------------v
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
                    print("Gravity has been inverted")
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
                if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                    self.toggleGlitch("ledgewalk")
                if event.type == pygame.KEYDOWN and event.key == pygame.K_y:
                    self.toggleGlitch("ledge")
                # ^----------------------------------------------------------^
                # Temporary toggles for pause menu and saveGame
                # v----------------------------------------------------------v
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    pauseMenu().main(screen, keys, self)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    self.saveGame()
                # ^----------------------------------------------------------^
            screen.blit(self.bg, (-self.tilemap.viewport.x/6,
                                  -self.tilemap.viewport.y/6))
            screen.blit(self.middleback, (-self.tilemap.viewport.x/4,
                                          -self.tilemap.viewport.y/4))
            self.tilemap.update(dt, self)
            self.helptxts.update(dt, self)
            screen.blit(self.middle, (-self.tilemap.viewport.x/2,
                                      -self.tilemap.viewport.y/2))
            self.tilemap.draw(screen)
            self.particlesurf.fill((0, 0, 0, 0))
            self.player.particles.update()
            self.player.particles.draw(self.particlesurf)
            screen.blit(self.particlesurf, (-self.tilemap.viewport.x,
                                            -self.tilemap.viewport.y))
            if self.hasOverlay:
                screen.blit(self.overlay, (-self.tilemap.viewport.x*1.5,
                                           -self.tilemap.viewport.y*1.5))
            pygame.display.update()
