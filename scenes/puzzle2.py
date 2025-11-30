import pygame
from scenes import fonts

class Puzzle2:
    def __init__(self, previous_scene=None):
        self.font = fonts.malgun_font
        self.previous_scene = previous_scene
        self.completed = False

    def start(self):
        pass

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):
            self.completed = True
            if hasattr(self.previous_scene, "bridge_fixed"):
                self.previous_scene.bridge_fixed = True
            return self.previous_scene
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return self.previous_scene
        return None

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill((40,60,40))
        s, r = self.font.render("퍼즐2: 엔터를 눌러 다리 복구", (240,240,240))
        screen.blit(s, (180,280))
