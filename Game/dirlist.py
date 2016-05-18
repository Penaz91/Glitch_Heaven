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
        itemno = len(dirlist)
        self.itemList = []
        if save:
            itemno+=1
            # Create save menu button
        width = 300
        itemH = 20
        spacing = 10
        self.font = pygame.font.Font(pjoin("resources",
                                      "fonts",
                                      "TranscendsGames.otf"), itemH)
        height = (2*itemno - 1) * itemH
        self.surface = pygame.surface.Surface((width, height))
        xpos, ypos = 0, 0
        for item in dirlist:
            self.itemList.append(menuItem.menuitem(
                self.font.render(item, False, (255,255,255)).convert_alpha(),
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
        for item in self.itemList:
            self.surface.blit(item.image, item.rect.topleft)
            
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((640,480))
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
    loadList = dirList(pjoin("savegames"), False, config, sounds)
    while True:
        loadList.update()
        screen.blit(loadList.surface, (0,0))
        pygame.display.update()