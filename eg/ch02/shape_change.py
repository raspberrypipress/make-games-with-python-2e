import pygame, sys, random
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS

pygame.init()
clock = pygame.time.Clock()

win_width = 640
win_height = 480
surface = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('Pygame Shapes!')

rect_x = win_width / 2
rect_y = win_height / 2
rect_width = 50
rect_height = 50

while True:
    surface.fill((0,0,0))
    pygame.draw.rect(surface, (255,255,0), 
                     (rect_x - rect_width / 2, rect_y - rect_height / 2,
                      rect_width, rect_height))
    rect_width += 1
    rect_height += 1

    for event in GAME_EVENTS.get():
        if event.type == GAME_GLOBALS.QUIT:
            pygame.quit()
            sys.exit()
    clock.tick(60)
    pygame.display.update()