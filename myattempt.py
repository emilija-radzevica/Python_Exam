import words
import pygame
from pygame.locals import *
import sys
import random
import datetime

pygame.init()
game_width = 450
game_height = 600
game = pygame.display.set_mode(size = (game_width, game_height))
pygame.display.set_caption("Faux Lingo 2024")

PEACH = (254, 241, 207)
BLACK = (0, 0, 0)
GREEN = (150, 245, 71)
YELLOW = (245, 237, 73)

record_win_streak = 0
current_win_streak = 0
correctly_guessed_words = 0
lives = 3
target_word = random.choice(words.word_list)
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
        result_list[key] = value

for key, value in result_list.items():
    print(key, " : ", value)



playing = True
while playing:
    game.fill(PEACH)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
