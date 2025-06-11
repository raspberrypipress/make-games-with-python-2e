import pygame
import random
from pygame.math import Vector2

class Fred(pygame.sprite.Sprite):

    def __init__(self, win_width, win_height, game_time):
        super().__init__()
        
        # Load images
        self.leftImage = pygame.image.load("assets/Fred-Left.png")
        self.rightImage = pygame.image.load("assets/Fred-Right.png")
        self.leftImageHit = pygame.image.load("assets/Fred-Left-Hit.png")
        self.rightImageHit = pygame.image.load("assets/Fred-Right-Hit.png")
        print(self.leftImage.get_rect())
        
        # Set initial image and rect
        self.image = self.rightImage
        self.rect = self.image.get_rect()

        self.game_time = game_time
        
        self.window_dims = Vector2(win_width, win_height)
        self.reset()

    def reset(self):
        self.rect.centerx = self.window_dims.x // 2
        self.rect.y = self.window_dims.y - 143

        self.isHit = False
        self.timeHit = 0
        self.health = 100

        self.direction = 1  # 0 = left, 1 = right
        self.speed = 8

    def moveLeft(self, leftBound):
        if self.direction != 0:
            self.direction = 0

        if (self.rect.x - self.speed) > leftBound:
            self.rect.x -= self.speed  

    def moveRight(self, rightBound):
        if self.direction != 1:
            self.direction = 1

        if (self.rect.x + self.speed) + self.rect.width < rightBound:
            self.rect.x += self.speed      

    def update(self):

        time = self.game_time.get_ticks()
        # Handle hit state timeout
        if self.timeHit > 0 and time - self.timeHit > 800:
            self.timeHit = 0
            self.isHit = False

        # Update sprite image based on direction and hit state
        if self.direction == 1:
            if self.isHit:
                self.image = self.rightImageHit
            else:
                self.image = self.rightImage
        else:
            if self.isHit:
                self.image = self.leftImageHit
            else:
                self.image = self.leftImage

    def hit(self, time):
        # Call this when Fred gets hit
        self.isHit = True
        self.timeHit = time
        self.health -= 10

class Barrel(pygame.sprite.Sprite):

    # Calculate slot positions; these correspond to the
    # slots that are drawn on the background image
    slots = []
    for i in range(13):
        if i % 2 == 1:
            y = 27
        else:
            y = 104
        slots.append((4 + (i * 76), y))
    lastBarrelSlot = 0

    def __init__(self, win_width, win_height, game_time):
        super().__init__()
        
        # Load images
        self.barrelImage = pygame.image.load("assets/Barrel.png")
        self.brokenImage = pygame.image.load("assets/Barrel_break.png")
        
        # Set initial image and rect
        self.image = self.barrelImage
        self.rect = self.image.get_rect()

        while True:
            slot = random.randint(0, 12)
            if slot != Barrel.lastBarrelSlot:
                break
        Barrel.lastBarrelSlot = slot
        self.rect.x = self.slots[slot][0]
        self.rect.y = self.slots[slot][1] + 24

        self.game_time = game_time
        self.window_dims = Vector2(win_width, win_height)

        self.isBroken = False
        self.timeBroken = 0

        self.vy = 1.5
        self.gravity = 1.05
        self.maxY = 20

    def split(self):
        self.isBroken = True
        self.timeBroken = self.game_time.get_ticks()
        self.vy = 5
        self.rect.x -= 10
        self.image = self.brokenImage

    def update(self):
        # Apply gravity and movement
        if self.vy < self.maxY:
            self.vy = self.vy * self.gravity
        self.rect.y += self.vy

        # Remove if off screen or broken for too long
        if self.rect.y > self.window_dims.y or self.timeBroken and self.game_time.get_ticks() - self.timeBroken > 1000:
            print("killing barrel", self.game_time.get_ticks() - self.timeBroken)
            self.kill()

    def checkForCollision(self, fred):
        return self.rect.colliderect(fred.rect)
