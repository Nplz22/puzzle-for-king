import pygame, os
from scenes import fonts
from scenes.audio import get_audio_manager
from scenes.play import PlayScene

class OptionsScene:
    def __init__(self, previous_scene=None):
        self.font = fonts.malgunbd_font_small
        self.previous_scene = previous_scene
        self.options = ["BGM 볼륨", "효과음 볼륨"]
        self.selected = 0
        self.audio = get_audio_manager()
        self.bgm_volume = self.audio.music_volume
        self.sfx_volume = self.audio.sfx_volume
        self.bg_image = None
        try:
            img = pygame.image.load("assets/images/title background.png").convert()
            self.bg_image = pygame.transform.scale(img, (800,600))
        except Exception:
            self.bg_image = None
        try:
            self.sfx_move = pygame.mixer.Sound("assets/sounds/방향키 이동 브금.wav")
            self.audio.register_sfx(self.sfx_move)
        except Exception:
            self.sfx_move = None
        try:
            self.sfx_confirm = pygame.mixer.Sound("assets/sounds/선택 브금.wav")
            self.audio.register_sfx(self.sfx_confirm)
        except Exception:
            self.sfx_confirm = None
        self.bgm_path = "assets/sounds/설정 화면 브금.mp3"
        self._start_called = False

    def start(self):
        self._start_called = True
        if self.bgm_path:
            self.audio.play_music(self.bgm_path)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                prev = self.selected
                self.selected = (self.selected - 1) % len(self.options)
                if self.selected != prev and self.sfx_move:
                    try: self.sfx_move.play()
                    except Exception: pass
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                prev = self.selected
                self.selected = (self.selected + 1) % len(self.options)
                if self.selected != prev and self.sfx_move:
                    try: self.sfx_move.play()
                    except Exception: pass
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                if self.selected == 0:
                    self.bgm_volume = max(0.0, round(self.bgm_volume - 0.1, 2))
                    self.audio.set_music_volume(self.bgm_volume)
                else:
                    self.sfx_volume = max(0.0, round(self.sfx_volume - 0.1, 2))
                    self.audio.set_sfx_volume(self.sfx_volume)
                if self.sfx_move:
                    try: self.sfx_move.play()
                    except Exception: pass
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                if self.selected == 0:
                    self.bgm_volume = min(1.0, round(self.bgm_volume + 0.1, 2))
                    self.audio.set_music_volume(self.bgm_volume)
                else:
                    self.sfx_volume = min(1.0, round(self.sfx_volume + 0.1, 2))
                    self.audio.set_sfx_volume(self.sfx_volume)
                if self.sfx_move:
                    try: self.sfx_move.play()
                    except Exception: pass
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                if self.sfx_confirm:
                    try: self.sfx_confirm.play()
                    except Exception: pass
            elif event.key == pygame.K_ESCAPE:
                if self.previous_scene:
                    if hasattr(self.previous_scene, "start"):
                        if isinstance(self.previous_scene, PlayScene):
                            self.previous_scene.start(resume_from_options=True)
                        else:
                            self.previous_scene.start()
                    return self.previous_scene
        return None

    def update(self, dt):
        return

    def draw(self, screen):
        if self.bg_image:
            screen.blit(self.bg_image, (0,0))
        else:
            screen.fill((50,50,60))
        for i, opt in enumerate(self.options):
            color = (255,69,0) if i == self.selected else (80,80,80)
            if i == 0:
                text = f"{opt}: {int(self.bgm_volume*100)}%"
            else:
                text = f"{opt}: {int(self.sfx_volume*100)}%"
            surf, rect = self.font.render(text, color)
            screen.blit(surf, (400 - rect.width//2, 200 + i*60))
        hint_surf, hint_rect = self.font.render("ESC를 눌러 이전 화면으로 돌아가세요", (200,200,200))
        screen.blit(hint_surf, (10, screen.get_height() - hint_rect.height - 10))
