import pygame
import projectiles
import random

class Player(pygame.sprite.Sprite):

    def __init__(self, surface, all_sprites):
        super().__init__()
        self.surface = surface
        
        # Load image and set up sprite
        self.image = pygame.image.load("assets/you_ship.png")
        self.rect = self.image.get_rect()
        
        self.rect.centerx = surface.get_width() / 2
        self.rect.bottom = surface.get_height() - 10
        
        # Instance attributes
        self.health = 5
        self.sound_effect = 'sounds/player_laser.wav'
        self.bullet_image = "assets/you_pellet.png"
        self.bullet_speed = -10
        
        # Use sprite group for bullets
        self.bullets = pygame.sprite.Group()
        self.all_sprites = all_sprites
        all_sprites.add(self)

    def set_position(self, pos):
        self.rect.centerx = pos[0]

    def fire(self):
        bullet = projectiles.Bullet(
            self.rect.centerx, 
            self.rect.top, 
            self.bullet_speed, 
            self.bullet_image,
            self.surface.get_height(),
            self.all_sprites
        )
        self.bullets.add(bullet)
        
        # Play sound
        sound = pygame.mixer.Sound(self.sound_effect)
        sound.set_volume(0.2)
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

    def __init__(self, surface, all_sprites, health):
        super().__init__(surface, all_sprites)
        
        # Override player-specific attributes
        self.image = pygame.image.load("assets/them_ship.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0, self.surface.get_width())
        self.rect.y = -60
        
        self.sound_effect = 'sounds/enemy_laser.wav'
        self.bullet_image = "assets/them_pellet.png"
        self.bullet_speed = 10
        self.speed = 2
        self.health = health
        
        # Reset bullets group for enemy
        self.bullets = pygame.sprite.Group()

    def update(self):
        super().update()

        self.rect.y += self.speed
        if self.rect.y >= self.surface.get_height():
            self.kill()

    def try_to_fire(self):
        should_fire = random.random()
        if should_fire <= 0.01:
            self.fire() 
