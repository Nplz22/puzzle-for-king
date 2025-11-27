import pygame, sys

class TitleScene:
    def __init__(self):
        self.font_large = pygame.font.Font(None, 64)
        self.font_small = pygame.font.Font(None, 28)
        self.buttons = ["게임 시작", "설정", "종료"]
        self.selected = 0
        self.blink = True
        self.blink_timer = 0

        self.select_sfx = pygame.mixer.Sound("assets/sounds/방향키 이동 브금.wav")
        self.confirm_sfx = pygame.mixer.Sound("assets/sounds/선택 브금.wav")
        self.select_sfx.set_volume(0.3)
        self.confirm_sfx.set_volume(0.3)

    def start(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load("assets/sounds/타이틀 브금.mp3")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.confirm_sfx.play()
                choice = self.buttons[self.selected]
                if choice == "게임 시작":
                    return "play"
                elif choice == "설정":
                    print("Settings 선택됨")
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
            for i, btn in enumerate(self.buttons):
                btn_rect = pygame.Rect(300, 250 + i*50, 200, 40)
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
        screen.fill((30,30,50))
        title_surf = self.font_large.render("MY GAME", True, (240,240,240))
        screen.blit(title_surf, title_surf.get_rect(center=(400, 150)))

        for i, btn in enumerate(self.buttons):
            color = (255,255,255) if i == self.selected else (180,180,180)
            btn_surf = self.font_small.render(btn, True, color)
            screen.blit(btn_surf, btn_surf.get_rect(center=(400, 250 + i*50)))

        if self.blink:
            info_surf = self.font_small.render("스페이스 바/엔터 키를 눌러서 선택하세요", True, (200,200,200))
            screen.blit(info_surf, info_surf.get_rect(center=(400, 500)))
