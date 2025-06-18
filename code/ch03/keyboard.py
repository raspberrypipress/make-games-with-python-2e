import pygame

# Pygame Variables
pygame.init()
clock = pygame.time.Clock()

WIN_WIDTH = 800
WIN_HEIGHT = 800

surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Pygame Keyboard!')

# Constants
PLAYER_SIZE = 20
MAXJUMP_VY = 25.0
MOVE_SPEED = 1.0
MAX_VX = 10.0

# Variables
player_x = (WIN_WIDTH / 2) - (PLAYER_SIZE / 2)
player_y = WIN_HEIGHT - PLAYER_SIZE
player_vx = 1.0
player_vy = 0.0
gravity = 1.0

def move(direction, jump):
    global player_x, player_y, player_vx, player_vy, gravity

    # Did we switch direction along the x axis?
    if (direction > 0 and player_vx < 0) or (direction < 0 and
                                             player_vx > 0):
        player_vx = MOVE_SPEED * direction

    # Move the player along the x axis
    if direction != 0:
        player_x += player_vx
    
    # Keep the player within the screen bounds along the x axis
    if player_x > WIN_WIDTH - PLAYER_SIZE:
        player_x = WIN_WIDTH - PLAYER_SIZE
    if player_x < 0:
        player_x = 0

    # If we're not already jumping, max out the y velocity
    if jump and player_y == WIN_HEIGHT - PLAYER_SIZE:
        player_vy = MAXJUMP_VY

    if player_vy > 1.0:
        # Decrease player_vy throughout the jump
        player_vy = player_vy * 0.9
    else:
        player_vy = 0.0

    # Is our square in the air? 
    # Better add some gravity to bring it back down!
    if player_y < WIN_HEIGHT - PLAYER_SIZE:
        player_y += gravity
        gravity = gravity * 1.1
    else: # Reset gravity so it starts at 1.0 next time we jump
        gravity = 1.0
    
    # Move the player along the y axis
    player_y -= player_vy

    # Don't let the player fall through the floor
    player_y = min(player_y, WIN_HEIGHT - PLAYER_SIZE)

    # Increase x velocity if we're moving but not at maximum.
    if direction and abs(player_vx) < MAX_VX:
        # But only if we're not in the air!
        if player_y >= WIN_HEIGHT - PLAYER_SIZE:
            player_vx = player_vx * 1.1

# How to quit our program
def quitGame():
    pygame.quit()
    raise SystemExit

while True:

    surface.fill((0,0,0))

    jump = False

    # Get all events since the last redraw
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quitGame()
            if event.key == pygame.K_UP:
                jump = True

        if event.type == pygame.QUIT:
            quitGame()

    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_LEFT]:
        move(-1, jump)
    elif pressed_keys[pygame.K_RIGHT]:
        move(1, jump)
    else:
        move(0, jump)

    pygame.draw.rect(surface, (255,0,0), 
                     (player_x, player_y, 
                      PLAYER_SIZE, PLAYER_SIZE))

    pygame.display.update()

    clock.tick(60)