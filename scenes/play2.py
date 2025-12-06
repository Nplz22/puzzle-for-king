import pygame, os
from scenes import fonts
from scenes.audio import get_audio_manager
from player import Player
from scenes.puzzle2 import Puzzle2

class Scroll(pygame.sprite.Sprite):
    def __init__(self, image_path, x, min_y, max_y, speed=80, size=(150,150)):
        super().__init__()
        try:
            img = pygame.image.load(image_path).convert_alpha()
            img = pygame.transform.smoothscale(img, size)
        except Exception:
            img = pygame.Surface(size, pygame.SRCALPHA)
            img.fill((255,255,0,255))
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.min_y = min_y
        self.max_y = max_y
        self.rect.y = self.min_y
        self.speed = speed
        self.direction = 1
        self.scroll_triggered = False
        self.next_scene = None

    def update(self, dt):
        self.rect.y += self.direction * self.speed * dt
        if self.rect.y >= self.max_y:
            self.rect.y = self.max_y
            self.direction = -1
        elif self.rect.y <= self.min_y:
            self.rect.y = self.min_y
            self.direction = 1

class Play2Scene:
    def __init__(self, previous_scene=None, bgm_path="assets/sounds/플레이 브금.mp3"):
        self.previous_scene = previous_scene
        self.font = fonts.malgun_font
        self.name_font = fonts.malgunbd_font_small
        try:
            img = pygame.image.load(os.path.join("assets","images","second map.png")).convert()
            screen = pygame.display.get_surface()
            if screen:
                w, h = screen.get_size()
                self.bg_image = pygame.transform.smoothscale(img, (max(w, 1600), h))
            else:
                self.bg_image = img
        except Exception:
            self.bg_image = None
        self.audio = get_audio_manager()
        self.bgm_path = bgm_path
        self.camera_x = 0
        self.ground_y = 550
        self.player_speed = 220
        bg_path = os.path.join("assets","images","prince.png")
        self.player = Player(400, self.ground_y, bg_path, scale=2.0, speed=self.player_speed)
        self.player.name = "현우"
        self.player_group = pygame.sprite.Group(self.player)
        scroll_img = os.path.join("assets","images","scroll.png")
        min_y = self.ground_y - 150
        max_y = self.ground_y - 100
        self.scroll = Scroll(scroll_img, x=1200, min_y=min_y, max_y=max_y, speed=80, size=(150,150))
        self.scroll_group = pygame.sprite.Group(self.scroll)
        self.show_initial_dialogue = True
        self.initial_dialogue_lines = ["좋아 앞으로 하나만 더 풀면 돼 힘내자!"]
        self.dialog_active = False
        self.dialog_lines = []
        self.dialog_index = 0
        self.typing = True
        self.type_pos = 0
        self.type_speed = 60.0
        self.type_timer = 0.0
        self.left_pressed = False
        self.right_pressed = False
        self._resuming_from_options = False
        self.next_scene = None

    def start(self, resume_from_options=False):
        if resume_from_options:
            if self.bgm_path:
                self.audio.play_music(self.bgm_path)
            return
        self._resuming_from_options = False
        if self.bgm_path:
            self.audio.play_music(self.bgm_path)
        self.camera_x = 0
        if self.bg_image:
            bgw = self.bg_image.get_width()
        else:
            screen = pygame.display.get_surface()
            bgw = screen.get_width() if screen else 800
        halfw = self.player.rect.width // 2
        px = max(halfw, min(400, bgw - halfw))
        self.player.rect.midbottom = (px, self.ground_y)
        self.left_pressed = False
        self.right_pressed = False
        self.dialog_active = False
        self.dialog_index = 0
        self.type_pos = 0
        self.type_timer = 0.0
        if self.show_initial_dialogue:
            self.dialog_lines = list(self.initial_dialogue_lines)
            self.dialog_active = True
            self.typing = True
            self.dialog_index = 0
            self.type_pos = 0
            self.left_pressed = False
            self.right_pressed = False

    def handle_event(self, event):
        if self.dialog_active:
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                if self.typing:
                    self.type_pos = len(self.dialog_lines[self.dialog_index])
                    self.typing = False
                else:
                    if self.dialog_index < len(self.dialog_lines) - 1:
                        self.dialog_index += 1
                        self.type_pos = 0
                        self.typing = True
                        self.type_timer = 0.0
                    else:
                        self.dialog_active = False
                        self.type_pos = 0
                        self.type_timer = 0.0
                        self.left_pressed = False
                        self.right_pressed = False
                        self.next_scene = "play2"
                return None
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "options"
            return None

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_p):
                return "options"
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self.left_pressed = True
            if event.key in (pygame.K_RIGHT, pygame.K_d):
                self.right_pressed = True
            if event.key in (pygame.K_UP, pygame.K_w):
                self.player.jump = True
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self.left_pressed = False
            if event.key in (pygame.K_RIGHT, pygame.K_d):
                self.right_pressed = False
            if event.key in (pygame.K_UP, pygame.K_w):
                self.player.jump = False

        if self.next_scene:
            tmp = self.next_scene
            self.next_scene = None
            return tmp
        return None

    def update(self, dt):
        if self.dialog_active:
            if self.typing:
                self.type_timer += dt
                chars = int(self.type_timer * self.type_speed)
                if chars > 0:
                    self.type_pos = min(len(self.dialog_lines[self.dialog_index]), self.type_pos + chars)
                    self.type_timer -= chars / self.type_speed
                    if self.type_pos >= len(self.dialog_lines[self.dialog_index]):
                        self.typing = False
            return

        keys = pygame.key.get_pressed()
        moving_left = keys[pygame.K_LEFT] or keys[pygame.K_a] or self.left_pressed
        moving_right = keys[pygame.K_RIGHT] or keys[pygame.K_d] or self.right_pressed
        if moving_left:
            self.player.rect.x = max(0, int(self.player.rect.x - self.player_speed * dt))
        if moving_right:
            bgw = self.bg_image.get_width() if self.bg_image else pygame.display.get_surface().get_width()
            self.player.rect.x = min(int(self.player.rect.x + self.player_speed * dt), bgw - self.player.rect.width)

        self.scroll_group.update(dt)

        if self.player.rect.colliderect(self.scroll.rect):
            self.next_scene = Puzzle2(previous_scene=self)

        screen_w = pygame.display.get_surface().get_width()
        bgw = self.bg_image.get_width() if self.bg_image else screen_w
        self.camera_x = max(0, min(self.player.rect.centerx - screen_w // 2, bgw - screen_w))

    def _wrap_text(self, text, maxw):
        words = text.split(" ")
        lines = []
        cur = ""
        for word in words:
            test = (cur + " " + word).strip()
            surf, rect = self.font.render(test, (220,220,220))
            if surf.get_width() > maxw and cur != "":
                lines.append(cur)
                cur = word
            else:
                cur = test
        if cur != "": lines.append(cur)
        return lines

    def draw(self, screen):
        w, h = screen.get_size()
        if self.bg_image:
            screen.blit(self.bg_image, (-self.camera_x, 0))
        else:
            screen.fill((30,120,80))

        draw_x = self.player.rect.x - self.camera_x
        try:
            screen.blit(self.player.image, (draw_x, self.player.rect.y))
        except Exception:
            pygame.draw.rect(screen, (255,0,0), (draw_x, self.player.rect.y, self.player.rect.width, self.player.rect.height))

        for scroll in self.scroll_group:
            screen.blit(scroll.image, (scroll.rect.x - self.camera_x, scroll.rect.y))

        if self.dialog_active:
            avatar_w = 96
            avatar_h = 96
            avatar_x = 48
            avatar_y = h - 180 - avatar_h
            try:
                av = pygame.transform.smoothscale(self.player.image, (avatar_w, avatar_h))
                screen.blit(av, (avatar_x, avatar_y))
            except Exception:
                pass
            name = getattr(self.player, "name", "현우")
            name_surf, name_rect = self.name_font.render(name, (255,215,0))
            name_x = avatar_x + (avatar_w - name_rect.width) // 2
            name_y = avatar_y - name_rect.height - 6
            screen.blit(name_surf, (name_x, name_y))
            bubble_w = w - avatar_x - avatar_w - 80
            bubble_h = 120
            bubble_x = avatar_x + avatar_w + 20
            bubble_y = h - 180 - bubble_h - 10
            bubble = pygame.Rect(bubble_x, bubble_y, bubble_w, bubble_h)
            pygame.draw.rect(screen, (250,250,250), bubble, border_radius=8)
            pygame.draw.rect(screen, (180,180,180), bubble, 2, border_radius=8)
            tri = [(bubble_x-8, bubble_y + 30), (bubble_x-8, bubble_y + 60), (bubble_x+6, bubble_y + 45)]
            pygame.draw.polygon(screen, (250,250,250), tri)
            pygame.draw.polygon(screen, (180,180,180), tri, 2)
            cur_text = self.dialog_lines[self.dialog_index][:self.type_pos]
            lines = self._wrap_text(cur_text, bubble_w - 20)
            y = bubble.top + 10
            text_color = (20,20,20)
            for ln in lines:
                surf, rect = self.font.render(ln, text_color)
                screen.blit(surf, (bubble.left + 10, y))
                y += rect.height + 6
            hint = "엔터: 문장 빨리 표시" if self.typing else "엔터: 다음 / 완료"
            hint_surf, hint_rect = self.font.render(hint, (120,120,120))
            screen.blit(hint_surf, (bubble.right - hint_rect.width - 10, bubble.bottom - hint_rect.height - 8))
            return

        hud_s, hud_r = self.font.render("ESC: 옵션", (240,240,240))
        screen.blit(hud_s, (10,10))
