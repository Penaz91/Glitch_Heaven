# Game Component
# Part of the Glitch_Heaven Project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
#
# ------------------------------------------------
# TODO Area
# - Add a game HUD
# ------------------------------------------------
import pygame
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
from tkinter import filedialog
from os import getcwd
from libs.textglitcher import makeGlitched, makeMoreGlitched
from tkinter import Tk
from libs.debugconstants import _debugkeys_
_garbletimer_ = 0.1
_dialogConstants_ = {
    "saveGame": {
        "filetypes": [("Glitch_Heaven Savegame", "*.dat")],
        "initialdir": pjoin(getcwd(), "savegames"),
        "defaultextension": ".dat"
                },
    "loadGame": {
        "filetypes": [("Glitch_Heaven Savegame", "*.dat")],
        "initialdir": pjoin(getcwd(), "savegames"),
        "multiple": False
                }
                    }


class Game(object):
    """ The Main Game """

    def customGlitchToggle(self, glitchname, trueFunction, falseFunction):
        if self.glitches[glitchname]:
            trueFunction()
        else:
            falseFunction()

    def changeGravity(self):
            self.gravity *= -1

    def toggleGlitch(self, glitch, garble):
        """
        Debug method for toggling glitches

        Works only with glitches in the "Glitches" dictionary

        Keyword Arguments:
        - Glitch: String key which identifies the glitch to toggle

        Retuns:
        - Nothing
        """
        self.glitches[glitch] = not self.glitches[glitch]
        self.mod_logger.debug("{0} Glitch has been set to {1}".format(
            glitch,
            self.glitches[glitch]))
        pl = self.player
        self.customGlitchToggle("highJump", pl.HiJumpOn, pl.HiJumpOff)
        self.customGlitchToggle("speed", pl.DoubleSpeedOn, pl.DoubleSpeedOff)
        if glitch == "invertedGravity":
            self.changeGravity()
        if garble:
            self.garble = True
            self.sounds["sfx"]["static"].play()

    def generatePath(self, campaignname, level):
        self.gameStatus["currentLevel"] = level
        # self.currentLevel = level
        return pjoin("data", "maps", campaignname, level)

    def RealLoadLevel(self, path, mode, screen):
        self.mod_logger.info("LoadLevel Routine is loading %(path)s"
                             % locals())
        self.eraseCurrentLevel()
        if mode not in ["singlemap"]:
            self.checkIntermission()
        with open(path+".conf") as f:
            levelconfig = json.loads(f.read())
        self.mod_logger.debug("Level configuration loaded")
        self.loadChaosParameters(levelconfig)
        if mode == "cfsingle":
            # self.cftime = int(levelconfig["Level Info"]["CFTime"])
            self.gameStatus["cftime"] = levelconfig.getint("Level Info",
                                                           "CFTime")
        self.glitches = levelconfig["Glitches"]["Standard"]
        self.mod_logger.debug("Glitches Active: {0}".format(self.glitches))
        # ^--------------------------------------------------------------^
        # Loads the level map, triggers, obstacles
        # v--------------------------------------------------------------v
        self.mod_logger.debug("Loading Tilemap")
        self.tilemap = tmx.load(path+".tmx",
                                self.screensize)
        self.mod_logger.debug("Tilemap Loaded, building map")
        self.obstacles = tmx.SpriteLayer()
        # Small optimisation in case the same background is loaded
        # v------------------------------v
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
        """
        self.oldbgpath = self.bgpath
        self.oldmbackpath = self.mbackpath
        self.oldmiddlepath = self.middlepath
        self.oldoverpath = self.overpath
        self.bgpath = pjoin("resources", "backgrounds",
                            levelconfig["Level Components"]
                            ["background"])
        self.mbackpath = pjoin("resources", "backgrounds",
                               levelconfig["Level Components"]
                               ["middle_back1"])
        self.middlepath = pjoin("resources", "backgrounds",
                                levelconfig["Level Components"]
                                ["middle_back2"])
        if self.bgpath != self.oldbgpath:
            self.bg = pygame.image.load(self.bgpath).convert_alpha()
        if self.mbackpath != self.oldmbackpath:
            self.middleback = pygame.image.load(self.mbackpath
                                                ).convert_alpha()
        if self.middlepath != self.oldmiddlepath:
            self.middle = pygame.image.load(self.middlepath).convert_alpha()
        if levelconfig["Level Components"]["overlay"] is not None:
            self.hasOverlay = True
            self.overpath = pjoin("resources", "overlays",
                                  levelconfig["Level Components"]
                                  ["overlay"])
            if self.overpath != self.oldoverpath:
                self.overlay = pygame.image.load(self.overpath).convert_alpha()
        else:
            self.hasOverlay = False
        """
        for obstacle in self.tilemap.layers['Triggers'].find('Obstacle'):
            Obstacle((obstacle.px, obstacle.py), ("v" in obstacle['Obstacle']),
                     obstacle['ObsSpeed'], None, self.obstacles,
                     preloaded_ani=self.preloaded_sprites["glitches"])
        self.tilemap.layers.append(self.obstacles)
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
        for trig in self.tilemap.layers['Triggers'].find('ToggleGlitch'):
            self.GlitchTriggers.add(CollectibleTrigger(
                trig.px, trig.py, self, trig['ToggleGlitch'],
                preloaded_animation=self.preloaded_sprites[
                    "collectibleitem"
                    ]))
        self.tilemap.layers.append(self.GlitchTriggers)
        self.titletxt = None
        if self.gameStatus["mode"] in ["criticalfailure", "cfsingle"]:
            self.titletxt = makeMoreGlitched(
                                str(levelconfig['Level Info']['Name']),
                                50)
        else:
            self.titletxt = str(levelconfig['Level Info']['Name'])
        self.title = makeGlitched(self.titletxt, self.font)
        center = (self.screensize[0] - int(self.title.get_rect().width))/2
        self.titleposition = (center, 578)
        if mode.lower() == "cfsingle":
            # self.time = 0.
            self.gameStatus["time"] = 0.
        self.mod_logger.info("Map Loaded and built Successfully")
        # ^--------------------------------------------------------------^

    def LoadLevel(self, level, campaignname, mode, screen):
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
        """
        self.mod_logger.info("Loading campaign {0}".format(campaignfile))
        with open(campaignfile,
                  "r") as campfile:
            cmpf = json.loads(campfile.read())
            # self.currentLevel = cmpf["FirstMap"]
            self.gameStatus["currentLevel"] = cmpf["FirstMap"]
            self.intermissions = cmpf["Intermissions"]
            if mode == "criticalfailure":
                # self.cftime = cmpf["CFTime"]
                self.gameStatus["cftime"] = cmpf["CFTime"]

    def startIntermission(self, ID):
        """IM = comicReader(pjoin("resources",
                               "intermissions",
                               self.campaignname,
                               ID), self.screen,
                         self.keys["action"], self.mainLogger)"""
        IM = comicReader(pjoin("resources",
                               "intermissions",
                               self.gameStatus["campaignName"],
                               ID), self.screen,
                         self.keys["action"], self.mainLogger)

        IM.look()

    def checkIntermission(self):
        # if self.currentLevel in self.intermissions.keys():
        if self.gameStatus["currentLevel"] in self.intermissions.keys():
            self.mod_logger.debug("Intermission found, starting intermission")
            # self.startIntermission(self.intermissions[self.currentLevel])
            self.startIntermission(
                    self.intermissions[self.gameStatus["currentLevel"]])

    def eraseCurrentLevel(self):
        """
        Erases the whole level, tilemap, kills the player and
        prepares for a new load
        """
        # At first call, does nothing (Player still has to be created)
        # Self-remaps at runtime to the stage deleting function
        self.eraseCurrentLevel = self.eraseCurrentLevel_Post

    def eraseCurrentLevel_Post(self):
        self.gravity = 1
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
        and spawning the player.
        """
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
        self.mod_logger.debug("Creating Particle Surface")
        self.particlesurf = pygame.surface.Surface((self.tilemap.px_width,
                                                    self.tilemap.px_height),
                                                   pygame.SRCALPHA,
                                                   32).convert_alpha()
        # In case the invertedgravity glitch is up, invert gravity
        # v--------v
        if self.glitches["invertedGravity"]:
            self.gravity = -1
        # ^--------^
        pl = self.player
        self.customGlitchToggle("highJump", pl.HiJumpOn, pl.HiJumpOff)
        self.customGlitchToggle("speed", pl.DoubleSpeedOn, pl.DoubleSpeedOff)
        self.mod_logger.info("Loading of the level completed" +
                             " successfully, ready to play")
        # pygame.mouse.set_visible(False)
        # self.mod_logger.debug("Mouse cursor hidden")

    def saveGame(self):
        """
        Saves the game level/campaign in a shelf file.
        """
        Tk().withdraw()
        # formats = [("Glitch_Heaven Savegame", "*.dat")]
        # path = filedialog.asksaveasfilename(filetypes=formats,
        #                                     initialdir="./savegames",
        #                                     defaultextension=".dat")
        path = filedialog.asksaveasfilename(**_dialogConstants_["saveGame"])
        if path:
            # if not (self.mode.lower() in ["criticalfailure", "cfsingle"]):
            if not (self.gameStatus["mode"] in ["criticalfailure",
                                                "cfsingle"]):
                self.gameStatus["cftime"] = 0
                self.gameStatus["time"] = 0
                self.gameStatus["mode"] = "newgame"
                # self.cftime, self.time = 0, 0
                # self.mode = "newgame"
            """shelf = {"campaignfile": self.campaignFile,
                     "currentLevel": self.currentLevel,
                     "campaignname": self.campaignname,
                     "cftime": self.cftime,
                     "time": self.time,
                     "mode": self.mode,
                     "deathCounter": self.deathCounter,
                     "modifiers": self.modifiers}"""
            self.mod_logger.debug("Saved with data: {0}"
                                  % self.gameStatus)
            with open(path, "w") as savefile:
                # savefile.write(json.dumps(shelf))
                savefile.write(json.dumps(self.gameStatus))
                self.mod_logger.info("Game saved on the file: \
                        %(savefile)s" % locals())

    def loadGame(self):
        """
        Opens the game from a json file
        """
        Tk().withdraw()
        # formats = [("Glitch_Heaven Savegame", "*.dat")]
        # path = filedialog.askopenfilename(filetypes=formats,
        #                                   initialdir="savegames",
        #                                   multiple=False)
        path = filedialog.askopenfilename(**_dialogConstants_["loadGame"])
        if not path:
            raise FileNotFoundError
        self.mod_logger.info("Loading Save from: %(path)s"
                             % locals())
        with open(path, "r") as savefile:
            """
            string = savefile.read()
            shelf = json.loads(string)
            self.campaignFile = shelf["campaignfile"]
            self.campaignname = shelf["campaignname"]
            self.mode = shelf["mode"]
            self.cftime = shelf["cftime"]
            self.time = shelf["time"]
            self.deathCounter = shelf["deathCounter"]
            self.modifiers = shelf["modifiers"]
            self.currentLevel = shelf["currentLevel"]
            """
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
        self.chaosParameters["timer"] = float(randint(5, 20))

    def loadChaosParameters(self, lvlconf):
        self.chaosParameters = {"glitches": None, "timer": None}
        self.chaosParameters["glitches"] = \
            [x
             for x in lvlconf["Glitches"]["ChaosMode"]
             if lvlconf["Glitches"]["ChaosMode"][x]]
        self.newChaosTime()
        self.mod_logger.debug("Chaos Mode Parameters: {0}".format(
            self.chaosParameters))

    def forceNextLevel(self):
        return self.tilemap.layers["Triggers"].find("playerExit")[0]["playerExit"]

    def main(self, screen, keys, mode, cmp, config, sounds, modifiers, log):
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
        self.gameStatus = {
                "campaignFile": None,
                "campaignName": None,
                "mode": None,
                "cftime": None,
                "time": None,
                "deathCounter": None,
                "modifiers": None,
                "currentLevel": None
                }
        self.oldComponentPaths = {
                "background": None,
                "middle_back1": None,
                "middle_back2": None,
        }
        self.componentPaths = {
                "background": None,
                "middle_back1": None,
                "middle_back2": None,
        }
        self.components = {
                "background": None,
                "middle_back1": None,
                "middle_back2": None,
        }
        self.mainLogger = log
        self.mod_logger = log.getChild("game")
        self.mod_logger.info("Entering main game")
        self.running = True
        self.gravity = 1
        # self.time = 0.
        self.gameStatus["time"] = 0.
        self.sounds = sounds
        # self.deathCounter = 0
        self.gameStatus["deathCounter"] = 0
        self.gameStatus["mode"] = mode
        # self.bgpath, self.mbackpath = 2 * [None]
        self.screensize = screen.get_size()
        # self.middlepath, self.overpath = 2 * [None]
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
        # self.modifiers = modifiers
        self.gameStatus["modifiers"] = modifiers
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
        # v--------------------------------------------------------------v
        if self.gameStatus["mode"] == "load":
            self.mod_logger.debug("Using Load mode")
            try:
                self.loadGame()
                # self.LoadLevel(self.currentLevel, self.campaignname,
                #                self.mode, self.screen)
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
            # self.campaignFile = cmp
            # self.campaignname = splitext(basename(cmp))[0]
            self.gameStatus["campaignName"] = splitext(basename(cmp))[0]
            # self.loadCampaign(self.campaignFile, self.mode)
            self.loadCampaign(self.gameStatus["campaignFile"],
                              self.gameStatus["mode"])
            self.LoadLevel(self.gameStatus["currentLevel"],
                           self.gameStatus["campaignName"],
                           self.gameStatus["mode"],
                           self.screen)

            # self.LoadLevel(self.currentLevel, self.campaignname,
            #                self.mode, self.screen)
        elif self.gameStatus["mode"] in ["criticalfailure", "cfsingle"]:
            self.mod_logger.debug("Using New Game mode - \
                    Critical Failure Modifier")
            # self.cftime = 0
            self.gameStatus["cftime"] = 0
            # self.campaignFile = cmp
            # self.campaignname = splitext(basename(cmp))[0]
            self.gameStatus["campaignName"] = splitext(basename(cmp))[0]
            # self.loadCampaign(self.campaignFile, self.mode)
            self.LoadCampaign(self.gameStatus["campaignFile"],
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
            # self.LoadLevel(self.currentLevel, self.campaignname,
            #                self.mode, self.screen)
            self.LoadLevel(self.gameStatus["currentLevel"],
                           self.gameStatus["campaignName"],
                           self.gameStatus["mode"],
                           self.screen)
        # elif self.mode.lower() == "singlemap":
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
            dt = min (self.clock.tick(self.fps)/1000., 0.05)
            # For Critical Failure mode
            # v-------------------------------------------------------------------v
            # if self.mode.lower() in ["criticalfailure", "cfsingle"]:
            if self.gameStatus["mode"] in ["criticalfailure", "cfsingle"]:
                # self.time += dt
                self.gameStatus["time"] += dt
                # self.redsurfrect.y = -self.gsize[1] + \
                #    (self.gsize[1] * self.time) / self.cftime
                self.redsurfrect.y = -self.gsize[1] + \
                    (self.gsize[1] * self.gameStatus["time"]) \
                    / self.gameStatus["cftime"]
                # self.rcftime = self.cftime - self.time
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
            # if self.modifiers["chaos"]:
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
                if config.getboolean("Debug", "debugmode") and\
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
                            # self.LoadLevel(level, self.campaignname,
                            #                self.mode, self.screen)
                            self.LoadLevel(level,
                                           self.gameStatus["campaignName"],
                                           self.gameStatus["mode"],
                                           self.screen)
                            self.loadLevelPart2(self.keys, sounds)
                if config.getboolean("Debug", "keydebug") and\
                        event.type == pygame.KEYDOWN:
                    self.mod_logger.debug("A key was pressed: {0}"
                                          .format(pygame.key.name(event.key)))
                # ^----------------------------------------------------------^
                # Temporary toggles for pause menu and saveGame
                # v----------------------------------------------------------v
                if event.type == pygame.KEYDOWN and\
                        event.key == keys["escape"]:
                    pauseMenu(screen, keys, self,
                              self.config, sounds, self.mainLogger).mainLoop()
                if event.type == pygame.KEYDOWN and\
                        event.key == self.keys["restart"]:
                            self.sprites.remove(*self.deadbodies)
                            self.deadbodies.empty()
                            self.player.respawn(self)
            self.backpos = (min(-self.tilemap.viewport.x/6, 0),
                            min(-self.tilemap.viewport.y / 6, 0))
            self.middlebackpos = (min(-self.tilemap.viewport.x/4, 0),
                                  min(-self.tilemap.viewport.y / 4, 0))
            self.middlepos = (min(-self.tilemap.viewport.x/2, 0),
                              min(-self.tilemap.viewport.y / 2, 0))
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
                                       (-self.tilemap.viewport.x*1.5,
                                        -self.tilemap.viewport.y*1.5))
            # if self.mode.lower() in ["criticalfailure", "cfsingle"]:
            if self.gameStatus["mode"] in ["criticalfailure", "cfsingle"]:
                self.gameviewport.blit(self.redsurf, (0, self.redsurfrect.y))
            # if self.modifiers["vflip"] or self.modifiers["hflip"]:
            if self.gameStatus["modifiers"]["vflip"] or\
                    self.gameStatus["modifiers"]["hflip"]:
                self.gameviewport = pygame.transform.flip(
                        self.gameviewport,
                        self.gameStatus["modifiers"]["hflip"],
                        self.gameStatus["modifiers"]["vflip"])
            screen.blit(self.gameviewport, (0, 0))
            # if self.mode.lower() in ["criticalfailure", "cfsingle"]:
            if self.gameStatus["mode"] in ["criticalfailure", "cfsingle"]:
                screen.blit(self.timer, (50, 70))
            screen.blit(self.titleholder, (0, 576))
            screen.blit(self.title, self.titleposition)
            if config.getboolean("Video","deathcounter"):
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
