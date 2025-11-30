import pygame
from scenes import fonts

class EndingScene:
    def __init__(self, previous_scene=None):
        self.font = fonts.malgun_font
        self.previous_scene = previous_scene

    def start(self):
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("assets/sounds/타이틀 브금.mp3")
            pygame.mixer.music.set_volume(0.1)
            pygame.mixer.music.play(-1)
        except Exception:
            pass

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):
            return self.previous_scene
        return None

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill((10,10,10))
        s, r = self.font.render("엔딩: 주인공이 왕이 되었습니다. 엔터: 타이틀로", (230,230,230))
        screen.blit(s, (80,280))
