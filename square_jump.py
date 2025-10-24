import pygame
import sys
import threading
from finger_tap import is_tapping, set_tap_signal, get_tap_signal

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jumping Square")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)

# Square setup
square_size = 50
x = WIDTH // 2 - square_size // 2
y = HEIGHT - square_size
velocity_y = 0
gravity = 0.8
jump_strength = -15
is_jumping = False

# is_tap = False

thread = threading.Thread(target=is_tapping, daemon=True)
thread.start()

clock = pygame.time.Clock()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # print(is_tap)
    # Jump when user taps
    if get_tap_signal() and not is_jumping:
        velocity_y = jump_strength
        is_jumping = True
        set_tap_signal(False)

    # Apply gravity
    velocity_y += gravity
    y += velocity_y

    # Stop square when it hits the ground
    if y >= HEIGHT - square_size:
        y = HEIGHT - square_size
        velocity_y = 0
        is_jumping = False

    # Draw
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, (x, y, square_size, square_size))

    pygame.display.flip()
    clock.tick(60)

