import numpy as np
import random
import pygame

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 600
BLOCK_SIZE = 20
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set up the display
win = pygame.display.set_mode((WIDTH, HEIGHT))

class SnakeGame:
    def __init__(self):
        self.snake = [(200, 200), (220, 200), (240, 200)]
        self.direction = 'RIGHT'
        self.apple = self.generate_apple()

    def generate_apple(self):
        while True:
            x = random.randint(0, WIDTH - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE
            y = random.randint(0, HEIGHT - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE
            if (x, y) not in self.snake:
                return (x, y)

    def step(self, action):
        reward = 0
        done = False

        # Move the snake
        head = self.snake[-1]
        if action == 0:  # UP
            new_head = (head[0], head[1] - BLOCK_SIZE)
        elif action == 1:  # DOWN
            new_head = (head[0], head[1] + BLOCK_SIZE)
        elif action == 2:  # LEFT
            new_head = (head[0] - BLOCK_SIZE, head[1])
        elif action == 3:  # RIGHT
            new_head = (head[0] + BLOCK_SIZE, head[1])

        # Check for collision with the wall or itself
        if (new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT or
            new_head in self.snake[:-1]):
            done = True
        else:
            self.snake.append(new_head)

            # Check if the snake ate the apple
            if self.snake[-1] == self.apple:
                reward = 1
                self.apple = self.generate_apple()
            else:
                self.snake.pop(0)

        return np.array([self.snake[-1][0] / WIDTH, self.snake[-1][1] / HEIGHT, self.apple[0] / WIDTH, self.apple[1] / HEIGHT]), reward, done, {}

    def reset(self):
        self.snake = [(200, 200), (220, 200), (240, 200)]
        self.direction = 'RIGHT'
        self.apple = self.generate_apple()
        return np.array([self.snake[-1][0] / WIDTH, self.snake[-1][1] / HEIGHT, self.apple[0] / WIDTH, self.apple[1] / HEIGHT])

    def render(self):
        win.fill((0, 0, 0))
        for pos in self.snake:
            pygame.draw.rect(win, GREEN, (pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(win, RED, (self.apple[0], self.apple[1], BLOCK_SIZE, BLOCK_SIZE))
        pygame.display.update()

# Create the Snake game environment
env = SnakeGame()

# Train the model
for episode in range(1000):
    state = env.reset()
    done = False
    rewards = 0
    while not done:
        action = np.random.randint(0, 4)
        next_state, reward, done, _ = env.step(action)
        env.render()
        print(f"Episode {episode}, Reward: {reward}, Done: {done}")
        rewards += reward
    print(f"Episode {episode}, Total Reward: {rewards}")