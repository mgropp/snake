import random
from typing import Tuple, Type

import pygame

TILE_SIZE = 30

# The color and direction values are saved in variables for easy access
SNAKE_HEAD_COLOR = (60, 215, 60)
SNAKE_BODY_COLOR = (40, 195, 40)
BRICK_COLOR = (200, 200, 200)
CHERRY_COLOR = (200, 0, 0)
BACKGROUND_COLOR = (70, 70, 70)

RIGHT = (1, 0)
LEFT = (-1, 0)
UP = (0, -1)
DOWN = (0, 1)


# Item defines a class for objects with x and y coordinates and a method to check if they occupy a given coordinate.
class Item:
    def __init__(self, x: int, y: int) -> None:
        self._x = x
        self._y = y

    # returns whether both given coordinates match with the objects coordinates
    def occupies(self, x: int, y: int) -> bool:
        if x == self._x and y == self._y:
            return True
        return False


# Brick defines a class for objects that represent walls.
# They inherit from Item and have a method to draw themselves on the given surface.
class Brick(Item):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)

    def draw(self, surface: pygame.Surface) -> None:
        # x and y have to be multiplied with Tile_size so that the scaling is properly done
        # and every object on the field appears in the according size.
        pygame.draw.rect(surface,
                         BRICK_COLOR,
                         [TILE_SIZE * self._x,
                          TILE_SIZE * self._y,
                          TILE_SIZE,
                          TILE_SIZE]
                         )


# Cherry is a class that defines objects that represent cherrys.
# They inherit from Item and have a method to draw themselves on the given surface.
# They can also move to a random position that is not preoccupied by a wall or the snake.

# Snake defines objects that represent snakes.
class Snake:
    def __init__(self, x: int, y: int) -> None:
        # _occupies stores the positions (x and y coordinates) of every snake part
        self._occupies = [(x, y)]
        # _direction stores the direction the snake is headed, represented by x and y vectors. e.g. (1,0) means right
        self._direction = tuple[int, int]
        # _grow stores whether the snake still needs to grow a part because it ate a cherry.
        self._grow = 0
        # _last_direction stores the direction before the last direction change
        # to ensure the snake doesn't turn 180° at once because this would lead to a crash that is not intended
        self._last_direction = RIGHT

        # _direction and grow are now set by the corresponding method.
        self.set_direction(self._last_direction)
        self.grow(3)

    # get_head returns the position (x and y) of the head of the snake.
    def get_head(self) -> Tuple[int, int]:
        return self._occupies[0]

    # occupies checks if one of the snake parts occupies a given position on the field.
    def occupies(self, x: int, y: int) -> bool:
        for coordinate in self._occupies:
            if x == coordinate[0] and y == coordinate[1]:
                return True
        return False

    # draw draws the whole snake on the given surface.
    # It differentiates between the head and body parts through color and shape
    def draw(self, surface: pygame.Surface) -> None:

        for ind, part in enumerate(self._occupies):
            if ind == 0:
                pygame.draw.ellipse(surface,
                                    SNAKE_HEAD_COLOR,
                                    [TILE_SIZE * part[0],
                                     TILE_SIZE * part[1],
                                     TILE_SIZE,
                                     TILE_SIZE]
                                    )
            else:
                pygame.draw.rect(surface,
                                 SNAKE_BODY_COLOR,
                                 [TILE_SIZE * part[0],
                                  TILE_SIZE * part[1],
                                  TILE_SIZE,
                                  TILE_SIZE]
                                 )

    # set_direction receives a direction and checks if it is a valid direction. If not it raises an exception.
    # It also compares to the last direction and if the new direction is the complete opposite
    # it doesn't update the direction because this would lead to a non-intended crash.
    def set_direction(self, direction: tuple[int, int]) -> None:
        if ((direction == RIGHT or direction == LEFT or direction == UP or direction == DOWN) and
                self._last_direction != (direction[0] * -1, direction[1] * -1)):
            self._direction = direction

    # The grow method adds a number to grow but not if this number is less than 1
    def grow(self, g: int) -> None:
        if g > 0:
            self._grow += g
        else:
            # just to make sure that it resets if something goes wrong
            self._grow = 0

    # step calculates with the head position and the direction the field the snake will now land on
    # and checks whether this might lead to a crash or not and updates the game accordingly
    def step(self, forbidden: list[Item]) -> bool:
        new_field = (self.get_head()[0] + self._direction[0], self.get_head()[1] + self._direction[1])

        # forbidden fields are normally walls.
        for forbidden_field in forbidden:
            if forbidden_field.occupies(new_field[0], new_field[1]):
                return False

        # This checks whether the snake already occupies the position and would bite itself
        if self.occupies(new_field[0], new_field[1]):
            return False

        # This ensures the snake grows if necessary and also that it moves forward.
        self._occupies.insert(0, new_field)
        if self._grow <= 0:
            self._occupies.pop()
        else:
            self._grow -= 1

        # The now last direction is saved.
        self._last_direction = self._direction
        return True


