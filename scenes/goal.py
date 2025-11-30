import pygame
from scenes import fonts

class GoalScene:
    def __init__(self, previous_scene=None):
        self.font = fonts.malgun_font
        self.previous_scene = previous_scene

    def start(self):
        pass

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):
            return "ending"
        return None

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill((20,40,20))
        s, r = self.font.render("목표에 도착했습니다. 엔터를 눌러 엔딩으로", (240,240,240))
        screen.blit(s, (120,280))
