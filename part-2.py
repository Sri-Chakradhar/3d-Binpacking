import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 1920
screen_height = 1080

# Number of rows and columns in the matrix
num_rows = 120
num_cols = 80

# Spacing between numbers
spacing_x = screen_width // num_cols + 6
spacing_y = screen_height // num_rows

# Colors
black = (0, 0, 0)
green = (0, 255, 0)

# Create the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Matrix Numbers")

# Load font
font = pygame.font.Font(None, 20)

running = True
numbers = []

for row in range(num_rows):
    for col in range(num_cols):
        number = random.randint(0, 9)
        x = col * spacing_x
        y = row * spacing_y
        speed = random.randint(3, 40)  # Speed of movement
        opacity = 255  # Initial opacity
        numbers.append({'number': str(number), 'x': x, 'y': y, 'speed': speed, 'opacity': opacity})

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(black)

    for num in numbers:
        num_text = font.render(num['number'], True, (green[0], green[1], green[2], num['opacity']))
        screen.blit(num_text, (num['x'], num['y']))

        # Move the number in a straight line
        num['y'] += num['speed']

        # Reduce opacity gradually over time
        num['opacity'] -= 1  # Adjust this value for desired opacity decrease rate
        if num['opacity'] <= 0:
            num['opacity'] = 252  # Reset opacity when it reaches 0

        # Wrap the number to the top of the screen when it reaches the bottom
        if num['y'] > screen_height:
            num['y'] = 0

    pygame.display.flip()

    # Apply a translucent black rectangle over the screen to create a blur effect
    translucent_black = pygame.Surface((screen_width, screen_height))
    translucent_black.fill((0, 0, 0, 5))  # Adjust alpha value for desired blur intensity
    screen.blit(translucent_black, (0, 0))

    # Delay for a short time
    pygame.time.delay(50)

pygame.quit()
