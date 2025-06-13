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
    pygame.draw.rect(window, (255,0,0), (100, 100, 25, 25))
    pygame.draw.rect(window, (0,255,0), (200, 150, 25, 25))
    pygame.draw.rect(window, (0,0,255), (300, 200, 25, 25))
    # End drawing statements

    pygame.display.update()
    clock.tick(60)