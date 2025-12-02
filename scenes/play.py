import pygame, os
from scenes import fonts
from scenes.audio import get_audio_manager
from player import Player

class Scroll(pygame.sprite.Sprite):
    def __init__(self, image_path, x, min_y, max_y, speed=80, size=(40,40)):
        super().__init__()
        try:
            img = pygame.image.load(image_path).convert_alpha()
            img = pygame.transform.smoothscale(img, size)
        except Exception:
            img = pygame.Surface(size, pygame.SRCALPHA)
            img.fill((255,255,0,255))
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = min_y
        self.min_y = min_y
        self.max_y = max_y
        self.speed = speed
        self.direction = 1

    def update(self, dt):
        self.rect.y += self.direction * self.speed * dt
        if self.rect.y >= self.max_y:
            self.rect.y = self.max_y
            self.direction = -1
        elif self.rect.y <= self.min_y:
            self.rect.y = self.min_y
            self.direction = 1

class PlayScene:
    def __init__(self, previous_scene=None, bgm_path="assets/sounds/플레이 브금.mp3"):
        self.previous_scene = previous_scene
        self.font = fonts.malgun_font
        try:
            img = pygame.image.load(os.path.join("assets","images","first map.png")).convert()
            screen = pygame.display.get_surface()
            if screen:
                w, h = screen.get_size()
                self.bg_image = pygame.transform.smoothscale(img, (max(w, 1600), h))
            else:
                self.bg_image = img
        except Exception:
            self.bg_image = None
        self.audio = get_audio_manager()
        self.bgm_path = bgm_path
        self.camera_x = 0
        self.ground_y = 520
        self.player_speed = 220
        self.left_pressed = False
        self.right_pressed = False
        bg_path = os.path.join("assets","images","prince.png")
        self.player = Player(400, self.ground_y, bg_path, scale=2.0, speed=self.player_speed)
        self.player_group = pygame.sprite.Group(self.player)

        scroll_img = os.path.join("assets","images","scroll.png")
        min_y = self.ground_y - 140
        max_y = self.ground_y - 100
        self.scroll = Scroll(scroll_img, x=1200, min_y=min_y, max_y=max_y, speed=80, size=(120,120))
        self.scroll_group = pygame.sprite.Group(self.scroll)

    def start(self):
        if self.bgm_path:
            self.audio.play_music(self.bgm_path)
        self.camera_x = 0
        if self.bg_image:
            bgw = self.bg_image.get_width()
        else:
            screen = pygame.display.get_surface()
            bgw = screen.get_width() if screen else 800
        halfw = self.player.rect.width // 2
        px = max(halfw, min(400, bgw - halfw))
        self.player.rect.midbottom = (px, self.ground_y)
        self.left_pressed = False
        self.right_pressed = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_p):
                return "pause"
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self.left_pressed = True
            if event.key in (pygame.K_RIGHT, pygame.K_d):
                self.right_pressed = True
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self.left_pressed = False
            if event.key in (pygame.K_RIGHT, pygame.K_d):
                self.right_pressed = False
        return None

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.player.update(dt, keys)
        self.scroll_group.update(dt)
        screen = pygame.display.get_surface()
        w = screen.get_width()
        if self.bg_image:
            bgw = self.bg_image.get_width()
        else:
            bgw = w
        if self.player.rect.left < 0:
            self.player.rect.left = 0
        if self.player.rect.right > bgw:
            self.player.rect.right = bgw
        self.camera_x = min(max(0, int(self.player.rect.centerx - w // 2)), max(0, bgw - w))
        if pygame.sprite.spritecollideany(self.player, self.scroll_group):
            return "puzzle1"

    def draw(self, screen):
        w, h = screen.get_size()
        if self.bg_image:
            screen.blit(self.bg_image, (-self.camera_x, 0))
        else:
            screen.fill((30,120,80))
        draw_x = self.player.rect.x - self.camera_x
        screen.blit(self.player.image, (draw_x, self.player.rect.y))
        for scroll in self.scroll_group:
            screen.blit(scroll.image, (scroll.rect.x - self.camera_x, scroll.rect.y))
        hud_s, hud_r = self.font.render("플레이 씬 - 좌/우 이동", (240,240,240))
        screen.blit(hud_s, (10,10))
