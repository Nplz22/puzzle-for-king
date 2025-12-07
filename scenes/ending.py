import pygame, os, sys
from scenes import fonts
from player import Player
from scenes.audio import get_audio_manager

class EndingScene:
    def __init__(self, previous_scene=None):
        self.font = fonts.malgun_font
        self.dialog_font = fonts.malgunbd_font_small
        self.previous_scene = previous_scene
        self.audio = get_audio_manager()
        self.bg_image = None
        self.screen_w = 800
        self.screen_h = 600
        
        self.ground_y = 540
        
        self.characters = {}
        self.dialog_index = 0
        self.dialog_lines = []
        self.typing = True
        self.type_pos = 0
        self.type_timer = 0.0
        self.dialog_active = True
        self.current_bgm = "ending1"
        self.show_the_end = False
        
        self.is_fading = False
        self.fade_alpha = 0

        self.the_end_y = self.screen_h + 100
        self.the_end_target_y = self.screen_h // 2 - 50
        self.is_text_animating = False

        self.hyeonwoo_final_x = 50
        self.queen_x = 600
        self.jinwoo_final_x = 300
        self.king_final_x = 480
        self.jinwoo_entered = False
        self.king_entered = False

        try:
            img = pygame.image.load(os.path.join("assets","images","second map.png")).convert()
            screen = pygame.display.get_surface()
            if screen:
                w, h = screen.get_size()
                self.bg_image = pygame.transform.smoothscale(img, (w, h))
            else:
                self.bg_image = pygame.transform.smoothscale(img, (800, 600))
        except Exception:
            self.bg_image = None

        self._load_characters()
        self._prepare_dialogs()

    def _load_characters(self):
        self.characters["현우"] = Player(-150, self.ground_y, "assets/images/prince.png", scale=2.0, speed=200)
        self.characters["왕비"] = Player(self.queen_x, self.ground_y, "assets/images/queen2.png", scale=2.0, speed=0)
        self.characters["진우"] = Player(-150, self.ground_y, "assets/images/jinwoo.png", scale=2.0, speed=200)
        self.characters["왕"] = Player(900, self.ground_y, "assets/images/king.png", scale=2.0, speed=200)
        self.characters["???"] = None

    def _prepare_dialogs(self):
        self.dialog_sequence = [
            ("현우", "좋아 내가 해냈어! 내가 먼저 클리어 했다고!"),
            ("왕비", "난 인정할 수 없어! 솔직히 말해 너 반칙 썼지? 넌 왕이 될 자격이 없어!"),
            ("???", "제발 그만!!!!!"),
            ("진우", "엄마 제발 그만해! 나도 내가 부족해서 진 거... 인정한다고."),
            ("진우", "엄마가 결과를 인정하지 않으면... 최선을 다한 나까지 더 비참해질 뿐이야. 현우는 정정당당했어."),
            ("왕비", "진우야... 난 그저 네가 왕이 되었으면 하는 마음에..."),
            ("왕비", "하아... 그래, 네 뜻이 정 그렇다면 내가 물러서마. 현우야, 어른답지 못하게 굴어서 미안하다."),
            ("???", "껄껄껄! 비 온 뒤에 땅이 굳는 법이지."),
            ("왕", "먼저 푼 현우도, 패배를 멋지게 인정하는 진우도 모두 대견하구나. 역시 내 아들들 답다."),
            ("왕", "약속은 약속이니, 내 뒤를 이을 차기 왕은 현우가 될 것이다!")
        ]
        self.dialog_lines = list(self.dialog_sequence)

    def start(self):
        try:
            pygame.mixer.music.stop()
            self.audio.play_music("assets/sounds/엔딩1 브금.mp3")
        except Exception:
            pass
        self.characters["현우"].rect.x = -150
        self.characters["진우"].rect.x = -150
        self.characters["왕"].rect.x = 900
        
        self.is_fading = False
        self.fade_alpha = 0
        self.show_the_end = False
        self.is_text_animating = False
        self.the_end_y = self.screen_h + 100

    def handle_event(self, event):
        if self.show_the_end:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            return None

        if self.is_fading:
            return None

        if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):
            if self.dialog_active:
                if self.typing:
                    self.type_pos = len(self.dialog_lines[self.dialog_index][1])
                    self.typing = False
                else:
                    self._next_dialog()
        return None

    def _next_dialog(self):
        if self.dialog_index < len(self.dialog_lines)-1:
            self.dialog_index += 1
            self.typing = True
            self.type_pos = 0
            self.type_timer = 0.0
            
            if self.dialog_index == 2:
                if self.current_bgm == "ending1":
                    self.audio.play_music("assets/sounds/엔딩2 브금.mp3")
                    self.current_bgm = "ending2"
            elif self.dialog_index == 3:
                self.jinwoo_entered = True
            elif self.dialog_index == 7:
                if self.current_bgm == "ending2":
                    self.audio.play_music("assets/sounds/엔딩3 브금.mp3")
                    self.current_bgm = "ending3"
            elif self.dialog_index == 8:
                self.king_entered = True
        else:
            self.dialog_active = False
            self.is_fading = True
            pygame.mixer.music.stop()
            self.audio.play_sfx("assets/sounds/the end 효과음.mp3")

    def update(self, dt):
        if self.is_fading:
            self.fade_alpha += 100 * dt
            if self.fade_alpha >= 255:
                self.fade_alpha = 255
                self.is_fading = False
                self.show_the_end = True
                self.is_text_animating = True

        if self.is_text_animating:
            dy = self.the_end_target_y - self.the_end_y
            self.the_end_y += dy * 5 * dt
            if abs(dy) < 1:
                self.the_end_y = self.the_end_target_y
                self.is_text_animating = False

        if self.dialog_active and self.typing:
            self.type_timer += dt
            chars = int(self.type_timer * 60)
            if chars > 0:
                current_text = self.dialog_lines[self.dialog_index][1]
                self.type_pos = min(len(current_text), self.type_pos + chars)
                self.type_timer -= chars / 60
                if self.type_pos >= len(current_text):
                    self.typing = False

        if self.characters["현우"].rect.x < self.hyeonwoo_final_x:
            self.characters["현우"].rect.x += self.characters["현우"].speed * dt
            if self.characters["현우"].rect.x > self.hyeonwoo_final_x:
                self.characters["현우"].rect.x = self.hyeonwoo_final_x

        if self.jinwoo_entered:
            if self.characters["진우"].rect.x < self.jinwoo_final_x:
                self.characters["진우"].rect.x += self.characters["진우"].speed * dt
                if self.characters["진우"].rect.x > self.jinwoo_final_x:
                    self.characters["진우"].rect.x = self.jinwoo_final_x

        if self.king_entered:
            if self.characters["왕"].rect.x > self.king_final_x:
                self.characters["왕"].rect.x -= self.characters["왕"].speed * dt
                if self.characters["왕"].rect.x < self.king_final_x:
                    self.characters["왕"].rect.x = self.king_final_x

    def draw(self, screen):
        w, h = screen.get_size()
        
        if self.bg_image:
            screen.blit(self.bg_image, (0,0))
        else:
            screen.fill((0,0,0))

        char_order = ["현우", "왕비", "진우", "왕"]
        for name in char_order:
            char = self.characters[name]
            if char:
                screen.blit(char.image, (char.rect.x, char.rect.y))

        if self.dialog_active:
            name, text = self.dialog_lines[self.dialog_index]
            
            bubble_w = 600
            bubble_h = 120
            bubble_x = (w - bubble_w) // 2
            
            bubble_y = 200
            
            pygame.draw.rect(screen, (250,250,250), (bubble_x, bubble_y, bubble_w, bubble_h), border_radius=8)
            pygame.draw.rect(screen, (50,50,50), (bubble_x, bubble_y, bubble_w, bubble_h), 2, border_radius=8)
            
            text_color = (20,20,20)
            cur_text = text[:self.type_pos]
            self._draw_wrapped_text(screen, cur_text, bubble_x+20, bubble_y+20, bubble_w-40, text_color)
            
            display_name = name if name != "???" else "???"
            name_surf, name_rect = self.dialog_font.render(display_name, (255, 255, 255))
            
            name_bg_rect = pygame.Rect(bubble_x + 20, bubble_y - 15, name_rect.width + 20, name_rect.height + 6)
            pygame.draw.rect(screen, (0, 0, 0), name_bg_rect, border_radius=4)
            screen.blit(name_surf, (bubble_x + 30, bubble_y - 12))

        if self.is_fading or self.show_the_end:
            overlay = pygame.Surface((w,h))
            overlay.fill((0,0,0))
            alpha_val = int(self.fade_alpha) if self.is_fading else 255
            overlay.set_alpha(alpha_val)
            screen.blit(overlay, (0,0))
            
            if self.show_the_end:
                surf, rect = self.font.render("The End", (255,255,255))
                screen.blit(surf, (w//2 - rect.width//2, int(self.the_end_y)))
                
                surf2, rect2 = self.font.render("Esc를 눌러 게임을 종료하십시오", (255,255,255))
                screen.blit(surf2, (w//2 - rect2.width//2, int(self.the_end_y) + rect.height + 40))

    def _draw_wrapped_text(self, screen, text, x, y, max_width, color):
        words = text.split(" ")
        line = ""
        start_x = x
        for word in words:
            test_line = (line + " " + word).strip()
            surf, _ = self.font.render(test_line, color)
            
            if surf.get_width() > max_width and line != "":
                surf_line, _ = self.font.render(line, color)
                screen.blit(surf_line, (x, y))
                y += surf_line.get_height() + 5
                line = word
            else:
                line = test_line
        
        if line:
            surf_line, _ = self.font.render(line, color)
            screen.blit(surf_line, (x, y))