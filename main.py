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
                if play_scene is None:
                    from scenes.play import PlayScene
                    play_scene = PlayScene(bgm_volume=getattr(current_scene, "bgm_volume", 0.1),
                                           sfx_volume=getattr(current_scene, "sfx_volume", 0.3))
                current_scene = play_scene

            elif result == "pause":
                if pause_menu is None:
                    from scenes.pause import PauseMenu
                    pause_menu = PauseMenu(bgm_volume=getattr(current_scene, "bgm_volume", 0.1),
                                           sfx_volume=getattr(current_scene, "sfx_volume", 0.3),
                                           previous_scene=current_scene)
                else:
                    pause_menu.previous_scene = current_scene
                current_scene = pause_menu

            elif result == "options":
                if pause_menu is not None and current_scene is pause_menu:
                    current_scene = pause_menu.options_scene
                    try:
                        current_scene.start()
                    except Exception:
                        pass
                else:
                    from scenes.options import OptionsScene
                    opt = OptionsScene(
                        bgm_volume=getattr(current_scene, "bgm_volume", title_scene.bgm_volume),
                        sfx_volume=getattr(current_scene, "sfx_volume", title_scene.sfx_volume),
                        previous_scene=current_scene
                    )
                    try:
                        opt.start()
                    except Exception:
                        pass
                    current_scene = opt

            elif result == "title":
                current_scene = title_scene

            elif isinstance(result, object) and hasattr(result, "draw"):
                current_scene = result

        if current_scene is not last_scene:
            try:
                if hasattr(current_scene, "start"):
                    current_scene.start()
            except Exception:
                pass
            last_scene = current_scene

        current_scene.update(dt)
        current_scene.draw(SCREEN)
        pygame.display.flip()

if __name__ == "__main__":
    main()
