import pygame, random
from scenes import fonts

class Puzzle3:
    def __init__(self, previous_scene=None):
        self.font = fonts.malgun_font
        self.previous_scene = previous_scene
        self.cards = list(range(6))
        self.shown = False
        self.start_timer = 0.0
        self.phase = "show"
        self.revealed = [False]*6
        self.permute = list(range(6))
        self.cheated = True
        random.shuffle(self.permute)
        if self.cheated:
            i,j = 2,4
            self.permute[i], self.permute[j] = self.permute[j], self.permute[i]

    def start(self):
        self.phase = "show"
        self.start_timer = 0.0
        self.shown = True
        self.revealed = [False]*6

    def handle_event(self, event):
        if self.phase == "play":
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5,pygame.K_6):
                idx = int(event.unicode)-1
                self.revealed[idx] = not self.revealed[idx]
                if all(self.revealed):
                    return self.previous_scene
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return self.previous_scene
        return None

    def update(self, dt):
        if self.phase == "show":
            self.start_timer += dt
            if self.start_timer >= 3.0:
                self.phase = "play"

    def draw(self, screen):
        screen.fill((30,30,50))
        title_s, title_r = self.font.render("퍼즐3: 기억력 카드 (1-6키로 뒤집기)", (230,230,230))
        screen.blit(title_s, (60,40))
        for i in range(6):
            x = 120 + i*100
            y = 220
            rect = pygame.Rect(x,y,80,120)
            if self.phase == "show":
                v = str(self.permute[i])
                s, r = self.font.render(v, (10,10,10))
                pygame.draw.rect(screen, (240,240,240), rect)
                screen.blit(s, (x+30,y+40))
            else:
                if self.revealed[i]:
                    v = str(self.permute[i])
                    s, r = self.font.render(v, (10,10,10))
                    pygame.draw.rect(screen, (240,240,240), rect)
                    screen.blit(s, (x+30,y+40))
                else:
                    pygame.draw.rect(screen, (80,80,110), rect)
