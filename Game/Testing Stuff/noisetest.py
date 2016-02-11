import pygame
import numpy
pygame.init()
size = (1024, 768)
screen = pygame.display.set_mode(size)
whitesurf = pygame.surface.Surface((200, 200), 0, 32)
whitesurf.fill((255, 255, 255))
pygame.surfarray.use_arraytype("numpy")
ws = pygame.surfarray.array3d(whitesurf)
noise_small = numpy.random.random((50, 50)) * 0.2 + 0.4
noise_big = noise_small.repeat(4, 0).repeat(4, 1)
ws = (ws.astype(noise_big.dtype) * noise_big[:, :, numpy.newaxis]).astype(ws.dtype)
whitesurf = pygame.surfarray.make_surface(ws)
del ws
# v-----------------------------------------------------------------v
# ^-----------------------------------------------------------------^
clock = pygame.time.Clock()
Truth = True
time = 0.
x = 50
while Truth:
    dt = clock.tick(30) / 1000.
    screen.fill((0, 0, 0))
    screen.blit(whitesurf, (100, 100))
    pygame.display.update()
pygame.quit()
quit()
