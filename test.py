with open('results.txt', 'r') as f:
        lines = f.readlines()
        scores = [(line.split()[0:2], int(line.split()[-1])) for line in lines]
        scores.sort(key=lambda x: x[1], reverse=True)
        top_scores = scores[:5]
        print(top_scores[1][1])

# for i, (date_time, score) in enumerate(top_scores):
#     score_text = f"Top {i+1}    Score: {score}    Achieved on:  {' '.join(date_time)}"
#     score_surface = font.render(score_text, True, WHITE)
#     score_width = score_surface.get_rect().width
#     score_x = window_width - score_width - 20
#     window.blit(score_surface, (score_x, 150 + i * 25))
        

    moves_left = font.render("Atlikušie gājieni", True, BLACK)
    win_streak = font.render("Uzvaras pēc kārtas", True, BLACK)
    lives_left = font.render("Dzīvības", True, BLACK)
    moves_left_rect = moves_left.get_rect(center = (window_width/6, 30))
    win_streak_rect = win_streak.get_rect(center = (window_width/2, 30))
    lives_left_rect = lives_left.get_rect(center = (window_width/6*5, 30))
    window.blit(moves_left, moves_left_rect)
    window.blit(win_streak, win_streak_rect)
    window.blit(lives_left, lives_left_rect)

    moves_left_value = font.render(max_attempts-attempts, True, BLACK)
    moves_left_value_rect = moves_left_value.get_rect(center = (window_width/6+35, 60))
    window.blit(moves_left_value, moves_left_rect)
    win_streak_value = font.render(current_win_streak, True, BLACK)
    win_streak_value_rect = win_streak_value.get_rect(center = (window_width/2+40, 60))
    window.blit(win_streak_value, win_streak_value_rect)

def draw_main_info(text, value, lives, position_x)
    info_title = font.render(text, True, BLACK)
    info_title_rect = info_title.get_rect(center = (position_x, 30))
    window.blit(info_title, info_title_rect)

    if lives:
        show_lives(value)
    else:
        info_value = font.render(value, True, BLACK)
        info_value_rect = info_value.get_rect(center = (position_x, 60))
        window.blit(info_value, info_value_rect)

draw_main_info("Atlikušie gājieni", max_attempts-attempts, False, window_width/6)
draw_main_info("Uzvaras pēc kārtas", current_win_streak, False, window_width/2)
draw_main_info("Dzīvības", lives, True, window_width/6*5)
