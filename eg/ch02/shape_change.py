import pygame, random
pygame.init()
clock = pygame.time.Clock()

win_width = 640
win_height = 480
window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('Pygame Shapes!')

rect_x = win_width / 2
rect_y = win_height / 2
rect_width = 50
rect_height = 50

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    # Begin drawing statements
    window.fill((0,0,0))
    pygame.draw.rect(window, (255,255,0), 
                     (rect_x - rect_width / 2, 
                      rect_y - rect_height / 2,
                      rect_width, rect_height))
    rect_width += 1
    rect_height += 1
    # End drawing statements

    pygame.display.flip()
    clock.tick(60)
