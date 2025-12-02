import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.speed = 220
        self.vx = 0
        self.vy = 0
        self.inventory = []
        self.puzzles_cleared = 0
        self.name = "Hero"

    def update(self, dt, keys):
        self.vx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -self.speed * dt
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = self.speed * dt
        self.rect.x += int(self.vx)

    def add_item(self, item):
        self.inventory.append(item)

    def clear_puzzle(self):
        self.puzzles_cleared += 1
