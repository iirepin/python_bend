import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Настройки игры
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE
BACKGROUND_COLOR = (0, 0, 0)

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class GameObject:
    """Базовый класс для всех игровых объектов."""
    
    def __init__(self, position=None):
        """
        Инициализирует игровой объект.
        
        Args:
            position (tuple): Начальная позиция объекта (x, y). 
                             Если None, используется центр экрана.
        """
        if position is None:
            position = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        self.position = position
        self.body_color = None
    
    def draw(self, surface):
        """Абстрактный метод для отрисовки объекта."""
        pass


class Apple(GameObject):
    """Класс яблока, наследуется от GameObject."""
    
    def __init__(self):
        """Инициализирует яблоко со случайной позицией и красным цветом."""
        super().__init__()
        self.body_color = (255, 0, 0)  # Красный
        self.randomize_position()
    
    def randomize_position(self):
        """Устанавливает случайную позицию яблока в пределах игрового поля."""
        self.position = (
            random.randint(0, GRID_WIDTH - 1),
            random.randint(0, GRID_HEIGHT - 1)
        )
    
    def draw(self, surface):
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE,
            self.position[1] * GRID_SIZE,
            GRID_SIZE, GRID_SIZE
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, (255, 255, 255), rect, 1)


class Snake(GameObject):
    """Класс змейки, наследуется от GameObject."""
    
    def __init__(self):
        """Инициализирует змейку в начальном состоянии."""
        super().__init__()
        self.body_color = (0, 255, 0)  # Зеленый
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
    
    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            # Запрещаем движение в противоположном направлении
            opposite_dir = (
                self.next_direction[0] * -1,
                self.next_direction[1] * -1
            )
            if opposite_dir != self.direction:
                self.direction = self.next_direction
            self.next_direction = None
    
    def move(self):
        """Двигает змейку, добавляя новую голову и удаляя хвост."""
        head_x, head_y = self.positions[0]
        dx, dy = self.direction
        new_head = (
            (head_x + dx) % GRID_WIDTH,
            (head_y + dy) % GRID_HEIGHT
        )
        
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()
    
    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]
    
    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
    
    def draw(self, surface):
        """Отрисовывает змейку на экране."""
        for position in self.positions:
            rect = pygame.Rect(
                position[0] * GRID_SIZE,
                position[1] * GRID_SIZE,
                GRID_SIZE, GRID_SIZE
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, (255, 255, 255), rect, 1)


def handle_keys(snake):
    """Обрабатывает нажатия клавиш для изменения направления змейки."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT:
                snake.next_direction = RIGHT


def main():
    """Основная функция игры."""
    # Инициализация игрового окна
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Змейка')
    
    # Создание игровых объектов
    snake = Snake()
    apple = Apple()
    
    # Создание часов для контроля FPS
    clock = pygame.time.Clock()
    
    # Основной игровой цикл
    while True:
        # Обработка событий
        handle_keys(snake)
        
        # Обновление направления змейки
        snake.update_direction()
        
        # Движение змейки
        snake.move()
        
        # Проверка съедания яблока
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            # Убедимся, что яблоко не появилось на змейке
            while apple.position in snake.positions:
                apple.randomize_position()
        
        # Проверка столкновения с собой
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
        
        # Отрисовка
        screen.fill(BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()
        
        # Контроль скорости игры
        clock.tick(10)  # 10 FPS


if __name__ == "__main__":
    main()