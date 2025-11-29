import pygame
import sys
from scenes.title import TitleScene
from scenes.story_intro import StoryIntro
from scenes.play import PlayScene
from scenes.pause import PauseMenu
from scenes.options import OptionsScene

pygame.init()
SCREEN = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Puzzle for the King")
clock = pygame.time.Clock()

def main():
    title_scene = TitleScene()
    story_lines = [
        "주인공 현우는 네모 왕국의 왕자로 태어났습니다.",
        "하지만 어린 나이에 어머니(왕비)를 잃고 말았죠.",
        "왕은 새 왕비를 맞이했고, 또 다른 왕자가 태어났습니다.",
        "시간이 흐르며 왕의 건강은 악화되었고,",
        "왕은 퍼즐 코스를 먼저 푼 사람에게 왕위를 물려주겠다고 했습니다.",
        "현우는 과연 왕위에 오를 수 있을까요?"
    ]
    story_scene = StoryIntro(
        lines=story_lines,
        bgm_path="assets/sounds/스토리 요약 브금.mp3",
        bgm_volume=0.07,
        sfx_path="assets/sounds/선택 브금.wav",
        previous_scene=title_scene
    )

    current_scene = title_scene
    last_scene = None
    pause_menu = None
    play_scene = None

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            result = current_scene.handle_event(event)
            if result == "play":
                current_scene = story_scene
            elif result == "pause":
                if pause_menu is None:
                    pause_menu = PauseMenu(bgm_volume=getattr(current_scene,"bgm_volume",0.1),
                                           sfx_volume=getattr(current_scene,"sfx_volume",0.3),
                                           previous_scene=current_scene)
                else:
                    pause_menu.previous_scene = current_scene
                current_scene = pause_menu
            elif result == "options":
                if isinstance(current_scene, PauseMenu):
                    current_scene = current_scene.options_scene
                else:
                    current_scene = OptionsScene(
                        bgm_volume=getattr(current_scene,"bgm_volume",0.1),
                        sfx_volume=getattr(current_scene,"sfx_volume",0.3),
                        previous_scene=current_scene
                    )
            elif result == "title":
                current_scene = title_scene
            elif hasattr(result, "draw"):
                current_scene = result

        if current_scene is not last_scene:
            try:
                if hasattr(current_scene,"start"):
                    current_scene.start()
            except Exception:
                pass
            last_scene = current_scene

        current_scene.update(dt)
        current_scene.draw(SCREEN)
        pygame.display.flip()

if __name__ == "__main__":
    main()
