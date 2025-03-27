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

game_started = False
game_ended = False

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.gravity = 1
        self.x = win_width / 2
        self.y = 1
        self.speed_x = 3

        self.surf = pygame.Surface((10, 25))
        self.surf.fill((255, 0, 0))

        self.mask = pygame.mask.from_surface(self.surf) # Collision mask
        self.rect = self.surf.get_rect()
        self.rect.midbottom = (self.x, self.y)

    def move(self, direction=0):
        self.x += direction * self.speed_x
        self.y += self.gravity
         
        if self.x > win_width: # FIXME: in the text, explain how to do the same for y so they get a reward for reaching the bottom of the screen (back to the top)
            self.x = 0
        if self.x < 0:
            self.x = win_width
            
        self.rect.midbottom = (self.x, self.y)
    
    def check_collisions(self, platforms, floor):
        # Check for collisions with all platforms
        hits = pygame.sprite.spritecollide(self, platforms, 
                False, collided=pygame.sprite.collide_mask)
        if hits:
            self.y = hits[0].rect.top + 1 # The +1 to maintain collision condition, so we don't hop.
            self.gravity = 0
        elif pygame.sprite.collide_rect(self, floor):
            self.y = floor.rect.top + 1
            self.gravity = 0
        else:
            self.gravity = 1


class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.x = win_width/2
        self.y = win_height
        self.speed = 2

        self.surf = pygame.Surface((win_width, 20), pygame.SRCALPHA)
        self.surf.fill((255, 255, 255, 0))

        gap_loc = random.randint(0, win_width-50)
        pygame.draw.rect(self.surf, (255,255,255,255), (0, 0, gap_loc, 20))
        pygame.draw.rect(self.surf, (255,255,255,255), 
                         (gap_loc + 50, 0, win_width - gap_loc - 50, 20))

        self.mask = pygame.mask.from_surface(self.surf) # Collision mask
        # Scale it so we ignore collisions halfway through the gap
        self.mask= self.mask.scale((self.surf.get_width(),
                                    self.surf.get_height() * .5))

        self.rect = self.surf.get_rect()
        self.rect.center = (self.x, self.y)

    def move(self):
        self.y -= self.speed    
        self.rect.center = (self.x, self.y)


class Floor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.x = win_width/2
        self.y = win_height - 10

        self.surf = pygame.Surface((win_height, 4))
        self.surf.fill((255, 0, 255))

        self.mask = pygame.mask.from_surface(self.surf) # Collision mask
        self.rect = self.surf.get_rect()
        self.rect.center = (self.x, self.y)

    def move(self):
        pass


def movePlatforms(platforms):
    for p in platforms: # Keep the platforms moving
        p.move()
        # Add a new platform when one is halfway up the screen
        if p.rect.topleft[1] == int(win_height/2): 
            new_platform = Platform()
            platforms.add(new_platform)

        # Destroy platforms when they move offscreen
        if p.rect.bottomleft[1] <= 0:
            p.kill()
            del p

def check_game_over(player):
    global game_ended, game_started
    if player.rect.bottomleft[1] <= 0:
        game_ended = True
        game_started = False


def restartGame():
    global platforms, player, floor
    platforms = pygame.sprite.Group()
    platforms.add(Platform())
    player = Player()
    floor = Floor()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
     
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
        player.move(direction)
        movePlatforms(platforms)

        player.check_collisions(platforms, floor)
        check_game_over(player)

        for p in platforms:
            window.blit(p.surf, p.rect)
        window.blit(floor.surf, floor.rect)
        window.blit(player.surf, player.rect)

    elif game_ended:
        window.blit(game_over_image, (0, 150))

    else:
        window.blit(title_image, (0, 150))
    
    pygame.display.update()
    clock.tick(fps)