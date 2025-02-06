import pygame, random
pygame.init()
clock = pygame.time.Clock()

win_width = 640
win_height = 480
window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('Pygame Shapes!')

blue_square_x = 0.0
blue_square_y = 0.0
blue_square_vx = 1
blue_square_vy = 1

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    # Begin drawing statements
    window.fill((0,0,0))
    pygame.draw.rect(window, (0, 0, 255),
                     (blue_square_x, blue_square_y, 10, 10))
    blue_square_x += blue_square_vx
    blue_square_y += blue_square_vy
    blue_square_vx += 0.1
    blue_square_vy += 0.1
    # End drawing statements

    pygame.display.flip()
    clock.tick(60)
