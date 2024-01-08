# Izveidoja: Emīlija Radzeviča_er22080 un Elīza Riekstiņa_er22060 
# Pabeigts: 08.01.2024.

# -*- coding: utf-8 -*-

# Import the necessary modules
import pygame
import sys
import random
import datetime

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 450
window_height = 600
window = pygame.display.set_mode(size = (window_width, window_height))
pygame.display.set_caption("Faux Lingo 2024")
results_width = 300
results_height = 460


# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (150, 245, 71)
YELLOW = (245, 237, 73)
PEACH = (254, 241, 207)

# Define game variables
with open('words.txt', 'r', encoding='utf-8') as f:
    word_list = [line.strip() for line in f]
with open('results.txt', 'r') as f:
    lines = f.readlines()
    if lines:
        highest_score = max(int(line.split()[-1]) for line in lines)
    else:
        highest_score = 0
current_win_streak = 0
correctly_guessed_word_count = 0
lives = 3
target_word = random.choice(word_list)
guess_word = [["_" for _ in target_word], [WHITE for _ in target_word]]
max_attempts = 5
attempts = 0
input_word = ""
guesses = []
message_lines = ""
print(guess_word)

# Define button dimensions and positions
button_width = 100
button_height = 30
play_again_button_position = (window_width // 2 - button_width // 2, window_height//2 - button_height//2)
restart_button_position = (window_width//2-button_width//2, 480)
close_button_position = (window_width // 2 - button_width // 2, window_height - button_height)
results_button_position = (window_width-120, window_height-45)
close_results_button_position = (365, 60)

# Create a font objects
font = pygame.font.SysFont('Arial', 16)
letter_font = pygame.font.SysFont('Arial', 20)
main_font = pygame.font.SysFont('Arial', 16)
results_font = pygame.font.SysFont('Arial', 12)


# Function to draw a button
def draw_button(text, position):
    # message_surface = font.render(message, True, BLACK)
    # message_rect = message_surface.get_rect(center=(position[0] + button_width // 2, position[1] - button_height // 2))
    # window.blit(message_surface, message_rect)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(position[0] + button_width // 2, position[1] + button_height // 2))
    window.blit(text_surface, text_rect)

# Function to draw the main information
def draw_main_info(text, value, lives, position_x):
    info_title = font.render(text, True, BLACK)
    info_title_rect = info_title.get_rect(center = (position_x, 30))
    window.blit(info_title, info_title_rect)

    if lives:
        draw_lives(value)
    else:
        info_value = font.render(str(value), True, BLACK)
        info_value_rect = info_value.get_rect(center = (position_x, 60))
        window.blit(info_value, info_value_rect)

# Function to show player's lives
def draw_lives(lives):
    heart_x = window_width/6*5 - 30
    for i in range(0, lives):
        life = pygame.image.load('img/heart_icon.png')
        life = pygame.transform.scale(life, (20, 20))
        life_rect = life.get_rect(center = (heart_x, 60))
        window.blit(life, life_rect)
        heart_x += 30

# Function to list all played words
def draw_played_words(played_word_list):
    played_word_x = 160
    if len(played_word_list) < 5:
        for i in range(0, len(played_word_list)):
            played_word = font.render(played_word_list[i] + " ", True, BLACK)
            window.blit(played_word, (played_word_x, 550))
            played_word_x += 50
    else:
        for i in range(len(played_word_list)-5, len(played_word_list)):
            played_word = font.render(played_word_list[i] + " ", True, BLACK)
            window.blit(played_word, (played_word_x, 550))
            played_word_x += 50 

# Function to draw results surface
def draw_results():
    results_title = font.render("Tavi labākie rezultāti", True, BLACK)
    results_title_rect = results_title.get_rect(center = (results_width/2, 30))
    results.blit(results_title, results_title_rect)

    pygame.draw.rect(results, BLACK, (65, 140, 50, 50))
    pygame.draw.rect(results, BLACK, (125, 100, 50, 90))
    pygame.draw.rect(results, BLACK, (185, 160, 50, 30))
    pygame.draw.line(results, BLACK, (20, 210), (280, 210))

    place = 0
    row_y = 230
    with open('results.txt', 'r') as f:
        lines = f.readlines()
        scores = [(line.split()[0:2], int(line.split()[-1])) for line in lines]
        scores.sort(key=lambda x: x[1], reverse=True)
        top_scores = scores[:9]
    
    for place, (date_time, score) in enumerate(top_scores):
        if place < 3:
            top3_score = font.render(str(score), True, BLACK)
            if place == 0:
                top3_score_rect = top3_score.get_rect(center = (150, 90))
                first_date_time = ' '.join(date_time)
            elif place == 1:
                top3_score_rect = top3_score.get_rect(center = (90, 130))
                second_date_time = ' '.join(date_time)
            elif place == 2:
                top3_score_rect = top3_score.get_rect(center = (210, 150))
                third_date_time = ' '.join(date_time)
            results.blit(top3_score, top3_score_rect)
        else:
            score_text = f"{place+1}.    {' '.join(date_time)}     {score}"
            score_text = font.render(score_text, True, BLACK)
            # score_text_width = score_text.get_rect().width
            results.blit(score_text, (40, row_y))
            row_y += 30
        place += 1
    return first_date_time, second_date_time, third_date_time

# Function to show top 3 score dates
def draw_top_score_date(date_time, date_time_x):
    date_time = font.render(str(date_time), True, BLACK)
    date_time_rect = date_time.get_rect(center = (date_time_x, 200))
    results.blit(date_time, date_time_rect)   

# Game loop
running = True
game_over = False
result_written = False
show_results = False
top_scores = []
played_word_list = []
while running:
    # Handle events
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if restart_button_position[0] <= mouse_pos[0] <= restart_button_position[0] + button_width and restart_button_position[1] <= mouse_pos[1] <= restart_button_position[1] + button_height and lives <= 0:
                # Reset game variables for new game
                lives = 3
                current_win_streak = 0
                target_word = random.choice(word_list)
                guess_word = [["_" for _ in target_word], [WHITE for _ in target_word]]
                attempts = 0
                input_word = ""
                guesses = []
                game_over = False
                result_written = False
                message_lines = []
                show_results = False
            if results_button_position[0] <= mouse_pos[0] <= results_button_position[0] + 120 and results_button_position[1] <= mouse_pos[1] <= results_button_position[1] + 45:
                show_results = True
            elif close_results_button_position[0] < mouse_pos[0] <= close_results_button_position[0] + 20 and close_results_button_position[1] <= mouse_pos[1] <= close_results_button_position[1] + 20:
                show_results = False
                if lives == 0:
                    # Reset game variables for new game
                    lives = 3
                    current_win_streak = 0
                    target_word = random.choice(word_list)
                    guess_word = [["_" for _ in target_word], [WHITE for _ in target_word]]
                    attempts = 0
                    input_word = ""
                    guesses = []
                    game_over = False
                    result_written = False
                    message_lines = []
                    show_results = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and game_over and lives > 0:
                # Reset game variables for next round
                target_word = random.choice(word_list)
                # guess_word = [["_" for _ in target_word], [WHITE for _ in target_word]]
                attempts = 0
                input_word = ""
                guesses = []
                game_over = False
                message_lines = []
            elif event.key == pygame.K_BACKSPACE and not game_over:
                if len(input_word)>0:
                    input_word = input_word.rstrip(input_word[-1])
        elif event.type == pygame.KEYUP and not game_over:
            letter = event.unicode
            if letter.isalpha():
                input_word += letter.upper()
                if len(input_word) == 5:
                    guesses.append([input_word, []])
                    for i, l in enumerate(input_word):
                        if l == target_word[i].upper():
                            guess_word[0][i] = l
                            guess_word[1][i] = GREEN
                            guesses[-1][1].append(GREEN)
                        elif l in target_word.upper():
                            guesses[-1][1].append(YELLOW)
                        else:
                            guesses[-1][1].append(BLACK)
                    input_word = ""
                    attempts += 1

    # Update game logic
    if not game_over:
        if guess_word[0] == list(target_word.upper()):
            # message = "Tu uzminēji vārdu"
            game_over = True
            current_win_streak += 1
            played_word_list.append(target_word)
            correctly_guessed_word_count += 1
        elif attempts >= max_attempts:
            # message_lines = [f"Tu neuzminēji vārdu!", f"Pareizais vārds bija: {target_word}"]
            game_over = True
            lives -= 1
            played_word_list.append(target_word)
            current_win_streak = 0       

    # Render graphics
    window.fill(PEACH)
    print(target_word)
    
    draw_main_info("Atlikušie gājieni", max_attempts-attempts, False, window_width/6)
    draw_main_info("Uzvaras pēc kārtas", current_win_streak, False, window_width/2)
    draw_main_info("Dzīvības", lives, True, window_width/6*5)

    # draw gameboard
    grid = pygame.image.load('img/grid.png')
    grid = pygame.transform.scale(grid, (350, 418))
    grid_rect = grid.get_rect(center = (window_width/2, window_height/2))
    window.blit(grid, grid_rect)

    correctly_guessed_words = font.render(f"Uzminētie vārdi: {correctly_guessed_word_count}", True, BLACK)
    window.blit(correctly_guessed_words, (40, 530))
    played_words = font.render("Izspēlētie vārdi: ", True, BLACK)
    window.blit(played_words, (40, 550))

    draw_played_words(played_word_list)

    results_text = font.render("Rezultāti", True, BLACK)
    results_text_rect = results_text.get_rect(center = (window_width-50, window_height-20))
    window.blit(results_text, results_text_rect)
    
    # Draw the current input
    letter_count = 0
    for i in input_word:
        input_word_surface = font.render(i, True, BLACK)
        window.blit(input_word_surface, (84 + letter_count * 68, 465))
        letter_count += 1

    # draw previous inputs
    for i, guess in enumerate(guesses):
        for j, l in enumerate(guess[0]):
            guess_surface = font.render(l, True, guess[1][j])
            window.blit(guess_surface, (84 + j * 68, 113 + i * 70))
    
    # Draw results 
    if show_results == True:
        results = pygame.Surface((results_width, results_height), pygame.SRCALPHA)
        results.fill((255, 255, 255, 230))
        first_date_time, second_date_time, third_date_time = draw_results()
        if 140 <= mouse_pos[0] <= 190 and 190 <= mouse_pos[1] <= 260:
            pygame.draw.rect(results, PEACH, (65, 140, 50, 50))
            draw_top_score_date(second_date_time, 90)
        elif 200 <= mouse_pos[0] <= 250 and 150 <= mouse_pos[1] <= 260:
            pygame.draw.rect(results, PEACH, (125, 100, 50, 90))
            draw_top_score_date(first_date_time, 150)
        elif 260 <= mouse_pos[0] <= 310 and 210 <= mouse_pos[1] <= 260:
            pygame.draw.rect(results, PEACH, (185, 160, 50, 30))
            draw_top_score_date(third_date_time, 210)

        window.blit(results, (75, 70))
        close_results_button = pygame.draw.circle(window, GREEN, (375, 70), 20)
        close_results = font.render("X", True, BLACK)
        close_results_rect = close_results.get_rect(center = (375, 70))
        window.blit(close_results, close_results_rect)

    # Draw the message and the buttons when the game is over
    if game_over:
        game_over = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
        message_y = 150 + len(guesses) * 25
        if message_y + 40 > play_again_button_position[1]: 
            message_y = play_again_button_position[1] - 40
        for i, line in enumerate(message_lines):
            message_surface = font.render(line, True, BLACK)
            game_over.blit(message_surface, (20, message_y + i * 20))
        if lives > 0:
            game_over.fill((255, 255, 255, 230))
            window.blit(game_over, (0, 0))
            draw_button("Nospied ENTER, lai turpinātu", play_again_button_position)
        else:
            if not result_written:
                now = datetime.datetime.now()
                date_time = now.strftime("%Y-%m-%d %H:%M:%S")
                result = f"{date_time} {correctly_guessed_word_count}\n"
                with open("results.txt", "a") as f:
                    f.write(result)
                result_written = True
            show_results = True
            pygame.draw.rect(window, GREEN, (restart_button_position[0], restart_button_position[1], button_width, button_height))     
            draw_button("Jauna spēle", restart_button_position)

    pygame.display.update()

# Clean up
pygame.quit()
sys.exit()