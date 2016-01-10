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
from components.collectibletrigger import CollectibleTrigger
import pickle
import logging
from logging import handlers as loghandler
from os.path import join as pathjoin
from tkinter import filedialog
from tkinter import Tk
mod_logger = logging.getLogger("Glitch_Heaven.Game")
fh = loghandler.TimedRotatingFileHandler(pathjoin("logs", "Game.log"),
                                         "midnight", 1)
ch = logging.StreamHandler()
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
        if glitch.lower() == "invertedgravity":
            self.gravity *= -1
            mod_logger.debug("Gravity has been inverted")
        else:
            truth = self.glitches.get(glitch)
            if truth:
                truth = False
                mod_logger.debug("The {0} glitch has been disabled"
                                 .format(glitch))
            else:
                truth = True
                mod_logger.debug("The {0} glitch has been enabled"
                                 .format(glitch))
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
        for trig in self.tilemap.layers['Triggers'].find('ToggleGlitch'):
            totrigger = trig['ToggleGlitch']
            tr = CollectibleTrigger(trig.px, trig.py, self, totrigger)
            self.GlitchTriggers.add(tr)
        self.tilemap.layers.append(self.GlitchTriggers)
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
        with open(campaignfile,
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
            self.gravity = 1
            self.tilemap = None
            self.player.kill()
            self.plats.empty()
            self.GlitchTriggers.empty()
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
        self.gravity = 1
        # In case the invertedgravity glitch is up, invert gravity
        # v--------v
        if self.glitches["invertedgravity"]:
            self.gravity = -1
        # ^--------^
        mod_logger.info("Loading of the level completed" +
                        " successfully, ready to play")

    def saveGame(self):
        """
        Saves the game level/campaign in a shelf file.
        """
        # TODO: If custom campaign support will be added
        #       add support for multiple savefiles.
        Tk().withdraw()
        formats = [("Glitch_Heaven Savegame", "*.dat")]
        path = filedialog.asksaveasfilename(filetypes=formats,
                                            initialdir="./savegames")
        shelf = {"currentcampaign": self.currentcampaign,
                 "campaignfile": self.campaignFile,
                 "campaignIndex": self.campaignIndex - 1}
        pickle.dump(shelf, open(path, "wb"))
        """with shelve.open(path, 'c') as shelf:
            shelf["currentcampaign"] = self.currentcampaign
            shelf["campaignfile"] = self.campaignFile
            # When loadNextLevel will be called, it will be the right one
            # v--------v
            shelf["campaignIndex"] = self.campaignIndex - 1
            # ^--------^
        """
    def loadGame(self):
        """
        Opens the game from a shelf file
        """
        Tk().withdraw()
        formats = [("Glitch_Heaven Savegame", "*.dat")]
        path = filedialog.askopenfilename(filetypes=formats,
                                          initialdir="./savegames")
        if not path:
            raise FileNotFoundError
        mod_logger.info("Loading Save from: "+path)
        """with shelve.open(path, 'r') as shelf:
        """
        shelf = pickle.load(open(path, "rb"))
        self.currentcampaign = shelf["currentcampaign"]
        self.campaignFile = shelf["campaignfile"]
        self.campaignIndex = shelf["campaignIndex"]
        # Debug Area
        # v--------------------------------------------------------------v
        mod_logger.debug("Loadgame: "+str(self.currentcampaign))
        mod_logger.debug("Campaign Index: "+str(self.campaignIndex))
        # ^--------------------------------------------------------------^

    def main(self, screen, keys, mode, cmp, config):
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
        self.GlitchTriggers = tmx.SpriteLayer()
        # Defines if a level should be loaded or a
        # new campaign should be started.
        # v--------------------------------------------------------------v
        if mode.lower() == "load":
            mod_logger.info("Using Load mode")
            try:
                self.loadGame()
                self.loadNextLevel(self.currentcampaign, screen)
            except FileNotFoundError:
                mod_logger.info("No file provided, loading cancelled")
                self.running = False
        else:
            mod_logger.info("Using New Game mode")
            self.campaignFile = cmp
            self.currentcampaign = self.loadCampaign(self.campaignFile)
            self.campaignIndex = -1
            self.loadNextLevel(self.currentcampaign, screen)
        # ^--------------------------------------------------------------^
        self.fps = 30
        self.deadbodies = pygame.sprite.Group()
        pygame.init()
        pygame.display.set_caption("Glitch_Heaven")
        if self.running:
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
                if config.getboolean("Debug", "debugmode") and\
                        pygame.key.get_pressed()[304]:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:
                            self.toggleGlitch("wallclimb")
                        if event.key == pygame.K_2:
                            self.toggleGlitch("multijump")
                        if event.key == pygame.K_3:
                            self.toggleGlitch("highjump")
                        if event.key == pygame.K_4:
                            self.toggleGlitch("featherfalling")
                        if event.key == pygame.K_5:
                            self.toggleGlitch("gravity")
                        if event.key == pygame.K_6:
                            self.toggleGlitch("hover")
                        if event.key == pygame.K_7:
                            self.toggleGlitch("stickyceil")
                        if event.key == pygame.K_8:
                            self.toggleGlitch("invertedgravity")
                        if event.key == pygame.K_9:
                            self.toggleGlitch("permbodies")
                        if event.key == pygame.K_q:
                            self.toggleGlitch("solidhelp")
                        if event.key == pygame.K_w:
                            self.toggleGlitch("cliponcommand")
                        if event.key == pygame.K_e:
                            self.toggleGlitch("hwrapping")
                        if event.key == pygame.K_r:
                            self.toggleGlitch("vwrapping")
                        if event.key == pygame.K_t:
                            self.toggleGlitch("ledgewalk")
                        if event.key == pygame.K_y:
                            self.toggleGlitch("ledge")
                        if event.key == pygame.K_u:
                            self.toggleGlitch("slideinvert")
                        if event.key == pygame.K_i:
                            self.toggleGlitch("noleft")
                        if event.key == pygame.K_o:
                            self.toggleGlitch("noright")
                        if event.key == pygame.K_p:
                            self.toggleGlitch("nojump")
                        if event.key == pygame.K_a:
                            self.toggleGlitch("stopbounce")
                        if event.key == pygame.K_BACKSPACE:
                            mod_logger.debug("Debug key used,a" +
                                             "Loading next level")
                            self.loadNextLevel(self.currentcampaign,
                                               self.screen)
                            self.loadLevelPart2(self.keys)
                    if config.getboolean("Debug", "keydebug"):
                        mod_logger.debug("A key was pressed: {0}"
                                         .format(pygame.key.name(event.key)))
                # ^----------------------------------------------------------^
                # Temporary toggles for pause menu and saveGame
                # v----------------------------------------------------------v
                if event.type == pygame.KEYDOWN and\
                        event.key == keys["escape"]:
                    pauseMenu().main(screen, keys, self, self.config)
                if event.type == pygame.QUIT:
                    self.running = False
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
