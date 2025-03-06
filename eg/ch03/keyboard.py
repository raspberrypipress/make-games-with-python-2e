import pygame

# Pygame Variables
pygame.init()
clock = pygame.time.Clock()

win_width = 800
win_height = 800

surface = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('Pygame Keyboard!')

# Square Variables
playerSize = 20
playerX = (win_width / 2) - (playerSize / 2)
playerY = win_height - playerSize
player_vx = 1.0
player_vy = 0.0
maxjump_vy = 25.0
move_speed = 1.0
max_vx = 10.0
gravity = 1.0

def move(direction, jump):
    global playerX, playerY, player_vx, player_vy, haveJumped, gravity

    if jump and playerY == win_height - playerSize:
        # If we're not already jumping, max out the y velocity
        player_vy = maxjump_vy

    # Did we switch direction?
    if (direction > 0 and player_vx < 0) or (direction < 0 and player_vx > 0):
        player_vx = move_speed * direction

    # Move the player
    if direction != 0:
        playerX += player_vx
    
    # Keep the player within the screen bounds
    if playerX > win_width - playerSize:
        playerX = win_width - playerSize
    if playerX < 0:
        playerX = 0

    if player_vy > 1.0: # Decrease speed throughout the jump
        player_vy = player_vy * 0.9
    else:
        player_vy = 0.0

    # Is our square in the air? 
    # Better add some gravity to bring it back down!
    if playerY < win_height - playerSize:
        playerY += gravity
        gravity = gravity * 1.1
    else: # Reset gravity so it starts at 1.0 next time we jump
        gravity = 1.0
    
    playerY -= player_vy

    # Don't let the player fall through the floor
    playerY = min(playerY, win_height - playerSize)

    # Increase x velocity if we're moving but not yet at the maximum
    if direction and abs(player_vx) < max_vx:
        # But only if we're not in the air!
        if player_vy == 0:
            player_vx = player_vx * 1.1

# How to quit our program
def quitGame():
    pygame.quit()
    raise SystemExit

while True:

    surface.fill((0,0,0))

    pygame.draw.rect(surface, (255,0,0), (playerX, playerY, playerSize, playerSize))

    # Get a list of all events that happened since 
    # the last redraw
    for event in pygame.event.get():

        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN 
                                         and event.key == pygame.K_ESCAPE):
            quitGame()

    pressed_keys = pygame.key.get_pressed()            
    jump = pressed_keys[pygame.K_UP]

    if pressed_keys[pygame.K_LEFT]:
        move(-1, jump)
    elif pressed_keys[pygame.K_RIGHT]:
        move(1, jump)
    else:
        move(0, jump)

    pygame.display.update()

    clock.tick(60)