import pygame
from scenes import fonts
from scenes.audio import get_audio_manager
from scenes.puzzle import Puzzle

class Puzzle1:
    def __init__(self, previous_scene=None):
        self.font = fonts.malgun_font
        self.previous_scene = previous_scene
        self.completed = False
        self.audio = get_audio_manager()
        self.bgm_path = "assets/sounds/puzzle1 브금.mp3"
        screen = pygame.display.get_surface()
        screen_size = screen.get_size() if screen else (800, 600)
        self.bg_image = Puzzle(previous_scene=self.previous_scene, bgm_path=self.bgm_path, screen_size=screen_size).bg_image

    def start(self):
        if self.bgm_path:
            self.audio.play_music(self.bgm_path)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.completed = True
                return self.previous_scene
            if event.key == pygame.K_ESCAPE:
                return "options"
        return None

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.blit(self.bg_image, (0, 0))
        text_surf, text_rect = self.font.render("퍼즐1: 엔터를 눌러 완료", (240, 240, 240))
        screen.blit(text_surf, (200, 280))
        esc_surf, esc_rect = self.font.render("ESC: 옵션", (240, 240, 240))
        screen.blit(esc_surf, (10, 10))
