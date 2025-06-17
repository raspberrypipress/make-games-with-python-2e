import pygame
import random
import ships

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
FPS = 60

WIN_HEIGHT = 614
WIN_WIDTH = 1024
window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Aliens Are Gonna Kill Me!')
text_font = pygame.font.SysFont("monospace", 50)
pygame.mixer.init()

start_screen = pygame.image.load("assets/start_screen.png")
background = pygame.image.load("assets/background.png")
# Define the clickable area for the start button
start_button_rect = pygame.Rect(445, 450, 135, 60)

game_started = False
start_time = 0
time_lasted = 0
NEW_ENEMY = pygame.USEREVENT + 0

all_sprites = pygame.sprite.Group()
ship = ships.Player(window, all_sprites)

def add_new_enemy():
    ships.Enemy(window, all_sprites)
    enemy_interval = random.randint(1000, 2500)
    pygame.time.set_timer(NEW_ENEMY, enemy_interval)

def quit_game():
    pygame.quit()
    raise SystemExit

# main loop
while True:

    clicked = False
    # Handle events 
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit_game()
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                clicked = True

        if event.type == pygame.QUIT:
            quit_game()

        if event.type == NEW_ENEMY:
            add_new_enemy()

    mouse_position = pygame.mouse.get_pos()

    if not game_started:
        window.blit(start_screen, (0, 0))
        if clicked:
            if start_button_rect.collidepoint(mouse_position):
                game_started = True
                start_time = pygame.time.get_ticks()
                add_new_enemy()

    elif game_started and ship.health > 0:
        window.blit(background, (0, 0))

        if clicked:
            ship.fire()
        ship.set_position(mouse_position)

        all_sprites.update()

        for enemy in all_sprites:
            if isinstance(enemy, ships.Enemy):
                enemy.try_to_fire()
                enemy.check_for_hit(ship)
                ship.check_for_hit(enemy)

        if ship.health <= 0:
            end_time = pygame.time.get_ticks()
            time_lasted = (end_time - start_time) // 1000

        all_sprites.draw(window)
        window.blit(ship.shield_meter(), (0, WIN_HEIGHT - 5))
        window.blit(ship.health_meter(), (0, WIN_HEIGHT - 10))

    elif game_started and ship.health <= 0:
        print(f"Game Over! You lasted {time_lasted} seconds.")
        quit_game()
 
    clock.tick(FPS)
    pygame.display.update()