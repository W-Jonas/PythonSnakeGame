import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
width, height = 640, 480
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Define colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Define the snake class
class Snake:
    def __init__(self):
        self.size = 1
        self.positions = [(width // 2, height // 2)]
        self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
    
    def move(self):
        x, y = self.positions[0]
        if self.direction == "UP":
            y -= 10
        elif self.direction == "DOWN":
            y += 10
        elif self.direction == "LEFT":
            x -= 10
        elif self.direction == "RIGHT":
            x += 10
        self.positions.insert(0, (x, y))
        if len(self.positions) > self.size:
            self.positions.pop()
    
    def change_direction(self, direction):
        if direction == "UP" and self.direction != "DOWN":
            self.direction = "UP"
        elif direction == "DOWN" and self.direction != "UP":
            self.direction = "DOWN"
        elif direction == "LEFT" and self.direction != "RIGHT":
            self.direction = "LEFT"
        elif direction == "RIGHT" and self.direction != "LEFT":
            self.direction = "RIGHT"
    
    def draw(self):
        for position in self.positions:
            pygame.draw.rect(window, GREEN, (position[0], position[1], 10, 10))

# Define the food class
class Food:
    def __init__(self):
        self.position = None
    
    def spawn(self, snake_positions):
        valid_positions = []
        for x in range(0, width, 10):
            for y in range(0, height, 10):
                if (x, y) not in snake_positions:
                    valid_positions.append((x, y))
        self.position = random.choice(valid_positions)
    
    def draw(self):
        pygame.draw.rect(window, RED, (self.position[0], self.position[1], 10, 10))

# Create instances of the snake and food
snake = Snake()
food = Food()
food.spawn(snake.positions)

# Load highscore from file
highscore = 0
try:
    with open("score.txt", "r") as file:
        highscore = int(file.read())
except FileNotFoundError:
    pass

# Set up the score label
score = 0
score_font = pygame.font.Font(None, 36)

# Set up the highscore label
highscore_label = None
if highscore > 0:
    highscore_label = score_font.render(f"Highscore: {highscore}", True, WHITE)
    highscore_rect = highscore_label.get_rect()
    highscore_rect.topleft = (10, 50)

# Game loop
running = True
clock = pygame.time.Clock()
while running:
    clock.tick(20)  # Set the frame rate
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction("UP")
            elif event.key == pygame.K_DOWN:
                snake.change_direction("DOWN")
            elif event.key == pygame.K_LEFT:
                snake.change_direction("LEFT")
            elif event.key == pygame.K_RIGHT:
                snake.change_direction("RIGHT")
    
    # Move the snake
    snake.move()
    
    # Check for collision with food
    if (food.position[0] <= snake.positions[0][0] < food.position[0] + 10) and (food.position[1] <= snake.positions[0][1] < food.position[1] + 10):
        snake.size += 1
        score += 10
        food.spawn(snake.positions)
    
    # Check for collision with walls
    if snake.positions[0][0] < 0 or snake.positions[0][0] > width or snake.positions[0][1] < 0 or snake.positions[0][1] > height:
        snake = Snake()
        score = 0  # Reset the score to 0
        if score > highscore:
            highscore = score

    # Check for collision with self
    for position in snake.positions[1:]:
        if snake.positions[0] == position:
            snake = Snake()
            score = 0  # Reset the score to 0
            if score > highscore:
                highscore = score
    
    # Update the highscore label if necessary
    if highscore_label is not None and score > highscore:
        highscore = score
        highscore_label = score_font.render(f"Highscore: {highscore}", True, WHITE)
    
    # Clear the window
    window.fill(BLACK)
    
    # Draw the snake and food
    snake.draw()
    food.draw()
    
    # Update the display
    pygame.display.update()
    
    # Update the window name with score and highscore
    pygame.display.set_caption(f"Snake Game | Score: {score} | Highscore: {highscore}")

# Save the highscore to file
with open("score.txt", "w") as file:
    file.write(str(highscore))

# Quit the game
pygame.quit()