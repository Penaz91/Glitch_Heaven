# Keyboard Settings Component
# Part of the Glitch_Heaven project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
from components.UI.menu import menu
from components.UI import keyboarditem as kitem
from components.UI import menuItem
from libs.textglitcher import makeGlitched
import pygame


class KeyboardSettings(menu):

    def __init__(self, screen, keys, config, sounds):
        self.writings = []
        self.logSectionName = "Glitch_Heaven.KeyboardSettings"
        super().__init__(screen, keys, config, sounds)

    def makeLeftKeyItem(self):
        # ^------------------------------------------------------------------^
        # "Left Key" menu element
        # v------------------------------------------------------------------v
        self.lefttext = self.font.render("Move Left: ",
                                         False,
                                         (255, 255, 255)).convert_alpha()
        key = self.config.get("Controls", "left")
        keytext = str(pygame.key.name(int(key)))
        self.leftimg = self.font.render(keytext.upper(),
                                        False, (255, 255, 255)).convert_alpha()
        self.leftsel = makeGlitched(keytext.upper(), self.font)
        self.left = kitem.KeyboardItem(self.leftimg,
                                       self.leftsel,
                                       (self.lefttext.get_rect().width + 70,
                                           180),
                                       lambda: None,
                                       lambda: self.left.KeySelect(self.font,
                                                                   "left",
                                                                   self.config,
                                                                   self.keys),
                                       self.config,
                                       self.sounds)
        self.activeItems.append(self.left)
        self.items.append(self.left)
        self.writings.append((self.lefttext, (50, 180)))

    def makeRightKeyItem(self):
        # ^------------------------------------------------------------------^
        # "Right Key" menu element
        # v------------------------------------------------------------------v
        self.righttext = self.font.render("Move Right: ",
                                          False,
                                          (255, 255, 255)).convert_alpha()
        key = self.config.get("Controls", "right")
        keytext = str(pygame.key.name(int(key)))
        self.rightimg = self.font.render(keytext.upper(),
                                         False,
                                         (255, 255, 255)).convert_alpha()
        self.rightsel = makeGlitched(keytext.upper(), self.font)
        self.right = kitem.KeyboardItem(self.rightimg,
                                        self.rightsel,
                                        (self.righttext.get_rect().width + 70,
                                            240),
                                        lambda: None,
                                        lambda: self.right.KeySelect(
                                            self.font,
                                            "right",
                                            self.config,
                                            self.keys),
                                        self.config,
                                        self.sounds)
        self.activeItems.append(self.right)
        self.items.append(self.right)
        self.writings.append((self.righttext, (50, 240)))

    def makeJumpKeyItem(self):
        # ^------------------------------------------------------------------^
        # "Jump Key" menu element
        # v------------------------------------------------------------------v
        self.jumptext = self.font.render("Jump: ",
                                         False,
                                         (255, 255, 255)).convert_alpha()
        key = self.config.get("Controls", "jump")
        keytext = str(pygame.key.name(int(key)))
        self.jumpimg = self.font.render(keytext.upper(),
                                        False, (255, 255, 255)).convert_alpha()
        self.jumpsel = makeGlitched(keytext.upper(), self.font)
        self.jump = kitem.KeyboardItem(self.jumpimg,
                                       self.jumpsel,
                                       (self.jumptext.get_rect().width + 70,
                                           300),
                                       lambda: None,
                                       lambda: self.jump.KeySelect(self.font,
                                                                   "jump",
                                                                   self.config,
                                                                   self.keys),
                                       self.config,
                                       self.sounds)
        self.activeItems.append(self.jump)
        self.items.append(self.jump)
        self.writings.append((self.jumptext, (50, 300)))

    def makeRunKeyItem(self):
        # ^------------------------------------------------------------------^
        # "Run Key" menu element
        # v------------------------------------------------------------------v
        self.runtext = self.font.render("Run: ",
                                        False,
                                        (255, 255, 255)).convert_alpha()
        key = self.config.get("Controls", "run")
        keytext = str(pygame.key.name(int(key)))
        self.runimg = self.font.render(keytext.upper(),
                                       False,
                                       (255, 255, 255)).convert_alpha()
        self.runsel = makeGlitched(keytext.upper(), self.font)
        self.run = kitem.KeyboardItem(self.runimg,
                                      self.runsel,
                                      (self.runtext.get_rect().width + 70,
                                          360),
                                      lambda: None,
                                      lambda: self.run.KeySelect(self.font,
                                                                 "run",
                                                                 self.config,
                                                                 self.keys),
                                      self.config,
                                      self.sounds)
        self.activeItems.append(self.run)
        self.items.append(self.run)
        self.writings.append((self.runtext, (50, 360)))

    def makeActionKeyItem(self):
        # ^------------------------------------------------------------------^
        # "Action Key" menu element
        # v------------------------------------------------------------------v
        self.acttext = self.font.render("Action/Interact: ",
                                        False, (255, 255, 255)).convert_alpha()
        key = self.config.get("Controls", "action")
        keytext = str(pygame.key.name(int(key)))
        self.actimg = self.font.render(keytext.upper(),
                                       False,
                                       (255, 255, 255)).convert_alpha()
        self.actsel = makeGlitched(keytext.upper(), self.font)
        self.act = kitem.KeyboardItem(self.actimg,
                                      self.actsel,
                                      (self.acttext.get_rect().width + 70,
                                          420),
                                      lambda: None,
                                      lambda: self.act.KeySelect(self.font,
                                                                 "action",
                                                                 self.config,
                                                                 self.keys),
                                      self.config,
                                      self.sounds)
        self.activeItems.append(self.act)
        self.items.append(self.act)
        self.writings.append((self.acttext, (50, 420)))

    def makeRestartKeyItem(self):
        # ^------------------------------------------------------------------^
        # "Restart Key" menu element
        # v------------------------------------------------------------------v
        self.resttext = self.font.render("Restart Level: ",
                                         False,
                                         (255, 255, 255)).convert_alpha()
        key = self.config.get("Controls", "restart")
        keytext = str(pygame.key.name(int(key)))
        self.restimg = self.font.render(keytext.upper(),
                                        False,
                                        (255, 255, 255)).convert_alpha()
        self.restsel = makeGlitched(keytext.upper(), self.font)
        self.rest = kitem.KeyboardItem(self.restimg,
                                       self.restsel,
                                       (self.resttext.get_rect().width + 70,
                                        480),
                                       lambda: None,
                                       lambda: self.rest.KeySelect(self.font,
                                                                   "restart",
                                                                   self.config,
                                                                   self.keys),
                                       self.config,
                                       self.sounds)
        self.activeItems.append(self.rest)
        self.items.append(self.rest)
        self.writings.append((self.resttext, (50, 480)))

    def makeMainMenuItem(self):
        # ^------------------------------------------------------------------^
        # "Main Menu" menu element
        # v------------------------------------------------------------------v
        self.menu = self.font.render("Previous Menu",
                                     False, (255, 255, 255)).convert_alpha()
        self.menusel = makeGlitched("Previous Menu", self.font)
        self.mainmenu = menuItem.menuitem(self.menu,
                                          self.menusel,
                                          (50, 560),
                                          lambda: None,
                                          lambda: self.goToMenu(),
                                          self.config,
                                          self.sounds)
        self.items.append(self.mainmenu)
        self.activeItems.append(self.mainmenu)
        # ^------------------------------------------------------------------^

    def makeMenuItems(self):
        self.makeLeftKeyItem()
        self.makeRightKeyItem()
        self.makeJumpKeyItem()
        self.makeRunKeyItem()
        self.makeActionKeyItem()
        self.makeRestartKeyItem()
        self.makeMainMenuItem()

    def doAdditionalBlits(self):
        for item in self.writings:
            self.screen.blit(*item)
