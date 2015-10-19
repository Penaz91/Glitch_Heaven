import pygame
pygame.init()
screen=pygame.display.set_mode((320,240))
while 1:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            break
        if event.type==pygame.KEYDOWN:
            print(event.key)
pygame.quit()
quit()
