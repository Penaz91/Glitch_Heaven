# Game Component
# Part of the Glitch_Heaven Project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
#
# ------------------------------------------------
# TODO Area
# - Add a game HUD
# ------------------------------------------------
import pygame
from operator import __mul__, __floordiv__
from components.player import Player
from datetime import timedelta
from libs import tmx
from os.path import join as pjoin
from os.path import splitext, basename
from components.mobileobstacle import Obstacle
from escmenu import pauseMenu
from components.UI.comicreader import comicReader
from components.triggerableplatform import TriggerablePlatform
from components.collectibletrigger import CollectibleTrigger
import json
from random import randint, choice
from os.path import join as pathjoin
from libs.textglitcher import makeGlitched, makeMoreGlitched
from libs.debugconstants import _debugkeys_
_garbletimer_ = 0.1


class Game(object):

    def customGlitchToggle(self, glitchname, trueFunction, falseFunction):
        """
        Toggles glitches via a custom function by checking the
        self.glitches list

        Keyword Parameters:
        - glitchname: Name of the glitch to toggle
        - trueFunction: Function to be executed when enabling
                        the glitch
        - falseFunction: Function to be executed when disabling
                         the glitch
        """
        if self.glitches[glitchname]:
            trueFunction()
        else:
            falseFunction()

    def changeGravity(self):
        """Inverts gravity"""
        self.gravity *= -1

    def toggleGlitch(self, glitch, garble):
        """
        Debug method for toggling glitches

        Works only with glitches in the "Glitches" dictionary

        Keyword Arguments:
        - Glitch: String key which identifies the glitch to toggle
        - Garble: Allows to enable a "static" effect on toggle
        """
        # Inverts the status of the glitch
        # v--------------------------------------------------v
        self.glitches[glitch] = not self.glitches[glitch]
        self.mod_logger.debug("{0} Glitch has been set to {1}".format(
            glitch,
            self.glitches[glitch]))
        # ^--------------------------------------------------^
        # Does a custom toggle of Highjump, speed, and inverted gravity glitch
        # v--------------------------------------------------v
        pl = self.player
        self.customGlitchToggle("highJump", pl.HiJumpOn, pl.HiJumpOff)
        self.customGlitchToggle("speed", pl.DoubleSpeedOn, pl.DoubleSpeedOff)
        self.customGlitchToggle("featherFalling", pl.FeatherFallOn,
                                pl.FeatherFallOff)
        self.customGlitchToggle("highAccel", pl.HighAccel, pl.ResetAccel)
        self.customGlitchToggle("lowAccel", pl.LowAccel, pl.ResetAccel)
        if glitch == "invertedGravity":
            self.changeGravity()
        # ^--------------------------------------------------^
        # Plays static
        # v--------------------------------------------------v
        if garble:
            self.garble = True
            self.sounds["sfx"]["static"].play()
        # ^--------------------------------------------------^

    def generatePath(self, campaignname, level):
        """
        Generates a level path from the campaign Name and
        its level name

        Keyword Arguments:
        - campaignname: Name of the campaign
        - level: Name of the level
        """
        self.gameStatus["currentLevel"] = level
        return pjoin("data", "maps", campaignname, level)

    def RealLoadLevel(self, path, mode, screen):
        """
        Loads a level structure, given path, mode and screen

        Keyword Arguments:
        - path: Full path to the level
        - mode: Mode to open the level in
        - screen: The screen instance
        """
        self.mod_logger.info("LoadLevel Routine is loading %(path)s"
                             % locals())
        # Erases level and if we're doing a campaign, checks for intermissions
        # v--------------------------------------------------v
        self.eraseCurrentLevel()
        if mode not in ["singlemap"]:
            self.checkIntermission()
        # ^--------------------------------------------------^
        # Loads the level configuration and its chaos parameters
        # v--------------------------------------------------v
        with open(path+".json") as f:
            levelconfig = json.loads(f.read())
        self.mod_logger.debug("Level configuration loaded")
        self.loadChaosParameters(levelconfig)
        # ^--------------------------------------------------^
        # If we're in the single timer Critical Failure, load the level time
        # And reset the time to 0.
        # v--------------------------------------------------v
        if mode == "cfsingle":
            self.gameStatus["cftime"] = levelconfig["Level Info"]["CFTime"]
            self.gameStatus["time"] = 0.
        # ^--------------------------------------------------^
        # Loads the level glitches
        # v--------------------------------------------------v
        self.glitches = levelconfig["Glitches"]["Standard"]
        self.mod_logger.debug("Glitches Active: {0}".format(self.glitches))
        # ^--------------------------------------------------------------^
        # Loads the level map
        # v--------------------------------------------------------------v
        self.mod_logger.debug("Loading Tilemap")
        self.tilemap = tmx.load(path+".tmx",
                                self.screensize)
        self.mod_logger.debug("Tilemap Loaded, building map")
        # ^--------------------------------------------------------------^
        # Loads backgrounds and overlays, optimised in case
        # the same ones are used
        # v--------------------------------------------------------------v
        self.mod_logger.debug("Loading Backgrounds")
        self.oldComponentPaths = self.componentPaths.copy()
        for key in self.componentPaths.keys():
            self.componentPaths[key] = pjoin("resources", "backgrounds",
                                             levelconfig["Level Components"]
                                             [key])
            if self.componentPaths[key] != self.oldComponentPaths[key]:
                self.components[key] = pygame.image.load(
                        self.componentPaths[key]).convert_alpha()
        self.hasOverlay = levelconfig["Level Components"]["overlay"]\
            is not None
        if self.hasOverlay:
            self.overpath = pjoin("resources", "overlays",
                                  levelconfig["Level Components"]
                                  ["overlay"])
            if self.overpath != self.oldoverpath:
                self.overlay = pygame.image.load(self.overpath).convert_alpha()
        # ^--------------------------------------------------------------^
        # Creates all the mobile obstacles
        # v--------------------------------------------------------------v
        self.obstacles = tmx.SpriteLayer()
        for obstacle in self.tilemap.layers['Triggers'].find('Obstacle'):
            Obstacle((obstacle.px, obstacle.py), ("v" in obstacle['Obstacle']),
                     obstacle['ObsSpeed'], None, self.obstacles,
                     preloaded_ani=self.preloaded_sprites["glitches"])
        self.tilemap.layers.append(self.obstacles)
        # ^--------------------------------------------------------------^
        # Creates all the triggerable platforms
        # v--------------------------------------------------------------v
        for platform in self.tilemap.layers['Triggers'].find('Platform'):
            bouncy = "bouncyplat" in platform
            bouncepwr = int(platform['bouncyplat']) if bouncy else 0
            TriggerablePlatform(
                    platform.px, platform.py,
                    ("v" in platform['Platform']), bouncepwr,
                    int(platform['PlatSpeed']), int(platform['PlatSize']),
                    False, platform['id'], self.plats, game=self,
                    bouncy=bouncy, image=self.preloaded_sprites["platforms"])
        self.tilemap.layers.append(self.plats)
        # ^--------------------------------------------------------------^
        # Creates all the glitch toggles
        # v--------------------------------------------------------------v
        for trig in self.tilemap.layers['Triggers'].find('ToggleGlitch'):
            self.GlitchTriggers.add(CollectibleTrigger(
                trig.px, trig.py, self, trig['ToggleGlitch'],
                preloaded_animation=self.preloaded_sprites[
                    "collectibleitem"
                    ]))
        self.tilemap.layers.append(self.GlitchTriggers)
        # ^--------------------------------------------------------------^
        # In case of critical failure modes, further garbles
        # level title texts, then renders the title
        # v--------------------------------------------------------------v
        if self.gameStatus["mode"] in ["criticalfailure", "cfsingle"]:
            self.titletxt = makeMoreGlitched(
                                str(levelconfig['Level Info']['Name']),
                                50)
        else:
            self.titletxt = str(levelconfig['Level Info']['Name'])
        self.title = makeGlitched(self.titletxt, self.font)
        # ^--------------------------------------------------------------^
        # Finds the center position of the title
        # v--------------------------------------------------------------v
        center = (self.screensize[0] - int(self.title.get_rect().width))/2
        self.titleposition = (center, 578)
        # ^--------------------------------------------------------------^
        self.mod_logger.info("Map Loaded and built Successfully")
        # ^--------------------------------------------------------------^

    def LoadLevel(self, level, campaignname, mode, screen):
        """
        Check if the level exists and loads it

        Keyword Arguments:
        - level: The level name, without the file extension.
        - campaignname: The campaign name
        - mode: The game mode
        - screen: The surface to draw the level to
        """
        if level == "":
            # No more levels, close
            self.running = False
        else:
            lvl = self.generatePath(campaignname, level)
            self.RealLoadLevel(lvl, mode, screen)

    def loadCampaign(self, campaignfile, mode):
        """
        Loads the levels of the campaign defined in the argument

        Keyword Arguments:
        - campaignFile: The file (Without extension) defining the campaign
        - mode: The game mode
        """
        self.mod_logger.info("Loading campaign {0}".format(campaignfile))
        with open(campaignfile, "r") as campfile:
            cmpf = json.loads(campfile.read())
            self.gameStatus["currentLevel"] = cmpf["FirstMap"]
            self.gameStatus["intermissions"] = cmpf["Intermissions"]
            if mode == "criticalfailure":
                self.gameStatus["cftime"] = cmpf["CFTime"]

    def startIntermission(self, ID):
        """Starts an comicReader intermission instance

        Keyword Arguments:
        - ID: The intermission Identifier
        """
        IM = comicReader(pjoin("resources",
                               "intermissions",
                               self.gameStatus["campaignName"],
                               ID), self.screen,
                         self.keys["action"], self.mainLogger)
        IM.look()

    def checkIntermission(self):
        """
        Checks if in the current level that is about to load
        there is an intermission to be played
        """
        if self.gameStatus["currentLevel"] in\
                self.gameStatus["intermissions"].keys():
            self.mod_logger.debug("Intermission found, starting intermission")
            self.startIntermission(
                    self.gameStatus[
                        "intermissions"][self.gameStatus["currentLevel"]])

    def eraseCurrentLevel(self):
        # At first call, does nothing (Player still has to be created)
        # Self-remaps at runtime to the stage deleting function
        self.eraseCurrentLevel = self.eraseCurrentLevel_Post

    def eraseCurrentLevel_Post(self):
        """
        Erases the whole level, tilemap, memorises the player and
        prepares for a new load
        """
        self.gravity = 1
        self.titletxt = None
        self.tilemap = None
        self.player.x_speed, self.player.y_speed = 0, 0
        self.plats.empty()
        self.GlitchTriggers.empty()
        self.sprites.empty()
        self.helpflagActive = False
        self.currenthelp = ""

    def loadLevelPart2(self, keys, sounds):
        """
        Terminates the level loading by defining the sprite layer,
        and moving the player to the spawn point.

        Keyword Arguments:
        - keys: The instance of the keyboard assignments dictionary
        - sounds: The instance of the sounds dictionary
        """
        # Creates the sprite level, positions the player
        # and the backgrounds
        # v--------------------------------------------------------------v
        self.mod_logger.info("Starting loadLevelPart2 Routine")
        self.sprites = tmx.SpriteLayer()
        start_cell = self.tilemap.layers['Triggers'].find('playerEntrance')[0]
        self.tilemap.layers.append(self.sprites)
        self.backpos, self.middlepos, self.middlebackpos = 3*[[0, 0]]
        self.mod_logger.debug("Positioning Player")
        if self.player is not None:
            self.player.rect.x, self.player.rect.y = start_cell.px,\
                                                     start_cell.py
        else:
            self.player = Player((start_cell.px, start_cell.py),
                                 self.sprites, keys=keys, game=self,
                                 sounds=sounds, log=self.mainLogger)
        self.player.lastcheckpoint = start_cell.px, start_cell.py
        self.sprites.add(self.player)
        # ^--------------------------------------------------------------^
        self.mod_logger.debug("Creating Particle Surface")
        # Builds the particle surface
        # v--------------------------------------------------------------v
        self.particlesurf = pygame.surface.Surface((self.tilemap.px_width,
                                                    self.tilemap.px_height),
                                                   pygame.SRCALPHA,
                                                   32).convert_alpha()
        # In case the invertedgravity glitch is up, invert gravity
        # And check for highjump and speed glitches
        # v--------------------------------------------------------------v
        if self.glitches["invertedGravity"]:
            self.gravity = -1
        pl = self.player
        self.customGlitchToggle("highJump", pl.HiJumpOn, pl.HiJumpOff)
        self.customGlitchToggle("speed", pl.DoubleSpeedOn, pl.DoubleSpeedOff)
        self.customGlitchToggle("featherFalling", pl.FeatherFallOn,
                                pl.FeatherFallOff)
        self.customGlitchToggle("highAccel", pl.HighAccel, pl.ResetAccel)
        self.customGlitchToggle("lowAccel", pl.LowAccel, pl.ResetAccel)
        self.mod_logger.info("Loading of the level completed" +
                             " successfully, ready to play")
        # ^--------------------------------------------------------------^

    def loadGame(self, path=None):
        """
        Opens the game from a JSON file
        """
        self.mod_logger.info("Loading Save from: %(path)s"
                             % locals())
        with open(path, "r") as savefile:
            self.gameStatus = json.loads(savefile.read())
        if self.gameStatus["mode"] in ["criticalfailure", "cfsingle"]:
            self.mod_logger.debug("Using Load Game mode -\
                    Critical Failure Modifier")
            self.redsurf = pygame.surface.Surface(self.gsize,
                                                  pygame.SRCALPHA)
            linesize = 3
            bot = self.redsurf.get_rect().bottom
            self.redsurf.fill((255, 0, 0, 50))
            self.redsurf.fill((255, 255, 255, 255),
                              pygame.rect.Rect(0,
                                               bot - linesize,
                                               self.gsize[0],
                                               linesize))
            self.redsurfrect = self.redsurf.get_rect()

    def newChaosTime(self):
        """ Generates a new timer to countdown to a new random
        glitch toggle"""
        self.chaosParameters["timer"] = float(randint(5, 20))

    def loadChaosParameters(self, lvlconf):
        """
        Loads the chaos mode glitches from a level config instance

        Keyword Parameters:
        - lvlconf: The level config instance
        """
        self.chaosParameters = {"glitches": None, "timer": None}
        self.chaosParameters["glitches"] = \
            [x
             for x in lvlconf["Glitches"]["ChaosMode"]
             if lvlconf["Glitches"]["ChaosMode"][x]]
        self.newChaosTime()
        self.mod_logger.debug("Chaos Mode Parameters: {0}".format(
            self.chaosParameters))

    def forceNextLevel(self):
        """
        DEBUG METHOD
        Used to jump to the first playerexit level found
        """
        return self.tilemap.layers["Triggers"].find(
                "playerExit")[0]["playerExit"]

    def givePosition(self, op, fact):
        """
        Returns the viewport position, scaled by a certain factor,
        according to a certain operation

        Keyword Arguments:
        - op: Operation to perform (usually __mul__ or __floordiv__)
        - fact: Scaling factor
        """
        return (min(op(-self.tilemap.viewport.x, fact), 0),
                min(op(-self.tilemap.viewport.y, fact), 0))

    def main(self, screen, keys, mode, cmp, config, sounds, modifiers, log):
        """
        Main Game method

        Keyword Arguments:
        - Screen: The surface to draw the game to.
        - keys: The control keys to use.
        - Mode: Identifies the mode of the game (newgame, load,
                singlemap, criticalfailure, cfsingle)
        - cmp: campaign file
        - config: Game configuration instance
        - sounds: Sounds dictionary instance
        - modifiers: Modifiers Dictionary instance
        - log: The main logger, inherited by the bootstrapper
        """
        self.gameStatus = {
                "campaignFile": None,
                "campaignName": None,
                "mode": mode,
                "cftime": None,
                "time": 0.,
                "deathCounter": 0,
                "modifiers": modifiers,
                "currentLevel": None
                }
        self.oldComponentPaths = {
                "background": None,
                "middle_back1": None,
                "middle_back2": None
        }
        self.componentPaths = {
                "background": None,
                "middle_back1": None,
                "middle_back2": None
        }
        self.components = {
                "background": None,
                "middle_back1": None,
                "middle_back2": None
        }
        self.oldoverpath = None
        self.mainLogger = log
        self.mod_logger = log.getChild("game")
        self.mod_logger.info("Entering main game")
        self.running = True
        self.titletxt = None
        self.gravity = 1
        self.sounds = sounds
        self.screensize = screen.get_size()
        self.gsize = (800, 576)
        self.gameviewport = pygame.surface.Surface(self.gsize)
        self.clock = pygame.time.Clock()
        self.titleholder = pygame.image.load(pjoin(
                                             "resources",
                                             "UI",
                                             "TitleHolder.png"))
        self.font = pygame.font.Font(pjoin(
                            "resources", "fonts",
                            "TranscendsGames.otf"), 20)
        self.title, self.titleposition, self.player = 3 * [None]
        self.screen = screen
        self.keys = keys
        self.config = config
        self.helptxts = pygame.sprite.Group()
        self.plats = tmx.SpriteLayer()
        self.GlitchTriggers = tmx.SpriteLayer()
        self.mod_logger.debug("Current Active Modifiers: {0}".format(
            modifiers))
        # Preloading graphics area
        # v-------------------------------------------------------------------v
        self.preloaded_sprites = {
                "platforms": pygame.image.load(pathjoin("resources",
                                                        "tiles",
                                                        "Plats.png")
                                               ).convert_alpha(),
                "glitches": pathjoin("resources",
                                     "sprites",
                                     "MobileObstacle.png"),
                "collectibleitem": pathjoin("resources",
                                            "sprites",
                                            "GlitchTrigger.png"
                                            ),
                "static": pygame.image.load(pathjoin("resources",
                                                     "backgrounds",
                                                     "screengarble.png")
                                            ).convert_alpha()
                }
        # ^-------------------------------------------------------------------^
        # Defines if a level should be loaded or a
        # new campaign should be started.
        # It also defines the modes
        # v--------------------------------------------------------------v
        if self.gameStatus["mode"] == "load":
            self.mod_logger.debug("Using Load mode")
            try:
                self.loadGame(cmp)
                self.LoadLevel(self.gameStatus["currentLevel"],
                               self.gameStatus["campaignName"],
                               self.gameStatus["mode"],
                               self.screen)
            except FileNotFoundError:
                self.mod_logger.info("No file provided, loading cancelled")
                self.running = False
        elif self.gameStatus["mode"] == "newgame":
            self.mod_logger.debug("Using New Game mode")
            self.gameStatus["campaignFile"] = cmp
            self.gameStatus["campaignName"] = splitext(basename(cmp))[0]
            self.loadCampaign(self.gameStatus["campaignFile"],
                              self.gameStatus["mode"])
            self.LoadLevel(self.gameStatus["currentLevel"],
                           self.gameStatus["campaignName"],
                           self.gameStatus["mode"],
                           self.screen)
        elif self.gameStatus["mode"] in ["criticalfailure", "cfsingle"]:
            self.mod_logger.debug("Using New Game mode - \
                    Critical Failure Modifier")
            self.gameStatus["cftime"] = 0
            self.gameStatus["campaignFile"] = cmp
            self.gameStatus["campaignName"] = splitext(basename(cmp))[0]
            self.loadCampaign(self.gameStatus["campaignFile"],
                              self.gameStatus["mode"])
            self.redsurf = pygame.surface.Surface(self.gsize,
                                                  pygame.SRCALPHA)
            linesize = 3
            bot = self.redsurf.get_rect().bottom
            self.redsurf.fill((255, 0, 0, 50))
            self.redsurf.fill((255, 255, 255, 255),
                              pygame.rect.Rect(0,
                                               bot - linesize,
                                               self.gsize[0],
                                               linesize))
            self.redsurfrect = self.redsurf.get_rect()
            self.LoadLevel(self.gameStatus["currentLevel"],
                           self.gameStatus["campaignName"],
                           self.gameStatus["mode"],
                           self.screen)
        elif self.gameStatus["mode"] == "singlemap":
            self.RealLoadLevel(cmp, "singlemap", self.screen)
        # ^--------------------------------------------------------------^
        self.fps = 30
        self.garble = False
        self.garbletimer = _garbletimer_
        self.deadbodies = pygame.sprite.Group()
        pygame.display.set_caption("Glitch_Heaven - Pre-Pre-Alpha Version")
        if self.running:
            self.loadLevelPart2(self.keys, sounds)
            self.mod_logger.debug("Glitches Loaded: {0}".format(self.glitches))
        """Game Loop"""
        while self.running:
            dt = min(self.clock.tick(self.fps)/1000., 0.05)
            # For Critical Failure mode
            # v-------------------------------------------------------------------v
            if self.gameStatus["mode"] in ["criticalfailure", "cfsingle"]:
                self.gameStatus["time"] += dt
                self.redsurfrect.y = -self.gsize[1] + \
                    (self.gsize[1] * self.gameStatus["time"]) \
                    / self.gameStatus["cftime"]
                self.rcftime = self.gameStatus["cftime"] \
                    - self.gameStatus["time"]
                self.timer = makeGlitched("Time Before Failure: {0}".format(
                    str(timedelta(seconds=self.rcftime))),
                                          self.font)
                if self.redsurfrect.y > 0:
                    pygame.mouse.set_visible(True)  # Make the cursor visible
                    self.running = False
            # ^-------------------------------------------------------------------^
            # For Chaos Mode
            # v-------------------------------------------------------------------v
            if self.gameStatus["modifiers"]["chaos"]:
                self.chaosParameters["timer"] -= dt
                if self.chaosParameters["timer"] <= 0.:
                    self.toggleGlitch(choice(
                                      self.chaosParameters["glitches"]), True)
                    self.newChaosTime()
            # ^-------------------------------------------------------------------^
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.mod_logger.info("QUIT signal received, quitting")
                    pygame.quit()
                    quit()
                # Debug Area - Glitch Toggles
                # v----------------------------------------------------------v
                mods = pygame.key.get_mods()
                # if config.getboolean("Debug", "debugmode") and\
                if config["Debug"]["debugmode"] and\
                        mods & pygame.KMOD_LSHIFT and\
                        mods & pygame.KMOD_LCTRL and\
                        mods & pygame.KMOD_LALT:
                    if event.type == pygame.KEYDOWN:
                        if event.key in _debugkeys_:
                            self.toggleGlitch(_debugkeys_[event.key],
                                              True)
                        if event.key == pygame.K_RETURN:
                            self.garble = True
                        if event.key == pygame.K_BACKSPACE and\
                                self.gameStatus["mode"] not in ["singlemap"]:
                            self.mod_logger.debug("Debug key used, " +
                                                  "Loading next level")
                            level = self.forceNextLevel()
                            self.LoadLevel(level,
                                           self.gameStatus["campaignName"],
                                           self.gameStatus["mode"],
                                           self.screen)
                            self.loadLevelPart2(self.keys, sounds)
                # Temporary toggles for pause menu and saveGame
                # v----------------------------------------------------------v
                elif event.type == pygame.KEYDOWN and\
                        event.key == keys["escape"]:
                    pauseMenu(screen, keys, self,
                              self.config, sounds, self.mainLogger).mainLoop()
                elif event.type == pygame.KEYDOWN and\
                        event.key == self.keys["restart"]:
                            self.sprites.remove(*self.deadbodies)
                            self.deadbodies.empty()
                            self.player.respawn(self)
                # if config.getboolean("Debug", "keydebug") and\
                if config["Debug"]["keydebug"] and\
                        event.type == pygame.KEYDOWN:
                    self.mod_logger.debug("A key was pressed: {0}"
                                          .format(pygame.key.name(event.key)))
                # ^----------------------------------------------------------^
            self.backpos = self.givePosition(__floordiv__, 6)
            self.middlebackpos = self.givePosition(__floordiv__, 4)
            self.middlepos = self.givePosition(__floordiv__, 2)
            self.gameviewport.blit(self.components["background"],
                                   self.backpos)
            self.gameviewport.blit(self.components["middle_back1"],
                                   self.middlebackpos)
            self.tilemap.update(dt, self)
            self.helptxts.update(dt, self)
            self.gameviewport.blit(self.components["middle_back2"],
                                   self.middlepos)
            self.tilemap.draw(self.gameviewport)
            if not self.glitches["timeLapse"] or self.player.x_speed != 0:
                self.particlesurf.fill((0, 0, 0, 0))
                self.player.particles.update()
            self.player.particles.draw(self.particlesurf)
            self.gameviewport.blit(self.particlesurf,
                                   (-self.tilemap.viewport.x,
                                    -self.tilemap.viewport.y))
            if self.hasOverlay:
                self.gameviewport.blit(self.overlay,
                                       self.givePosition(__mul__, 1.5))
            if self.gameStatus["mode"] in ["criticalfailure", "cfsingle"]:
                self.gameviewport.blit(self.redsurf, (0, self.redsurfrect.y))
            if self.gameStatus["modifiers"]["vflip"] or\
                    self.gameStatus["modifiers"]["hflip"]:
                self.gameviewport = pygame.transform.flip(
                        self.gameviewport,
                        self.gameStatus["modifiers"]["hflip"],
                        self.gameStatus["modifiers"]["vflip"])
            screen.blit(self.gameviewport, (0, 0))
            if self.gameStatus["mode"] in ["criticalfailure", "cfsingle"]:
                screen.blit(self.timer, (50, 70))
            screen.blit(self.titleholder, (0, 576))
            screen.blit(self.title, self.titleposition)
            # if config.getboolean("Video", "deathcounter"):
            if config["Video"]["deathcounter"]:
                self.dcounttxt = makeGlitched(
                            "Deaths: %d"
                            % self.gameStatus["deathCounter"],
                            self.font)
                screen.blit(self.dcounttxt, (50, 50))
            if self.garble:
                screen.blit(self.preloaded_sprites["static"], (0, 0))
                self.garbletimer -= dt
                if self.garbletimer <= 0:
                    self.garble = False
                    self.garbletimer = _garbletimer_
            pygame.display.update()