class Cherry(Item):
    def __init__(self) -> None:
        super().__init__(0, 0)

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.ellipse(surface,
                            CHERRY_COLOR,
                            [TILE_SIZE * self._x,
                             TILE_SIZE * self._y,
                             TILE_SIZE,
                             TILE_SIZE]
                            )

    def move(self, snake: Type[Snake], wall: list[tuple[int, int]], width: int, height: int, ) -> None:
        occupied = True
        # The loop generates random positions on the board
        # as long as the cherry can't be placed on the generated position.
        # If it can be placed there, because the position isn't occupied by a snake part or a brick
        # it sets this position as new position.
        while occupied:
            x = random.randrange(0, width)
            y = random.randrange(0, height)
            if snake.occupies(x, y):
                occupied = True
            else:
                for brick in wall:
                    if brick.occupies(x, y):
                        occupied = True
                        break
                    else:
                        occupied = False

        self._x = x
        self._y = y


def main() -> None:
    width = 30
    height = 20
    speed = 7

    pygame.init()
    screen = pygame.display.set_mode((
        TILE_SIZE * width,
        TILE_SIZE * height
    ))

    clock = pygame.time.Clock()

    # defines a wall on the outer coordinates of the field, a cherry
    # and a snake positioned in the approximated field center
    wall = [
        Brick(x, y)
        for x in range(width)
        for y in range(height)
        if x == 0 or x == width - 1 or y == 0 or y == height - 1
    ]
    cherry = Cherry()
    snake = Snake(width // 2, height // 2)

    # To place the cherry on the field it needs to move once.
    cherry.move(snake, wall, width, height)

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

        # update the snake's new position on the field
        snake.draw(screen)

        # check if the Snake hits a cherry and if yes grow the snake and move the cherry.
        if cherry.occupies(snake.get_head()[0], snake.get_head()[1]):
            snake.grow(2)
            cherry.move(snake, wall, width, height)

        # update the cherry's new position on the field
        cherry.draw(screen)

        pygame.display.flip()
        clock.tick(speed)

    font = pygame.font.SysFont('ressources/Elronmonospace.ttf', TILE_SIZE*3)

    # render text
    message = font.render("You Loose!", 5, (200, 50, 50))
    message_w = message.get_width()
    message_h = message.get_height()
    screen.blit(message, (TILE_SIZE * width / 2 - message_w / 2, TILE_SIZE * height / 2 - message_h / 2))
    pygame.display.flip()
    # If the game is finished the game doesn't quit imediately. It waits for the user to close the window.
    waiting_to_quit = True
    while waiting_to_quit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Spiel beenden
                waiting_to_quit = False
                break

    pygame.display.quit()
    pygame.quit()


if __name__ == '__main__':
    main()
