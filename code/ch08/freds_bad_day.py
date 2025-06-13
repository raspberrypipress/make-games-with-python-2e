import pygame
import objects

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
FPS = 60

WIN_WIDTH = 1000
WIN_HEIGHT = 768
FRED_OFFSET = 23
window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Fred's Bad Day")
textFont = pygame.font.SysFont("monospace", 50)

start_screen = pygame.image.load("assets/startgame.png")
end_screen = pygame.image.load("assets/gameover.png")
background = pygame.image.load("assets/background.png")

game_started = False
start_time = 0
time_lasted = 0
barrel_delay = 1500
NEW_BARREL = pygame.USEREVENT + 0

fred = objects.Fred(WIN_WIDTH, WIN_HEIGHT, FRED_OFFSET)
barrels = pygame.sprite.Group()

def restart_game():
    global game_started, start_time, barrels, barrel_delay

    fred.reset()
    for barrel in barrels:
        barrel.kill()

    barrel_delay = 1500
    pygame.time.set_timer(NEW_BARREL, barrel_delay)

    game_started = True
    start_time = pygame.time.get_ticks()

def new_barrel():
    global barrels, barrel_delay

    new_barrel = objects.Barrel(WIN_WIDTH, WIN_HEIGHT)
    barrels.add(new_barrel)
    if barrel_delay > 150:
        barrel_delay -= 50
    pygame.time.set_timer(NEW_BARREL, barrel_delay)

def quit_game():
    pygame.quit()
    raise SystemExit

# main loop
while True:

    # Handle events    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit_game()
            elif event.key == pygame.K_RETURN:
                if not game_started or fred.health <= 0:
                    restart_game()

        if event.type == pygame.QUIT:
            quit_game()
        if event.type == NEW_BARREL and fred.health > 0:
            new_barrel()

    # If the game hasn't been started, show the start screen
    if not game_started:
        window.blit(start_screen, (0, 0))

    # If the game is started and Fred's alive, play the game
    elif game_started and fred.health > 0:
        window.blit(background, (0, 0))

        # Set Fred's direction based on the keys pressed
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT]:
            fred.set_direction(-1)
        elif pressed_keys[pygame.K_RIGHT]:
            fred.set_direction(1)  

        fred.update()
        barrels.update()

        # Check for collisions and check Fred's health
        fred.check_collisions(barrels)
        if fred.health <= 0:
            time_tick = pygame.time.get_ticks()
            time_lasted = (time_tick - start_time) // 1000

        # Draw the barrels, Fred, and the health meter
        barrels.draw(window)
        window.blit(fred.image, fred.rect)
        window.blit(fred.health_meter(), (0, WIN_HEIGHT - 10))

    # If Fred's health falls to 0, it's game over!
    elif fred.health <= 0:
        window.blit(end_screen, (0, 0))
        renderedText = textFont.render(f"{time_lasted:02}",
                                       1, (175,59,59))
        window.blit(renderedText, (495, 430))

    pygame.display.update()
    clock.tick(FPS)