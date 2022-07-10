import torch
import random
import numpy as np

from matplotlib.pyplot import plot as plt
from collections import deque

from configurations import Direction, Point, BLOCK_SIZE
from snake_game_ai import SnakeGameAI
from model import Linear_QNetwork, QTrainer
from helper import visualization_plot


MAX_MEMORY = 100_000
BATCH_SIZE = 1_000
LEANING_RATING = .001

INPUT_SIZE = 11
HIDDEN_SIZE = 256
OUTPUT_SIZE = 3


class Agent:

    def __init__(self):

        # Randomly initialize the weights of the neural network.
        self.number_of_games = 0

        # Randomness.
        self.epsilon = 0

        # Discount rate.
        self.gamma = 0.999

        self.memory = deque(maxlen=MAX_MEMORY)

        #TODO: Implement the neural network (model and training).
        self.model = Linear_QNetwork(INPUT_SIZE, HIDDEN_SIZE, OUTPUT_SIZE)
        self.trainer = QTrainer(model=self.model, learning_rate=LEANING_RATING, gamma=self.gamma)

    def get_game_state(self, game):
        # Snake's head position.
        snake_head = game.snake[0]

        point_right = Point(snake_head.x + BLOCK_SIZE, snake_head.y)
        point_left = Point(snake_head.x - BLOCK_SIZE, snake_head.y)
        point_up = Point(snake_head.x, snake_head.y - BLOCK_SIZE)
        point_down = Point(snake_head.x, snake_head.y + BLOCK_SIZE)

        direction_right = game.direction == Direction.RIGHT
        direction_left = game.direction == Direction.LEFT
        direction_up = game.direction == Direction.UP
        direction_down = game.direction == Direction.DOWN

        state = [
            # Danger is in the straight.
            (direction_right and game.is_collision(point_right))
            or (direction_left and game.is_collision(point_left))
            or (direction_up and game.is_collision(point_up))
            or (direction_down and game.is_collision(point_down)),

            # Danger is in the right side.
            (direction_up and game.is_collision(point_right))
            or (direction_down and game.is_collision(point_left))
            or (direction_left and game.is_collision(point_up))
            or (direction_right and game.is_collision(point_down)),

            # Danger is in the left side.
            (direction_down and game.is_collision(point_right))
            or (direction_up and game.is_collision(point_left))
            or (direction_right and game.is_collision(point_up))
            or (direction_left and game.is_collision(point_down)),

            # Move snake in this direction.
            direction_right,
            direction_left,
            direction_up,
            direction_down,

            # Food locations:
            # Food is in the left side of the snake.
            game.food.x < game.head.x,
            # Food is in the right side of the snake.
            game.food.x > game.head.x,
            # Food is in the up side of the snake.
            game.food.y < game.head.y,
            # Food is in the down side of the snake.
            game.food.y > game.head.y
        ]

        return np.array(state, dtype=int)

    def remember_state(self, state, action, reward, next_state, done):
        # Auto popleft the oldest element if the memory is full (MAX_MEMORY).
        self.memory.append((state, action, reward, next_state, done))

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            minimal_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            minimal_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*minimal_sample)
        self.train_short_memory(states, actions, rewards, next_states, dones)

    def get_action(self, state):
        # In the binging of the game, the agent will do random moves.
        # Tradeoff: exploration vs. exploitation.

        # Randomly choose an action.
        self.epsilon = 80 - self.number_of_games
        final_move = [0, 0, 0]

        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            initial_state = torch.tensor(state, dtype=torch.float)
            prediction = self.model(initial_state)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move


def print_game_information(number_of_games, score, record_score):
    print(f'Number of games: {number_of_games}')
    print(f'Score: {score}')
    print(f'Record score: {record_score}')


def training():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record_score = 0

    agent = Agent()
    game = SnakeGameAI()

    # Main training loop.
    while True:
        # get the old state of the game.
        old_state = agent.get_game_state(game)

        # Get the final move action of the old state of the game.
        action = agent.get_action(old_state)

        # Perform the action and get the new state.
        reward, done, score = game.play_step(action)
        new_state = agent.get_game_state(game)

        # Train the agent with short memory.
        agent.train_short_memory(old_state, action, reward, new_state, done)

        # Remember the state and action.
        agent.remember_state(old_state, action, reward, new_state, done)

        # If game over.
        if done:
            # Train the agent with long memory.
            game.reset_state()
            agent.number_of_games += 1
            agent.train_long_memory()

            if score > record_score:
                record_score = score
                print("New record: ", record_score)

                agent.model.save_model()

            print_game_information(agent.number_of_games, score, record_score)
            plot_scores.append(score)
            total_score += score
            plot_mean_scores.append(np.mean(plot_scores))

            visualization_plot(plot_scores, plot_mean_scores)


if __name__ == '__main__':
    training()
