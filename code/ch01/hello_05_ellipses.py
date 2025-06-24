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
    pygame.draw.rect(window, (255, 0, 0),
                     (100, 100, 100, 50), 2)
    pygame.draw.ellipse(window, (255, 0, 0),
                        (100, 100, 100, 50))
    pygame.draw.rect(window, (0, 255, 0),
                     (100, 150, 80, 40), 2)
    pygame.draw.ellipse(window, (0, 255, 0),
                        (100, 150, 80, 40))
    pygame.draw.rect(window, (0, 0, 255),
                     (100, 190, 60, 30), 2)
    pygame.draw.ellipse(window, (0, 0, 255),
                        (100, 190, 60, 30))
    #Circle
    pygame.draw.ellipse(window, (0, 0, 255),
                                (100, 250, 40, 40))

    # End drawing statements

    pygame.display.update()
    clock.tick(60)