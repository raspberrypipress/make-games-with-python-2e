import pygame

class Bullet(pygame.sprite.Sprite):

    def __init__(self, midtop, speed, image_path, window_height):
        super().__init__()
        
        # Load and set up the image
        self.image = pygame.image.load(image_path)

        # Center the bullet horizontally
        self.rect = self.image.get_rect(midtop=midtop)
        self.velocity = pygame.Vector2(0, speed)
        self.window_height = window_height

    def update(self):
        self.rect.move_ip(self.velocity)
        
        # Remove bullet if it goes off screen
        if self.rect.bottom < 0 or self.rect.top > self.window_height:
            self.kill()