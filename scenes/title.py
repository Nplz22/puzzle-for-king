import pygame, sys
from scenes import fonts
from scenes.options import OptionsScene

class TitleScene:
    def __init__(self):
        self.font_large = fonts.malgunbd_font_big
        self.font_small = fonts.malgun_font
        self.buttons = ["게임 시작", "설정", "종료"]
        self.selected = 0
        self.blink = True
        self.blink_timer = 0
        self.select_sfx = pygame.mixer.Sound("assets/sounds/방향키 이동 브금.wav")
        self.confirm_sfx = pygame.mixer.Sound("assets/sounds/선택 브금.wav")
        self.select_sfx.set_volume(0.3)
        self.confirm_sfx.set_volume(0.3)
        self.bg_image = pygame.image.load("assets/images/title background.png").convert()
        self.bg_image = pygame.transform.scale(self.bg_image, (800, 600))
        self.bgm_volume = 0.1
        self.sfx_volume = 0.3

    def start(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load("assets/sounds/타이틀 브금.mp3")
        pygame.mixer.music.set_volume(self.bgm_volume)
        pygame.mixer.music.play(-1)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.confirm_sfx.play()
                choice = self.buttons[self.selected]
                if choice == "게임 시작":
                    return "play"
                elif choice == "설정":
                    return "options"
                elif choice == "종료":
                    pygame.quit()
                    sys.exit()
            elif event.key in (pygame.K_UP, pygame.K_w):
                self.selected = (self.selected - 1) % len(self.buttons)
                self.select_sfx.play()
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected = (self.selected + 1) % len(self.buttons)
                self.select_sfx.play()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            button_gap = 80
            start_y = 250
            for i, btn in enumerate(self.buttons):
                btn_rect = pygame.Rect(300, start_y + i*button_gap, 200, 40)
                if btn_rect.collidepoint(mx, my):
                    self.selected = i
                    self.select_sfx.play()
                    return self.handle_event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))
        return None

    def update(self, dt):
        self.blink_timer += dt
        if self.blink_timer > 1.0:
            self.blink = not self.blink
            self.blink_timer = 0

    def draw(self, screen):
        screen.blit(self.bg_image, (0,0))
        title_text = "Puzzle for the King"
        title_surf, title_rect = self.font_large.render(title_text, (255,215,0))
        screen.blit(title_surf, (400 - title_rect.width//2, 150 - title_rect.height//2))
        button_gap = 80
        start_y = 250
        for i, btn in enumerate(self.buttons):
            color = (255,69,0) if i == self.selected else (80,80,80)
            btn_surf, btn_rect = self.font_small.render(btn, color)
            screen.blit(btn_surf, (400 - btn_rect.width//2, start_y + i*button_gap - btn_rect.height//2))
        if self.blink:
            info_text = "스페이스 바/엔터 키를 눌러서 선택하세요"
            info_surf, info_rect = self.font_small.render(info_text, (255,255,255))
            screen.blit(info_surf, (400 - info_rect.width//2, 500 - info_rect.height//2))
