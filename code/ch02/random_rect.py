import pygame, random
pygame.init()
clock = pygame.time.Clock()

WIN_WIDTH = 640
WIN_HEIGHT = 480
window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Pygame Shapes!')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    # Begin drawing statements
    window.fill((0,0,0))
    x = random.randint(0, WIN_WIDTH)
    y = random.randint(0, WIN_HEIGHT)
    pygame.draw.rect(window, (255,0,0), (x, y, 10, 10))
    # End drawing statements

    pygame.display.update()
    clock.tick(60)
