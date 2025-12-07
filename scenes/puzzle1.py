import pygame
from scenes import fonts
from scenes.audio import get_audio_manager
from scenes.puzzle import PuzzleBackground

class Puzzle1:
    def __init__(self, previous_scene=None, bgm_path=None, screen_size=None):
        self.font = fonts.malgunbd_font_small
        self.label_font = fonts.malgun_font
        self.previous_scene = previous_scene
        self.completed = False
        self.audio = get_audio_manager()
        self.bgm_path = "assets/sounds/puzzle1 브금.mp3"
        self.clear_music_path = "assets/sounds/clear.mp3"
        screen = pygame.display.get_surface()
        w, h = screen.get_size() if screen else (800, 600)
        self.bg_image = PuzzleBackground(width=w, height=h).image
        self.current_index = 0
        self.problems = [
            "1.물음표에 들어갈 것은?\n\n  I am on Ear Pad [?]",
            "2.다음 영어 수수께끼의 정답은 무엇일까요?\n\n 'I am an odd number. \nTake away a letter and I become even. \nWhat am I?'\n(저는 홀수입니다. 제 철자 하나를 \n빼면 짝수가 됩니다. 저는 무엇일까요?)",
            "3.다음 물음표에 들어갈 숫자는 무엇일까요?\n\n8809=6\n7111=0\n2172=0\n6666=4\n3213=0\n9312=?"
        ]
        self.answers = [["love"], ["seven", "7"], ["1"]]
        self.hints = [
            "트럼프 카드 모양들,\n 영어로 뭐였죠?",
            "1~10 사이에 숫자입니다\n (문제 사이에 힌트가 있어요!)",
            "세모... 네모... 동그라미?"
        ]
        self.show_hint = False
        self.hint_rect = pygame.Rect(20, h - 50, 80, 30)
        self.answer_text = ""
        self.input_active = True
        self.input_rect = pygame.Rect(250, h - 110, 400, 36)
        self.feedback_msg = ""
        self.feedback_timer = 0
        self.cleared = False
        self.next_scene_result = None
        self.clear_playing = False
        self.waiting_enter = False

    def start(self):
        if self.bgm_path:
            self.audio.play_music(self.bgm_path)
        self.clear_playing = False

    def handle_event(self, event):
        if self.cleared:
            if self.waiting_enter and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.next_scene_result = "play2"
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.hint_rect.collidepoint(event.pos):
                self.show_hint = not self.show_hint
            if self.input_rect.collidepoint(event.pos):
                self.input_active = True
            else:
                self.input_active = False

        if event.type == pygame.KEYDOWN:
            if self.input_active:
                if event.key == pygame.K_BACKSPACE:
                    self.answer_text = self.answer_text[:-1]
                elif event.key == pygame.K_RETURN:
                    submitted = self.answer_text.strip().lower()
                    valid_answers = self.answers[self.current_index]
                    
                    if submitted != "" and submitted in valid_answers:
                        try:
                            self.audio.play_sfx("assets/sounds/correct.wav")
                        except Exception:
                            pass
                        self.answer_text = ""
                        self.current_index += 1
                        self.show_hint = False
                        if self.current_index >= len(self.problems):
                            self.cleared = True
                            self.input_active = False
                            self.waiting_enter = True
                            try:
                                self.audio.stop_music()
                            except Exception:
                                pass
                            try:
                                self.audio.play_music(self.clear_music_path, loop=0)
                                self.clear_playing = True
                            except Exception:
                                pass
                    else:
                        try:
                            self.audio.play_sfx("assets/sounds/wrong.wav")
                        except Exception:
                            pass
                        self.feedback_msg = "틀렸습니다"
                        self.feedback_timer = 120
                else:
                    if hasattr(event, "unicode") and event.unicode and len(self.answer_text) < 40:
                        if not (ord(event.unicode) == 13):
                            self.answer_text += event.unicode
            else:
                pass
        return None

    def update(self, dt):
        if self.feedback_timer > 0:
            self.feedback_timer -= 1
            if self.feedback_timer <= 0:
                self.feedback_msg = ""

    def draw(self, screen):
        screen.blit(self.bg_image, (0, 0))

        if not self.cleared and self.current_index < len(self.problems):
            text = self.problems[self.current_index]
            if self.current_index == 1:
                x_offset = 150
                y_offset = 140
            elif self.current_index == 2:
                x_offset = 150
                y_offset = 80
            else:
                x_offset = 250
                y_offset = 240
            max_width = screen.get_width() - x_offset - 50

            def wrap_text(text, font, max_w):
                lines = []
                for para in text.split("\n"):
                    if para == "":
                        lines.append("")
                        continue
                    words = para.split(" ")
                    line = ""
                    for w in words:
                        test = line + (" " if line else "") + w
                        surf, _ = font.render(test, (0,0,0))
                        if surf.get_width() <= max_w:
                            line = test
                        else:
                            if line:
                                lines.append(line)
                            line = w
                    if line:
                        lines.append(line)
                return lines

            lines = wrap_text(text, self.font, max_width)
            sample_surf, _ = self.font.render("Ay", (0,0,0))
            line_h = sample_surf.get_height() + 6
            for line in lines:
                text_surf, _ = self.font.render(line, (0,0,0))
                screen.blit(text_surf, (x_offset, y_offset))
                y_offset += line_h

        if self.cleared:
            clear_surf, _ = self.label_font.render("Clear!", (0,0,0))
            cx = (screen.get_width() - clear_surf.get_width()) // 2
            cy = (screen.get_height() - clear_surf.get_height()) // 2
            screen.blit(clear_surf, (cx, cy))

            if self.waiting_enter:
                next_surf, _ = self.font.render("엔터를 눌러 계속", (0,0,0))
                nx = (screen.get_width() - next_surf.get_width()) // 2
                ny = cy + clear_surf.get_height() + 20
                screen.blit(next_surf, (nx, ny))
            return

        hint_label_surf, _ = self.label_font.render("힌트", (0,0,0))
        label_w = hint_label_surf.get_width()
        label_h = hint_label_surf.get_height()
        pad_x = 12
        pad_y = 6
        self.hint_rect.x = 20
        self.hint_rect.width = label_w + pad_x * 2
        self.hint_rect.height = label_h + pad_y * 2
        self.hint_rect.y = screen.get_height() - self.hint_rect.height - 20
        pygame.draw.rect(screen, (200,200,200), self.hint_rect, border_radius=4)
        screen.blit(hint_label_surf, (self.hint_rect.x + pad_x, self.hint_rect.y + pad_y))

        if self.show_hint:
            hints = getattr(self, "hints", None)
            if not hints or len(hints) <= self.current_index:
                hints = [getattr(self, "hint_text", "")] * max(1, len(getattr(self, "problems", [""])))
            hint_text = hints[self.current_index] if self.current_index < len(hints) else ""
            max_w = 400 - 20
            hint_lines = []
            for para in hint_text.split("\n"):
                words = para.split(" ")
                line = ""
                for w in words:
                    test = line + (" " if line else "") + w
                    surf, _ = self.font.render(test, (0,0,0))
                    if surf.get_width() <= max_w:
                        line = test
                    else:
                        if line:
                            hint_lines.append(line)
                        line = w
                if line:
                    hint_lines.append(line)
            sample_surf, _ = self.font.render("Ay", (0,0,0))
            lh = sample_surf.get_height() + 4
            box_h = max(60, len(hint_lines) * (lh) + 20)
            hint_box = pygame.Rect(120, 100, 400, box_h)
            pygame.draw.rect(screen, (255,255,255), hint_box, border_radius=6)
            pygame.draw.rect(screen, (0,0,0), hint_box, 2, border_radius=6)
            hx = hint_box.x + 10
            hy = hint_box.y + 10
            for line in hint_lines:
                surf, _ = self.font.render(line, (0,0,0))
                screen.blit(surf, (hx, hy))
                hy += surf.get_height() + 4

        pygame.draw.rect(screen, (255,255,255), self.input_rect, border_radius=4)
        pygame.draw.rect(screen, (0,0,0), self.input_rect, 2, border_radius=4)
        prompt_surf, _ = self.label_font.render("답 입력:", (0,0,0))
        prompt_w = prompt_surf.get_width()
        prompt_h = prompt_surf.get_height()
        prompt_x = self.input_rect.x - prompt_w - 12
        prompt_y = self.input_rect.y + (self.input_rect.height - prompt_h) // 2
        screen.blit(prompt_surf, (prompt_x, prompt_y))

        answer_surf, _ = self.label_font.render(self.answer_text, (0,0,0))
        answer_y = self.input_rect.y + (self.input_rect.height - answer_surf.get_height()) // 2
        screen.blit(answer_surf, (self.input_rect.x + 8, answer_y))

        if self.input_active:
            ticks = pygame.time.get_ticks()
            if (ticks // 500) % 2 == 0:
                cursor_x = self.input_rect.x + 8 + answer_surf.get_width() + 2
                cursor_y1 = self.input_rect.y + 6
                cursor_y2 = self.input_rect.y + self.input_rect.height - 6
                pygame.draw.line(screen, (0,0,0), (cursor_x, cursor_y1), (cursor_x, cursor_y2), 2)

        if self.feedback_msg:
            fb_surf, _ = self.label_font.render(self.feedback_msg, (255,0,0))
            screen.blit(fb_surf, (self.input_rect.x, self.input_rect.y - 30))