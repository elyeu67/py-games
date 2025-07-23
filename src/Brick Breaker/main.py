import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Window configuration
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Basic Pygame Brick Breaker")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
GRAY = (100, 100, 100)
# List of possible brick colors
BRICK_COLORS = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0),  # Yellow
]

# Fonts
font = pygame.font.SysFont(None, 60)
small_font = pygame.font.SysFont(None, 40)

def draw_button(rect, text):
    pygame.draw.rect(screen, GRAY, rect)
    pygame.draw.rect(screen, WHITE, rect, 3)
    label = small_font.render(text, True, WHITE)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)

def main_menu():
    while True:
        screen.fill(BLACK)
        title = font.render("Brick Breaker", True, WHITE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 120))
        play_button = pygame.Rect(WIDTH//2 - 100, 250, 200, 60)
        quit_button = pygame.Rect(WIDTH//2 - 100, 350, 200, 60)
        draw_button(play_button, "Play")
        draw_button(quit_button, "Quit")
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_button.collidepoint(event.pos):
                    return  # Start the game
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

def countdown():
    """Display a 3-second countdown before the game starts, with the ball above the paddle."""
    global ball_x, ball_y
    for i in range(3, 0, -1):
        screen.fill(BLACK)
        # Position the ball just above the paddle
        ball_x = player_pos[0] + player_size // 2
        ball_y = player_pos[1] - ball_radius - 1
        pygame.draw.rect(screen, RED, (player_pos[0], player_pos[1], player_size, 20))
        pygame.draw.circle(screen, CYAN, (int(ball_x), int(ball_y)), ball_radius)
        label = font.render(str(i), True, WHITE)
        screen.blit(label, (WIDTH//2 - label.get_width()//2, HEIGHT//2 - label.get_height()//2))
        pygame.display.flip()
        pygame.time.delay(1000)

def make_bricks():
    """Create all bricks with random colors from the color list."""
    bricks = []
    for i in range(12):
        for k in range(4):
            color = random.choice(BRICK_COLORS)
            rect = pygame.Rect(50 + i*60, 100, brique_length, brique_height)
            bricks.append((rect, color))
            color2 = random.choice(BRICK_COLORS)
            rect2 = pygame.Rect(50 + i*60, 100 + k*50, brique_length, brique_height)
            bricks.append((rect2, color2))
    return bricks

# Player paddle properties
player_pos = [400, 550]
player_size = 50
player_speed = 10
player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, 20)

# Brick properties
brique_length = 50
brique_height = 30
bricks = make_bricks()

# Ball properties
ball_radius = 10
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_speed_x = 5
ball_speed_y = 5

# Clock for FPS control
clock = pygame.time.Clock()

# --- MENU ---
main_menu()

# --- COUNTDOWN ---
countdown()

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Keyboard input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT]:
        player_pos[0] += player_speed
    # Update paddle rect position
    player_rect.x = player_pos[0]
    player_rect.y = player_pos[1]
    # Update ball position
    ball_x += ball_speed_x
    ball_y += ball_speed_y
    # Ball collision with screen borders
    if ball_x - ball_radius <= 0 or ball_x + ball_radius >= WIDTH:
        ball_speed_x = -ball_speed_x  # Reverse horizontal direction
    if ball_y - ball_radius <= 0:
        ball_speed_y = -ball_speed_y  # Reverse vertical direction (top)
    # Ball falls below the paddle (lose condition)
    if ball_y + ball_radius > HEIGHT:
        screen.fill(BLACK)
        label = font.render("YOU LOST", True, RED)
        screen.blit(label, (WIDTH//2 - label.get_width()//2, HEIGHT//2 - label.get_height()//2))
        pygame.display.flip()
        pygame.time.delay(2000)
        running = False
        continue
    # Ball collision with paddle
    if player_rect.collidepoint(ball_x, ball_y):
        center = player_pos[0] + player_size // 2
        offset = (ball_x - center) / (player_size // 2)  # -1 (left) to 1 (right)
        ball_speed_x = offset * 7  # 7 = max horizontal speed
        ball_speed_y = -abs(ball_speed_y)  # Always bounce upward
    # Ball collision with bricks
    for brick in bricks[:]:  # Iterate over a copy of the list
        rect, color = brick
        if rect.collidepoint(ball_x, ball_y):
            bricks.remove(brick)
            ball_speed_x = -ball_speed_x
            ball_speed_y = -ball_speed_y
    # Drawing
    screen.fill(BLACK)
    # Draw paddle
    pygame.draw.rect(screen, RED, (player_pos[0], player_pos[1], player_size, 20))
    # Draw bricks
    for rect, color in bricks:
        pygame.draw.rect(screen, color, rect)
    # Draw ball
    pygame.draw.circle(screen, CYAN, (int(ball_x), int(ball_y)), ball_radius)
    # Update display
    pygame.display.flip()
    # FPS control
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()