import pygame
from scenes import fonts

class PlayScene:
    def __init__(self, bgm_volume=0.1, sfx_volume=0.3, previous_scene=None):
        self.player = pygame.Rect(380, 260, 32, 48)
        self.speed = 200
        self.font = fonts.malgun_font
        self.menu_items = ["계속하기", "설정", "종료"]
        self.menu_index = 0
        self.bgm_volume = bgm_volume
        self.sfx_volume = sfx_volume
        self.previous_scene = previous_scene
        try:
            self.sfx_move = pygame.mixer.Sound("assets/sounds/방향키 이동 브금.wav")
        except Exception:
            self.sfx_move = None
        self.grid_origin = (100, 100)
        self.cell_size = 48
        self.grid_cols = 10
        self.grid_rows = 8

    def start(self):
        try:
            if self.bgm_volume <= 0:
                pygame.mixer.music.stop()
                return
            pygame.mixer.music.stop()
            pygame.mixer.music.load("assets/sounds/스토리 요약 브금.mp3")
            pygame.mixer.music.set_volume(self.bgm_volume)
            pygame.mixer.music.play(-1)
        except Exception:
            pass

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "pause"
        return None

    def update(self, dt):
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * self.speed * dt
        dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * self.speed * dt
        self.player.x += dx
        self.player.y += dy
        left, top = self.grid_origin
        max_x = left + self.grid_cols*self.cell_size - self.player.width
        max_y = top + self.grid_rows*self.cell_size - self.player.height
        self.player.x = max(left, min(self.player.x, max_x))
        self.player.y = max(top, min(self.player.y, max_y))

    def draw(self, screen):
        screen.fill((40,60,50))
        gx, gy = self.grid_origin
        cs = self.cell_size
        for r in range(self.grid_rows):
            for c in range(self.grid_cols):
                cell_rect = pygame.Rect(gx + c*cs, gy + r*cs, cs, cs)
                pygame.draw.rect(screen, (60,80,70), cell_rect, 1)
        px, py = self.player.center
        cell_x = (px - gx) // cs
        cell_y = (py - gy) // cs
        if 0 <= cell_x < self.grid_cols and 0 <= cell_y < self.grid_rows:
            highlight = pygame.Rect(gx + cell_x*cs, gy + cell_y*cs, cs, cs)
            pygame.draw.rect(screen, (120,160,120), highlight)
        pygame.draw.rect(screen, (200,200,255), self.player)
        info_surf, info_rect = self.font.render("ESC: 일시정지 메뉴", (220,220,220))
        screen.blit(info_surf, (10,10))
