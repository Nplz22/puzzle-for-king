import pygame, sys, os
from scenes import fonts
from scenes.audio import get_audio_manager

class TitleScene:
    def __init__(self):
        self.font_large = fonts.malgunbd_font_big
        self.font_small = fonts.malgun_font
        self.buttons = ["게임 시작", "설정", "종료"]
        self.selected = 0
        self.blink = True
        self.blink_timer = 0

        self.audio = get_audio_manager()

        try:
            self.select_sfx = pygame.mixer.Sound("assets/sounds/방향키 이동 브금.wav")
            self.audio.register_sfx(self.select_sfx)
        except Exception:
            self.select_sfx = None

        try:
            self.confirm_sfx = pygame.mixer.Sound("assets/sounds/선택 브금.wav")
            self.audio.register_sfx(self.confirm_sfx)
        except Exception:
            self.confirm_sfx = None

        try:
            img = pygame.image.load("assets/images/title background.png").convert()
            self.bg_image = pygame.transform.scale(img, (800, 600))
        except Exception:
            self.bg_image = None

        self.bgm_path = "assets/sounds/타이틀 브금.mp3"

    def start(self):
        try:
            pygame.mixer.stop()
        except Exception:
            pass
        self.audio.play_music(self.bgm_path)

    def _play_sfx_now(self, sfx):
        if not sfx:
            return
        try:
            sfx.set_volume(self.audio.sfx_volume * getattr(self.audio, "master_volume", 1.0))
        except Exception:
            pass
        try:
            sfx.play()
        except Exception:
            pass

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                if self.confirm_sfx:
                    self._play_sfx_now(self.confirm_sfx)
                choice = self.buttons[self.selected]
                if choice == "게임 시작":
                    return "story"
                elif choice == "설정":
                    return "options"
                elif choice == "종료":
                    pygame.quit()
                    sys.exit()

            elif event.key in (pygame.K_UP, pygame.K_w):
                self.selected = (self.selected - 1) % len(self.buttons)
                if self.select_sfx:
                    self._play_sfx_now(self.select_sfx)

            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected = (self.selected + 1) % len(self.buttons)
                if self.select_sfx:
                    self._play_sfx_now(self.select_sfx)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            button_gap = 80
            start_y = 250
            for i, btn in enumerate(self.buttons):
                btn_rect = pygame.Rect(300, start_y + i * button_gap, 200, 40)
                if btn_rect.collidepoint(mx, my):
                    self.selected = i
                    if self.select_sfx:
                        self._play_sfx_now(self.select_sfx)

                    choice = self.buttons[self.selected]
                    if choice == "게임 시작":
                        return "story"
                    elif choice == "설정":
                        return "options"
                    elif choice == "종료":
                        pygame.quit()
                        sys.exit()

        return None

    def update(self, dt):
        self.blink_timer += dt
        if self.blink_timer > 1.0:
            self.blink = not self.blink
            self.blink_timer = 0

    def draw(self, screen):
        if self.bg_image:
            screen.blit(self.bg_image, (0, 0))
        else:
            screen.fill((0, 0, 0))

        title_text = "Puzzle for the King"
        title_surf, title_rect = self.font_large.render(title_text, (255, 215, 0))
        screen.blit(title_surf, (400 - title_rect.width // 2, 150 - title_rect.height // 2))

        button_gap = 80
        start_y = 250
        for i, btn in enumerate(self.buttons):
            color = (255, 69, 0) if i == self.selected else (80, 80, 80)
            btn_surf, btn_rect = self.font_small.render(btn, color)
            screen.blit(btn_surf, (400 - btn_rect.width // 2, start_y + i * button_gap - btn_rect.height // 2))

        if self.blink:
            info_text = "스페이스 바/엔터 키를 눌러서 선택하세요"
            info_surf, info_rect = self.font_small.render(info_text, (255, 255, 255))
            screen.blit(info_surf, (400 - info_rect.width // 2, 500 - info_rect.height // 2))
