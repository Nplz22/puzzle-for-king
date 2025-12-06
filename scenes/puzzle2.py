import pygame, random, time
from scenes.puzzle import Puzzle

CARD_SIZE = 100
CARD_MARGIN = 10
ROWS = 4
COLS = 4
SHOW_TIME = 2.0
START_X = 180
START_Y = 110
SHOW_COUNTDOWN = 5

class Puzzle2(Puzzle):
    def __init__(self, previous_scene=None):
        super().__init__(previous_scene=previous_scene,
                         bgm_path="assets/sounds/puzzle2 브금.mp3")
        self.grid = []
        self.flipped = []
        self.matched = []
        self.start_time = None
        self.show_phase = True
        self.finished = False
        self.countdown = SHOW_COUNTDOWN
        self.countdown_start = time.time()
        self.queen_speaking = False
        self.queen_speak_start = None
        self.queen_image = None
        try:
            self.queen_image = pygame.image.load("assets/images/queen.png").convert_alpha()
        except Exception:
            self.queen_image = pygame.Surface((50, 50))
            self.queen_image.fill((255,0,0))
        try:
            self.small_font = pygame.freetype.SysFont("Malgun Gothic", 25)
        except Exception:
            try:
                self.small_font = pygame.freetype.SysFont("Malgun", 25)
            except Exception:
                self.small_font = getattr(self, "font", None)
        if self.small_font is None:
            self.small_font = getattr(self, "font", None)
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
        self.countdown = SHOW_COUNTDOWN
        self.countdown_start = time.time()
        self.queen_speaking = False
        self.queen_speak_start = None

    def shuffle_cards(self):
        all_cards = [card for row in self.grid for card in row]
        random.shuffle(all_cards)
        for row in range(ROWS):
            for col in range(COLS):
                idx = row*COLS + col
                card = all_cards[idx]
                card["rect"].x = START_X + col*(CARD_SIZE + CARD_MARGIN)
                card["rect"].y = START_Y + row*(CARD_SIZE + CARD_MARGIN)
                self.grid[row][col] = card

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_p):
                return "options"
            if event.key in (pygame.K_RETURN, pygame.K_SPACE) and self.finished:
                return "play2"
            if self.queen_speaking and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.shuffle_cards()
                self.queen_speaking = False
                return None
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.show_phase and not self.queen_speaking:
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
                                    self.audio.play_sfx("assets/sounds/correct.wav")
                                    self.matched.extend(self.flipped)
                                else:
                                    self.audio.play_sfx("assets/sounds/wrong.wav")
                                pygame.time.set_timer(pygame.USEREVENT + 1, 500)
        if event.type == pygame.USEREVENT + 1:
            self.flipped = []
            pygame.time.set_timer(pygame.USEREVENT + 1, 0)
        return None

    def update(self, dt):
        if self.show_phase:
            elapsed = time.time() - self.countdown_start
            if elapsed >= 1:
                self.countdown -= 1
                self.countdown_start = time.time()
            if self.countdown <= 0:
                self.show_phase = False
                self.queen_speaking = True
                self.queen_speak_start = time.time()
        if len(self.matched) == ROWS*COLS:
            self.finished = True

    def _wrap_text_lines(self, text, font, max_width):
        words = text.split()
        lines = []
        cur = ""
        for w in words:
            test = cur + (" " if cur else "") + w
            surf, rect = font.render(test, (0,0,0))
            if rect.width <= max_width:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines[:2]

    def draw(self, screen):
        screen.fill((50, 50, 80))
        if self.show_phase:
            instruction_text = "카드를 보고 숫자를 기억하세요!"
            inst_surf, inst_rect = self.font.render(instruction_text, (255, 255, 0))
            inst_x = (screen.get_width() - inst_rect.width) // 2
            screen.blit(inst_surf, (inst_x, 20))
            for row in range(ROWS):
                for col in range(COLS):
                    card = self.grid[row][col]
                    rect = card["rect"]
                    num = card["num"]
                    pygame.draw.rect(screen, (255, 255, 255), rect)
                    num_surf, num_rect = self.font.render(str(num), (0,0,0))
                    screen.blit(num_surf, (rect.x + (CARD_SIZE - num_rect.width)//2,
                                           rect.y + (CARD_SIZE - num_rect.height)//2))
            countdown_surf, countdown_rect = self.font.render(str(self.countdown), (255, 255, 0))
            screen.blit(countdown_surf, (400, 50))
        elif self.queen_speaking:
            bubble_w = 600
            bubble_h = 140
            bubble_x = (screen.get_width() - bubble_w) // 2
            bubble_y = (screen.get_height() - bubble_h) // 2
            bubble_rect = pygame.Rect(bubble_x, bubble_y, bubble_w, bubble_h)
            pygame.draw.rect(screen, (50,50,50), bubble_rect)
            pygame.draw.rect(screen, (255,255,255), bubble_rect, 2)
            padding = 14
            img_w = self.queen_image.get_width()
            img_h = self.queen_image.get_height()
            img_x = bubble_rect.x + padding
            img_y = bubble_rect.y + (bubble_h - img_h) // 2
            screen.blit(self.queen_image, (img_x, img_y))
            name_x = img_x + img_w + 12
            name_y = bubble_rect.y + padding
            name_surf, name_rect = self.small_font.render("왕비", (255, 255, 255))
            screen.blit(name_surf, (name_x, name_y))
            text = "어딜! 너가 왕이 될려고? 왕은 내 아들 진우가 되어야 해! 카드 위치를 랜덤하게 섞어주마"
            max_text_width = bubble_rect.width - (img_w + padding*3)
            lines = self._wrap_text_lines(text, self.small_font, max_text_width)
            text_start_x = name_x
            text_start_y = name_y + name_rect.height + 8
            y = text_start_y
            for line in lines:
                line_surf, line_rect = self.small_font.render(line, (255, 200, 200))
                screen.blit(line_surf, (text_start_x, y))
                y += line_rect.height + 6
            prompt_surf, prompt_rect = self.small_font.render("엔터를 눌러 계속하세요", (200,200,200))
            prompt_x = bubble_rect.x + bubble_rect.width - prompt_rect.width - padding
            prompt_y = bubble_rect.y + bubble_rect.height - prompt_rect.height - padding//2
            screen.blit(prompt_surf, (prompt_x, prompt_y))
        else:
            for row in range(ROWS):
                for col in range(COLS):
                    card = self.grid[row][col]
                    rect = card["rect"]
                    num = card["num"]
                    if (row, col) in self.flipped or (row, col) in self.matched:
                        pygame.draw.rect(screen, (255, 255, 255), rect)
                        num_surf, num_rect = self.font.render(str(num), (0,0,0))
                        screen.blit(num_surf, (rect.x + (CARD_SIZE - num_rect.width)//2,
                                               rect.y + (CARD_SIZE - num_rect.height)//2))
                    else:
                        pygame.draw.rect(screen, (200, 0, 0), rect)
        esc_surf, esc_rect = self.font.render("ESC: 옵션", (240, 240, 240))
        screen.blit(esc_surf, (10, 10))
