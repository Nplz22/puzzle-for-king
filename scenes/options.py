# scenes/options.py
import pygame
from scenes import fonts

class OptionsScene:
    def __init__(self, bgm_volume=0.1, sfx_volume=0.3, previous_scene=None):
        self.font = fonts.malgunbd_font_small
        self.options = ["BGM 볼륨", "효과음 볼륨", "타이틀로 돌아가기"]
        self.selected = 0
        self.bgm_volume = bgm_volume
        self.sfx_volume = sfx_volume
        self.previous_scene = previous_scene
        try:
            self.bg_image = pygame.image.load("assets/images/title background.png").convert()  # <-- 배경 이미지 추가
            self.bg_image = pygame.transform.scale(self.bg_image, (800, 600))
        except:
            self.bg_image = pygame.Surface((800, 600))
            self.bg_image.fill((50,50,70))
        
        self.options_bgm = "assets/sounds/설정 화면 브금.mp3"
        self.bgm_playing = False

    def start(self):
        if self.bgm_volume > 0:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.options_bgm)
            pygame.mixer.music.set_volume(self.bgm_volume)
            pygame.mixer.music.play(-1)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                if self.selected == 0:
                    self.bgm_volume = max(0.0, self.bgm_volume - 0.1)
                    pygame.mixer.music.set_volume(self.bgm_volume)
                elif self.selected == 1:
                    self.sfx_volume = max(0.0, self.sfx_volume - 0.1)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                if self.selected == 0:
                    self.bgm_volume = min(1.0, self.bgm_volume + 0.1)
                    pygame.mixer.music.set_volume(self.bgm_volume)
                elif self.selected == 1:
                    self.sfx_volume = min(1.0, self.sfx_volume + 0.1)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                if self.selected == 2:
                    return self.previous_scene
        return None

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.blit(self.bg_image, (0, 0))
        for i, opt in enumerate(self.options):
            color = (255,69,0) if i == self.selected else (80, 80, 80)
            if i == 0:
                text = f"{opt}: {int(self.bgm_volume*100)}%"
            elif i == 1:
                text = f"{opt}: {int(self.sfx_volume*100)}%"
            else:
                text = opt
            surf, rect = self.font.render(text, color)
            screen.blit(surf, (400 - rect.width//2, 200 + i*60))
