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
wrong_words_list = ["ābols", "galds", "ziema", "kokle", "volvo", "bēbis"]

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

def show_lives(life_count):
    heart_placement = game_width/6*5 - 30
    for i in range(0, life_count):
        life = pygame.image.load("img/heart_icon.png")
        life = pygame.transform.scale(life, (20, 20))
        life_rect = life.get_rect(center = (heart_placement, 60))
        game.blit(life,life_rect)
        heart_placement += 30

def show_wrong_words(wrong_list):
    x=140
    if len(wrong_list) < 8:
        for i in range(0, len(wrong_list)):
            last_unknown_word = font.render(wrong_list[i] + " ", True, BLACK)
            game.blit(last_unknown_word, (x, 550))
            x+=33
    else:
        for i in range(len(wrong_list)-8, len(wrong_list)):
            last_unknown_word = font.render(wrong_list[i] + " ", True, BLACK)
            game.blit(last_unknown_word, (x, 550))
            x+=33

#  spēle
playing = True
while playing:
    game.fill(PEACH)

    moves_left = font.render("Atlikušie gājieni", True, BLACK)
    win_streak = font.render("Uzvaras pēc kārtas", True, BLACK)
    lives_left = font.render("Dzīvības", True, BLACK)
    moves_left_rect = moves_left.get_rect(center = (game_width/6, 30))
    win_streak_rect = win_streak.get_rect(center = (game_width/2, 30))
    lives_left_rect = lives_left.get_rect(center = (game_width/6*5, 30))
    game.blit(moves_left,moves_left_rect)
    game.blit(win_streak,win_streak_rect)
    game.blit(lives_left,lives_left_rect)

    moves_left_value = font.render("5", True, BLACK)
    win_streak_value = font.render("0", True, BLACK)
    # life = pygame.image.load("img/heart_icon.png")
    # life = pygame.transform.scale(life, (20, 20))
    moves_left_value_rect = moves_left.get_rect(center = (game_width/6+35, 60))
    win_streak_value_rect = win_streak.get_rect(center = (game_width/2+40, 60))
    # life_rect = life.get_rect(center = (game_width/6*5, 60))
    game.blit(moves_left_value,moves_left_value_rect)
    game.blit(win_streak_value,win_streak_value_rect)
    # game.blit(life,life_rect)
    show_lives(1)

    grid = pygame.image.load("img/grid.png")
    grid = pygame.transform.scale(grid, (350, 418))
    grid_rect = grid.get_rect(center = (game_width/2, game_height/2))
    game.blit(grid, grid_rect)

    button = pygame.draw.rect(game, BLACK, (100, 550, button_width, button_height))
    one_text = smallfont.render("Statistics", True, GREEN)
    mouse = pygame.mouse.get_pos()

    if 100 <= mouse[0] <= 100 + button_width and 550 <= mouse[1] <= 550 +button_height:
        button = pygame.draw.rect(game, YELLOW, (100, 550, button_width, button_height))

    
    one_text_rect = one_text.get_rect(center = (100 + button_width/2, 550 + button_height/2))

    game.blit(one_text, one_text_rect)

    guessed_words = font.render("Uzminētie vārdi: 5", True, BLACK)
    game.blit(guessed_words, (40, 530))
    unknown_words = font.render("Neuzminētie vārdi: ", True, BLACK)
    game.blit(unknown_words, (40, 550))

    # target_word = "ābols"
    show_wrong_words(wrong_words_list)
    # game.blit(wrong_words_list, (140, 550))

    results = font.render("Rezultāti", True, BLACK)
    results_rect = guessed_words.get_rect(center = (game_width-20, 580))
    game.blit(results, results_rect)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            if 100 <= mouse[0] <= 100 + button_width and 550 <= mouse[1] <= 550 +button_height:
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
            wordy = "volvo"
            wrong_words_list.append(wordy)
            show_wrong_words(wrong_words_list)
    pygame.display.update()