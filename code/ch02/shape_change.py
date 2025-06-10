import pygame, random
pygame.init()
clock = pygame.time.Clock()

WIN_WIDTH = 640
WIN_HEIGHT = 480
window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Pygame Shapes!')

rect_x = WIN_WIDTH / 2
rect_y = WIN_HEIGHT / 2
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

    pygame.display.update()
    clock.tick(60)
