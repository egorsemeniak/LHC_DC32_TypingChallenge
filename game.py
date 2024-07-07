# v0.0.2

""" 
Typing Challenge for DEF CON 32
This challenge will be hosted at the LHC Room
"""


# Importing Packages
import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Typing Minigame")

# Fonts and Colors
FONT = pygame.font.Font(pygame.font.match_font('courier'), 36)
BUTTON_FONT = pygame.font.Font(None, 48)
TIMER_FONT = pygame.font.Font(None, 36)
COLOR_BG = (30, 30, 30)
COLOR_TEXT_FADED = (100, 100, 100)
COLOR_TEXT_CORRECT = (255, 255, 255)
COLOR_TEXT_INCORRECT = (255, 0, 0)
COLOR_BUTTON = (70, 130, 180)
COLOR_BUTTON_HOVER = (100, 149, 237)
COLOR_BUTTON_TEXT = (255, 255, 255)
COLOR_CURSOR = (255, 255, 255)
COLOR_TIMER = (255, 255, 0)

# Pre-planned texts
texts = [
    "The quick brown fox jumps over the lazy dog."
]

# Game state
current_text = texts[0]
user_input = ""
text_index = 0
game_active = False
game_over = False
start_time = 0
end_time = 0

def draw_text():
    global SCREEN
    SCREEN.fill(COLOR_BG)
    x_offset = 50  # Starting x position for text
    y_offset = SCREEN.get_height() // 2  # Center text vertically
    cursor_x = x_offset + len(user_input) * FONT.size(' ')[0]  # Calculate cursor x position

    for i, char in enumerate(current_text):
        if i < len(user_input):
            if user_input[i] == char:
                color = COLOR_TEXT_CORRECT
            else:
                color = COLOR_TEXT_INCORRECT
        else:
            color = COLOR_TEXT_FADED
        text_surface = FONT.render(char, True, color)
        SCREEN.blit(text_surface, (x_offset + i * FONT.size(char)[0], y_offset))

    # Draw the blinking cursor
    if time.time() % 1 < 0.5:
        pygame.draw.rect(SCREEN, COLOR_CURSOR, (cursor_x, y_offset, 2, FONT.get_height()))

    # Draw the timer
    elapsed_time = time.time() - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    milliseconds = int((elapsed_time * 1000) % 1000)
    timer_text = f"Time: {minutes:02}:{seconds:02}:{milliseconds:03}"
    timer_surface = TIMER_FONT.render(timer_text, True, COLOR_TIMER)
    SCREEN.blit(timer_surface, (50, 50))

    # Draw the quit button
    mouse_pos = pygame.mouse.get_pos()
    quit_hovered = draw_button("Quit", (SCREEN.get_width() - 100, 50), (SCREEN.get_width() - 150 <= mouse_pos[0] <= SCREEN.get_width() - 50) and (25 <= mouse_pos[1] <= 75)).collidepoint(mouse_pos)
    pygame.display.flip()

    return quit_hovered

def draw_button(text, position, is_hovered):
    color = COLOR_BUTTON_HOVER if is_hovered else COLOR_BUTTON
    button_surface = BUTTON_FONT.render(text, True, COLOR_BUTTON_TEXT)
    button_rect = button_surface.get_rect(center=position)
    pygame.draw.rect(SCREEN, color, button_rect.inflate(20, 10))
    SCREEN.blit(button_surface, button_rect)
    return button_rect

