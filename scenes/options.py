import pygame
from scenes import fonts

class OptionsScene:
    def __init__(self, bgm_volume=0.1, sfx_volume=0.3, previous_scene=None):
        self.font = fonts.malgunbd_font_small
        self.selected = 0
        self.bgm_volume = bgm_volume
        self.sfx_volume = sfx_volume
        self.previous_scene = previous_scene
        try:
            self.bg_image = pygame.image.load("assets/images/title background.png").convert()
            self.bg_image = pygame.transform.scale(self.bg_image, (800, 600))
        except Exception:
            self.bg_image = pygame.Surface((800, 600))
            self.bg_image.fill((50, 50, 70))
        self.options_bgm = "assets/sounds/설정 화면 브금.mp3"
        self.bgm_playing = False
        try:
            self.sfx_move = pygame.mixer.Sound("assets/sounds/방향키 이동 브금.wav")
        except Exception:
            self.sfx_move = None
        try:
            self.sfx_confirm = pygame.mixer.Sound("assets/sounds/선택 브금.wav")
        except Exception:
            self.sfx_confirm = None
        self._build_options()
        self._apply_sfx_volume()

    def _build_options(self):
        base = ["BGM 볼륨", "효과음 볼륨"]
        add_prev = False
        if self.previous_scene is not None:
            clsname = getattr(self.previous_scene.__class__, "__name__", "")
            if clsname != "TitleScene":
                add_prev = True
        if add_prev:
            base.append("원래 화면으로 돌아가기")
        base.append("타이틀로 돌아가기")
        self.options = base

    def _apply_sfx_volume(self):
        if self.sfx_move:
            try:
                self.sfx_move.set_volume(self.sfx_volume)
            except Exception:
                pass
        if self.sfx_confirm:
            try:
                self.sfx_confirm.set_volume(self.sfx_volume)
            except Exception:
                pass

    def _ensure_bgm_playing(self):
        try:
            if self.bgm_volume <= 0:
                try:
                    pygame.mixer.music.stop()
                except Exception:
                    pass
                self.bgm_playing = False
                return
            if not pygame.mixer.music.get_busy() or not self.bgm_playing:
                try:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(self.options_bgm)
                    pygame.mixer.music.set_volume(self.bgm_volume)
                    pygame.mixer.music.play(-1)
                    self.bgm_playing = True
                except Exception:
                    self.bgm_playing = False
            else:
                try:
                    pygame.mixer.music.set_volume(self.bgm_volume)
                except Exception:
                    pass
        except Exception:
            pass

    def start(self):
        self._ensure_bgm_playing()
        self._build_options()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                prev = self.selected
                self.selected = (self.selected - 1) % len(self.options)
                if self.selected != prev and self.sfx_move:
                    try:
                        self.sfx_move.play()
                    except Exception:
                        pass
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                prev = self.selected
                self.selected = (self.selected + 1) % len(self.options)
                if self.selected != prev and self.sfx_move:
                    try:
                        self.sfx_move.play()
                    except Exception:
                        pass
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                if self.options[self.selected] == "BGM 볼륨":
                    self.bgm_volume = max(0.0, round(self.bgm_volume - 0.1, 2))
                    if self.bgm_volume == 0:
                        try:
                            pygame.mixer.music.stop()
                        except Exception:
                            pass
                        self.bgm_playing = False
                    else:
                        self._ensure_bgm_playing()
                    if self.sfx_move:
                        try:
                            self.sfx_move.play()
                        except Exception:
                            pass
                elif self.options[self.selected] == "효과음 볼륨":
                    self.sfx_volume = max(0.0, round(self.sfx_volume - 0.1, 2))
                    self._apply_sfx_volume()
                    if self.sfx_move:
                        try:
                            self.sfx_move.play()
                        except Exception:
                            pass
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                if self.options[self.selected] == "BGM 볼륨":
                    self.bgm_volume = min(1.0, round(self.bgm_volume + 0.1, 2))
                    self._ensure_bgm_playing()
                    if self.sfx_move:
                        try:
                            self.sfx_move.play()
                        except Exception:
                            pass
                elif self.options[self.selected] == "효과음 볼륨":
                    self.sfx_volume = min(1.0, round(self.sfx_volume + 0.1, 2))
                    self._apply_sfx_volume()
                    if self.sfx_move:
                        try:
                            self.sfx_move.play()
                        except Exception:
                            pass
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                if self.sfx_confirm:
                    try:
                        self.sfx_confirm.play()
                    except Exception:
                        pass
                return self._select_current()
        elif event.type == pygame.MOUSEMOTION:
            mx, my = event.pos
            for i, opt in enumerate(self.options):
                item_rect = pygame.Rect(300, 200 + i * 60, 400, 40)
                if item_rect.collidepoint(mx, my):
                    if self.selected != i:
                        self.selected = i
                        if self.sfx_move:
                            try:
                                self.sfx_move.play()
                            except Exception:
                                pass
                    break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            for i, opt in enumerate(self.options):
                item_rect = pygame.Rect(300, 200 + i * 60, 400, 40)
                if item_rect.collidepoint(mx, my):
                    self.selected = i
                    if self.sfx_confirm:
                        try:
                            self.sfx_confirm.play()
                        except Exception:
                            pass
                    return self._select_current()
        return None

    def _select_current(self):
        choice = self.options[self.selected]
        if choice == "원래 화면으로 돌아가기":
            if self.previous_scene is not None:
                try:
                    self.previous_scene.bgm_volume = self.bgm_volume
                    self.previous_scene.sfx_volume = self.sfx_volume
                except Exception:
                    pass
            return self.previous_scene
        if choice == "타이틀로 돌아가기":
            if self.previous_scene is not None:
                try:
                    self.previous_scene.bgm_volume = self.bgm_volume
                    self.previous_scene.sfx_volume = self.sfx_volume
                except Exception:
                    pass
            return "title"
        return None

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.blit(self.bg_image, (0, 0))
        for i, opt in enumerate(self.options):
            color = (255,165,0) if i == self.selected else (80,80,80)
            if opt == "BGM 볼륨":
                text = f"{opt}: {int(self.bgm_volume * 100)}%"
            elif opt == "효과음 볼륨":
                text = f"{opt}: {int(self.sfx_volume * 100)}%"
            else:
                text = opt
            surf, rect = self.font.render(text, color)
            screen.blit(surf, (400 - rect.width // 2, 200 + i * 60))
