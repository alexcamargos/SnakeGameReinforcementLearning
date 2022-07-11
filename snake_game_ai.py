import random

import numpy as np
import pygame

from configurations import *

pygame.init()
font = pygame.font.Font(r'resources\calibri.ttf', 20)


class SnakeGameAI:

    def __init__(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT):
        # Screen size.
        self.width = width
        self.height = height

        # Initialize display.
        self.display = pygame.display.set_mode((self.width, self.height))

        # Screen title.
        pygame.display.set_caption(
            'Snake! Reinforcement Learning With PyTorch and Pygame')

        # Initialize clock.
        self.clock = pygame.time.Clock()

        # Reset game state.
        self.reset_state()

    def reset_state(self):
        # Initialize game state
        self.direction = Direction.RIGHT

        self.head = Point(self.width // 2, self.height // 2)
        self.snake = [
            self.head,
            Point(self.head.x - BLOCK_SIZE, self.head.y),
            Point(self.head.x - 2 * BLOCK_SIZE, self.head.y)
        ]

        # Default values.
        self.score = 0
        self.game_over = False
        self.food = None
        self.state_iteration = 0

        self.__place_random_food()

    def __place_random_food(self):
        x = random.randint(0, self.width // BLOCK_SIZE - 1) * BLOCK_SIZE
        y = random.randint(0, self.height // BLOCK_SIZE - 1) * BLOCK_SIZE

        self.food = Point(x, y)

        if self.food in self.snake:
            self.__place_random_food()

    def play_step(self, action):

        reward = 0
        self.state_iteration += 1

        # Collect user input.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Update snake position.
        self.__make_move(action)
        self.snake.insert(0, self.head)

        # Check if game is over or if the AI was stuck in a loop.
        if self.is_collision() or self.state_iteration > 100 * len(self.snake):

            self.game_over = True
            reward -= 10

            return reward, self.game_over, self.score

        # Check if snake ate food.
        if self.head == self.food:
            self.score += 1
            reward += 10
            self.__place_random_food()
        else:
            self.snake.pop()

        # Update display and clock.
        self.__update_user_interface()
        self.clock.tick(SPEED_FOR_AI)

        return reward, self.game_over, self.score

    def is_collision(self, point=None):

        if point is None:
            point = self.head

        # Check collision with boundary.
        if point.x > self.width - BLOCK_SIZE or point.x < 0 or point.y > self.height - BLOCK_SIZE or point.y < 0:
            return True

        # Check collision with self.
        if point in self.snake[1:]:
            return True

        return False

    def __update_user_interface(self):
        # Clear display.
        self.display.fill(BLACK)

        # Draw the Snake.
        for point in self.snake:
            pygame.draw.rect(
                self.display, RED if point == self.head else BLUE1,
                pygame.Rect(point.x, point.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display,
                             RED if point == self.head else BLUE2,
                             pygame.Rect(point.x + 4, point.y + 4, 12, 12))

        # Draw the Food.
        pygame.draw.rect(
            self.display, GREEN,
            pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        # Display score.
        score_text = font.render('Score: ' + str(self.score), True, WHITE)
        self.display.blit(score_text, (0, 0))

        pygame.display.flip()

    def __make_move(self, action):
        """ Make a move in the given direction.

            action: [straight, right, left]
            straight = [1, 0, 0]
            right = [0, 1, 0]
            left = [0, 0, 1]
        """

        moving_direction_clock_wise = [
            Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP
        ]
        index = moving_direction_clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_direction = moving_direction_clock_wise[index]
        elif np.array_equal(action, [0, 1, 0]):
            # Turn right clockwise:
            # right -> down -> left -> up
            new_index = (index + 1) % 4
            new_direction = moving_direction_clock_wise[new_index]
        else:  # [0, 0, 1]
            # Turn left clockwise:
            # left -> up -> down -> right
            new_index = (index - 1) % 4
            new_direction = moving_direction_clock_wise[new_index]

        self.direction = new_direction

        if self.direction == Direction.RIGHT:
            self.head = Point(self.head.x + BLOCK_SIZE, self.head.y)
        elif self.direction == Direction.LEFT:
            self.head = Point(self.head.x - BLOCK_SIZE, self.head.y)
        elif self.direction == Direction.DOWN:
            self.head = Point(self.head.x, self.head.y + BLOCK_SIZE)
        elif self.direction == Direction.UP:
            self.head = Point(self.head.x, self.head.y - BLOCK_SIZE)
        else:
            raise ValueError('Invalid direction.')

        self.head = Point(self.head.x, self.head.y)
