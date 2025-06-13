import pygame
pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((500, 400))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    # Begin drawing statements
    pygame.draw.circle(window,(255,255,0),
                       (200, 200), 20, 0)
    # Not filled
    pygame.draw.circle(window,(255,255,0),
                       (300, 200), 20, 2)
    # End drawing statements

    pygame.display.update()
    clock.tick(60)