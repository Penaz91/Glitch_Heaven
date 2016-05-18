# Directory Listing Component
# Part of the Glitch_Heaven project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
import pygame
from os import listdir
from os.path import join as pjoin
from components.UI import menuItem
from libs.textglitcher import makeGlitched
import json


class dirList(object):
    def __init__(self, directory, save, config, sounds):
        dirlist = listdir(directory)
        width = 300
        itemH = 20
        spacing = 10
        self.location = (100, 50)
        itemno = len(dirlist)
        self.itemList = []
        xpos, ypos = 0, 0
        self.font = pygame.font.Font(pjoin("resources",
                                           "fonts",
                                           "TranscendsGames.otf"), itemH)

        if save:
            self.itemList.insert(0,
                                 menuItem.menuitem(
                                     self.font.render("<make new>",
                                                      False,
                                                      (255, 255, 255)
                                                      ).convert_alpha(),
                                     makeGlitched("<make new>", self.font),
                                     (0, 0),
                                     lambda: None,
                                     lambda: None,
                                     config,
                                     sounds
                                     )
                                 )
            ypos += itemH + spacing
            itemno += 1
            # Create save menu button

        self.selectionrect = pygame.surface.Surface((width, itemH),
                                                    pygame.SRCALPHA)
        self.selectlocation = (0, 0)
        self.selectionrect.fill((255, 255, 255, 200))
        height = (2*itemno - 1) * itemH
        self.surface = pygame.surface.Surface((width, height))
        self.selectedItem = None

        for item in dirlist:
            self.itemList.append(menuItem.menuitem(
                self.font.render(item, False, (255, 255, 255)).convert_alpha(),
                makeGlitched(item, self.font),
                (xpos, ypos),
                lambda: None,
                lambda: None,
                config,
                sounds
                )
            )
            ypos += itemH + spacing

    def update(self):
        self.surface.fill((0, 0, 0))
        for item in self.itemList:
            self.surface.blit(item.image, item.rect.topleft)
        if self.selectedItem is not None:
            self.selectlocation = self.selectedItem.rect.topleft
            self.surface.blit(self.selectionrect, self.selectlocation)

    def selectItem(self, item):
        self.selectedItem = item

    def checkMouseHover(self):
        for item in loadList.itemList:
            collpt = [i1 - i2 for i1, i2
                      in zip(pygame.mouse.get_pos(), self.location)]
            if item.rect.collidepoint(collpt):
                item.makeSelected()
            else:
                item.makeUnselected()

    def checkMouseClick(self):
        for item in loadList.itemList:
            collpt = [i1 - i2 for i1, i2
                      in zip(pygame.mouse.get_pos(), self.location)]
            if item.rect.collidepoint(collpt):
                self.selectItem(item)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    with open(pjoin("config.json")) as conf:
        config = json.loads(conf.read())
    sounds = {
                "sfx": {
                    "jump": pygame.mixer.Sound(pjoin("resources",
                                                     "sounds",
                                                     "jump.wav")),
                    "death": pygame.mixer.Sound(pjoin("resources",
                                                      "sounds",
                                                      "death.wav")),
                    "bounce": pygame.mixer.Sound(pjoin("resources",
                                                       "sounds",
                                                       "bounce.wav")),
                    "static": pygame.mixer.Sound(pjoin("resources",
                                                       "sounds",
                                                       "static.wav"))
                    },
                "menu": {
                    "test": pygame.mixer.Sound(pjoin("resources",
                                                     "sounds",
                                                     "testSound.wav")),
                    "select": pygame.mixer.Sound(pjoin("resources",
                                                       "sounds",
                                                       "menuSelect.wav")),
                    "confirm": pygame.mixer.Sound(pjoin("resources",
                                                        "sounds",
                                                        "select.wav"))
                    },
                "music": {}}
    loadList = dirList(pjoin("savegames"), True, config, sounds)
    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                loadList.checkMouseHover()
            elif event.type == pygame.MOUSEBUTTONUP:
                loadList.checkMouseClick()
        loadList.update()
        screen.blit(loadList.surface, loadList.location)
        pygame.display.update()
