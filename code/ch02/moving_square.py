import pygame, random
pygame.init()
clock = pygame.time.Clock()

WIN_WIDTH = 640
WIN_HEIGHT = 480
window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Pygame Shapes!')

green_square_x = WIN_WIDTH / 2
green_square_y = WIN_HEIGHT / 2

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    # Begin drawing statements
    window.fill((0,0,0))
    pygame.draw.rect(window, (0, 255, 0), 
                     (green_square_x, green_square_y, 10, 10))
    green_square_x += 1
    #green_square_y += 1
    # End drawing statements

    pygame.display.update()
    clock.tick(60)
