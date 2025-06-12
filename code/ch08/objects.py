import pygame
import random
from pygame.math import Vector2

class Fred(pygame.sprite.Sprite):

    MAX_HEALTH = 100
    DEFAULT_IMG = pygame.image.load("assets/Fred-Right.png")
    HIT_IMG = pygame.image.load("assets/Fred-Right-Hit.png")
    GROUND_HEIGHT = 143

    def __init__(self, win_width, win_height):
        super().__init__()
        
        # Set initial image and rect
        self.image = Fred.DEFAULT_IMG
        self.rect = self.image.get_rect()
        
        self.window_dims = Vector2(win_width, win_height)
        self.reset()

    def reset(self):
        self.rect.centerx = self.window_dims.x // 2
        self.rect.y = self.window_dims.y - Fred.GROUND_HEIGHT

        self.is_hit = False
        self.time_hit = 0
        self.health = Fred.MAX_HEALTH

        self.direction = 1  # 0 = left, 1 = right
        self.speed = 8

    def set_direction(self, direction):
        left_max = 0
        right_max = self.window_dims.x
        self.direction = direction

        # Make sure Fred remains within bounds before moving
        next_x = self.rect.x + self.speed * self.direction
        if left_max < next_x < right_max - self.rect.width:
            self.rect.x = next_x

    def update(self):
        time = pygame.time.get_ticks()
        # Handle hit state timeout
        if self.is_hit and time - self.time_hit > 800:
            self.time_hit = 0
            self.is_hit = False

        # Update sprite image based on hit state
        if self.is_hit:
            self.image = Fred.HIT_IMG
        else:
            self.image = Fred.DEFAULT_IMG
        # Flip the image if Fred is facing left
        if self.direction == -1:
            self.image = pygame.transform.flip(self.image,
                                               True, False)
    
    def health_meter(self):
        health_percentage = self.health / Fred.MAX_HEALTH
        surf = pygame.Surface((health_percentage
                               * self.window_dims.x, 10))
        surf.fill((175,59,59))
        return surf

    def check_collisions(self, barrels):
        if b := pygame.sprite.spritecollideany(self, barrels):
            if not b.is_broken:
                b.split()
                self.is_hit = True
                self.time_hit = pygame.time.get_ticks()
                self.health -= 10

class Barrel(pygame.sprite.Sprite):

    BARREL_IMG = pygame.image.load("assets/Barrel.png")
    BROKEN_IMG = pygame.image.load("assets/Barrel_break.png")
    GRAVITY = 1.05
    MAX_Y = 20

    # Calculate slot positions; these correspond to the slots
    # that are drawn on the background image
    slots = []
    for i in range(13):
        if i % 2 == 1:
            y = 27
        else:
            y = 104
        slots.append((4 + (i * 76), y))
    last_barrel_slot = 0

    def __init__(self, win_width, win_height):
        super().__init__()
        
        self.image = Barrel.BARREL_IMG
        self.rect = self.image.get_rect()

        while True:
            slot = random.randint(0, 12)
            if slot != Barrel.last_barrel_slot:
                break
        Barrel.last_barrel_slot = slot
        self.rect.x = self.slots[slot][0]
        self.rect.y = self.slots[slot][1] + 24

        self.window_dims = Vector2(win_width, win_height)

        self.is_broken = False
        self.vy = 1.5

    def split(self):
        self.is_broken = True
        self.vy = 5
        self.rect.x -= 10
        self.image = Barrel.BROKEN_IMG

    def update(self):
        # Apply gravity and movement
        if self.vy < Barrel.MAX_Y:
            self.vy = self.vy * Barrel.GRAVITY
        self.rect.y += self.vy

        # Remove if off screen
        if self.rect.y > self.window_dims.y:
            self.kill()