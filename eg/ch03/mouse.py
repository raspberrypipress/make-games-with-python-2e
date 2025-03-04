import pygame, sys

# Pygame setup and variables
pygame.init()
clock = pygame.time.Clock()
win_width = 800
win_height = 800

surface = pygame.display.set_mode((win_width, win_height))

pygame.display.set_caption('Pygame Mouse!')

# Gameplay Variables
square_size = 40
square_x = win_width / 2
square_y = win_height - square_size
gravity = 2.0
mouse_pressed = False
is_dragging = False

def checkBounds():

    global is_dragging

    if mouse_pressed:
        box = pygame.Rect((square_x, square_y, square_size, square_size))
        if box.collidepoint(pygame.mouse.get_pos()):
            is_dragging = True
            pygame.mouse.set_visible(0)
    else:
        pygame.mouse.set_visible(1)
        is_dragging = False

def checkGravity():

    global gravity, square_y

    # Is our square in the air and have we let go of it?
    if square_y < win_height - square_size and not mouse_pressed:
        square_y += gravity
        gravity = gravity * 1.05
    else:
        square_y = win_height - square_size
        gravity = 2.0

def drawSquare():

    global square_x, square_y

    if is_dragging:
        square_colour = (0, 255, 0)
        mouse_pos = pygame.mouse.get_pos()
        square_x = mouse_pos[0] - square_size / 2
        square_y = mouse_pos[1] - square_size / 2
    else:
        square_colour = (255,0,0)

    pygame.draw.rect(surface, square_colour, (square_x, square_y, square_size, square_size))

while True:

    surface.fill((0,0,0))

    checkBounds()
    checkGravity()
    drawSquare()

    pygame.display.update()
    clock.tick(60)

    for event in pygame.event.get():
        mouse_pressed = pygame.mouse.get_pressed()[0]
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
