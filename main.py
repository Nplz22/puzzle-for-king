import pygame, sys
from scenes.title import TitleScene
from scenes.story_intro import StoryIntro
from scenes.play import PlayScene
from scenes import fonts

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    play_scene = PlayScene()
    title_scene = TitleScene()
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
        bg_image_path="assets/images/story background.png"
    )

    current_scene = title_scene
    current_scene.start()

    while True:
        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            result = current_scene.handle_event(event)
            if result == "play":
                current_scene = story_scene
                current_scene.start()
            elif isinstance(result, PlayScene):
                current_scene = result
                current_scene.start()
            elif result in ("options", "pause"):
                pass

        current_scene.update(dt)
        current_scene.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    main()
