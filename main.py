import pygame
import sys
from scenes.title import TitleScene

pygame.init()
SCREEN = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Puzzle for the King")
clock = pygame.time.Clock()

def main():
    title_scene = TitleScene()
    try:
        title_scene.start()
    except Exception:
        pass

    current_scene = title_scene
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
                if play_scene is None:
                    from scenes.play import PlayScene
                    play_scene = PlayScene(title_scene.bgm_volume, title_scene.sfx_volume)
                    play_scene.start()
                current_scene = play_scene

            elif result == "pause":
                if pause_menu is None:
                    from scenes.pause import PauseMenu
                    pause_menu = PauseMenu(title_scene.bgm_volume, title_scene.sfx_volume)
                current_scene = pause_menu

            elif result == "options":
                if current_scene == pause_menu and pause_menu is not None:
                    current_scene = pause_menu.options_scene
                else:
                    from scenes.options import OptionsScene
                    current_scene = OptionsScene(
                        bgm_volume=title_scene.bgm_volume,
                        sfx_volume=title_scene.sfx_volume,
                        previous_scene=current_scene
                    )
                    current_scene.start()

            elif result == "title":
                current_scene = title_scene
                try:
                    title_scene.start()
                except Exception:
                    pass

            elif isinstance(result, object) and hasattr(result, "draw"):
                current_scene = result

        current_scene.update(dt)
        current_scene.draw(SCREEN)
        pygame.display.flip()

if __name__ == "__main__":
    main()
