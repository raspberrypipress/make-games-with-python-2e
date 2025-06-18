import pygame
import ships
import gamelevels

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
incoming_wave = pygame.image.load("assets/next_level.png")
win_screen = pygame.image.load("assets/win_screen.png")
lose_screen = pygame.image.load("assets/lose_screen.png")
last_lvl_screen = pygame.image.load("assets/final_level.png")
# Define the clickable area for the start button
start_button_rect = pygame.Rect(445, 450, 135, 60)

game_started = False
curr_lvl = 0
curr_wave = 0
show_msg = False
game_won = False
last_lvl = False
NEW_WAVE = pygame.USEREVENT + 0
CLEAR_NEXT_LEVEL_MSG = pygame.USEREVENT + 1

all_sprites = pygame.sprite.Group()
ship = ships.Player(window, all_sprites)

def add_new_wave():
    global curr_lvl, curr_wave, show_msg, game_won, last_lvl

    this_level = gamelevels.level[curr_lvl]["structure"]
    if curr_wave < len(this_level):
        wave = this_level[curr_wave]
        for idx, enemy in enumerate(wave):
            if enemy:
                ships.Enemy(window, idx,
                            len(wave), all_sprites)
        curr_wave += 1

    elif curr_lvl + 1 < len(gamelevels.level):
        curr_lvl += 1
        curr_wave = 0
        ship.shield = ship.MAX_SHIELD
        show_msg = True
        pygame.time.set_timer(CLEAR_NEXT_LEVEL_MSG, 5000)
        if curr_lvl == len(gamelevels.level) - 1:
            last_lvl = True

    else:
        game_won = True
    
    delay = gamelevels.level[curr_lvl]["interval"] * 1000
    pygame.time.set_timer(NEW_WAVE, delay)

def reset_game():
    global game_won, curr_lvl, curr_wave, show_msg, last_lvl

    game_won = False
    curr_lvl = 0
    curr_wave = 0
    show_msg = False
    last_lvl = False

    # Add the ship back to the sprites group.
    all_sprites.add(ship)
    ship.health = ship.MAX_HEALTH
    ship.shield = ship.MAX_SHIELD
    add_new_wave()

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
            if event.key == pygame.K_SPACE:
                if game_won or ship.health <= 0:
                    reset_game()
        if event.type == NEW_WAVE:
            add_new_wave()
        if event.type == CLEAR_NEXT_LEVEL_MSG:
            show_msg = False
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                clicked = True
        if event.type == pygame.QUIT:
            quit_game()

    mouse_position = pygame.mouse.get_pos()

    if not game_started:
        window.blit(start_screen, (0, 0))
        if clicked:
            if start_button_rect.collidepoint(mouse_position):
                game_started = True
                add_new_wave()

    elif game_started and ship.health > 0 and not game_won:
        window.blit(background, (0, 0))
        if show_msg:
            if last_lvl:
                window.blit(last_lvl_screen, (250, 150))
            else:
                window.blit(incoming_wave, (250, 150))

        if clicked:
            ship.fire()
        ship.set_position(mouse_position)

        all_sprites.update()

        for enemy in all_sprites:
            if isinstance(enemy, ships.Enemy):
                enemy.try_to_fire()
                enemy.check_for_hit(ship)
                ship.check_for_hit(enemy)

        all_sprites.draw(window)
        window.blit(ship.shield_meter(), (0, WIN_HEIGHT - 5))
        window.blit(ship.health_meter(), (0, WIN_HEIGHT - 10))

    elif game_started and ship.health <= 0:
        window.blit(lose_screen, (0, 0))
        all_sprites.empty()

    elif game_started and game_won:
        window.blit(win_screen, (0, 0))
        all_sprites.empty()

    clock.tick(FPS)
    pygame.display.update()