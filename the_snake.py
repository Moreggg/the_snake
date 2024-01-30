from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

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
SPEED = 5

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject():
    position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

    def __init__(self, body_color):
        self.body_color = body_color

    def draw(self):
        pass


class Apple(GameObject):

    def __init__(self, body_color=APPLE_COLOR):
        super().__init__(body_color)
        self.position = self.randomize_position()

    def randomize_position(self):
        return [randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE]

# Метод draw класса Apple
    def draw(self, surface):

        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):

    def __init__(self, body_color):
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        super().__init__(body_color)

# Метод обновления направления после нажатия на кнопку
    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

# # Метод draw класса Snake
    def draw(self, surface):
        for position in self.positions:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        return self.positions[0]

    def move(self):
        head_positton = self.get_head_position()
        new_head_positton_x = head_positton[0] + self.direction[0] * GRID_SIZE
        new_head_positton_y = head_positton[1] + self.direction[1] * GRID_SIZE
        if new_head_positton_x == SCREEN_WIDTH:
            new_head_positton_x = 0
        if new_head_positton_x < 0:
            new_head_positton_x = SCREEN_WIDTH - 20
        if new_head_positton_y == SCREEN_HEIGHT:
            new_head_positton_y = 0
        if new_head_positton_y < 0:
            new_head_positton_y = SCREEN_HEIGHT - 20
        self.positions.insert(0, [new_head_positton_x, new_head_positton_y])
        if len(self.positions) > self.length:
            self.positions.pop()


    def reset(self):
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([LEFT, RIGHT, UP, DOWN])


# Функция обработки действий пользователя
def handle_keys(game_object):
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


def main():
    # Тут нужно создать экземпляры классов.
    snake = Snake(SNAKE_COLOR)
    apple = Apple(APPLE_COLOR)

    while True:
        clock.tick(SPEED)

        # Тут опишите основную логику игры.
        if apple.position == snake.positions[0]:
            snake.length += 1
            # screen.fill(BOARD_BACKGROUND_COLOR)
            apple.position = apple.randomize_position()
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            print(snake.get_head_position(), snake.positions, snake.positions[:-1])
        snake.draw(screen)
        apple.draw(screen)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        # print(snake.positions, snake.get_head_position(), apple.position)
        pygame.display.update()
        screen.fill(BOARD_BACKGROUND_COLOR)



if __name__ == '__main__':
    main()
