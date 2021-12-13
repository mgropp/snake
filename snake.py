import pygame
import random
from typing import Optional, List, Tuple
import time

TILE_SIZE = 20
SNAKE_HEAD = (50, 205, 50)
SNAKE_BODY = (40, 195, 40)

RIGHT = (1, 0)
LEFT = (-1, 0)
UP = (0, -1)
DOWN = (0, 1)


# TODO: Spielklassen

class Item:
    def __init__(self, x: int, y: int) -> None:
        self._x = x
        self._y = y

    # returns whether both given coordinates match with the objects coordinates
    def occupies(self, x: int, y: int) -> bool:
        if x == self._x and y == self._y:
            return True
        return False

    # returns a string that represents this object of item with the two attributes x and y
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


class Snake:
    def __init__(self, x: int, y: int) -> None:
        self._occupies = [(x, y)]
        self._direction = tuple[int, int]
        self._grow = 0

        self.set_direction(RIGHT)
        self.grow(3)

    def get_head(self) -> Tuple[int, int]:
        return self._occupies[0]

    def occupies(self, x: int, y: int) -> bool:
        print('check occupied')
        for coordinate in self._occupies:
            print(coordinate, x, y)

            if x == coordinate[0] and y == coordinate[1]:
                return True
        return False

    def draw(self, surface: pygame.Surface) -> None:

        for ind, part in enumerate(self._occupies):
            if ind != 0:
                color = SNAKE_BODY
            else:
                color = SNAKE_HEAD

            pygame.draw.rect(surface,
                             color,
                             [TILE_SIZE * part[0],
                              TILE_SIZE * part[1],
                              TILE_SIZE,
                              TILE_SIZE]
                             )

    def set_direction(self, direction: tuple[int, int]) -> None:
        if direction == RIGHT or direction == LEFT or direction == UP or direction == DOWN:
            self._direction = direction
        else:
            raise Exception('Wrong direction')

    # The snake can only grow 1 field per tick -> grow can only be 1 or 0 to prevent errors
    def grow(self, g: int) -> None:
        if g > 0:
            self._grow = 1

        # TODO weitere Body teile hinzufügen? Nein?

    def step(self, forbidden: list[Item]) -> bool:
        new_field = (self._occupies[0][0] + self._direction[0], self._occupies[0][1] + self._direction[1])

        for forbidden_field in forbidden:
            print(f'{new_field} ?= {forbidden_field}')
            if forbidden_field.occupies(new_field[0], new_field[1]):
                return False

        if self.occupies(new_field[0], new_field[1]):
            return False

        self._occupies.insert(0, new_field)
        if self._grow == 0:
            self._occupies.pop()
        else:
            self._grow = 0

        return True


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

    snake = Snake(width // 2, height // 2)
    # TODO zusätzliche Steine im innern erstellen
    # wall.append(Brick(7,7))

    running = True
    while running:
        screen.fill((20, 20, 20))

        # draws every brick in wall on 'screen'
        for brick in wall:
            brick.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Spiel beenden
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake.set_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.set_direction(RIGHT)
                elif event.key == pygame.K_UP:
                    snake.set_direction(UP)
                elif event.key == pygame.K_DOWN:
                    snake.set_direction(DOWN)

        if not running:
            break

        running = snake.step(wall)
        print(running)
        snake.draw(screen)

        # TODO: Ueberpruefen, ob die Kirsche erreicht wurde, falls ja, wachsen und Kirsche bewegen.

        # TODO: Kirsche zeichnen

        pygame.display.flip()
        clock.tick(speed)

    pygame.display.quit()
    pygame.quit()


if __name__ == '__main__':
    main()
