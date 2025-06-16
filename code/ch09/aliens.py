import pygame, sys, random, math
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS
import pygame.time as GAME_TIME
import ships

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
FPS = 60

window_width = 1024
window_height = 614
surface = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Alien\'s Are Gonna Kill Me!')
text_font = pygame.font.SysFont("monospace", 50)

# Image Variables
start_screen = pygame.image.load("assets/start_screen.png")
background = pygame.image.load("assets/background.png")
start_button_rect = pygame.Rect(445, 450, 135, 60)

game_started = False
game_started_time = 0
game_finished_time = 0
game_over = False
NEW_ENEMY = pygame.USEREVENT + 0
# Mouse Variables
mouse_position = (0, 0)

# Ships
all_sprites = pygame.sprite.Group()
ship = ships.Player(surface, all_sprites)
enemy_ships = pygame.sprite.Group()

# Sound Setup
pygame.mixer.init()

def quit_game():
    pygame.quit()
    sys.exit()

def add_new_enemy():
    enemy = ships.Enemy(surface, all_sprites, 1)
    enemy_ships.add(enemy)
    enemy_interval = random.randint(1000, 2500)
    pygame.time.set_timer(NEW_ENEMY, enemy_interval)

# 'main' loop
add_new_enemy()
while True:

    clicked = False
    # Handle user and system events 
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit_game()
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                clicked = True
        if event.type == NEW_ENEMY:
            add_new_enemy()
        if event.type == GAME_GLOBALS.QUIT:
            quit_game()

    time_tick = GAME_TIME.get_ticks()
    mouse_position = pygame.mouse.get_pos()

    if game_started and not game_over:
        surface.blit(background, (0, 0))

        if clicked:
            ship.fire()
        ship.set_position(mouse_position)

        all_sprites.update()

        for enemy in enemy_ships:
            enemy.try_to_fire()
            enemy.check_for_hit(ship)
            ship.check_for_hit(enemy)

        if ship.health <= 0:
            game_over = True
            game_finished_time = GAME_TIME.get_ticks()

        all_sprites.draw(surface)

    elif not game_started and not game_over:
        surface.blit(start_screen, (0, 0))
        if clicked:
            if start_button_rect.collidepoint(mouse_position):
                game_started = True
                game_started_time = GAME_TIME.get_ticks()

    elif game_started and game_over:
        surface.blit(start_screen, (0, 0))
        time_lasted = (game_finished_time - game_started_time) // 1000
        print(f"Game Over! You lasted {time_lasted} seconds.")
        quit_game()
 
    clock.tick(FPS)
    pygame.display.update()
