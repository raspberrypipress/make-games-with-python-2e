import pygame, random
pygame.init()
clock = pygame.time.Clock()

win_width = 640
win_height = 480
window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('Pygame Shapes!')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    # Begin drawing statements
    window.fill((0,0,0))
    x = random.randint(0, win_width)
    y = random.randint(0, win_height)
    pygame.draw.rect(window, (255,0,0), (x, y, 10, 10))
    # End drawing statements

    pygame.display.update()
    clock.tick(60)
