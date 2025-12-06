import pygame, random, time
from scenes.puzzle import Puzzle
from scenes.audio import get_audio_manager

CARD_SIZE = 100
CARD_MARGIN = 10
ROWS = 4
COLS = 4
SHOW_TIME = 2.0
START_X = 180
START_Y = 130

class Puzzle2(Puzzle):
    def __init__(self, previous_scene=None):
        super().__init__(previous_scene=previous_scene,
                         bgm_path="assets/sounds/puzzle2 브금.mp3")
        self.audio = get_audio_manager()
        self.grid = []
        self.flipped = []
        self.matched = []
        self.start_time = None
        self.show_phase = True
        self.finished = False
        self.generate_cards()
    
    def generate_cards(self):
        numbers = list(range(1, 9)) * 2
        random.shuffle(numbers)
        self.grid = []
        for row in range(ROWS):
            row_cards = []
            for col in range(COLS):
                num = numbers.pop()
                rect = pygame.Rect(
                    START_X + col*(CARD_SIZE + CARD_MARGIN),
                    START_Y + row*(CARD_SIZE + CARD_MARGIN),
                    CARD_SIZE,
                    CARD_SIZE
                )
                row_cards.append({"num": num, "rect": rect})
            self.grid.append(row_cards)
        self.start_time = time.time()
        self.show_phase = True
        self.flipped = []
        self.matched = []
        self.finished = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_p):
                return "options"
            if event.key in (pygame.K_RETURN, pygame.K_SPACE) and self.finished:
                return "play2"
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.show_phase:
            pos = event.pos
            for row in range(ROWS):
                for col in range(COLS):
                    card = self.grid[row][col]
                    if card["rect"].collidepoint(pos):
                        if (row, col) not in self.flipped and (row, col) not in self.matched:
                            self.flipped.append((row, col))
                            if len(self.flipped) == 2:
                                r1, c1 = self.flipped[0]
                                r2, c2 = self.flipped[1]
                                if self.grid[r1][c1]["num"] == self.grid[r2][c2]["num"]:
                                    self.matched.extend(self.flipped)
                                pygame.time.set_timer(pygame.USEREVENT + 1, 500)
        if event.type == pygame.USEREVENT + 1:
            self.flipped = []
            pygame.time.set_timer(pygame.USEREVENT + 1, 0)
        return None

    def update(self, dt):
        if self.show_phase:
            if time.time() - self.start_time >= SHOW_TIME:
                self.show_phase = False
        if len(self.matched) == ROWS*COLS:
            self.finished = True

    def draw(self, screen):
        screen.fill((50, 50, 80))
        for row in range(ROWS):
            for col in range(COLS):
                card = self.grid[row][col]
                rect = card["rect"]
                num = card["num"]
                if self.show_phase or (row, col) in self.flipped or (row, col) in self.matched:
                    pygame.draw.rect(screen, (255, 255, 255), rect)
                    num_surf, num_rect = self.font.render(str(num), (0,0,0))
                    screen.blit(num_surf, (rect.x + (CARD_SIZE - num_rect.width)//2,
                                           rect.y + (CARD_SIZE - num_rect.height)//2))
                else:
                    pygame.draw.rect(screen, (200, 0, 0), rect)
        esc_surf, esc_rect = self.font.render("ESC: 옵션", (240, 240, 240))
        screen.blit(esc_surf, (10, 10))
