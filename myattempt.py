import words
import pygame
from pygame.locals import *
import sys
import random
import datetime
from operator import itemgetter

pygame.init()
game_width = 450
game_height = 600
game = pygame.display.set_mode(size = (game_width, game_height))
pygame.display.set_caption("Faux Lingo 2024")

PEACH = (254, 241, 207)
BLACK = (0, 0, 0)
GREEN = (150, 245, 71)
YELLOW = (245, 237, 73)
WHITE = (255, 255, 255)

record_win_streak = 0
current_win_streak = 0
correctly_guessed_words = 0
lives = 3
target_word = random.choice(words.word_list)
show_stats = False
print(target_word)
print(["_" for _ in target_word])
print([BLACK for _ in target_word])

# saves games results inside a .txt file
result_key = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
text = "Hello from the text file"
f = open("results.txt", "a")
f.write(result_key + " : " + str(correctly_guessed_words) + "\n")
f.close()

# tranforms results from .txt file into a dictionary
result_list = {}
with open("results.txt") as f:
    for line in f:
        (key, value) = line.split(" : ")
        result_list[key] = int(value)

top_result_list = dict(sorted(result_list.items(), key = lambda x: x[1], reverse=True)[:10])
print(top_result_list)

smallfont = pygame.font.SysFont("Comic Sans", 35)
font = pygame.font.SysFont("Times New Roman", 12)

button_width = 180
button_height = 50
game.fill(PEACH)

def draw_stats():
    stats_title = smallfont.render("Tavi rezultāti", True, BLACK)
    stats_title_rect = stats_title.get_rect(center = (300/2, 30))
    stats.blit(stats_title, stats_title_rect)
    pygame.draw.rect(stats, BLACK, (65, 140, 50, 50))
    pygame.draw.rect(stats, BLACK, (125, 100, 50, 90))
    pygame.draw.rect(stats, BLACK, (185, 160, 50, 30))
    pygame.draw.line(stats, BLACK, (20, 210), (280, 210))
    place = 1
    row_placement = 230
    for key, value in top_result_list.items():
        stats_place = font.render(str(place)+".", True, BLACK)
        stats_date = font.render(key, True, BLACK)
        stats_result = font.render(str(value), True, BLACK)
        if place <= 3:
            if place == 1:
                stats_result_rect = stats_result.get_rect(center = (150, 90))
                first_key = key
            elif place == 2:
                stats_result_rect = stats_result.get_rect(center = (90, 130))
                second_key = key
            elif place == 3:
                stats_result_rect = stats_result.get_rect(center = (210, 150))
                third_key = key
        else:
            stats_place_rect = stats_place.get_rect(center = (40, row_placement))
            stats_date_rect = stats_date.get_rect(center = (130, row_placement))
            stats_result_rect = stats_result.get_rect(center = (230, row_placement))
            row_placement += 30
            stats.blit(stats_place, stats_place_rect)
            stats.blit(stats_date, stats_date_rect)
        stats.blit(stats_result, stats_result_rect)
        place += 1
    return first_key, second_key, third_key

def show_top_result_date(date, placement):
    stats_date = font.render(date, True, BLACK)
    stats_date_rect = stats_date.get_rect(center = (placement, 200))
    stats.blit(stats_date, stats_date_rect)

#  spēle
playing = True
while playing:
    # game.fill(PEACH)
    button = pygame.draw.rect(game, BLACK, (100, 50, button_width, button_height))
    pygame.draw.rect(game, BLACK, (300, 20, 50, 250))
    one_text = smallfont.render("Statistics", True, GREEN)
    mouse = pygame.mouse.get_pos()

    if 100 <= mouse[0] <= 100 + button_width and 50 <= mouse[1] <= 50 +button_height:
        button = pygame.draw.rect(game, YELLOW, (100, 50, button_width, button_height))

    
    one_text_rect = one_text.get_rect(center = (100 + button_width/2, 50 + button_height/2))

    game.blit(one_text, one_text_rect)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            if 100 <= mouse[0] <= 100 + button_width and 50 <= mouse[1] <= 50 +button_height:
                game.fill(GREEN)
                show_stats = True

    if show_stats == True:
        stats = pygame.Surface((300, 460), pygame.SRCALPHA)
        stats.fill((255, 255, 255, 230))
        first_key, second_key, third_key = draw_stats()
        if 140 <= mouse[0] <= 190 and 190 <= mouse[1] <= 260:
            pygame.draw.rect(stats, PEACH, (65, 140, 50, 50))
            show_top_result_date(first_key, 90)
        elif 200 <= mouse[0] <= 250 and 150 <= mouse[1] <= 260:
            pygame.draw.rect(stats, PEACH, (125, 100, 50, 90))
            show_top_result_date(second_key, 150)
        if 260 <= mouse[0] <= 310 and 210 <= mouse[1] <= 260:
            pygame.draw.rect(stats, PEACH, (185, 160, 50, 30))
            show_top_result_date(third_key, 210)
        game.blit(stats, (75, 70))
        close_stats_button = pygame.draw.circle(game, PEACH,(375, 70), 20)
        close_stats = font.render("X", True, BLACK)
        close_stats_rect = close_stats.get_rect(center = (375, 70))
        game.blit(close_stats, close_stats_rect)

        if event.type == MOUSEBUTTONDOWN and 365 <= mouse[0] <= 385 and 60 <= mouse[1] <= 80:
            show_stats = False
            game.fill(PEACH)
    pygame.display.update()