import pygame

pygame.init()
clock = pygame.time.Clock()
FPS = 60

WIN_WIDTH = 800
WIN_HEIGHT = 800
window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Pygame Mouse!')

SQUARE_SIZE = 40
square_x = WIN_WIDTH / 2
square_y = WIN_HEIGHT - SQUARE_SIZE
gravity = 2.0
pressed = False
is_dragging = False

def check_bounds():
    global is_dragging

    if pressed:
        box = pygame.Rect((square_x, square_y, 
                           SQUARE_SIZE, SQUARE_SIZE))
        if box.collidepoint(pygame.mouse.get_pos()):
            is_dragging = True
            pygame.mouse.set_visible(0)
    else:
        is_dragging = False
        pygame.mouse.set_visible(1)

def check_gravity():
    global gravity, square_y

    # Is our square in the air 
    if square_y < WIN_HEIGHT - SQUARE_SIZE:
        if not is_dragging: # have we let go of it?
            square_y += gravity
            gravity = gravity * 1.05
    else:
        square_y = WIN_HEIGHT - SQUARE_SIZE
        gravity = 2.0

def draw_square():
    global square_x, square_y

    if is_dragging:
        square_colour = (0, 255, 0)
        mouse_pos = pygame.mouse.get_pos()
        square_x = mouse_pos[0] - SQUARE_SIZE / 2
        square_y = mouse_pos[1] - SQUARE_SIZE / 2
    else:
        square_colour = (255,0,0)

    pygame.draw.rect(window, square_colour,
                     (square_x, square_y,
                      SQUARE_SIZE, SQUARE_SIZE))

def quit_game():
    pygame.quit()
    raise SystemExit

while True:
    window.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit_game()
        if event.type == pygame.QUIT:
            quit_game()

    pressed = pygame.mouse.get_pressed()[0]

    check_bounds()
    check_gravity()
    draw_square()

    pygame.display.update()
    clock.tick(FPS)