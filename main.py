import pygame, sys, os
from scenes.title import TitleScene
from scenes.story_intro import StoryIntro
from scenes.play import PlayScene
from scenes.puzzle1 import Puzzle1
from scenes.puzzle2 import Puzzle2
from scenes.puzzle3 import Puzzle3
from scenes.goal import GoalScene
from scenes.ending import EndingScene
from scenes.options import OptionsScene
from scenes.pause import PauseMenu
from scenes.audio import get_audio_manager

pygame.init()
SCREEN = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Puzzle for the King")
clock = pygame.time.Clock()

def main():
    audio = get_audio_manager()

    title_scene = TitleScene()
    try:
        play_scene = PlayScene(previous_scene=title_scene)
    except TypeError:
        play_scene = PlayScene()
        setattr(play_scene, "previous_scene", title_scene)

    story_lines = [
        "주인공인 현우는 네모 왕국 왕자로 태어났습니다.",
        "하지만 어린 나이에 자신의 어머니(왕비)가 세상을 떠나버렸어요.",
        "왕은 새 왕비를 모셔왔고 그렇게 둘 사이에 또 다른 왕자가 한 명 태어났습니다.",
        "시간이 지날수록 왕은 건강이 악화되었고,",
        "왕은 두 왕자에게 자신이 만든 퍼즐 코스를 먼저 해결하는 사람에게 왕위를 물려주겠다고 했습니다.",
        "과연 주인공은 무사히 왕위에 오를 수 있을까요?"
    ]
    story_scene = StoryIntro(
        lines=story_lines,
        bgm_path="assets/sounds/스토리 요약 브금.mp3",
        previous_scene=title_scene,
        next_scene=play_scene,
        sfx_path="assets/sounds/선택 브금.wav",
        bg_image_path=os.path.join("assets","images","story background.png")
    )
    options_scene = OptionsScene(bgm_volume=0.1, sfx_volume=0.3, previous_scene=title_scene)

    try:
        puzzle1 = Puzzle1(previous_scene=play_scene)
    except TypeError:
        puzzle1 = Puzzle1()
    try:
        puzzle2 = Puzzle2(previous_scene=play_scene)
    except TypeError:
        puzzle2 = Puzzle2()
    try:
        puzzle3 = Puzzle3(previous_scene=play_scene)
    except TypeError:
        puzzle3 = Puzzle3()
    try:
        goal_scene = GoalScene(previous_scene=play_scene)
    except TypeError:
        goal_scene = GoalScene()
    try:
        ending_scene = EndingScene(previous_scene=title_scene)
    except TypeError:
        ending_scene = EndingScene()
    try:
        pause_menu = PauseMenu(previous_scene=play_scene)
    except Exception:
        pause_menu = PauseMenu()
        pause_menu.previous_scene = play_scene

    current_scene = title_scene
    last_scene = None
    if hasattr(title_scene, "start"):
        try:
            pygame.mixer.stop()
        except Exception:
            pass
        title_scene.start()

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            result = None
            try:
                result = current_scene.handle_event(event)
            except Exception:
                result = None

            if result is not None:
                next_scene = None
                if isinstance(result, str):
                    cmd = result.lower()
                    mapping = {
                        "story": story_scene,
                        "play": play_scene,
                        "puzzle1": puzzle1,
                        "puzzle2": puzzle2,
                        "puzzle3": puzzle3,
                        "goal": goal_scene,
                        "ending": ending_scene,
                        "title": title_scene,
                        "options": options_scene,
                        "pause": pause_menu
                    }
                    next_scene = mapping.get(cmd, None)
                    if cmd == "pause":
                        pause_menu.previous_scene = current_scene
                else:
                    next_scene = result

                if next_scene is not None and next_scene is not current_scene:
                    try:
                        pygame.mixer.stop()
                    except Exception:
                        pass
                    current_scene = next_scene

        if current_scene is not last_scene:
            try:
                if hasattr(current_scene, "start"):
                    current_scene.start()
            except Exception:
                pass
            last_scene = current_scene

        try:
            if hasattr(current_scene, "update"):
                current_scene.update(dt)
        except Exception:
            pass

        try:
            if hasattr(current_scene, "draw"):
                current_scene.draw(SCREEN)
        except Exception:
            pass

        pygame.display.flip()

if __name__ == "__main__":
    main()
