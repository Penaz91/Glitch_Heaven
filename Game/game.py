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
import logging
from logging import handlers as loghandler
from os.path import join as pathjoin
mod_logger = logging.getLogger("Glitch_Heaven.Game")
fh = loghandler.TimedRotatingFileHandler(pathjoin("logs", "Game.log"),
                                         "midnight", 1)
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
formatter = logging.Formatter('[%(asctime)s] (%(name)s) -'
                              ' %(levelname)s --- %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
mod_logger.addHandler(fh)
mod_logger.addHandler(ch)


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
            mod_logger.debug("The {0} glitch has been disabled".format(glitch))
        else:
            truth = True
            mod_logger.debug("The {0} glitch has been enabled".format(glitch))
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
        mod_logger.info("LoadLevel Routing is loading: " + level)
        levelconfig = configparser.ConfigParser()
        levelconfig.read(os.path.join("data", "maps", level+".conf"))
        mod_logger.info("Level configuration loaded")
        self.helpflagActive = False
        self.currenthelp = ""
        self.screen = screen
        self.tempglitches = dict(levelconfig['Glitches'])
        self.tempkeys = self.tempglitches.keys()
        self.tempvalues = self.tempglitches.values()
        self.newvalues = []
        mod_logger.debug("Zipping new glitches")
        for value in self.tempvalues:
            if value.lower() in ["true", "1", "on", "yes"]:
                self.newvalues.append(True)
            else:
                self.newvalues.append(False)
        self.glitches = dict(zip(self.tempkeys,
                             self.newvalues))
        mod_logger.debug("Glitches Active: " + str(self.glitches))
        # Will this stop the automatic Garbage collector from working?
        # v--------v
        del self.tempglitches, self.tempkeys, self.tempvalues, self.newvalues
        # ^--------^
        # ^--------------------------------------------------------------^
        # Loads the level map, triggers, obstacles
        # v--------------------------------------------------------------v
        mod_logger.info("Loading Tilemap")
        self.tilemap = tmx.load(os.path.join("data", "maps", level+".tmx"),
                                screen.get_size())
        mod_logger.info("Tilemap Loaded, building map")
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
            """if "v" in plat:
                TriggerablePlatform(platform.px, platform.py, True, 100,
                                    False, platform['id'], self.plats,
                                    game=self)
            else:
                TriggerablePlatform(platform.px, platform.py, False, 100,
                                    False, platform['id'], self.plats,
                                    game=self)"""
            if "v" in plat:
                vertical = True
            else:
                vertical = False
            if "bouncyplat" in platform:
                bouncy = True
            else:
                bouncy = False
            TriggerablePlatform(platform.px, platform.py, vertical,
                                100, False, platform['id'], self.plats,
                                game=self, bouncy=bouncy)
        self.tilemap.layers.append(self.plats)
        mod_logger.info("Map Loaded and built Successfully")
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
        mod_logger.debug("Campaign index: " + str(self.campaignIndex + 1))
        mod_logger.debug("Length of campaign: " + str(len(campaign)))
        self.campaignIndex += 1
        if (self.campaignIndex) >= len(campaign):
            self.running = False
        else:
            # Debug Area
            # v--------------------------------------------------------------v
            mod_logger.debug("Loading Level: "+str(campaign))
            # ^--------------------------------------------------------------^
            self.eraseCurrentLevel()
            self.LoadLevel(campaign[self.campaignIndex], screen)

    def loadCampaign(self, campaignfile):
        """
        Loads the levels of the campaign defined in the argument

        Keyword Arguments:
        - campaignFile: The file (Without extension) defining the campaign
        """
        mod_logger.info("Loading campaign"+campaignfile)
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
        if self.player is not None:
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
        mod_logger.info("Starting loadLevelPart2 Routine")
        self.sprites = tmx.SpriteLayer()
        start_cell = self.tilemap.layers['Triggers'].find('playerEntrance')[0]
        self.tilemap.layers.append(self.sprites)
        self.backpos = [0, 0]       # DEPRECATED??
        self.middlepos = [0, 0]     # DEPRECATED??
        mod_logger.info("Positioning Player")
        self.player = Player((start_cell.px, start_cell.py),
                             self.sprites, keys=keys, game=self)
        mod_logger.info("Creating Particle Surface")
        self.particlesurf = pygame.surface.Surface((self.tilemap.px_width,
                                                    self.tilemap.px_height),
                                                   pygame.SRCALPHA,
                                                   32).convert_alpha()
        mod_logger.info("Loading of the level completed" +
                        " successfully, ready to play")

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
        mod_logger.debug("Loadgame: "+str(self.currentcampaign))
        mod_logger.debug("Campaign Index: "+self.campaignIndex)
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
        mod_logger.info("Entering main game")
        self.running = True
        self.clock = pygame.time.Clock()
        self.screen = screen
        self.player = None
        self.keys = keys
        self.config = config
        self.helptxts = pygame.sprite.Group()
        self.plats = tmx.SpriteLayer()
        # NEIN NEIN NEIN NEIN
        # v--------------------------------------------------------------v
        self.no = pygame.mixer.Sound(os.path.join("resources",
                                                  "sounds",
                                                  "no.wav"))
        # ^--------------------------------------------------------------^
        # Defines if a level should be loaded or a
        # new campaign should be started.
        # v--------------------------------------------------------------v
        if mode.lower() == "load":
            mod_logger.info("Using Load mode")
            self.loadGame()
            self.loadNextLevel(self.currentcampaign, screen)
        else:
            mod_logger.info("Using New Game mode")
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
        mod_logger.debug("Glitches Loaded: "+str(self.glitches))
        """Game Loop"""
        while self.running:
            dt = self.clock.tick(self.fps)/1000.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mod_logger.info("QUIT signal received, quitting")
                    pygame.quit()
                    quit()
                # Debug Area - Glitch Toggles
                # v----------------------------------------------------------v
                if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                    # self.toggleGlitch("wallclimb")
                    self.no.play()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                    self.no.play()
                    # self.toggleGlitch("multijump")
                if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                    self.no.play()
                    #self.toggleGlitch("highjump")
                if event.type == pygame.KEYDOWN and event.key == pygame.K_4:
                    #self.toggleGlitch("featherfalling")
                    self.no.play()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_5:
                    #self.toggleGlitch("gravity")
                    self.no.play()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_6:
                    #self.toggleGlitch("hover")
                    self.no.play()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_7:
                    #self.toggleGlitch("stickyceil")
                    self.no.play()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_8:
                    #self.gravity *= -1
                    #mod_logger.debug("Gravity has been inverted")
                    self.no.play()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_9:
                    #self.toggleGlitch("permbodies")
                    self.no.play()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    #self.toggleGlitch("solidhelp")
                    self.no.play()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                    #self.toggleGlitch("cliponcommand")
                    self.no.play()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    #self.toggleGlitch("hwrapping")
                    self.no.play()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    #self.toggleGlitch("vwrapping")
                    self.no.play()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                    #self.toggleGlitch("ledgewalk")
                    self.no.play()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_y:
                    #self.toggleGlitch("ledge")
                    self.no.play()
                # ^----------------------------------------------------------^
                # Temporary toggles for pause menu and saveGame
                # v----------------------------------------------------------v
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    pauseMenu().main(screen, keys, self, self.config)
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
