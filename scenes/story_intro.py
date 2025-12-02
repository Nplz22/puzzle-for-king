import pygame, os
from scenes import fonts
from scenes.audio import get_audio_manager

class StoryIntro:
    def __init__(self, lines, bgm_path=None, bgm_volume=0.1, previous_scene=None, next_scene=None, sfx_path=None, bg_image_path=None):
        self.lines = lines
        self.index = 0
        self.font = fonts.malgun_font
        self.bgm_path = bgm_path
        self.bgm_volume = bgm_volume
        self.previous_scene = previous_scene
        self.next_scene = next_scene
        self.typing = True
        self.type_pos = 0
        self.type_speed = 60.0
        self.type_timer = 0.0
        self.padding = 40
        self.bg_image = None
        self.audio = get_audio_manager()
        try:
            if sfx_path:
                self.select_sfx = pygame.mixer.Sound(sfx_path)
                self.audio.register_sfx(self.select_sfx)
            else:
                self.select_sfx = pygame.mixer.Sound("assets/sounds/선택 브금.wav")
                self.audio.register_sfx(self.select_sfx)
        except Exception:
            self.select_sfx = None
        if bg_image_path and os.path.isfile(bg_image_path):
            try:
                img = pygame.image.load(bg_image_path).convert()
                screen = pygame.display.get_surface()
                if screen:
                    w, h = screen.get_size()
                    self.bg_image = pygame.transform.smoothscale(img, (w, h))
                else:
                    self.bg_image = img
            except Exception:
                self.bg_image = None

    def start(self):
        if self.bgm_path:
            self.audio.play_music(self.bgm_path)
        else:
            self.audio.stop_music()
        self.index = 0
        self.type_pos = 0
        self.typing = True
        self.type_timer = 0.0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                if self.select_sfx:
                    try: self.select_sfx.play()
                    except Exception: pass
                if self.typing:
                    self.type_pos = len(self.lines[self.index])
                    self.typing = False
                    return None
                else:
                    if self.index < len(self.lines) - 1:
                        self.index += 1
                        self.type_pos = 0
                        self.typing = True
                        self.type_timer = 0.0
                        return None
                    else:
                        try: self.audio.stop_music()
                        except Exception: pass
                        if self.next_scene:
                            return self.next_scene
                        if self.previous_scene:
                            return self.previous_scene
                        return None
            elif event.key == pygame.K_ESCAPE:
                try: self.audio.stop_music()
                except Exception: pass
                if self.previous_scene:
                    return self.previous_scene
        return None

    def update(self, dt):
        if not self.typing:
            return
        self.type_timer += dt
        chars = int(self.type_timer * self.type_speed)
        if chars > 0:
            self.type_pos = min(len(self.lines[self.index]), self.type_pos + chars)
            self.type_timer -= chars / self.type_speed
            if self.type_pos >= len(self.lines[self.index]):
                self.typing = False

    def draw(self, screen):
        if self.bg_image:
            screen.blit(self.bg_image, (0,0))
        else:
            screen.fill((20,20,20))
        w, h = screen.get_size()
        box = pygame.Rect(self.padding, h - 180, w - self.padding*2, 140)
        pygame.draw.rect(screen, (10,10,14), box)
        pygame.draw.rect(screen, (80,80,90), box, 2)
        text = self.lines[self.index][:self.type_pos]
        maxw = box.width - 20
        words = text.split(" ")
        cur = ""
        lines = []
        for word in words:
            test = (cur + " " + word).strip()
            surf, rect = self.font.render(test, (220,220,220))
            if surf.get_width() > maxw and cur != "":
                lines.append(cur)
                cur = word
            else:
                cur = test
        if cur != "":
            lines.append(cur)
        y = box.top + 10
        for ln in lines:
            surf, rect = self.font.render(ln, (220,220,220))
            screen.blit(surf, (box.left + 10, y))
            y += rect.height + 6
        hint = "엔터: 문장 빠르게 표시" if self.typing else "엔터: 다음 / 마지막이면 종료"
        hint_surf, hint_rect = self.font.render(hint, (160,160,160))
        screen.blit(hint_surf, (box.right - hint_rect.width - 10, box.bottom - hint_rect.height - 8))
