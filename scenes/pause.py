import pygame
import sys

class PauseMenu:
    def __init__(self, screen_width=800, screen_height=600):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 32)
        self.menu_items = ["Resume", "Settings", "Quit"]
        self.menu_index = 0
        self.active = False

    def toggle(self):
        self.active = not self.active
        if self.active:
            self.menu_index = 0

    def handle_event(self, event):
        if not self.active:
            return None

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.menu_index = (self.menu_index - 1) % len(self.menu_items)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.menu_index = (self.menu_index + 1) % len(self.menu_items)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                return self.select_item()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            for i, item in enumerate(self.menu_items):
                item_rect = pygame.Rect(300, 200 + i*50, 200, 40)
                if item_rect.collidepoint(mx, my):
                    self.menu_index = i
                    return self.select_item()
        return None

    def select_item(self):
        choice = self.menu_items[self.menu_index]
        if choice == "Resume":
            self.active = False
        elif choice == "Settings":
            print("Settings 선택됨 (여기에 설정창 로직 추가)")
        elif choice == "Quit":
            pygame.quit()
            sys.exit()
        return None

    def draw(self, screen):
        if not self.active:
            return
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0,0,0,150))
        screen.blit(overlay, (0,0))

        for i, item in enumerate(self.menu_items):
            color = (255,255,255) if i == self.menu_index else (180,180,180)
            text_surf = self.font.render(item, True, color)
            screen.blit(text_surf, text_surf.get_rect(center=(self.screen_width//2, 200 + i*50)))
