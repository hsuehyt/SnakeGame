import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants for the game
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 24)

# Snake and food data structures
snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
snake_direction = (0, 0)  # Initial direction set to 0,0 until an arrow key is pressed
food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
score = 0

def draw_text(text, color, position):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

def start_screen():
    start_message = "Press Arrow Key to Start"
    draw_text(start_message, WHITE, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 20))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    return  # Start the game when any arrow key is pressed
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def handle_keys():
    global snake_direction
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and snake_direction != (0, 1):
        snake_direction = (0, -1)
    elif keys[pygame.K_DOWN] and snake_direction != (0, -1):
        snake_direction = (0, 1)
    elif keys[pygame.K_LEFT] and snake_direction != (1, 0):
        snake_direction = (-1, 0)
    elif keys[pygame.K_RIGHT] and snake_direction != (-1, 0):
        snake_direction = (1, 0)

def move_snake():
    global snake, snake_direction, food, score
    if snake_direction == (0, 0):
        return True  # Keep the game state running but do not move the snake until direction is set
    head_x, head_y = snake[0]
    new_head = (head_x + snake_direction[0], head_y + snake_direction[1])

    if new_head in snake or new_head[0] < 0 or new_head[0] >= GRID_WIDTH or new_head[1] < 0 or new_head[1] >= GRID_HEIGHT:
        return False  # Return False to indicate game over
    snake.insert(0, new_head)
    if new_head == food:
        score += 1
        food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    else:
        snake.pop()
    return True

def game_over():
    draw_text('You Lost! Press Q to quit, C to play again', WHITE, (50, 50))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_c:
                    reset_game()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def reset_game():
    global snake, snake_direction, food, score
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    snake_direction = (0, 0)  # Wait for arrow key press to start moving
    food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    score = 0
    run_game()

def run_game():
    start_screen()  # Show the start screen before the game loop starts
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        handle_keys()
        running = move_snake()

        screen.fill(BLACK)
        for segment in snake:
            pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, RED, (food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        draw_text(f'Score: {score}', WHITE, (5, 5))

        pygame.display.flip()
        clock.tick(10)

        if not running:
            game_over()
            return

run_game()
