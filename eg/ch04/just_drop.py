import pygame
import random

pygame.init()
clock = pygame.time.Clock()
fps = 60

title_image = pygame.image.load("assets/title.jpg")
game_over_image = pygame.image.load("assets/game_over.jpg")

win_width = 400
win_height = 600
window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('Drop!')

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.gravity = 1
        self.x = win_width / 2
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

        if self.x > win_width:
            self.x = 0
        if self.x < 0:
            self.x = win_width

        self.rect.midbottom = (self.x, self.y)
    
    def check_collisions(self, platforms):
        # Check for collisions with all platforms
        hits = pygame.sprite.spritecollide(self, platforms, 
                False, collided=pygame.sprite.collide_mask)
        if hits:
            self.gravity = 0
            self.y = hits[0].rect.top + 1
        elif self.y >= win_height:
            self.gravity = 0
            self.y = win_height + 1
        else:
            self.gravity = 2


class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.x = win_width/2
        self.y = win_height
        self.speed = 2

        self.image = pygame.Surface((win_width, 20), 
                                    pygame.SRCALPHA)
        self.image.fill((255, 255, 255, 255)) # solid platform

        # Draw a gap
        gap_loc = random.randint(0, win_width-50)
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


def restartGame():
    global platforms, player, platform_delay
    platforms = pygame.sprite.Group()
    platforms.add(Platform())
    player = Player()
    platform_delay = 2000
    pygame.time.set_timer(NEW_PLATFORM, platform_delay)    

def check_game_over(player):
    global game_ended, game_started
    if player.rect.bottomleft[1] <= 0:
        game_ended = True
        game_started = False

game_started = False
game_ended = False
NEW_PLATFORM = pygame.USEREVENT + 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == NEW_PLATFORM:
            platforms.add(Platform())
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
            restartGame()
            game_started = True

    if game_started: # Move, check collisions, and draw sprites
        player.set_direction(direction)
        player.update()
        platforms.update()

        player.check_collisions(platforms)
        check_game_over(player)

        platforms.draw(window)
        window.blit(player.image, player.rect)

    elif game_ended:
        window.blit(game_over_image, (0, 150))

    else:
        window.blit(title_image, (0, 150))
    
    pygame.display.update()
    clock.tick(fps)