def draw_end_screen():
    global SCREEN, end_time
    SCREEN.fill(COLOR_BG)

    elapsed_time = end_time - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    milliseconds = int((elapsed_time * 1000) % 1000)
    timer_text = f"Completed in: {minutes:02}:{seconds:02}:{milliseconds:03}"
    timer_surface = TIMER_FONT.render(timer_text, True, COLOR_TIMER)
    SCREEN.blit(timer_surface, (SCREEN.get_width() // 2 - 150, SCREEN.get_height() // 3))

    mouse_pos = pygame.mouse.get_pos()
    play_again_hovered = draw_button("Play Again", (SCREEN.get_width() // 2, SCREEN.get_height() // 2), (SCREEN.get_width() // 2 - 100 <= mouse_pos[0] <= SCREEN.get_width() // 2 + 100) and (SCREEN.get_height() // 2 - 25 <= mouse_pos[1] <= SCREEN.get_height() // 2 + 25)).collidepoint(mouse_pos)
    main_menu_hovered = draw_button("Main Menu", (SCREEN.get_width() // 2, SCREEN.get_height() // 2 + 100), (SCREEN.get_width() // 2 - 100 <= mouse_pos[0] <= SCREEN.get_width() // 2 + 100) and (SCREEN.get_height() // 2 + 75 <= mouse_pos[1] <= SCREEN.get_height() // 2 + 125)).collidepoint(mouse_pos)

    pygame.display.flip()

    return play_again_hovered, main_menu_hovered

def main_menu():
    global SCREEN, game_active, user_input, text_index, current_text, start_time, game_over

    while True:
        SCREEN.fill(COLOR_BG)

        mouse_pos = pygame.mouse.get_pos()
        new_game_hovered = draw_button("New Game", (SCREEN.get_width() // 2, SCREEN.get_height() // 3), (SCREEN.get_width() // 2 - 100 <= mouse_pos[0] <= SCREEN.get_width() // 2 + 100) and (SCREEN.get_height() // 3 - 25 <= mouse_pos[1] <= SCREEN.get_height() // 3 + 25)).collidepoint(mouse_pos)
        quit_hovered = draw_button("Quit", (SCREEN.get_width() // 2, SCREEN.get_height() // 2), (SCREEN.get_width() // 2 - 100 <= mouse_pos[0] <= SCREEN.get_width() // 2 + 100) and (SCREEN.get_height() // 2 - 25 <= mouse_pos[1] <= SCREEN.get_height() // 2 + 25)).collidepoint(mouse_pos)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if new_game_hovered:
                    game_active = True
                    game_over = False
                    user_input = ""
                    text_index = 0
                    current_text = texts[text_index]
                    start_time = time.time()
                    return
                elif quit_hovered:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
                SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

def main():
    global SCREEN, user_input, text_index, current_text, game_active, start_time, end_time, game_over

    clock = pygame.time.Clock()

    while True:
        quit_hovered = False
        play_again_hovered = False
        main_menu_hovered = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif game_active and not game_over:
                if event.type == pygame.MOUSEBUTTONDOWN and quit_hovered:
                    game_active = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    elif event.key == pygame.K_RETURN:
                        if user_input == current_text:
                            text_index += 1
                            if text_index < len(texts):
                                current_text = texts[text_index]
                                user_input = ""
                            else:
                                game_over = True
                                end_time = time.time()
                    else:
                        user_input += event.unicode
            elif event.type == pygame.VIDEORESIZE:
                SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
                SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
            elif game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_again_hovered:
                        game_active = True
                        game_over = False
                        user_input = ""
                        text_index = 0
                        current_text = texts[text_index]
                        start_time = time.time()
                    elif main_menu_hovered:
                        game_active = False
                        main_menu()

        if game_active and not game_over:
            quit_hovered = draw_text()
            if pygame.mouse.get_pressed()[0] and quit_hovered:
                game_active = False
        elif game_over:
            play_again_hovered, main_menu_hovered = draw_end_screen()
            mouse_pos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0]:
                if play_again_hovered:
                    game_active = True
                    game_over = False
                    user_input = ""
                    text_index = 0
                    current_text = texts[text_index]
                    start_time = time.time()
                elif main_menu_hovered:
                    game_active = False
                    main_menu()
        else:
            main_menu()

        clock.tick(30)

if __name__ == "__main__":
    main()

