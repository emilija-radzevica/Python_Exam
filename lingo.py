# -*- coding: utf-8 -*-

# Import the necessary modules
import pygame
import sys
import random
import datetime

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Lingo")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Define game variables
with open('words.txt', 'r', encoding='utf-8') as f:
    word_list = [line.strip() for line in f]
best_win_streak = 0
current_win_streak = 0
lives = 3
target_word = random.choice(word_list)
guess_word = [["_" for _ in target_word], [WHITE for _ in target_word]]
max_attempts = 5
attempts = 0
input_word = ""
guesses = []
message_lines = ""

# Define button dimensions and positions
button_width = 200
button_height = 50
play_again_button_position = (window_width // 2 - button_width // 2, window_height - 2.5 * button_height)
restart_button_position = (window_width // 2 - button_width // 2, window_height - 2.5 * button_height)
close_button_position = (window_width // 2 - button_width // 2, window_height - button_height)

# Create a font object
font = pygame.font.Font('arial.ttf', 16)

# Function to draw a button
def draw_button(text, position):
    pygame.draw.rect(window, WHITE, (*position, button_width, button_height))
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(position[0] + button_width // 2, position[1] + button_height // 2))
    window.blit(text_surface, text_rect)

# Game loop
running = True
game_over = False
result_written = False
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if play_again_button_position[0] <= mouse_pos[0] <= play_again_button_position[0] + button_width and play_again_button_position[1] <= mouse_pos[1] <= play_again_button_position[1] + button_height and lives > 0:
                # Reset game variables for next round
                target_word = random.choice(word_list)
                guess_word = [["_" for _ in target_word], [WHITE for _ in target_word]]
                attempts = 0
                input_word = ""
                guesses = []
                game_over = False
                message_lines = []
            elif restart_button_position[0] <= mouse_pos[0] <= restart_button_position[0] + button_width and restart_button_position[1] <= mouse_pos[1] <= restart_button_position[1] + button_height and lives <= 0:
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
            elif close_button_position[0] <= mouse_pos[0] <= close_button_position[0] + button_width and close_button_position[1] <= mouse_pos[1] <= close_button_position[1] + button_height:
                running = False
        elif event.type == pygame.KEYUP and not game_over:
            letter = event.unicode
            if letter.isalpha():
                input_word += letter.lower()
                if len(input_word) == 5:
                    guesses.append([input_word, []])
                    for i, l in enumerate(input_word):
                        if l == target_word[i]:
                            guess_word[0][i] = l
                            guess_word[1][i] = GREEN
                            guesses[-1][1].append(GREEN)
                        elif l in target_word:
                            guesses[-1][1].append(YELLOW)
                        else:
                            guesses[-1][1].append(WHITE)
                    input_word = ""
                    attempts += 1

    # Update game logic
    if not game_over:
        if guess_word[0] == list(target_word):
            message = "You won!"
            game_over = True
            current_win_streak += 1
            if current_win_streak > best_win_streak:
                best_win_streak = current_win_streak
        elif attempts >= max_attempts:
            message_lines = [f"You lost this round!", f"The correct word was: {target_word}"]
            game_over = True
            lives -= 1
            if lives > 0:
                message_lines.append(f"You have {lives} lives left.")

    # Render graphics
    window.fill(BLACK)
    # Draw the win streaks
    win_streak_surface = font.render(f"Best Win Streak: {best_win_streak}, Current Win Streak: {current_win_streak}", True, WHITE)
    window.blit(win_streak_surface, (20, 25))
    # Draw the lives left
    lives_surface = font.render(f"Lives left: {lives}", True, WHITE)
    window.blit(lives_surface, (20, 50))
    # Draw the attempts left
    attempts_surface = font.render(f"Attempts left: {max_attempts - attempts}", True, WHITE)
    window.blit(attempts_surface, (20, 75))
    # Draw the guessed word
    for i, l in enumerate(guess_word[0]):
        guess_surface = font.render(l, True, guess_word[1][i])
        window.blit(guess_surface, (20 + i * 40, 100))
    # Draw the current input
    input_word_surface = font.render(f"Current Input: {input_word}", True, WHITE)
    window.blit(input_word_surface, (20, 125))
    # Draw the previous guesses
    for i, guess in enumerate(guesses):
        for j, l in enumerate(guess[0]):
            guess_surface = font.render(l, True, guess[1][j])
            window.blit(guess_surface, (20 + j * 40, 150 + i * 25))
    # Draw the message and the buttons when the game is over
    if game_over:
        message_y = 150 + len(guesses) * 25
        if message_y + 40 > play_again_button_position[1]: 
            message_y = play_again_button_position[1] - 40
        for i, line in enumerate(message_lines):
            message_surface = font.render(line, True, WHITE)
            window.blit(message_surface, (20, message_y + i * 20))
        if lives > 0:
            draw_button("Next Round", play_again_button_position)
        else:
            if not result_written:
                now = datetime.datetime.now()
                date_time = now.strftime("%Y-%m-%d %H:%M:%S")
                result = f"Date and Time: {date_time}   Current Win Streak: {current_win_streak}\n"
                with open("results.txt", "a") as f:
                    f.write(result)
                result_written = True
            draw_button("Restart Game", restart_button_position)
        
        draw_button("Close", close_button_position)

    pygame.display.update()

# Clean up
pygame.quit()
sys.exit()