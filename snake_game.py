import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.Font('resources\calibri.ttf', 20)

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

Point = namedtuple('Point', 'x, y')

# RGB Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE1 = (0, 0, 128)
BLUE2 = (0, 0, 255)


BLOCK_SIZE = 20
SPEED = 20

class SnakeGame:

    def __init__(self, width=640, height=480):
        # Screen size.
        self.width = width
        self.height = height

        # Default values.
        self.score = 0
        self.game_over = False
        self.food = None

        # Initialize display.
        self.display = pygame.display.set_mode((self.width, self.height))

        # Screen title.
        pygame.display.set_caption('Snake Game!')

        # Initialize clock.
        self.clock = pygame.time.Clock()

        # Initialize game state
        self.direction = Direction.RIGHT

        self.head = Point(self.width // 2, self.height // 2)
        self.snake = [self.head,
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - 2 * BLOCK_SIZE, self.head.y)]
        
        self.__place_food()
    
    def __place_food(self):
        x = random.randint(0, self.width // BLOCK_SIZE - 1) * BLOCK_SIZE
        y = random.randint(0, self.height // BLOCK_SIZE - 1) * BLOCK_SIZE
        self.food = Point(x, y)

        if self.food in self.snake:
            self.__place_food()
    
    def play_step(self):

        # Collect user input.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN
                elif event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_ESCAPE:
                    return False
        
        # Update snake position.
        self._make_move(self.direction)
        self.snake.insert(0, self.head)

        # Check if game is over.
        if self._is_collision():
            self.game_over = True

            return self.game_over, self.score
        
        # Check if snake ate food.
        if self.head == self.food:
            self.score += 1
            self.__place_food()
        else:
            self.snake.pop()
        
        # Update display and clock.
        self._update_user_interface()
        self.clock.tick(SPEED)

        return self.game_over, self.score

    def _is_collision(self):
        # Check collision with boundary.
        if self.head.x > self.width - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.height - BLOCK_SIZE or self.head.y < 0:
            return True
        
        # Check collision with self.
        if self.head in self.snake[1:]:
            return True
        
        return False
    
    def _update_user_interface(self):
        # Clear display.
        self.display.fill(BLACK)

        # Draw the Snake.
        for point in self.snake:
            pygame.draw.rect(self.display, RED if point == self.head else BLUE1, pygame.Rect(point.x, point.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, RED if point == self.head else BLUE2, pygame.Rect(point.x + 4, point.y + 4, 12, 12))
        
        # Draw the Food.
        pygame.draw.rect(self.display, GREEN, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        # Display score.
        score_text = font.render('Score: ' + str(self.score), True, WHITE)
        self.display.blit(score_text, (0, 0))

        pygame.display.flip()
    
    def _make_move(self, direction):
        if direction == Direction.UP:
            self.head = Point(self.head.x, self.head.y - BLOCK_SIZE)
        elif direction == Direction.DOWN:
            self.head = Point(self.head.x, self.head.y + BLOCK_SIZE)
        elif direction == Direction.LEFT:
            self.head = Point(self.head.x - BLOCK_SIZE, self.head.y)
        elif direction == Direction.RIGHT:
            self.head = Point(self.head.x + BLOCK_SIZE, self.head.y)
        else:
            raise ValueError('Invalid direction.')

if __name__ == '__main__':
    # Initialize game.
    game = SnakeGame()

    # Game loop.
    while True:
        game_over, score = game.play_step()

        if game_over:
            print(f'Game over! Final Score: {str(score)}')
            break
    
    pygame.quit()