# Text Insertion Test
import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
font = pygame.font.SysFont("Arial", 24)
writing = []
accepted = [
    pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d, pygame.K_e,
    pygame.K_f, pygame.K_g, pygame.K_h, pygame.K_i, pygame.K_j,
    pygame.K_k, pygame.K_l, pygame.K_m, pygame.K_n, pygame.K_o,
    pygame.K_p, pygame.K_q, pygame.K_r, pygame.K_s, pygame.K_t,
    pygame.K_u, pygame.K_v, pygame.K_w, pygame.K_x, pygame.K_y,
    pygame.K_z, pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3,
    pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8,
    pygame.K_9, pygame.K_KP0, pygame.K_KP1, pygame.K_KP2, pygame.K_KP3,
    pygame.K_KP4, pygame.K_KP5, pygame.K_KP6, pygame.K_KP7, pygame.K_KP8,
    pygame.K_KP9
]
surf= pygame.surface.Surface((800, 200))
surf.fill((255, 0, 0))

while True:
    screen.fill((0, 0, 0))
    surf.fill((255, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if len(writing)!=0:
                    writing.pop()
            elif event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                print("Text sent: ", "".join(writing))
            elif event.key in accepted:
                if not (pygame.key.get_mods() & pygame.KMOD_LCTRL):
                    writing.append(event.unicode)
    write = font.render("".join(writing), False, (255, 255, 255))
    wrect = write.get_rect()
    wrect.center = surf.get_rect().center
    surf.blit(write, wrect)
    screen.blit(surf, (0, 200))
    pygame.display.update()