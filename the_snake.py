from random import randint

import pygame


pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

START_LENGTH_SNAKE = 1

SPEED = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
screen.fill(BOARD_BACKGROUND_COLOR)
clock = pygame.time.Clock()


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


class GameObject:
    """Базовый класс объектов игры."""

    def __init__(self, position=None, body_color=None):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод отрисовки объекта."""


class Apple(GameObject):
    """Класс, описывающий яблоко."""

    def __init__(self, position=None, body_color=None):
        position = self.randomize_position
        body_color = APPLE_COLOR
        super().__init__(position, body_color)

    @property
    def randomize_position(self):
        """Случайная позиция появления яблока."""
        return (
            randint(0, (GRID_WIDTH - 1)) * GRID_SIZE,
            randint(0, (GRID_HEIGHT - 1)) * GRID_SIZE
        )

    def draw(self, surface):
        """Метод отрисовки яблока на игровом поле."""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, описывающий змейку."""

    def __init__(self, position=None, body_color=None):
        body_color = SNAKE_COLOR
        position = self.get_head_position
        self.length = START_LENGTH_SNAKE
        self.positions = [position]
        self.direction = RIGHT
        self.next_direction = None
        super().__init__(position, body_color)

    @property
    def get_head_position(self):
        """Стартовая позиция змейки."""
        return SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

    @property
    def last(self):
        """Последний сегмент змейки."""
        return self.positions[-1]

    def update_direction(self):
        """Метод обновления направления змейки после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self, surface):
        """Метод отрисовки змейки на игровом поле."""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def move(self):
        """Метод перемещения змейки."""
        self.positions.insert(
            0,
            (
                self.positions[0][0] + self.direction[0] * GRID_SIZE,
                self.positions[0][1] + self.direction[1] * GRID_SIZE
            )
        )
        for i in range(len(self.positions)):
            if self.positions[i][0] == SCREEN_WIDTH:
                self.positions.insert(i, (0, self.positions[i][1]))
                self.positions.pop(i + 1)
            elif self.positions[i][0] == -GRID_SIZE:
                self.positions.insert(
                    i, (SCREEN_WIDTH - GRID_SIZE, self.positions[i][1])
                )
                self.positions.pop(i + 1)
            elif self.positions[i][1] == SCREEN_HEIGHT:
                self.positions.insert(i, (self.positions[i][0], 0))
                self.positions.pop(i + 1)
            elif self.positions[i][1] == -GRID_SIZE:
                self.positions.insert(
                    i, (self.positions[i][0], SCREEN_HEIGHT - GRID_SIZE)
                )
                self.positions.pop(i + 1)

    def reset(self):
        """Метод сброса игры."""
        if len(self.positions) != len(set(self.positions)):
            screen.fill(BOARD_BACKGROUND_COLOR)
            main()


def main():
    apple = Apple()
    apple.draw(screen)
    snake = Snake()
    snake.draw(screen)

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()
        snake.draw(screen)

        if snake.positions[0] == apple.position:
            apple.position = apple.randomize_position
            while apple.position in snake.positions:
                apple.position = apple.randomize_position
        else:
            snake.positions.pop(-1)

        snake.reset()
        apple.draw(screen)

        pygame.display.update()


if __name__ == '__main__':
    main()
