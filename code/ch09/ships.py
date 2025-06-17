import pygame
import projectiles
import random
from pygame import Vector2

class Player(pygame.sprite.Sprite):

    def __init__(self, win, *groups):
        super().__init__(*groups)
        
        # Load image and set up sprite
        self.image = pygame.image.load("assets/you_ship.png")
        midbottom = win.get_rect().midbottom - Vector2(0, 10)
        self.rect = self.image.get_rect(midbottom=midbottom)
        self.window = win
        
        # Instance attributes
        self.health = 5
        self.sound_effect = 'sounds/player_laser.wav'
        self.bullet_image = "assets/you_pellet.png"
        self.bullet_speed = -10
        
        # Use sprite group for bullets
        self.bullets = pygame.sprite.Group()
        self.groups = groups

    def set_position(self, pos):
        self.rect.centerx = pos[0]

    def fire(self):
        bullet = projectiles.Bullet(
            self.rect.midtop,
            self.bullet_speed,
            self.bullet_image,
            self.window.get_height()
        )
        bullet.add(self.groups, self.bullets)
        
        # Play sound
        sound = pygame.mixer.Sound(self.sound_effect)
        sound.set_volume(0.1)
        sound.play()

    def register_hit(self):
        self.health -= 1

    def check_for_hit(self, target):
        hit_bullets = pygame.sprite.spritecollide(target, self.bullets, True)
        if hit_bullets:
            target.register_hit()

        if target.health <= 0:
            target.kill()

class Enemy(Player):

    def __init__(self, window, *groups):
        super().__init__(window, *groups)
        
        # Override player-specific attributes
        self.image = pygame.image.load("assets/them_ship.png")
        x_pos = random.randint(0, self.window.get_width())
        self.rect = self.image.get_rect(midtop=(x_pos, -60))
        
        self.sound_effect = 'sounds/enemy_laser.wav'
        self.bullet_image = "assets/them_pellet.png"
        self.bullet_speed = 10
        self.speed = Vector2(0, 2)
        self.health = 1

    def update(self):
        super().update()

        self.rect.move_ip(self.speed)
        if self.rect.y >= self.window.get_height():
            self.kill()

    def try_to_fire(self):
        should_fire = random.random()
        if should_fire <= 0.01:
            self.fire() 