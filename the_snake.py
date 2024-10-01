from random import randint

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
    """Родительский класс для всех игровых объектов."""
    def __init__(self, position=(), body_color=()):
        """Инициализация объекта."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод отрисовки объекта."""
        pass


class Snake(GameObject):
    """Класс змейки."""
    def __init__(self, position: tuple = (), body_color: tuple = ()):
        """Инициализация змейки."""
        super().__init__(position, body_color)
        self.position = ((GRID_WIDTH // 2) * GRID_SIZE,
                         (GRID_HEIGHT // 2) * GRID_SIZE)
        self.body_color = SNAKE_COLOR
        self.direction = RIGHT
        self.positions = [self.position]
        self.next_direction = None
        self.length = 1
        self.last = self.positions[-1]
        self.is_length_changed = False

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод движения змейки."""
        self.update_direction()
        if self.is_snake_out_of_field():
            if self.direction == RIGHT:
                self.positions[0] = (0, self.positions[0][1])
            elif self.direction == DOWN:
                self.positions[0] = (self.positions[0][0], 0)
            elif self.direction == LEFT:
                self.positions[0] = (SCREEN_WIDTH - GRID_SIZE,
                                     self.positions[0][1])
            elif self.direction == UP:
                self.positions[0] = (self.positions[0][0],
                                     SCREEN_HEIGHT - GRID_SIZE)

        new_head = self.get_head_position()
        new_head_list = list(new_head)
        new_head = (new_head_list[0] + self.direction[0] * GRID_SIZE,
                    new_head_list[1] + self.direction[1] * GRID_SIZE)
        self.positions.insert(0, new_head)
        if not self.is_length_changed:
            self.last = self.positions.pop()
        else:
            self.is_length_changed = False

    def eat(self):
        """Метод съедания яблока."""
        self.length += 1
        self.is_length_changed = True

    def is_snake_out_of_field(self):
        """Метод проверки выхода змейки за границы поля."""
        return not (0 <= self.get_head_position()[0] < SCREEN_WIDTH and
                    0 <= self.get_head_position()[1] < SCREEN_HEIGHT)

    def touch_apple(self, apple: "Apple"):
        """Метод столкновения змейки с яблоком."""
        if self.get_head_position() == apple.position:
            self.eat()
            apple.randomize_position()

    def is_snake_eat_itself(self):
        """Метод проверки столкновения змейки с самой собой."""
        return self.get_head_position() in self.positions[1:]

    def get_head_position(self):
        """Возвращает позицию головы змеи."""
        return self.positions[0]

    def draw(self):
        """Отрисовка змеи."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Сбрасывает настройки змеи после проигрыша."""
        self.position = ((GRID_WIDTH // 2) * GRID_SIZE,
                         (GRID_HEIGHT // 2) * GRID_SIZE)
        self.direction = RIGHT
        self.positions = [self.position]
        self.next_direction = None
        self.length = 1
        self.last = self.positions[-1]
        self.is_length_changed = False


class Apple(GameObject):
    """Класс яблока."""
    def __init__(self, position: tuple = (), body_color: tuple = ()):
        """Инициализация яблока."""
        super().__init__(position, body_color)
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Рандомит позицию для яблока."""
        x = randint(0, 31)
        y = randint(0, 23)
        self.position = (x * GRID_SIZE, y * GRID_SIZE)

    def draw(self):
        """Отрисовывает яблоко."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(game_object):
    """Отлавливает нажатия."""
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
    """Основная функция."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()
    while True:
        clock.tick(SPEED)
        snake.draw()
        apple.draw()
        snake.move()
        snake.touch_apple(apple)
        if snake.is_snake_eat_itself():
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, screen.get_rect())
            snake.reset()
            apple.randomize_position()
        handle_keys(snake)
        snake.update_direction()
        pygame.display.update()


if __name__ == '__main__':
    main()
