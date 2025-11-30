import pygame, os
from scenes import fonts
from scenes.audio import get_audio_manager

class OptionsScene:
    def __init__(self, bgm_volume=0.1, sfx_volume=0.3, previous_scene=None):
        self.font = fonts.malgunbd_font_small
        self.options = ["BGM 볼륨", "효과음 볼륨", "타이틀 화면으로 돌아가기"]
        self.selected = 0
        self.bgm_volume = bgm_volume
        self.sfx_volume = sfx_volume
        self.previous_scene = previous_scene
        try:
            img = pygame.image.load("assets/images/title background.png").convert()
            self.bg_image = pygame.transform.scale(img, (800,600))
        except Exception:
            self.bg_image = None
        self.audio = get_audio_manager()
        self.audio.set_sfx_volume(self.sfx_volume)
        try:
            self.sfx_move = pygame.mixer.Sound("assets/sounds/방향키 이동 브금.wav")
            self.sfx_move.set_volume(self.audio.sfx_volume)
        except Exception:
            self.sfx_move = None
        try:
            self.sfx_confirm = pygame.mixer.Sound("assets/sounds/선택 브금.wav")
            self.sfx_confirm.set_volume(self.audio.sfx_volume)
        except Exception:
            self.sfx_confirm = None
        self.bgm_path = "assets/sounds/설정 화면 브금.mp3"

    def start(self):
        if self.bgm_path:
            self.audio.play_music(self.bgm_path, volume=self.bgm_volume)
        return

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                prev = self.selected
                self.selected = (self.selected - 1) % len(self.options)
                if self.selected != prev and self.sfx_move:
                    try: self.sfx_move.play()
                    except Exception: pass
                return None
            if event.key in (pygame.K_DOWN, pygame.K_s):
                prev = self.selected
                self.selected = (self.selected + 1) % len(self.options)
                if self.selected != prev and self.sfx_move:
                    try: self.sfx_move.play()
                    except Exception: pass
                return None
            if event.key in (pygame.K_LEFT, pygame.K_a):
                if self.selected == 0:
                    self.bgm_volume = max(0.0, round(self.bgm_volume - 0.1, 2))
                    self.audio.set_music_volume(self.bgm_volume)
                    if self.bgm_volume == 0:
                        try: self.audio.pause_music()
                        except Exception: pass
                    if self.sfx_move:
                        try: self.sfx_move.play()
                        except Exception: pass
                elif self.selected == 1:
                    self.sfx_volume = max(0.0, round(self.sfx_volume - 0.1, 2))
                    self.audio.set_sfx_volume(self.sfx_volume)
                    if self.sfx_move:
                        try: self.sfx_move.set_volume(self.audio.sfx_volume); self.sfx_move.play()
                        except Exception: pass
                return None
            if event.key in (pygame.K_RIGHT, pygame.K_d):
                if self.selected == 0:
                    prev = self.bgm_volume
                    self.bgm_volume = min(1.0, round(self.bgm_volume + 0.1, 2))
                    self.audio.set_music_volume(self.bgm_volume)
                    if prev == 0 and self.bgm_volume > 0 and self.audio.current_path:
                        try: self.audio.unpause_music()
                        except Exception: pass
                    if self.sfx_move:
                        try: self.sfx_move.play()
                        except Exception: pass
                elif self.selected == 1:
                    self.sfx_volume = min(1.0, round(self.sfx_volume + 0.1, 2))
                    self.audio.set_sfx_volume(self.sfx_volume)
                    if self.sfx_move:
                        try: self.sfx_move.set_volume(self.audio.sfx_volume); self.sfx_move.play()
                        except Exception: pass
                return None
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                if self.sfx_confirm:
                    try: self.sfx_confirm.play()
                    except Exception: pass
                if self.selected == 2:
                    return "title"
                return None
            if event.key == pygame.K_ESCAPE:
                return "title"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            for i, opt in enumerate(self.options):
                item_rect = pygame.Rect(300, 200 + i * 60, 400, 40)
                if item_rect.collidepoint(mx, my):
                    self.selected = i
                    if self.sfx_move:
                        try: self.sfx_move.play()
                        except Exception: pass
                    if i == 2:
                        if self.sfx_confirm:
                            try: self.sfx_confirm.play()
                            except Exception: pass
                        return "title"
        return None

    def update(self, dt):
        return

    def draw(self, screen):
        if self.bg_image:
            screen.blit(self.bg_image, (0,0))
        else:
            screen.fill((50,50,60))
        for i, opt in enumerate(self.options):
            color = (255,165,0) if i == self.selected else (180,180,180)
            if i == 0:
                text = f"{opt}: {int(self.bgm_volume*100)}%"
            elif i == 1:
                text = f"{opt}: {int(self.sfx_volume*100)}%"
            else:
                text = opt
            surf, rect = self.font.render(text, color)
            screen.blit(surf, (400 - rect.width//2, 200 + i*60))
