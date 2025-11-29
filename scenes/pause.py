import pygame, sys
from scenes import fonts

class PauseMenu:
    def __init__(self, screen_width=800, screen_height=600, bgm_volume=0.1, sfx_volume=0.3, previous_scene=None):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = fonts.malgunbd_font_small
        self.menu_items = ["계속하기", "설정", "종료"]
        self.menu_index = 0
        self.active = False
        self.bgm_volume = bgm_volume
        self.sfx_volume = sfx_volume
        self.previous_scene = previous_scene
        self.options_scene = None
        self.options_bgm = "assets/sounds/설정 화면 브금.mp3"
        self.bgm_playing = False
        try:
            self.sfx_move = pygame.mixer.Sound("assets/sounds/방향키 이동 브금.wav")
            self.sfx_confirm = pygame.mixer.Sound("assets/sounds/선택 브금.wav")
        except Exception:
            self.sfx_move = None
            self.sfx_confirm = None

    def start(self):
        self.active = True
        self.menu_index = 0
        try:
            if self.bgm_volume > 0:
                try:
                    pygame.mixer.music.stop()
                except Exception:
                    pass
                try:
                    pygame.mixer.music.load(self.options_bgm)
                    pygame.mixer.music.set_volume(self.bgm_volume)
                    pygame.mixer.music.play(-1)
                    self.bgm_playing = True
                except Exception:
                    self.bgm_playing = False
            else:
                try:
                    pygame.mixer.music.stop()
                except Exception:
                    pass
                self.bgm_playing = False
        except Exception:
            self.bgm_playing = False

    def stop(self):
        if self.bgm_playing:
            try:
                pygame.mixer.music.stop()
            except Exception:
                pass
            self.bgm_playing = False
        self.active = False

    def handle_event(self, event):
        if not self.active:
            return None
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                prev = self.menu_index
                self.menu_index = (self.menu_index - 1) % len(self.menu_items)
                if self.menu_index != prev and self.sfx_move:
                    try:
                        self.sfx_move.set_volume(self.sfx_volume)
                        self.sfx_move.play()
                    except Exception:
                        pass
                return None
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                prev = self.menu_index
                self.menu_index = (self.menu_index + 1) % len(self.menu_items)
                if self.menu_index != prev and self.sfx_move:
                    try:
                        self.sfx_move.set_volume(self.sfx_volume)
                        self.sfx_move.play()
                    except Exception:
                        pass
                return None
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                return self.select_item()
        elif event.type == pygame.MOUSEMOTION:
            mx, my = event.pos
            for i in range(len(self.menu_items)):
                item_rect = pygame.Rect(self.screen_width//2 - 100, 200 + i*50, 200, 40)
                if item_rect.collidepoint(mx, my):
                    if self.menu_index != i:
                        self.menu_index = i
                        if self.sfx_move:
                            try:
                                self.sfx_move.set_volume(self.sfx_volume)
                                self.sfx_move.play()
                            except Exception:
                                pass
                    break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            for i in range(len(self.menu_items)):
                item_rect = pygame.Rect(self.screen_width//2 - 100, 200 + i*50, 200, 40)
                if item_rect.collidepoint(mx, my):
                    self.menu_index = i
                    return self.select_item()
        return None

    def select_item(self):
        choice = self.menu_items[self.menu_index]
        if choice == "계속하기":
            try:
                if self.bgm_playing:
                    pygame.mixer.music.stop()
            except Exception:
                pass
            self.bgm_playing = False
            self.active = False
            return self.previous_scene
        elif choice == "설정":
            try:
                if self.bgm_playing:
                    pygame.mixer.music.stop()
            except Exception:
                pass
            self.bgm_playing = False
            try:
                from scenes.options import OptionsScene
                opt = OptionsScene(bgm_volume=self.bgm_volume, sfx_volume=self.sfx_volume, previous_scene=self.previous_scene)
                try:
                    opt.start()
                except Exception:
                    pass
                return opt
            except Exception:
                return "options"
        elif choice == "종료":
            pygame.quit()
            sys.exit()
        return None

    def update(self, dt):
        if not self.active:
            return
        # pause 내부에선 특별한 업데이트 없음

    def draw(self, screen):
        if not self.active:
            return
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0,0,0,150))
        screen.blit(overlay, (0,0))
        for i, item in enumerate(self.menu_items):
            color = (255,165,0) if i == self.menu_index else (80,80,80)
            text_surf, rect = self.font.render(item, color)
            x = self.screen_width//2 - rect.width//2
            y = 200 + i*50
            screen.blit(text_surf, (x, y))
            if i == self.menu_index:
                marker = self.font.render("▶", color)[0]
                screen.blit(marker, (x - 30, y))
