import pygame, random
pygame.init()
clock = pygame.time.Clock()

# Constants
WIN_WIDTH = 640
WIN_HEIGHT = 480
# Set up display
window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
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
    # Draw rectangle with current color
    pygame.draw.rect(window, 
                     (red_level, green_level, blue_level),
                     (50, 50, WIN_WIDTH / 2, WIN_HEIGHT / 2))

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

    pygame.display.update()
    clock.tick(60)
