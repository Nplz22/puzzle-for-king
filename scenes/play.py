import pygame, os
from scenes import fonts
from scenes.audio import get_audio_manager

class PlayScene:
    def __init__(self, previous_scene=None, bgm_path="assets/sounds/플레이 브금.mp3"):
        self.previous_scene = previous_scene
        self.font = fonts.malgun_font
        try:
            img = pygame.image.load("assets/images/first map.png").convert()
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
        surf = pygame.Surface((48,64), pygame.SRCALPHA)
        surf.fill((200,50,50))
        self.player = {
            "image": surf,
            "x": 400,
            "y": self.ground_y,
            "rect": surf.get_rect(midbottom=(400, self.ground_y))
        }

    def start(self):
        if self.bgm_path:
            self.audio.play_music(self.bgm_path)
        self.camera_x = 0
        self.player["x"] = 400
        self.player["rect"].midbottom = (self.player["x"], self.player["y"])
        self.left_pressed = False
        self.right_pressed = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_p):
                return "pause"
            if event.key == pygame.K_LEFT:
                self.left_pressed = True
            if event.key == pygame.K_RIGHT:
                self.right_pressed = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.left_pressed = False
            if event.key == pygame.K_RIGHT:
                self.right_pressed = False
        return None

    def update(self, dt):
        dx = 0
        if self.left_pressed:
            dx -= self.player_speed * dt
        if self.right_pressed:
            dx += self.player_speed * dt
        self.player["x"] += dx
        screen = pygame.display.get_surface()
        w = screen.get_width()
        self.player["rect"].midbottom = (self.player["x"], self.player["y"])
        bgw = self.bg_image.get_width() if self.bg_image else w
        self.camera_x = min(max(0, int(self.player["x"] - w // 2)), max(0, bgw - w))

    def draw(self, screen):
        w, h = screen.get_size()
        if self.bg_image:
            screen.blit(self.bg_image, (-self.camera_x, 0))
        else:
            screen.fill((30,120,80))
        if self.player:
            draw_x = self.player["rect"].x - self.camera_x
            screen.blit(self.player["image"], (draw_x, self.player["rect"].y))
        hud_s, hud_r = self.font.render("플레이 씬 - 좌/우 이동", (240,240,240))
        screen.blit(hud_s, (10,10))
