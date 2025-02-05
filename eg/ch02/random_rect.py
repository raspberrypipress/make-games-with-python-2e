import pygame, sys, random
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS

pygame.init()
clock = pygame.time.Clock()

win_width = 640
win_height = 480
surface = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('Pygame Shapes!')

while True:
    surface.fill((0,0,0))
    x = random.randint(0, win_width)
    y = random.randint(0, win_height)
    pygame.draw.rect(surface, (255,0,0), (x, y, 10, 10))
    for event in GAME_EVENTS.get():
        if event.type == GAME_GLOBALS.QUIT:
            pygame.quit()
            sys.exit()
    clock.tick(60)
    pygame.display.update()
