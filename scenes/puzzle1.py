import pygame
from scenes import fonts
from scenes.audio import get_audio_manager
from scenes.puzzle import PuzzleBackground

class Puzzle1:
    def __init__(self, previous_scene=None, bgm_path=None, screen_size=None):
        self.font = fonts.malgunbd_font_small
        self.previous_scene = previous_scene
        self.completed = False
        self.audio = get_audio_manager()
        self.bgm_path = "assets/sounds/puzzle1 브금.mp3"
        screen = pygame.display.get_surface()
        w, h = screen.get_size() if screen else (800, 600)
        self.bg_image = PuzzleBackground(width=w, height=h).image
        self.current_index = 0
        self.problems = [
            "물음표에 들어갈 것은?\n\n   I am on Ear Pad [?]",
            "문제 2 내용",
            "문제 3 내용"
        ]
        self.hint_text = "트럼프 카드 모양을\n생각해 보세요!"
        self.show_hint = False
        self.hint_rect = pygame.Rect(20, h - 50, 80, 30)

    def start(self):
        if self.bgm_path:
            self.audio.play_music(self.bgm_path)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.hint_rect.collidepoint(event.pos):
                self.show_hint = not self.show_hint
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):
            self.current_index += 1
            if self.current_index >= len(self.problems):
                self.completed = True
                return self.previous_scene
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "options"
        return None

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.blit(self.bg_image, (0, 0))
        if self.current_index < len(self.problems):
            lines = self.problems[self.current_index].split("\n")
            y_offset = 240
            x_offset = 250
            for line in lines:
                text_surf, _ = self.font.render(line, (0, 0, 0))
                screen.blit(text_surf, (x_offset, y_offset))
                y_offset += 40
        esc_surf, _ = self.font.render("ESC: 옵션", (240, 240, 240))
        screen.blit(esc_surf, (10, 10))
        pygame.draw.rect(screen, (200,200,200), self.hint_rect, border_radius=4)
        hint_label, _ = self.font.render("힌트", (0,0,0))
        screen.blit(hint_label, (self.hint_rect.x + 10, self.hint_rect.y + 5))
        if self.show_hint:
            hint_box = pygame.Rect(120, screen.get_height()-150, 400, 100)
            pygame.draw.rect(screen, (255,255,255), hint_box, border_radius=6)
            pygame.draw.rect(screen, (0,0,0), hint_box, 2, border_radius=6)
            hint_surf, _ = self.font.render(self.hint_text, (0,0,0))
            screen.blit(hint_surf, (hint_box.x + 10, hint_box.y + 10))
