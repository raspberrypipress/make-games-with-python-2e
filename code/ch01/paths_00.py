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
    pygame.draw.line(window, (0,255,0),
                     (150, 150), (225, 225), True)
    pygame.draw.line(window, (0, 255, 0),
                      (225, 225), (75, 225), True)
    pygame.draw.line(window, (0, 255, 0),
                     (75, 225), (150, 150), True)
    # End drawing statements

    pygame.display.update()
    clock.tick(60)