import pygame, sys
from scenes import fonts
from scenes.options import OptionsScene

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
        self.options_scene = OptionsScene(bgm_volume=self.bgm_volume, sfx_volume=self.sfx_volume, previous_scene=self)

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
        if choice == "계속하기":
            self.active = False
            return None
        elif choice == "설정":
            return "options"
        elif choice == "종료":
            pygame.quit(); sys.exit()
        return None

    def update(self, dt):
        if self.menu_index == 1:
            self.options_scene.update(dt)

    def draw(self, screen):
        if not self.active:
            return
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0,0,0,150))
        screen.blit(overlay, (0,0))
        for i, item in enumerate(self.menu_items):
            color = (255,69,0) if i == self.menu_index else (180,180,180)
            text_surf, rect = self.font.render(item, color)
            screen.blit(text_surf, (self.screen_width//2 - rect.width//2, 200 + i*50))
        if self.menu_index == 1:
            self.options_scene.draw(screen)
