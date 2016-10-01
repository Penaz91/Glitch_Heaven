# Generic Menu Component
# Part of the Glitch_Heaven Project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
import pygame
from os.path import join as pathjoin
from libs.textglitcher import makeGlitched
from libs.timedanimation import TimedAnimation


class menu(object):

    def __init__(self, screen, keys, config, sounds, log):
        self.mainLogger = log
        self.modlogger = log.getChild(self.logSectionName)
        self.running = True
        self.currentItem = None
        self.keys = keys
        self.config = config
        self.sounds = sounds
        self.update = False
        self.background = pygame.image.load(pathjoin("resources",
                                                     "UI",
                                                     "back.png")
                                            ).convert_alpha()
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(True)
        self.modlogger.debug("Mouse Cursor Shown")
        pygame.display.set_caption("Glitch_Heaven")
        self.screen = screen
        self.screensize = screen.get_size()
        self.font = pygame.font.Font(pathjoin("resources",
                                              "fonts",
                                              "TranscendsGames.otf"), 24)
        """self.titleTimings = [0.12]*24
        self.titleTimings[0], self.titleTimings[19] = 2., 2.
        self.titleani = TimedAnimation(self.titleTimings)
        self.titleani.loadFromDir(pathjoin("resources",
                                           "UI",
                                           "AnimatedTitle"))"""
        self.titleani = TimedAnimation([(2., 1), (0.12, 18),
                                        (2., 1), (0.12, 4)],
                                       pathjoin("resources",
                                                "UI",
                                                "AnimatedTitle"))
        self.title = self.titleani.next(0)
        self.titlesize = self.title.get_size()
        self.titlerect = self.title.get_rect()
        self.titlerect.x = self.screensize[0] / 2 - self.titlesize[0] / 2
        self.titlerect.y = 32
        self.items = []
        self.activeItems = []
        self.desc = None

    def doAdditionalClosingOperations(self):
        pass

    def doMoreLoopOperations(self):
        pass

    def makeMenuItems(self):
        pass

    def onEscape(self):
        self.goToMenu()

    def doAdditionalKeyboardHandling(self):
        pass

    def doAdditionalMouseHandling(self):
        pass

    def doAdditionalBlits(self):
        pass

    def doAdditionalMotionHandling(self):
        pass

    def doExternalClickHandling(self):
        pass

    def goToMenu(self):
        self.doAdditionalClosingOperations()
        self.modlogger.info("Going to the previous menu")
        self.running = False

    def editDesc(self, string):
        self.desc = makeGlitched(string, self.font)

    def mainLoop(self):
        self.makeMenuItems()
        while self.running:
            self.dt = self.clock.tick(30)/1000.
            self.doMoreLoopOperations()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    if self.currentItem is None:
                        self.currentItem = 0
                    if event.key == self.keys["down"]:
                        self.currentItem = ((self.currentItem + 1) %
                                            len(self.activeItems))
                    if event.key == self.keys["up"]:
                        self.currentItem = ((self.currentItem - 1) %
                                            len(self.activeItems))
                    if event.key == self.keys["confirm"]:
                        self.activeItems[self.currentItem].confirmSound.play()
                        self.activeItems[self.currentItem].function()
                    if event.key == self.keys["escape"]:
                        self.onEscape()
                    self.doAdditionalKeyboardHandling()
                    for item in self.activeItems:
                        item.makeUnselected()
                    self.activeItems[self.currentItem].makeSelected()
                if event.type == pygame.MOUSEMOTION:
                    self.currentItem = None
                    for item in self.activeItems:
                        # Wrong code, selects/deselects continuously
                        if item.rect.collidepoint(*pygame.mouse.get_pos())\
                                and not item.selected:
                            item.makeSelected()
                        else:
                            item.makeUnselected()
                    self.doAdditionalMotionHandling()
                if event.type == pygame.MOUSEBUTTONUP:
                    for item in self.activeItems:
                        if item.rect.collidepoint(*pygame.mouse.get_pos()):
                            item.confirmSound.play()
                            item.function()
                            item.makeSelected()
                            # Found the item, break the cycle
                            break
                        self.doAdditionalMouseHandling()
                    self.doExternalClickHandling()
            self.title = self.titleani.next(self.dt)
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.title, (self.titlerect.topleft))
            if self.desc is not None:
                self.screen.blit(self.desc, (750 - self.desc.get_rect().width,
                                 300))
            for item in self.items:
                self.screen.blit(item.image, item.rect.topleft)
            self.doAdditionalBlits()
            pygame.display.update()
