import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, scale=2.0, speed=220):
        super().__init__()
        img = pygame.image.load(image_path).convert_alpha()
        w, h = img.get_size()
        sw, sh = max(1, int(w * scale)), max(1, int(h * scale))
        self.image = pygame.transform.smoothscale(img, (sw, sh))
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.speed = speed
        self.vx = 0
        self.inventory = []
        self.puzzles_cleared = 0
        self.name = "현우"

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
