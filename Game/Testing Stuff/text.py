import pygame
import os
pygame.init()
screen = pygame.display.set_mode((800, 240))
font = pygame.font.Font(os.path.join("..",
                                     "resources", "fonts",
                                     "TranscendsGames.otf"), 32)
purple = font.render("Start the Main Campaign",
                     False,
                     (236, 0, 200)).convert_alpha()
green = font.render("Start the Main Campaign",
                    False,
                    (0, 236, 5)).convert_alpha()
white = font.render("Start the Main Campaign",
                    False,
                    (255, 255, 255)).convert_alpha()
entire = pygame.surface.Surface((purple.get_width() + 5, purple.get_height()))
entire.blit(purple, (0, 0))
entire.blit(green, (4, 0))
entire.blit(white, (2, 0))
clock = pygame.time.Clock()
while 1:
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
    screen.blit(entire, (50, 120))
    pygame.display.update()
pygame.quit()
quit()
