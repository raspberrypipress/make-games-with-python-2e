import pygame, random
pygame.init()
clock = pygame.time.Clock()

win_width = 640
win_height = 480
window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('Pygame Shapes!')

red_level = random.randint(0, 255)
green_level = random.randint(0, 255)
blue_level = random.randint(0, 255)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    # Begin drawing statements
    window.fill((0,0,0))
    pygame.draw.rect(window, 
                     (red_level, green_level, blue_level),
                     (50, 50, win_width / 2, win_height / 2))
    if red_level >= 255:
        red_level = random.randint(0, 255)
    else:
        red_level += 1
    if green_level >= 255:
        green_level = random.randint(0, 255)
    else:
        green_level += 1
    if blue_level >= 255:
        blue_level = random.randint(0, 255)
    else:
        blue_level += 1
    # End drawing statements

    pygame.display.flip()
    clock.tick(60)
