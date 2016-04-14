# Game Component
# Part of the Glitch_Heaven Project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
#
# ------------------------------------------------
# TODO Area
# - Add a game HUD
# - Add Joypad support
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
from libs.textglitcher import makeGlitched, makeMoreGlitched
from tkinter import Tk
_garbletimer_ = 0.1
_debugkeys_ = {
        pygame.K_1: "wallClimb", pygame.K_2: "multiJump",
        pygame.K_3: "highJump", pygame.K_4: "featherFalling",
        pygame.K_5: "gravity", pygame.K_6: "hover",
        pygame.K_7: "stickyCeil", pygame.K_8: "invertedGravity",
        pygame.K_9: "permBodies", pygame.K_q: "solidHelp",
        pygame.K_w: "clipOnCommand", pygame.K_e: "hWrapping",
        pygame.K_r: "vWrapping", pygame.K_t: "ledgeWalk",
        pygame.K_y: "ledgeJump", pygame.K_u: "slideInvert",
        pygame.K_i: "noLeft", pygame.K_o: "noRight",
        pygame.K_p: "noJump", pygame.K_a: "stopBounce",
        pygame.K_s: "speed", pygame.K_d: "invertedRun",
        pygame.K_f: "invertedControls", pygame.K_g: "obsResistant",
        pygame.K_h: "noStop", pygame.K_j: "timeLapse"}


