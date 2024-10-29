import pygame, sys
import os
import random

player_lives = 3
score = 0
fruits = ['barata','barataa','barataaa','barataaaa','barataaaaa', 'bomb']

# initialize pygame and create window

WIDTH = 1000
HEIGHT = 500
FPS = 12

pygame.init()
pygame.display.set_caption('Roach Hunter')
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Define colors

WHITE = (255,255,255) 
BLACK = (0,0,0) 
RED = (255,0,0) 
GREEN = (0,255,0) 
BLUE = (0,0,255)

background = pygame.image.load('./img/bgk.png')                                  # game background
font = pygame.font.Font(os.path.join(os.getcwd(), './fonts/DMSerifText-Regular.ttf'), 42)  # Font PDBI for scores
score_text = font.render('Score : ' + str(score), True, WHITE)                # score display
lives_icon = pygame.image.load('./img/w_h.png')                               # images that show remaining lives

# Generalized structure of the fruit Dictionary
def generate_random_fruits(fruit):
    fruit_path = "img/" + fruit + ".png"
    data[fruit] = {
        'img': pygame.image.load(fruit_path),
        'x' : random.randint(100,500),
        'y' : 800,
        'speed_x': random.randint(-10,10),
        'speed_y': random.randint(-80, -60),
        'throw': False,
        't': 0,
        'hit': False,
    }

    if random.random() >= 0.75:
        data[fruit]['throw'] = True
    else:
        data[fruit]['throw'] = False

# Dictionary to hold the data for random fruit generation
data = {}
for fruit in fruits:
    generate_random_fruits(fruit)

def hide_cross_lives(x, y):
    gameDisplay.blit(pygame.image.load("./img/r_h.png"), (x, y))

# Generic method to draw fonts on the screen
def draw_text(display, text, size, x, y):
    font = pygame.font.Font(os.path.join(os.getcwd(), './fonts/DMSerifText-Regular.ttf'), size)  # Font PDBI
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    display.blit(text_surface, text_rect)

# Draw player's lives
def draw_lives(display, x, y, lives, image):
    for i in range(lives):
        img = pygame.image.load(image)
        img_rect = img.get_rect()
        img_rect.x = int(x + 35 * i)
        img_rect.y = y
        display.blit(img, img_rect)

# Show game over display & front display
def show_gameover_screen():
    gameDisplay.blit(background, (0, 0))
    draw_text(gameDisplay, "Roach Hunter", 95, WIDTH / 2, HEIGHT / 4)
    if not game_over:
        draw_text(gameDisplay, "Score : " + str(score), 50, WIDTH / 2, HEIGHT / 2)

    draw_text(gameDisplay, "Aperte qualquer tecla para iniciar!", 23, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

# Game Loop
first_round = True
game_over = True
game_running = True
paused = False  # Variable to track if the game is paused

while game_running:
    if game_over:
        if first_round:
            show_gameover_screen()
            first_round = False
        game_over = False
        player_lives = 3
        draw_lives(gameDisplay, 690, 5, player_lives, './img/r_h.png')
        score = 0

    for event in pygame.event.get():
        # Checking for closing window
        if event.type == pygame.QUIT:
            game_running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # Toggle pause
                paused = not paused

    if paused:
        # Show pause message
        draw_text(gameDisplay, "PAUSE", 80, WIDTH / 2, HEIGHT / 4)
        draw_text(gameDisplay, "Aperte a 'P' para continuar", 30, WIDTH / 2, HEIGHT / 2)
        pygame.display.update()
        continue  # Skip game logic while paused

    gameDisplay.blit(background, (0, 0))
    gameDisplay.blit(score_text, (0, 0))
    draw_lives(gameDisplay, 690, 5, player_lives, './img/r_h.png')

    for key, value in data.items():
        if value['throw']:
            value['x'] += value['speed_x']
            value['y'] += value['speed_y']
            value['speed_y'] += (1 * value['t'])
            value['t'] += 1

            if value['y'] <= 800:
                gameDisplay.blit(value['img'], (value['x'], value['y']))
            else:
                generate_random_fruits(key)

            current_position = pygame.mouse.get_pos()

            if not value['hit'] and current_position[0] > value['x'] and current_position[0] < value['x'] + 60 \
                    and current_position[1] > value['y'] and current_position[1] < value['y'] + 60:
                if key == 'bomb':
                    player_lives -= 1
                    if player_lives == 0:
                        hide_cross_lives(690, 15)
                    elif player_lives == 1:
                        hide_cross_lives(725, 15)
                    elif player_lives == 2:
                        hide_cross_lives(760, 15)

                    if player_lives < 0:
                        show_gameover_screen()
                        game_over = True

                    half_fruit_path = "./img/ex.png"
                else:
                    half_fruit_path = "img/" + "h_" + key + ".png"

                value['img'] = pygame.image.load(half_fruit_path)
                value['speed_x'] += 10
                if key != 'bomb':
                    score += 1
                score_text = font.render('Score : ' + str(score), True, WHITE)  # Update score display using PDBI font
                value['hit'] = True
        else:
            generate_random_fruits(key)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()