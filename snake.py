import pygame
import random
from typing import Optional, List, Tuple
import time

TILE_SIZE = 20


# TODO: Spielklassen

class Item:
    def __init__(self, x: int, y: int) -> None:
        self._x = x
        self._y = y

    def occupies(self, x: int, y: int) -> bool:
        if x == self._x and y == self._y:
            return True
        return False

    def __repr__(self):
        return f'x = {self._x}, y = {self._y}'


class Brick(Item):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface,
                         (230, 230, 230),
                         [TILE_SIZE * self._x,
                          TILE_SIZE * self._y,
                          TILE_SIZE,
                          TILE_SIZE]
                         )


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

    # defines a wall on the outer coordinates of the field
    wall = [
        Brick(x, y)
        for x in range(width)
        for y in range(height)
        if x == 0 or x == width - 1 or y == 0 or y == height - 1
    ]

    # TODO zusätzliche Steine im innern erstellen
    # wall.append(Brick(7,7))

    running = True
    while running:
        screen.fill((20, 20, 20))

        for brick in wall:
            brick.draw(screen)

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