class Game(object):
    """ The Main Game """

    def customGlitchToggle(self, glitchname, trueFunction, falseFunction):
        if self.glitches[glitchname]:
            trueFunction()
        else:
            falseFunction()

    def checkGravity(self):
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
            self.checkGravity()
        if garble:
            self.garble = True
            self.sounds["sfx"]["static"].play()

    def getHelpFlag(self):
        """
        Getter method for helpflagactive

        Returns:
        - self.helpflagActive
        """
        return self.helpflagActive

    def setHelpFlag(self, flag):
        """
        Setter method for helpflagactive

        Keyword Arguments:
        - flag: The flag to set
        """
        self.helpflagActive = flag

    def setHelpText(self, txt):
        """
        Setter Method for currenthelp

        Keyword Arguments:
        - txt: The text to set
        """
        self.currenthelp = txt

    def getHelpText(self):
        """
        Getter Method for currenthelp

        Returns:
        - self.currenthelp
        """
        return self.currenthelp
        
    def generatePath(self, campaignname, level):
        self.currentLevel = level
        return pjoin("data", "maps", campaignname, level)

    def RealLoadLevel(self, path, mode, screen):
        self.mod_logger.info("LoadLevel Routine is loading %(path)s" %locals())
        self.eraseCurrentLevel()
        if not mode in ["singlemap"]:
            self.checkIntermission()
        with open(path+".conf") as f:
            levelconfig = json.loads(f.read())
        self.mod_logger.debug("Level configuration loaded")
        self.loadChaosParameters(levelconfig)
        if mode == "cfsingle":
            self.cftime = int(levelconfig["Level Info"]["CFTime"])
        self.helpflagActive = False
        self.currenthelp = ""
        self.screen = screen
        self.glitches = levelconfig["Glitches"]["Standard"]
        self.mod_logger.debug("Glitches Active: {0}".format(self.glitches))
        # ^--------------------------------------------------------------^
        # Loads the level map, triggers, obstacles
        # v--------------------------------------------------------------v
        self.mod_logger.debug("Loading Tilemap")
        self.tilemap = tmx.load(path+".tmx",
                                screen.get_size())
        self.mod_logger.debug("Tilemap Loaded, building map")
        self.obstacles = tmx.SpriteLayer()
        # Small optimisation in case the same background is loaded
        # v------------------------------v
        self.mod_logger.debug("Loading Backgrounds")
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
        for obstacle in self.tilemap.layers['Triggers'].find('Obstacle'):
            obs = obstacle['Obstacle']
            speed = obstacle['ObsSpeed']
            Obstacle((obstacle.px, obstacle.py), ("v" in obs), speed, None,
                     self.obstacles,
                     preloaded_ani=self.preloaded_sprites["glitches"])
        self.tilemap.layers.append(self.obstacles)
        for platform in self.tilemap.layers['Triggers'].find('Platform'):
            plat = platform['Platform']
            size = int(platform['PlatSize'])
            spd = int(platform['PlatSpeed'])
            if "bouncyplat" in platform:
                bouncy = True
                bouncepwr = int(platform['bouncyplat'])
            else:
                bouncy = False
                bouncepwr = 0
            TriggerablePlatform(platform.px, platform.py, ("v" in plat),
                                bouncepwr, spd, size, False, platform['id'],
                                self.plats, game=self, bouncy=bouncy,
                                image=self.preloaded_sprites["platforms"])
        self.tilemap.layers.append(self.plats)
        for trig in self.tilemap.layers['Triggers'].find('ToggleGlitch'):
            totrigger = trig['ToggleGlitch']
            tr = CollectibleTrigger(trig.px, trig.py, self, totrigger,
                                    preloaded_animation=self.preloaded_sprites[
                                        "collectibleitem"
                                        ])
            self.GlitchTriggers.add(tr)
        self.tilemap.layers.append(self.GlitchTriggers)
        if self.mode in ["criticalfailure", "cfsingle"]:
            self.title = makeGlitched(
                            makeMoreGlitched(
                                str(levelconfig['Level Info']['Name']),
                                50),
                            self.font)
        else:
            self.title = makeGlitched(
                            str(levelconfig['Level Info']['Name']),
                            self.font)
        center = 400 - int(self.title.get_rect().width)/2
        self.titleposition = (center, 578)
        if mode.lower() == "cfsingle":
            self.time = 0.
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
            self.currentLevel = cmpf["FirstMap"]
            self.intermissions = cmpf["Intermissions"]
            if mode == "criticalfailure":
                self.cftime = cmpf["CFTime"]

    def startIntermission(self, ID):
        IM = comicReader(pjoin("resources",
                               "intermissions",
                               self.campaignname,
                               ID), self.screen,
                         self.keys["action"], self.mainLogger)
        IM.look()

    def checkIntermission(self):
        if self.currentLevel in self.intermissions.keys():
            self.mod_logger.debug("Intermission found, starting intermission")
            self.startIntermission(self.intermissions[self.currentLevel])

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
        self.sprites.add(self.player)

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
        self.gravity = 1
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
        pygame.mouse.set_visible(False)
        self.mod_logger.debug("Mouse cursor hidden")

    def saveGame(self):
        """
        Saves the game level/campaign in a shelf file.
        """
        Tk().withdraw()
        formats = [("Glitch_Heaven Savegame", "*.dat")]
        path = filedialog.asksaveasfilename(filetypes=formats,
                                            initialdir="./savegames",
                                            defaultextension=".dat")
        if path:
            if not (self.mode.lower() in ["criticalfailure", "cfsingle"]):
                self.cftime, self.time = 0, 0
                self.mode = "newgame"
            shelf = {"campaignfile": self.campaignFile,
                     "currentLevel": self.currentLevel,
                     "campaignname": self.campaignname,
                     "cftime": self.cftime,
                     "time": self.time,
                     "mode": self.mode,
                     "deathCounter": self.deathCounter,
                     "modifiers": self.modifiers}
            self.mod_logger.debug("Shelf saved with data: %(shelf)s"
                                  % locals())
            with open(path, "w") as savefile:
                string = json.dumps(shelf)
                savefile.write(string)
                self.mod_logger.info("Game saved on the file: \
                        %(savefile)s" % locals())

    def loadGame(self):
        """
        Opens the game from a json file
        """
        Tk().withdraw()
        formats = [("Glitch_Heaven Savegame", "*.dat")]
        path = filedialog.askopenfilename(filetypes=formats,
                                          initialdir="savegames",
                                          multiple=False)
        if not path:
            raise FileNotFoundError
        self.mod_logger.info("Loading Save from: %(path)s"
                             % locals())
        with open(path, "r") as savefile:
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
        if self.mode.lower() in ["criticalfailure", "cfsingle"]:
            self.mod_logger.debug("Using Load Game mode -\
                    Critical Failure Modifier")
            self.redsurf = pygame.surface.Surface((800, self.gsize[1]),
                                                  pygame.SRCALPHA)
            linesize = 3
            bot = self.redsurf.get_rect().bottom
            self.redsurf.fill((255, 0, 0, 50))
            self.redsurf.fill((255, 255, 255, 255),
                              pygame.rect.Rect(0,
                                               bot - linesize,
                                               800,
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
        lvl = self.tilemap.layers["Triggers"].find("playerExit")[0]
        return lvl["playerExit"]

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
        self.mainLogger = log
        self.mod_logger = log.getChild("game")
        self.mod_logger.info("Entering main game")
        self.running = True
        self.time = 0.
        self.sounds = sounds
        self.DCactive = config.getboolean("Video", "deathcounter")
        self.deathCounter = 0
        self.mode = mode
        self.bgpath, self.mbackpath = 2 * [None]
        self.middlepath, self.overpath = 2 * [None]
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
        self.modifiers = modifiers
        self.mod_logger.debug("Current Active Modifiers: {0}".format(
            self.modifiers))
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
                                            )
                }
        # ^-------------------------------------------------------------------^
        # Defines if a level should be loaded or a
        # new campaign should be started.
        # v--------------------------------------------------------------v
        if self.mode.lower() == "load":
            self.mod_logger.debug("Using Load mode")
            try:
                self.loadGame()
                self.LoadLevel(self.currentLevel, self.campaignname,
                               self.mode, self.screen)
            except FileNotFoundError:
                self.mod_logger.info("No file provided, loading cancelled")
                self.running = False
        elif self.mode.lower() == "newgame":
            self.mod_logger.debug("Using New Game mode")
            self.campaignFile = cmp
            self.campaignname = splitext(basename(cmp))[0]
            self.loadCampaign(self.campaignFile, self.mode)
            self.LoadLevel(self.currentLevel, self.campaignname,
                           self.mode, self.screen)
        elif self.mode.lower() in ["criticalfailure", "cfsingle"]:
            self.mod_logger.debug("Using New Game mode - \
                    Critical Failure Modifier")
            self.cftime = 0
            self.campaignFile = cmp
            self.campaignname = splitext(basename(cmp))[0]
            self.loadCampaign(self.campaignFile, self.mode)
            self.redsurf = pygame.surface.Surface((800, self.gsize[1]),
                                                  pygame.SRCALPHA)
            linesize = 3
            bot = self.redsurf.get_rect().bottom
            self.redsurf.fill((255, 0, 0, 50))
            self.redsurf.fill((255, 255, 255, 255),
                              pygame.rect.Rect(0,
                                               bot - linesize,
                                               800,
                                               linesize))
            self.redsurfrect = self.redsurf.get_rect()
            self.LoadLevel(self.currentLevel, self.campaignname,
                           self.mode, self.screen)
        elif self.mode.lower() == "singlemap":
            self.RealLoadLevel(cmp, "singlemap", self.screen)
        # ^--------------------------------------------------------------^
        self.fps = 30
        self.garble = False
        self.garbletimer = _garbletimer_
        self.deadbodies = pygame.sprite.Group()
        self.screengarble = pygame.image.load(pathjoin("resources",
                                                       "backgrounds",
                                                       "screengarble.png")
                                              ).convert_alpha()
        pygame.display.set_caption("Glitch_Heaven - Pre-Pre-Alpha Version")
        if self.running:
            self.loadLevelPart2(self.keys, sounds)
            self.mod_logger.debug("Glitches Loaded: {0}".format(self.glitches))
        """Game Loop"""
        while self.running:
            dt = self.clock.tick(self.fps)/1000.
            dt = min(0.05, dt)
            # For Critical Failure mode
            # v-------------------------------------------------------------------v
            if self.mode.lower() in ["criticalfailure", "cfsingle"]:
                self.time += dt
                self.redsurfrect.y = -self.gsize[1] + \
                    (self.gsize[1] * self.time) / self.cftime
                self.rcftime = self.cftime - self.time
                self.timer = makeGlitched("Time Before Failure: {0}".format(
                    str(timedelta(seconds=self.rcftime))),
                                          self.font)
                if self.redsurfrect.y > 0:
                    pygame.mouse.set_visible(True)  # Make the cursor visible
                    self.running = False
            # ^-------------------------------------------------------------------^
            # For Chaos Mode
            # v-------------------------------------------------------------------v
            if self.modifiers["chaos"]:
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
                        if event.key == pygame.K_BACKSPACE and not self.mode in ["singlemap"]:
                            self.mod_logger.debug("Debug key used, " +
                                                  "Loading next level")
                            level = self.forceNextLevel()
                            self.LoadLevel(level, self.campaignname,
                                           self.mode, self.screen)

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
                if event.type == pygame.QUIT:
                    self.running = False
                # ^----------------------------------------------------------^
                # Renders the DeathCounter
                # v-------------------------------------------------------------------v
                if self.DCactive:
                    self.dcounttxt = makeGlitched("Deaths: %d"
                                                  % self.deathCounter,
                                                  self.font)
                # ^-------------------------------------------------------------------^
            self.backpos = (min(-self.tilemap.viewport.x/6, 0),
                            min(-self.tilemap.viewport.y / 6, 0))
            self.middlebackpos = (min(-self.tilemap.viewport.x/4, 0),
                                  min(-self.tilemap.viewport.y / 4, 0))
            self.middlepos = (min(-self.tilemap.viewport.x/2, 0),
                              min(-self.tilemap.viewport.y / 2, 0))
            self.gameviewport.blit(self.bg, self.backpos)
            self.gameviewport.blit(self.middleback, self.middlebackpos)
            self.tilemap.update(dt, self)
            self.helptxts.update(dt, self)
            self.gameviewport.blit(self.middle, self.middlepos)
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
            if self.mode.lower() in ["criticalfailure", "cfsingle"]:
                self.gameviewport.blit(self.redsurf, (0, self.redsurfrect.y))
            if self.modifiers["vflip"] or self.modifiers["hflip"]:
                self.gameviewport = pygame.transform.flip(
                        self.gameviewport,
                        self.modifiers["hflip"],
                        self.modifiers["vflip"])
            screen.blit(self.gameviewport, (0, 0))
            if self.mode.lower() in ["criticalfailure", "cfsingle"]:
                screen.blit(self.timer, (50, 70))
            screen.blit(self.titleholder, (0, 576))
            screen.blit(self.title, self.titleposition)
            if self.DCactive:
                screen.blit(self.dcounttxt, (50, 50))
            if self.garble:
                screen.blit(self.screengarble, (0, 0))
                self.garbletimer -= dt
                if self.garbletimer <= 0:
                    self.garble = False
                    self.garbletimer = _garbletimer_
            pygame.display.update()
