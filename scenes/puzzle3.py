from scenes.puzzle import Puzzle

class Puzzle3(Puzzle):
    def __init__(self, previous_scene=None):
        super().__init__(previous_scene=previous_scene,
                         bgm_path="assets/sounds/puzzle3 브금.mp3")
    
    def draw(self, screen):
        super().draw(screen)
        t_s, t_r = self.font.render("퍼즐3: 엔터를 눌러 완료", (240,240,240))
        screen.blit(t_s, (200, 280))
