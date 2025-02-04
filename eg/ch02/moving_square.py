import pygame, sys, random
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS

pygame.init()
win_width = 640
win_height = 480
surface = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('Pygame Shapes!')

green_square_x = win_width / 2
green_square_y = win_height / 2

while True:
    surface.fill((0,0,0))
    pygame.draw.rect(surface, (0, 255, 0), 
                     (green_square_x, green_square_y, 10, 10))
    green_square_x += 1
    #green_square_y += 1
    for event in GAME_EVENTS.get():
        if event.type == GAME_GLOBALS.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
