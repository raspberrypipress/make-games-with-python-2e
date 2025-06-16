import pygame

class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y, speed, image_path, window_height, all_sprites):
        super().__init__()
        
        # Load and set up the image
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        
        # Use Vector2 for position and velocity
        self.pos = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, speed)
        
        # Center the bullet horizontally
        self.rect.centerx = x
        self.rect.y = y
        self.window_height = window_height
        all_sprites.add(self)

    def update(self):
        # Move using Vector2
        self.pos += self.velocity
        self.rect.center = self.pos
        
        # Remove bullet if it goes off screen
        if self.rect.bottom < 0 or self.rect.top > self.window_height:
            self.kill()