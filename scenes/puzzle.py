import pygame
from scenes import fonts
from scenes.audio import get_audio_manager

class PuzzleBackground:
    def __init__(self, width=800, height=600, margin=50):
        self.width = width
        self.height = height
        self.margin = margin
        self.image = pygame.Surface((self.width, self.height))
        self._create_background()

    def _create_background(self):
        self.image.fill((139, 69, 19))
        paper_rect = pygame.Rect(
            self.margin,
            self.margin,
            self.width - 2 * self.margin,
            self.height - 2 * self.margin
        )
        pygame.draw.rect(self.image, (255, 255, 255), paper_rect)

class Puzzle:
    def __init__(self, previous_scene=None, bgm_path=None, screen_size=None):
        self.font = fonts.malgun_font
        self.previous_scene = previous_scene
        self.completed = False
        self.audio = get_audio_manager()
        self.bgm_path = bgm_path
        if screen_size:
            w, h = screen_size
        else:
            screen = pygame.display.get_surface()
            w, h = screen.get_size() if screen else (800, 600)
        self.bg_image = PuzzleBackground(width=w, height=h).image

    def start(self):
        if self.bgm_path:
            self.audio.play_music(self.bgm_path)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.completed = True
                return self.previous_scene
        return None

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.blit(self.bg_image, (0, 0))
