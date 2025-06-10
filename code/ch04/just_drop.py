import pygame
import random

pygame.init()
clock = pygame.time.Clock()
FPS = 60

title_image = pygame.image.load("assets/title.jpg")
game_over_image = pygame.image.load("assets/game_over.jpg")

WIN_WIDTH = 400
WIN_HEIGHT = 600
window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Drop!')

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.gravity = 1
        self.x = WIN_WIDTH / 2
        self.y = 1
        self.speed_x = 3
        self.direction = 0

        self.image = pygame.Surface((10, 25))
        self.image.fill((255, 0, 0))

        # Create a collision mask
        self.mask = pygame.mask.from_surface(self.image)

        # Get the image's rectangle and place it at x, y
        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.x, self.y)

    def set_direction(self, direction=0):
        self.direction = direction

    def update(self):            
        self.x = self.x + direction * self.speed_x
        self.y = self.y + self.gravity

        if self.x > WIN_WIDTH:
            self.x = 0
        if self.x < 0:
            self.x = WIN_WIDTH

        self.rect.midbottom = (self.x, self.y)
    
    def check_collisions(self, all_sprites):
        # Check for collisions with all platforms
        platforms = [p for p in all_sprites 
                     if isinstance(p, Platform)]
        hits = pygame.sprite.spritecollide(self, platforms, 
                False, collided=pygame.sprite.collide_mask)
        if hits:
            self.gravity = 0
            self.y = hits[0].rect.top + 1
        elif self.y >= WIN_HEIGHT:
            self.gravity = 0
            self.y = WIN_HEIGHT + 1
        else:
            self.gravity = 2


class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.x = WIN_WIDTH / 2
        self.y = WIN_HEIGHT
        self.speed = 2

        self.image = pygame.Surface((WIN_WIDTH, 20), 
                                    pygame.SRCALPHA)
        self.image.fill((255, 255, 255, 255)) # solid platform

        # Draw a gap
        gap_loc = random.randint(0, WIN_WIDTH-50)
        pygame.draw.rect(self.image, (255,255,255,0), 
                         (gap_loc, 0, 50, 20))

        # Create a collision mask
        self.mask = pygame.mask.from_surface(self.image)
        # Scale it so we ignore collisions halfway through the gap
        self.mask= self.mask.scale((self.image.get_width(),
                                    self.image.get_height() * .5))

        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def update(self):
        self.y = self.y - self.speed    
        self.rect.center = (self.x, self.y)
        # Destroy platforms when they move offscreen
        if self.rect.bottomleft[1] <= 0:
            self.kill()


def restart_game():
    global all_sprites, player, platform_delay, game_started
    all_sprites.clear()
    player = Player()
    all_sprites.add(player)
    platform_delay = 2000
    pygame.time.set_timer(NEW_PLATFORM, platform_delay)
    game_started = True

def check_game_over():
    global game_ended, game_started
    if player.rect.bottomleft[1] <= 0:
        game_ended = True
        game_started = False

all_sprites = pygame.sprite.Group()
player = None
platform_delay = 2000
game_started = False
game_ended = False
NEW_PLATFORM = pygame.USEREVENT + 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == NEW_PLATFORM:
            new_platform = Platform()
            all_sprites.add(new_platform)
            platform_delay = max(800, platform_delay - 50)
            pygame.time.set_timer(NEW_PLATFORM, platform_delay)
     
    window.fill((0, 0, 0))
 
    # Handle keyboard input
    direction = 0
    pressed_keys = pygame.key.get_pressed()            
    if pressed_keys[pygame.K_LEFT]:
        direction = -1
    elif pressed_keys[pygame.K_RIGHT]:
        direction = 1
    elif pressed_keys[pygame.K_SPACE]:
        if not game_started:
            restart_game()

    if game_started: # Move, check collisions, and draw sprites
        player.set_direction(direction)
        all_sprites.update()

        player.check_collisions(all_sprites)
        check_game_over()

        all_sprites.draw(window)

    elif game_ended:
        window.blit(game_over_image, (0, 150))

    else:
        window.blit(title_image, (0, 150))
    
    pygame.display.update()
    clock.tick(FPS)