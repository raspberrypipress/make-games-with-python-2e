import pygame
import projectiles
import random
from pygame import Vector2, Surface

class Player(pygame.sprite.Sprite):

    MAX_HEALTH = 5
    MAX_SHIELD = 3
    HEALTH_COLOURS = [(62, 180, 76), (180, 62, 62)]
    
    def __init__(self, win, *groups):
        super().__init__(*groups)
        
        self.ship_img = pygame.image.load(
            "assets/you_ship.png")
        self.shield_img = pygame.image.load(
            "assets/shield1.png")
        self.image = self.ship_img.copy()

        midbottom = win.get_rect().midbottom - Vector2(0, 10)
        self.rect = self.image.get_rect(midbottom=midbottom)
        
        # Instance attributes
        self.health = self.MAX_HEALTH
        self.shield = self.MAX_SHIELD
        self.last_hit = 0
        self.sound_effect = "sounds/player_laser.wav"
        self.bullet_image = "assets/you_pellet.png"
        self.bullet_speed = -10
        
        self.bullets = pygame.sprite.Group()
        self.window = win

    def update(self):
        super().update()
        self.image.fill((0, 0, 0, 0))
        self.image.blit(self.ship_img, (0, 0))
        if self.last_hit > 0 and self.shield > 0:
            elapsed = pygame.time.get_ticks() - self.last_hit
            if elapsed < 250:
                self.image.blit(self.shield_img, (-3, -2))

    def set_position(self, pos):
        self.rect.centerx = pos[0]

    def fire(self):
        bullet = projectiles.Bullet(
            self.rect.midtop,
            self.bullet_speed,
            self.bullet_image,
            self.window.get_height()
        )
        bullet.add(self.groups(), self.bullets)
        
        # Play sound
        sound = pygame.mixer.Sound(self.sound_effect)
        sound.set_volume(0.1)
        sound.play()

    def check_for_hit(self, t):
        if pygame.sprite.spritecollide(t, self.bullets, True):
            t.register_hit()

        if t.health <= 0:
            t.kill()

    def register_hit(self):
        if self.shield <= 0:
            self.health -= 1
        else:
            self.shield -= 1
        self.last_hit = pygame.time.get_ticks()

    def shield_meter(self):
        percent = self.shield / self.MAX_SHIELD
        s = Surface((percent * self.window.get_width(), 5))
        s.fill((62, 145, 180))
        return s
    
    def health_meter(self):
        percent = self.health / self.MAX_HEALTH
        s = Surface((percent * self.window.get_width(), 5))
        if self.health <= 1:
            which_colour = self.HEALTH_COLOURS[1]
        else:
            which_colour = self.HEALTH_COLOURS[0]
        s.fill(which_colour)
        return s

class Enemy(Player):

    def __init__(self, window, idx, len, *groups):
        super().__init__(window, *groups)
        
        # Override player-specific attributes
        self.ship_img = pygame.image.load(
            "assets/them_ship.png")
        self.image = self.ship_img.copy()

        x_pos = (window.get_width() // len) * idx
        self.rect = self.image.get_rect(midtop=(x_pos, -60))
        
        self.sound_effect = "sounds/enemy_laser.wav"
        self.bullet_image = "assets/them_pellet.png"
        self.bullet_speed = 10
        self.speed = Vector2(0, 4)
        self.health = 1
        self.shield = 0

    def update(self):
        super().update()

        self.rect.move_ip(self.speed)
        if self.rect.y >= self.window.get_height():
            self.kill()

    def try_to_fire(self):
        should_fire = random.random()
        if should_fire <= 0.01:
            self.fire() 