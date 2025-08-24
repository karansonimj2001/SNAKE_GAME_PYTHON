import pygame
import random
import os

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (0, 245, 0)

pygame.init()
screen_width = 500
screen_height = 600

# Create game window
gamewindow = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")
pygame.display.update()

# Game clock & fonts
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 50)

# Utility function to display text
def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gamewindow.blit(screen_text, [x, y])

# Plot snake on screen
def plot_snake(gamewindow, color, snake_list, snake_size):
    for x, y in snake_list:
        pygame.draw.rect(gamewindow, color, [x, y, snake_size, snake_size])

# Welcome screen
def welcome():
    exit_game = False
    while not exit_game:
        gamewindow.fill((233, 220, 29))
        text_screen("Welcome to Snake Game", black, 40, 250)
        text_screen("Press SPACE to Play", black, 85, 300)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gameloop()

        pygame.display.update()
        clock.tick(60)

# Main game loop
def gameloop():
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0

    food_x = random.randint(20, screen_width // 2)
    food_y = random.randint(20, screen_height // 2)

    score = 0
    init_velocity = 5
    snake_size = 20
    fps = 30

    snake_list = []
    snake_length = 1

    # Ensure hiscore file exists
    if not os.path.exists("hiscore.txt"):
        with open("hiscore.txt", "w") as f:
            f.write("0")

    with open("hiscore.txt", "r") as f:
        hiscore = f.read()

    while not exit_game:
        if game_over:
            with open("hiscore.txt", "w") as f:
                f.write(str(hiscore))

            gamewindow.fill((0, 0, 200))
            pygame.draw.rect(gamewindow, white, [45, 200, 400, 100])
            text_screen("Game Over!", red, 150, 200)
            text_screen("Press ENTER to Restart", red, 50, 260)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    elif event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    elif event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0
                    elif event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0
                    elif event.key == pygame.K_q:  # Cheat key
                        score += 5

            snake_x += velocity_x
            snake_y += velocity_y

            # Eating food
            if abs(snake_x - food_x) < 15 and abs(snake_y - food_y) < 15:
                score += 10
                food_x = random.randint(20, screen_width // 2)
                food_y = random.randint(20, screen_height // 2)
                snake_length += 5
                if score > int(hiscore):
                    hiscore = score

            gamewindow.fill(green)
            text_screen("Score: " + str(score), red, 5, 5)
            text_screen("High Score: " + str(hiscore), red, 5, 35)

            pygame.draw.rect(gamewindow, red, [food_x, food_y, snake_size, snake_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            if len(snake_list) > snake_length:
                del snake_list[0]

            # Game over conditions
            if head in snake_list[:-1]:
                game_over = True
            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True

            # Footer instructions
            text_screen("Snake Game", black, 165, 5)
            font2 = pygame.font.SysFont(None, 25)
            gamewindow.blit(font2.render("Made by Karan Soni", True, black), [10, 575])
            gamewindow.blit(font2.render("Use Arrow Keys to Play", True, black), [300, 575])

            plot_snake(gamewindow, black, snake_list, snake_size)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

welcome()
