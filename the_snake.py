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

EVENT_KEYS = {
    pygame.K_UP: UP,
    pygame.K_DOWN: DOWN,
    pygame.K_LEFT: LEFT,
    pygame.K_RIGHT: RIGHT
}

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
            game_object.next_direction = EVENT_KEYS[event.key]


class GameObject:
    """Базовый класс объектов игры."""

    def __init__(self, position=None, body_color=None):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод отрисовки объекта."""

    def draw_rect(self, rect):
        """Метод отрисовки сегмента объекта."""
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


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

    def draw(self):
        """Метод отрисовки яблока на игровом поле."""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        self.draw_rect(rect)


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
            if self.next_direction == UP and self.direction == DOWN:
                self.next_direction = None
            elif self.next_direction == DOWN and self.direction == UP:
                self.next_direction = None
            elif self.next_direction == LEFT and self.direction == RIGHT:
                self.next_direction = None
            elif self.next_direction == RIGHT and self.direction == LEFT:
                self.next_direction = None
            else:
                self.direction = self.next_direction

    def draw(self):
        """Метод отрисовки змейки на игровом поле."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(
                (position[0], position[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            self.draw_rect(rect)
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        self.draw_rect(head_rect)
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def move(self):
        """Метод перемещения змейки."""
        self.positions.insert(
            0,
            (
                self.positions[0][0] + self.direction[0] * GRID_SIZE,
                self.positions[0][1] + self.direction[1] * GRID_SIZE
            )
        )
        for i, position in enumerate(self.positions):
            if position[0] == SCREEN_WIDTH:
                self.positions.insert(i, (0, position[1]))
                self.positions.remove(position)
            elif position[0] == -GRID_SIZE:
                self.positions.insert(
                    i, (SCREEN_WIDTH - GRID_SIZE, position[1])
                )
                self.positions.remove(position)
            elif position[1] == SCREEN_HEIGHT:
                self.positions.insert(i, (position[0], 0))
                self.positions.remove(position)
            elif position[1] == -GRID_SIZE:
                self.positions.insert(
                    i, (position[0], SCREEN_HEIGHT - GRID_SIZE)
                )
                self.positions.remove(position)

    def reset(self):
        """Метод сброса игры."""
        if len(self.positions) != len(set(self.positions)):
            screen.fill(BOARD_BACKGROUND_COLOR)
            main()


def main():
    """Главная функция."""
    apple = Apple()
    apple.draw()
    snake = Snake()
    snake.draw()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()
        snake.draw()
        if snake.positions[0] == apple.position:
            apple.position = apple.randomize_position
            while apple.position in snake.positions:
                apple.position = apple.randomize_position
        else:
            snake.positions.pop(-1)
        snake.reset()
        apple.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
