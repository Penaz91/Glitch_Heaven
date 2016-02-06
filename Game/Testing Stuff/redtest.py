import pygame
pygame.init()
size = (800, 600)
y = - size[1]
secs = 60
screen = pygame.display.set_mode(size)
redsurf = pygame.surface.Surface(size, pygame.SRCALPHA)
whitesurf = pygame.surface.Surface((200, 200))
whitesurf.fill((255, 255, 255))
redsurf.fill((255, 0, 0, 127))
# v-----------------------------------------------------------------v
# ^-----------------------------------------------------------------^
clock = pygame.time.Clock()
Truth = True
time = 0.
x = 50
while Truth:
    print(y)
    dt = clock.tick(30)
    time += dt/1000.
    y = -size[1] + (600 * time) / secs
    if y > 0:
        y = - size[1]
        time = 0.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Truth = False
    screen.fill((0, 0, 0))
    screen.blit(whitesurf, (100, 100))
    screen.blit(redsurf, (0, y))
    pygame.display.update()
pygame.quit()
quit()
