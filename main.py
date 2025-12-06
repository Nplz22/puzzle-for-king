import pygame, sys, os
from scenes.title import TitleScene
from scenes.story_intro import StoryIntro
from scenes.play import PlayScene
from scenes.play2 import Play2Scene
from scenes.puzzle1 import Puzzle1
from scenes.puzzle2 import Puzzle2
from scenes.goal import GoalScene
from scenes.ending import EndingScene
from scenes.options import OptionsScene
from scenes.audio import get_audio_manager

pygame.init()
SCREEN = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Puzzle for the King")
clock = pygame.time.Clock()

def main():
    audio = get_audio_manager()

    title_scene = TitleScene()
    play_scene = PlayScene(previous_scene=title_scene)
    play2_scene = Play2Scene(previous_scene=None)
    puzzle1_scene = Puzzle1(previous_scene=play_scene)
    play2_scene.previous_scene = puzzle1_scene

    story_lines = [
        "주인공인 현우는 네모 왕국 왕자로 태어났습니다.",
        "하지만 어린 나이에 자신의 어머니(왕비)가 세상을 떠나버렸어요.",
        "왕은 새 왕비를 모셔왔고 그렇게 둘 사이에 또 다른 왕자가 한 명 태어났습니다.",
        "새 왕비는 본인한테서 태어난 왕자를 더 이뻐했고 현우를 못 살게 굴기 시작했습니다.",
        "그렇게 현우는 온갖 괴롭힘을 견뎌내며 왕자 생활을 하고 있었습니다.",
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

    options_scene = OptionsScene()
    options_scene.previous_scene = title_scene

    current_scene = title_scene
    current_scene.start()

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            try:
                result = current_scene.handle_event(event)
            except Exception:
                result = None

            if result is not None:
                next_scene = result
                if isinstance(result, str):
                    cmd = result.lower()
                    mapping = {
                        "title": title_scene,
                        "story": story_scene,
                        "play": play_scene,
                        "play2": play2_scene,
                        "puzzle1": puzzle1_scene,
                        "options": options_scene,
                    }
                    next_scene = mapping.get(cmd, None)
                    if cmd == "options":
                        options_scene.previous_scene = current_scene
                if next_scene is not None and next_scene != current_scene:
                    if hasattr(next_scene, "start"):
                        if next_scene == play_scene and isinstance(current_scene, OptionsScene):
                            next_scene.start(resume_from_options=True)
                        else:
                            next_scene.start()
                    current_scene = next_scene

        if hasattr(current_scene, "next_scene_result"):
            next_scene = current_scene.next_scene_result
            if next_scene and next_scene != current_scene:
                mapping = {
                    "title": title_scene,
                    "story": story_scene,
                    "play": play_scene,
                    "play2": play2_scene,
                    "puzzle1": puzzle1_scene,
                    "options": options_scene,
                }
                next_scene_obj = mapping.get(next_scene, None)
                if next_scene_obj and hasattr(next_scene_obj, "start"):
                    next_scene_obj.start()
                current_scene = next_scene_obj
            if hasattr(current_scene, "next_scene_result"):
                del current_scene.next_scene_result

        if hasattr(current_scene, "update"):
            try: current_scene.update(dt)
            except Exception: pass

        if hasattr(current_scene, "draw"):
            try: current_scene.draw(SCREEN)
            except Exception: pass

        pygame.display.flip()

if __name__ == "__main__":
    main()
