import pygame, sys
from scenes import fonts

class PlayScene:
    def __init__(self):
        self.player = pygame.Rect(380, 260, 32, 48)
        self.speed = 200
        self.font = fonts.malgun_font
        self.paused = False
        self.menu_items = ["계속하기", "설정", "종료"]
        self.menu_index = 0
        self.bgm_volume = 0.1
        self.sfx_volume = 0.3
        self.previous_scene = None

    def start(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load("assets/sounds/스토리 요약 브금.mp3")
        pygame.mixer.music.set_volume(self.bgm_volume)
        pygame.mixer.music.play(-1)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.paused = not self.paused
                if self.paused:
                    self.menu_index = 0
                return None
            if self.paused:
                if event.key in (pygame.K_UP, pygame.K_w):
                    self.menu_index = (self.menu_index - 1) % len(self.menu_items)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self.menu_index = (self.menu_index + 1) % len(self.menu_items)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return self.handle_menu_confirm()
                return None
        elif event.type == pygame.MOUSEBUTTONDOWN and self.paused:
            mx, my = event.pos
            for i, item in enumerate(self.menu_items):
                item_rect = pygame.Rect(300, 200 + i*50, 200, 40)
                if item_rect.collidepoint(mx, my):
                    self.menu_index = i
                    return self.handle_menu_confirm()
        return None

    def handle_menu_confirm(self):
        choice = self.menu_items[self.menu_index]
        if choice == "계속":
            self.paused = False
        elif choice == "설정":
            return "options"
        elif choice == "종료":
            pygame.quit()
            sys.exit()
        return None

    def update(self, dt):
        if self.paused:
            return
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * self.speed * dt
        dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * self.speed * dt
        self.player.x += dx
        self.player.y += dy

    def draw(self, screen):
        screen.fill((40,60,50))
        pygame.draw.rect(screen, (200,200,255), self.player)
        info_surf, info_rect = self.font.render("ESC: 일시정지 메뉴", (220,220,220))
        screen.blit(info_surf, (10,10))
