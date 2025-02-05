import pygame, sys, random
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS

pygame.init()
clock = pygame.time.Clock()

win_width = 640
win_height = 480
surface = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('Pygame Shapes!')

blue_square_x = 0.0
blue_square_y = 0.0
blue_square_vx = 1
blue_square_vy = 1

while True:
    surface.fill((0,0,0))
    pygame.draw.rect(surface, (0, 0, 255),
                     (blue_square_x, blue_square_y, 10, 10))
    blue_square_x += blue_square_vx
    blue_square_y += blue_square_vy
    blue_square_vx += 0.1
    blue_square_vy += 0.1

    for event in GAME_EVENTS.get():
        if event.type == GAME_GLOBALS.QUIT:
            pygame.quit()
            sys.exit()
    clock.tick(60)
    pygame.display.update()


