# Comicbook-style Intermission Reader
# Part of the Glitch_Heaven project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
import pygame
from os import listdir
from os.path import join as pjoin
# from os.path import isfile


class comicReader(object):

    def __init__(self, path, screen, logger):
        super()
        self.path = path
        self.mod_logger = logger.getChild("intermission")
        self.imagelist = [x for x in listdir(path)]
        self.images = [pygame.image.load(pjoin(path, x)).convert_alpha()
                       for x in sorted(self.imagelist)]
        self.iter = iter(self.images)
        self.blitting = next(self.iter)
        self.screen = screen
        self.running = True
        self.currentrect = self.blitting.get_rect()
        self.screenctr = self.screen.get_rect().center
        self.currentrect.center = self.screenctr
        self.font = pygame.font.Font(pjoin(
                            "resources", "fonts",
                            "TranscendsGames.otf"), 16)
        self.write1 = self.font.render("Press enter to continue",
                                       False, (255, 255, 255))
        self.write2 = self.font.render("Press ESC to skip",
                                       False, (255, 255, 255))

    def get_factor(self, img, bx, by):
        ix, iy = img.get_size()
        if ix > iy:
            # fit to width
            scale_factor = bx/float(ix)
            sy = scale_factor * iy
            if sy > by:
                scale_factor = by/float(iy)
                sx = scale_factor * ix
                sy = by
            else:
                sx = bx
        else:
            # fit to height
            scale_factor = by/float(iy)
            sx = scale_factor * ix
            if sx > bx:
                scale_factor = bx/float(ix)
                sx = bx
                sy = scale_factor * iy
            else:
                sy = by
        return (int(sx), int(sy))

    def look(self):
        self.clock = pygame.time.Clock()
        while self.running:
            self.screen.fill((0, 0, 0))
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        try:
                            self.mod_logger.debug("Getting next picture")
                            self.blitting = next(self.iter)
                            self.blitting = pygame.transform.scale(
                                    self.blitting,
                                    self.get_factor(self.blitting, 800, 600))
                            self.currentrect = self.blitting.get_rect()
                            self.currentrect.center = self.screenctr
                        except StopIteration:
                            self.mod_logger.debug("Iterator ended, stopping")
                            self.running = False
                    elif event.key == pygame.K_ESCAPE:
                        self.mod_logger.debug("Player stopped iteration, \
                                ending")
                        self.running = False
            self.screen.blit(self.blitting, self.currentrect.topleft)
            self.screen.blit(self.write1, (10, 10))
            self.screen.blit(self.write2, (10, 25))
            pygame.display.update()
