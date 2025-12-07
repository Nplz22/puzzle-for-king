import pygame, random, time
from scenes.puzzle import Puzzle

CARD_SIZE = 100
CARD_MARGIN = 10
ROWS = 4
COLS = 4
START_X = 180
START_Y = 110
SHOW_COUNTDOWN = 5
SWAP_DURATION = 0.6
FEEDBACK_DELAY_MS = 700
MAX_SWAPS = 5

class Puzzle2(Puzzle):
    def __init__(self, previous_scene=None):
        super().__init__(previous_scene=previous_scene,
                         bgm_path="assets/sounds/puzzle2 브금.mp3")
        self.grid = []
        self.generate_cards_ordered()
        self.flipped = []
        self.matched = []
        self.show_phase = True
        self.countdown = SHOW_COUNTDOWN
        self.countdown_start = time.time()
        self.queen_speaking = False
        self.queen_image = None
        try:
            self.queen_image = pygame.image.load("assets/images/queen.png").convert_alpha()
        except Exception:
            self.queen_image = pygame.Surface((64, 64), pygame.SRCALPHA)
            pygame.draw.circle(self.queen_image, (200, 180, 220), (32,32), 30)
        try:
            self.small_font = pygame.freetype.SysFont("Malgun Gothic", 25)
        except Exception:
            try:
                self.small_font = pygame.freetype.SysFont("Malgun", 25)
            except Exception:
                self.small_font = getattr(self, "font", None)
        if self.small_font is None:
            self.small_font = getattr(self, "font", None)
        self.questions = random.sample(list(range(1,17)), 5)
        self.q_index = 0
        self.awaiting_feedback = False
        self.finished = False
        self.last_click_was_correct = False
        self.swap_queue = []
        self.current_swap = None
        self.swap_start_time = None
        self.swap_progress = 0.0
        self.swap_target_flat = None
        self.swap_started = False
        self.countdown = SHOW_COUNTDOWN
        self.countdown_start = time.time()
        self.clear_music_path = "assets/sounds/clear.mp3"
        self.clear_playing = False

    def generate_cards_ordered(self):
        numbers = list(range(1, 17))
        self.grid = []
        idx = 0
        for row in range(ROWS):
            row_cards = []
            for col in range(COLS):
                num = numbers[idx]
                idx += 1
                rect = pygame.Rect(
                    START_X + col*(CARD_SIZE + CARD_MARGIN),
                    START_Y + row*(CARD_SIZE + CARD_MARGIN),
                    CARD_SIZE,
                    CARD_SIZE
                )
                row_cards.append({"num": num, "rect": rect})
            self.grid.append(row_cards)

    def _linear_index(self, row, col):
        return row * COLS + col

    def _rowcol_from_index(self, idx):
        return divmod(idx, COLS)

    def _flatten_cards(self):
        return [card for row in self.grid for card in row]

    def _set_grid_from_flat(self, flat):
        for i, card in enumerate(flat):
            r, c = self._rowcol_from_index(i)
            self.grid[r][c] = card

    def compute_swap_sequence(self):
        flat = self._flatten_cards()
        target = flat[:]
        def same_order(a,b):
            for i in range(len(a)):
                if a[i]["num"] != b[i]["num"]:
                    return False
            return True
        attempts = 0
        random.shuffle(target)
        while same_order(flat, target) and attempts < 50:
            random.shuffle(target)
            attempts += 1
        if same_order(flat, target):
            if len(target) >= 2:
                target[0], target[1] = target[1], target[0]
        num_to_target_idx = {card["num"]: idx for idx, card in enumerate(target)}
        perm = [num_to_target_idx[card["num"]] for card in flat]
        perm_copy = perm[:]
        swaps = []
        for i in range(len(perm_copy)):
            while perm_copy[i] != i:
                j = perm_copy[i]
                swaps.append((i, j))
                perm_copy[i], perm_copy[j] = perm_copy[j], perm_copy[i]
        if len(swaps) > MAX_SWAPS:
            swaps = swaps[:MAX_SWAPS]
        self.swap_target_flat = target
        return swaps

    def start_swap_sequence(self):
        if getattr(self, "swap_started", False):
            return
        pygame.time.set_timer(pygame.USEREVENT + 3, 0)
        self.swap_started = True
        self.swap_queue = self.compute_swap_sequence()
        self.queen_speaking = False
        if not self.swap_queue:
            self.swap_started = False
            return
        self.start_next_swap()

    def start_next_swap(self):
        if self.current_swap is not None:
            return
        if not self.swap_queue:
            self.current_swap = None
            self.swap_start_time = None
            self.swap_progress = 0.0
            if getattr(self, "swap_target_flat", None) is not None:
                self._set_grid_from_flat(self.swap_target_flat)
                for i, card in enumerate(self._flatten_cards()):
                    r, c = self._rowcol_from_index(i)
                    card["rect"].topleft = (START_X + c*(CARD_SIZE + CARD_MARGIN),
                                            START_Y + r*(CARD_SIZE + CARD_MARGIN))
            self.swap_started = False
            return
        a_idx, b_idx = self.swap_queue.pop(0)
        flat = self._flatten_cards()
        a_card = flat[a_idx]
        b_card = flat[b_idx]
        a_start = a_card["rect"].topleft
        b_start = b_card["rect"].topleft
        a_end = b_start
        b_end = a_start
        self.current_swap = {
            "a_idx": a_idx,
            "b_idx": b_idx,
            "a_card": a_card,
            "b_card": b_card,
            "a_start": a_start,
            "b_start": b_start,
            "a_end": a_end,
            "b_end": b_end
        }
        self.swap_start_time = time.time()
        self.swap_progress = 0.0

    def update_swap_animation(self):
        if not self.current_swap:
            return
        elapsed = time.time() - self.swap_start_time
        t = min(1.0, elapsed / SWAP_DURATION)
        self.swap_progress = t
        ax0, ay0 = self.current_swap["a_start"]
        bx0, by0 = self.current_swap["b_start"]
        ax1, ay1 = self.current_swap["a_end"]
        bx1, by1 = self.current_swap["b_end"]
        ax = ax0 + (ax1 - ax0) * t
        ay = ay0 + (ay1 - ay0) * t
        bx = bx0 + (bx1 - bx0) * t
        by = by0 + (by1 - by0) * t
        self.current_swap["a_card"]["rect"].topleft = (int(ax), int(ay))
        self.current_swap["b_card"]["rect"].topleft = (int(bx), int(by))
        if t >= 1.0:
            flat = self._flatten_cards()
            ai = self.current_swap["a_idx"]
            bi = self.current_swap["b_idx"]
            flat[ai], flat[bi] = flat[bi], flat[ai]
            self._set_grid_from_flat(flat)
            ar, ac = self._rowcol_from_index(ai)
            br, bc = self._rowcol_from_index(bi)
            self.grid[ar][ac]["rect"].topleft = (START_X + ac*(CARD_SIZE + CARD_MARGIN),
                                                 START_Y + ar*(CARD_SIZE + CARD_MARGIN))
            self.grid[br][bc]["rect"].topleft = (START_X + bc*(CARD_SIZE + CARD_MARGIN),
                                                 START_Y + br*(CARD_SIZE + CARD_MARGIN))
            self.current_swap = None
            self.swap_start_time = None
            self.swap_progress = 0.0
            pygame.time.set_timer(pygame.USEREVENT + 3, 150)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.queen_speaking and not getattr(self, "swap_started", False) and (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER):
                try:
                    self.audio.play_sfx("assets/sounds/queen_speak.wav")
                except Exception:
                    pass
                self.start_swap_sequence()
                return None
            if self.finished and (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER):
                return "ending"
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.show_phase and not self.queen_speaking and not self.awaiting_feedback and not self.finished and not self.current_swap:
            pos = event.pos
            for row in range(ROWS):
                for col in range(COLS):
                    card = self.grid[row][col]
                    if card["rect"].collidepoint(pos):
                        if (row, col) not in self.flipped:
                            self.flipped = [(row, col)]
                            num = card["num"]
                            target = self.questions[self.q_index]
                            if num == target:
                                try: self.audio.play_sfx("assets/sounds/correct.wav")
                                except Exception: pass
                                self.last_click_was_correct = True
                            else:
                                try: self.audio.play_sfx("assets/sounds/wrong.wav")
                                except Exception: pass
                                self.last_click_was_correct = False
                            pygame.time.set_timer(pygame.USEREVENT + 2, FEEDBACK_DELAY_MS)
                            self.awaiting_feedback = True
                        break
        if event.type == pygame.USEREVENT + 2:
            pygame.time.set_timer(pygame.USEREVENT + 2, 0)
            self.flipped = []
            self.awaiting_feedback = False
            if self.last_click_was_correct:
                self.q_index += 1
                if self.q_index >= len(self.questions):
                    self.finished = True
            self.last_click_was_correct = False
            return None
        if event.type == pygame.USEREVENT + 3:
            pygame.time.set_timer(pygame.USEREVENT + 3, 0)
            if not self.current_swap and self.swap_queue:
                self.start_next_swap()
            return None
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
                try:
                    self.audio.play_sfx("assets/sounds/queen_speak.wav")
                except Exception:
                    pass
        if self.current_swap:
            self.update_swap_animation()
        if self.finished and not self.clear_playing:
            try:
                self.audio.stop_music()
            except Exception:
                pass
            try:
                self.audio.play_music(self.clear_music_path, loop=0)
            except Exception:
                pass
            self.clear_playing = True

    def _wrap_text_lines(self, text, font, max_width, max_lines=2):
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
            if len(lines) >= max_lines:
                break
        if cur and len(lines) < max_lines:
            lines.append(cur)
        return lines[:max_lines]

    def draw(self, screen):
        screen.fill((50, 50, 80))
        if self.show_phase:
            instruction_text = "기억력 테스트 5초 동안 카드를 보고 숫자를 기억하세요!"
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
            return
        if self.queen_speaking:
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
            lines = self._wrap_text_lines(text, self.small_font, max_text_width, max_lines=2)
            text_start_x = name_x
            text_start_y = name_y + name_rect.height + 8
            y = text_start_y
            for line in lines:
                line_surf, line_rect = self.small_font.render(line, (255, 200, 200))
                screen.blit(line_surf, (text_start_x, y))
                y += line_rect.height + 6
            prompt_surf, prompt_rect = self.small_font.render("엔터를 눌러 카드 섞기 시작", (200,200,200))
            prompt_x = bubble_rect.x + bubble_rect.width - prompt_rect.width - padding
            prompt_y = bubble_rect.y + bubble_rect.height - prompt_rect.height - padding//2
            screen.blit(prompt_surf, (prompt_x, prompt_y))
            return
        if not self.finished:
            target = self.questions[self.q_index]
            q_text = f"문제 {self.q_index+1}/{len(self.questions)}: 숫자 {target}의 위치를 찾으시오"
            q_surf, q_rect = self.small_font.render(q_text, (255,255,0))
            q_x = (screen.get_width() - q_rect.width) // 2
            screen.blit(q_surf, (q_x, 20))
        for row in range(ROWS):
            for col in range(COLS):
                card = self.grid[row][col]
                rect = card["rect"]
                if (row, col) in self.flipped or self.finished:
                    pygame.draw.rect(screen, (255, 255, 255), rect)
                    num_surf, num_rect = self.font.render(str(card["num"]), (0,0,0))
                    screen.blit(num_surf, (rect.x + (CARD_SIZE - num_rect.width)//2,
                                           rect.y + (CARD_SIZE - num_rect.height)//2))
                else:
                    pygame.draw.rect(screen, (200, 0, 0), rect)
        if self.finished:
            msg = "게임 클리어! 엔터를 눌러 엔딩 보기"
            msg_s, msg_r = self.font.render(msg, (200,200,200))
            mx = (screen.get_width() - msg_r.width) // 2
            screen.blit(msg_s, (mx, 40))
