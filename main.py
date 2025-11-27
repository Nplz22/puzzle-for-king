import pygame, sys
from scenes.title import TitleScene
from scenes.play import PlayScene

pygame.init()
pygame.mixer.init()
SCREEN = pygame.display.set_mode((800, 600))
CLOCK = pygame.time.Clock()
FPS = 60

SCENES = {
    "title": TitleScene,
    "play": PlayScene
}

def run():
    current = SCENES["title"]()
    current.start()

    while True:
        dt = CLOCK.tick(FPS)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            change = current.handle_event(event)
            if change:
                current = SCENES[change]()
                current.start()

        current.update(dt)
        current.draw(SCREEN)
        pygame.display.flip()

if __name__ == "__main__":
    run()