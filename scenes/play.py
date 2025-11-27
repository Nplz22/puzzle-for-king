import pygame, sys

class PlayScene:
    def __init__(self):
        self.player = pygame.Rect(380, 260, 32, 48)
        self.speed = 200
        self.font = pygame.font.Font(None, 24)
        self.paused = False
        self.menu_items = ["Resume", "Settings", "Quit"]
        self.menu_index = 0

    def start(self):
        # 플레이 BGM
        pygame.mixer.music.stop()
        pygame.mixer.music.load("assets/sounds/play_bgm.mp3")
        pygame.mixer.music.set_volume(0.5)
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
        if choice == "Resume":
            self.paused = False
        elif choice == "Settings":
            print("Settings 선택됨")
        elif choice == "Quit":
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
        info = self.font.render("ESC: Pause Menu", True, (220,220,220))
        screen.blit(info, (10,10))

        if self.paused:
            # 메뉴 오버레이
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0,0,0,150))
            screen.blit(overlay, (0,0))
            for i, item in enumerate(self.menu_items):
                color = (255,255,255) if i==self.menu_index else (180,180,180)
                item_surf = self.font.render(item, True, color)
                screen.blit(item_surf, item_surf.get_rect(center=(400,200 + i*50)))
