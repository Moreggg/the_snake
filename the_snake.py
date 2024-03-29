from random import choice, randint
import sys

import pygame


# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты."""

    def __init__(self, body_color=BOARD_BACKGROUND_COLOR):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color

    def make_cell(self, position, surface):
        """Отрисовывает ячейки на игровой поверхности."""
        rect = pygame.Rect(
            (position[0], position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

    def draw(self):
        """Абстрактный метод, который предназначен
        для переопределения в дочерних классах.
        """
        pass


class Apple(GameObject):
    """Класс, унаследованный от GameObject,
    описывающий яблоко и действия с ним.
    """

    def __init__(self, snake=None, body_color=APPLE_COLOR):
        super().__init__(body_color)
        self.randomize_position(snake)

    def randomize_position(self, snake=None):
        """Устанавливает случайное положение яблока на игровом поле."""
        while snake and self.position in snake.positions:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self, surface=screen):
        """Отрисовывает яблоко на игровой поверхности."""
        self.make_cell(self.position, surface)


class Snake(GameObject):
    """Класс, унаследованный от GameObject,
    описывающий змейку и её поведение.
    """

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color)
        self.reset()
        self.next_direction = None
        self.last = None

# Метод обновления направления после нажатия на кнопку
    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self, surface=screen):
        """Отрисовывает змейку и затирает последний сегмент."""
        self.make_cell(self.get_head_position(), surface)
        if self.last:
            last_rect = pygame.Rect(
                self.last,
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def move(self):
        """Обновляет позицию змейки (координаты каждой секции),
        добавляя новую голову в начало списка
        positions и удаляя последний элемент,
        если длина змейки не увеличилась.
        """
        head_positton = self.get_head_position()
        new_x = ((head_positton[0] + self.direction[0] * GRID_SIZE)
                 % SCREEN_WIDTH)
        new_y = ((head_positton[1] + self.direction[1] * GRID_SIZE)
                 % SCREEN_HEIGHT)
        self.positions.insert(0, (new_x, new_y))
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def reset(self):
        """сбрасывает змейку в начальное состояние
        после столкновения с собой.
        """
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([LEFT, RIGHT, UP, DOWN])


# Функция обработки действий пользователя
def handle_keys(game_object):
    """Обрабатывает нажатия клавиш,
    чтобы изменить направление движения змейки.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif event.key == pygame.K_ESCAPE:
                sys.exit()


def main():
    """Основной игровой цикл, где происходит обновление состояния объектов."""
    # Тут нужно создать экземпляры классов.

    # Инициализация PyGame:
    pygame.init()

    snake = Snake()
    screen.fill(BOARD_BACKGROUND_COLOR)
    apple = Apple(snake)
    apple.draw()

    while True:
        clock.tick(SPEED)

        # Тут опишите основную логику игры.
        if apple.position == snake.get_head_position():
            snake.length += 1
            apple.randomize_position(snake)
            apple.draw()
        if snake.get_head_position() in snake.positions[1:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            apple.draw()
        snake.draw()
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        pygame.display.update()


if __name__ == '__main__':
    main()
