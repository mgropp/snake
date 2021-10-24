import pygame
import random
from typing import Optional, List, Tuple

TILE_SIZE = 20

# TODO: Spielklassen


def main():
    width = 20
    height = 15
    speed = 7

    pygame.init()
    screen = pygame.display.set_mode((
        TILE_SIZE * width,
        TILE_SIZE * height
    ))

    clock = pygame.time.Clock()

    # TODO: Spielobjekte anlegen

    running = True
    while running:
        screen.fill((20, 20, 20))

        # TODO: Mauer zeichnen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Spiel beenden
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    # TODO: Richtung aendern: nach links
                    pass
                elif event.key == pygame.K_RIGHT:
                    # TODO: Richtung aendern: nach rechts
                    pass
                elif event.key == pygame.K_UP:
                    # TODO: Richtung aendern: nach oben
                    pass
                elif event.key == pygame.K_DOWN:
                    # TODO: Richtung aendern: nach unten
                    pass

        if not running:
            break

        # TODO: Schlange bewegen

        # TODO: Schlange zeichnen

        # TODO: Ueberpruefen, ob die Kirsche erreicht wurde, falls ja, wachsen und Kirsche bewegen.

        # TODO: Kirsche zeichnen

        pygame.display.flip()
        clock.tick(speed)

    pygame.display.quit()
    pygame.quit()


if __name__ == '__main__':
    main()
