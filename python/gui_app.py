import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple 2D Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Player settings
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
PLAYER_SPEED = 5

# Obstacle settings
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 50, 50
OBSTACLE_SPEED = 7
OBSTACLE_GAP = 200

# Load sound effects
pygame.mixer.init()
# move_sound = pygame.mixer.Sound("mixkit-arcade-game-opener-222.wav")
# collision_sound = pygame.mixer.Sound("mixkit-arcade-game-opener-222.wav")

# Initialize player
player = pygame.Rect(WIDTH // 2 - PLAYER_WIDTH // 2, HEIGHT // 2 - PLAYER_HEIGHT // 2, PLAYER_WIDTH, PLAYER_HEIGHT)

# List to store obstacles
obstacles = []

# Clock
clock = pygame.time.Clock()

# Score
score = 0

def draw_objects():
    WINDOW.fill(BLACK)
    pygame.draw.rect(WINDOW, WHITE, player)
    for obstacle in obstacles:
        pygame.draw.rect(WINDOW, RED, obstacle)

def move_obstacles():
    for obstacle in obstacles:
        obstacle.x -= OBSTACLE_SPEED
        if obstacle.right < 0:
            obstacles.remove(obstacle)

def generate_obstacles():
    if len(obstacles) == 0 or obstacles[-1].right < WIDTH - OBSTACLE_GAP:
        obstacle_height = random.randint(100, 400)
        obstacle_top = pygame.Rect(WIDTH, 0, OBSTACLE_WIDTH, obstacle_height)
        obstacle_bottom = pygame.Rect(WIDTH, obstacle_height + OBSTACLE_GAP, OBSTACLE_WIDTH, HEIGHT - obstacle_height - OBSTACLE_GAP)
        obstacles.extend([obstacle_top, obstacle_bottom])

def check_collision():
    for obstacle in obstacles:
        if player.colliderect(obstacle):
            return True
    return False

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player.top > 0:
        player.y -= PLAYER_SPEED
        # move_sound.play()  # Play move sound
    if keys[pygame.K_DOWN] and player.bottom < HEIGHT:
        player.y += PLAYER_SPEED
        # move_sound.play()  # Play move sound

    # Move and generate obstacles
    move_obstacles()
    generate_obstacles()

    # Check collision
    if check_collision():
        print("Game Over!")
        # collision_sound.play()  # Play collision sound
        running = False

    # Increase score
    score += 1

    # Draw objects
    draw_objects()

    # Display score
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    WINDOW.blit(score_text, (10, 10))

    # Update display
    pygame.display.update()

    # Tick clock
    clock.tick(30)

# Quit Pygame
pygame.quit()
sys.exit()
