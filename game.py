# v0.0.8

""" 
Typing Challenge for DEF CON 32
This challenge will be hosted at the LHC Room
"""

# Importing Packages
import pygame
import sys
import time
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN.get_size()
pygame.display.set_caption("Typing Minigame")

# Fonts and Colors
FONT = pygame.font.Font(pygame.font.match_font('courier'), 36)
BUTTON_FONT = pygame.font.Font(None, 48)
TIMER_FONT = pygame.font.Font(None, 36)
LEADERBOARD_FONT = pygame.font.Font(None, 36)
INPUT_FONT = pygame.font.Font(pygame.font.match_font('courier'), 36)
COLOR_BG = (30, 30, 30)
COLOR_TEXT_FADED = (100, 100, 100)
COLOR_TEXT_CORRECT = (255, 255, 255)
COLOR_TEXT_INCORRECT = (255, 0, 0)
COLOR_BUTTON = (70, 130, 180)
COLOR_BUTTON_HOVER = (100, 149, 237)
COLOR_BUTTON_TEXT = (255, 255, 255)
COLOR_CURSOR = (255, 255, 255)
COLOR_TIMER = (255, 255, 0)
COLOR_FIRST = (255, 165, 0)  # Orange
COLOR_SECOND = (128, 0, 128)  # Purple
COLOR_THIRD = (0, 0, 255)  # Blue

# Paths
ASSETS_FOLDER = 'assets'
LEADERBOARD_FILE = os.path.join(ASSETS_FOLDER, 'leaderboard.txt')
BACKGROUND_IMAGE = os.path.join(ASSETS_FOLDER, 'background.png')

# Load the background image
background = pygame.image.load(BACKGROUND_IMAGE)
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Pre-planned texts
texts = [
    "a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a"
]

# Game state
current_text = texts[0]
user_input = ""
text_index = 0
game_active = False
game_over = False
start_time = 0
end_time = 0
typing_started = False
scroll_offset = 0
username = ""

# Application states
STATE_MAIN_MENU = 0
STATE_GAME = 1
STATE_END_SCREEN = 2
STATE_LEADERBOARD = 3

state = STATE_MAIN_MENU

def draw_text():
    global SCREEN, scroll_offset
    SCREEN.fill(COLOR_BG)
    x_offset = 50 - scroll_offset  # Starting x position for text with scroll offset
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

    # Scroll the text if cursor goes beyond the center of the screen width
    if cursor_x > SCREEN_WIDTH // 2:
        scroll_offset += FONT.size(' ')[0]
    # Scroll the text back if cursor goes before the starting scroll threshold
    elif cursor_x < 50 and scroll_offset > 0:
        scroll_offset -= FONT.size(' ')[0]

    # Draw the blinking cursor
    if time.time() % 1 < 0.5:
        pygame.draw.rect(SCREEN, COLOR_CURSOR, (cursor_x, y_offset, 2, FONT.get_height()))

    # Draw the timer
    elapsed_time = time.time() - start_time if typing_started else 0
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    milliseconds = int((elapsed_time * 1000) % 1000)
    timer_text = f"Time: {minutes:02}:{seconds:02}:{milliseconds:03}"
    timer_surface = TIMER_FONT.render(timer_text, True, COLOR_TIMER)
    SCREEN.blit(timer_surface, (50, 50))

    # Draw the quit and restart buttons
    mouse_pos = pygame.mouse.get_pos()
    quit_hovered = draw_button("Quit (Ctrl+Q)", (SCREEN.get_width() - 150, 50), (SCREEN.get_width() - 200 <= mouse_pos[0] <= SCREEN.get_width() - 100) and (25 <= mouse_pos[1] <= 75)).collidepoint(mouse_pos)
    restart_hovered = draw_button("Restart (Ctrl+R)", (SCREEN.get_width() - 400, 50), (SCREEN.get_width() - 450 <= mouse_pos[0] <= SCREEN.get_width() - 350) and (25 <= mouse_pos[1] <= 75)).collidepoint(mouse_pos)
    pygame.display.flip()

    return quit_hovered, restart_hovered

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

def draw_leaderboard():
    global SCREEN
    SCREEN.fill(COLOR_BG)

    leaderboard = load_leaderboard()
    y_offset = 50

    for index, entry in enumerate(leaderboard):
        name, elapsed_time = entry
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        milliseconds = int((elapsed_time * 1000) % 1000)
        time_text = f"{minutes:02}:{seconds:02}:{milliseconds:03}"

        text = f"{index + 1}. {name} - {time_text}"
        text_surface = LEADERBOARD_FONT.render(text, True, COLOR_TEXT_CORRECT)
        text_rect = text_surface.get_rect(center=(SCREEN.get_width() // 2, y_offset))

        if index == 0:
            pygame.draw.rect(SCREEN, COLOR_FIRST, text_rect.inflate(20, 10), 3)
        elif index == 1:
            pygame.draw.rect(SCREEN, COLOR_SECOND, text_rect.inflate(20, 10), 3)
        elif index == 2:
            pygame.draw.rect(SCREEN, COLOR_THIRD, text_rect.inflate(20, 10), 3)

        SCREEN.blit(text_surface, text_rect)
        y_offset += 50

    # Draw the "Back" button
    mouse_pos = pygame.mouse.get_pos()
    back_hovered = draw_button("Back", (SCREEN.get_width() // 2, SCREEN_HEIGHT - 50), (SCREEN.get_width() // 2 - 50 <= mouse_pos[0] <= SCREEN.get_width() // 2 + 50) and (SCREEN_HEIGHT - 75 <= mouse_pos[1] <= SCREEN_HEIGHT - 25)).collidepoint(mouse_pos)
    
    pygame.display.flip()
    return back_hovered

def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []

    with open(LEADERBOARD_FILE, 'r') as file:
        lines = file.readlines()

    leaderboard = []
    for line in lines:
        name, elapsed_time = line.strip().split(',')
        leaderboard.append((name, float(elapsed_time)))

    leaderboard.sort(key=lambda x: x[1])
    return leaderboard[:10]

def save_leaderboard(leaderboard):
    with open(LEADERBOARD_FILE, 'w') as file:
        for name, elapsed_time in leaderboard:
            file.write(f"{name},{elapsed_time}\n")

def update_leaderboard(username, elapsed_time):
    leaderboard = load_leaderboard()
    leaderboard.append((username, elapsed_time))
    leaderboard.sort(key=lambda x: x[1])
    save_leaderboard(leaderboard[:10])

def prompt_username(elapsed_time):
    global SCREEN, username
    SCREEN.fill(COLOR_BG)

    input_box = pygame.Rect(SCREEN.get_width() // 2 - 100, SCREEN.get_height() // 2 - 25, 200, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_active  # Set the color to active initially
    active = True  # Make the input box active initially
    done = False
    username = ''

    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    milliseconds = int((elapsed_time * 1000) % 1000)
    time_text = f"{minutes:02}:{seconds:02}:{milliseconds:03}"
    message_text1 = "Good Job! You are in Top 10."
    message_text2 = "Please Enter Your Handle"
    time_display_text = f"Your Time: {time_text}"

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        if len(username) < 16:
                            username += event.unicode

        SCREEN.fill(COLOR_BG)
        message_surface1 = TIMER_FONT.render(message_text1, True, COLOR_TIMER)
        message_surface2 = TIMER_FONT.render(message_text2, True, COLOR_TIMER)
        time_surface = TIMER_FONT.render(time_display_text, True, COLOR_TIMER)
        
        SCREEN.blit(message_surface1, (SCREEN.get_width() // 2 - message_surface1.get_width() // 2, SCREEN.get_height() // 2 - 150))
        SCREEN.blit(message_surface2, (SCREEN.get_width() // 2 - message_surface2.get_width() // 2, SCREEN.get_height() // 2 - 100))
        SCREEN.blit(time_surface, (SCREEN.get_width() // 2 - time_surface.get_width() // 2, SCREEN.get_height() // 2 - 50))

        txt_surface = INPUT_FONT.render(username, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        SCREEN.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(SCREEN, color, input_box, 2)

        # Draw the blinking cursor
        if time.time() % 1 < 0.5:
            cursor_rect = pygame.Rect(input_box.x + txt_surface.get_width() + 5, input_box.y + 5, 2, txt_surface.get_height())
            pygame.draw.rect(SCREEN, COLOR_CURSOR, cursor_rect)

        pygame.display.flip()

def draw_top_3():
    leaderboard = load_leaderboard()
    x_offset = SCREEN.get_width() - 200
    y_offset = 50

    for index, entry in enumerate(leaderboard[:3]):
        name, elapsed_time = entry
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        milliseconds = int((elapsed_time * 1000) % 1000)
        time_text = f"{minutes:02}:{seconds:02}:{milliseconds:03}"

        text = f"{index + 1}. {name} - {time_text}"
        text_surface = LEADERBOARD_FONT.render(text, True, COLOR_TEXT_CORRECT)
        text_rect = text_surface.get_rect(center=(x_offset, y_offset))

        if index == 0:
            pygame.draw.rect(SCREEN, COLOR_FIRST, text_rect.inflate(20, 10), 3)
        elif index == 1:
            pygame.draw.rect(SCREEN, COLOR_SECOND, text_rect.inflate(20, 10), 3)
        elif index == 2:
            pygame.draw.rect(SCREEN, COLOR_THIRD, text_rect.inflate(20, 10), 3)

        SCREEN.blit(text_surface, text_rect)
        y_offset += 50

def main_menu():
    global SCREEN, game_active, user_input, text_index, current_text, start_time, game_over, typing_started, scroll_offset, state

    while state == STATE_MAIN_MENU:
        SCREEN.blit(background, (0, 0))

        mouse_pos = pygame.mouse.get_pos()
        new_game_hovered = draw_button("New Game", (SCREEN.get_width() // 2, SCREEN.get_height() // 3), (SCREEN.get_width() // 2 - 100 <= mouse_pos[0] <= SCREEN.get_width() // 2 + 100) and (SCREEN.get_height() // 3 - 25 <= mouse_pos[1] <= SCREEN.get_height() // 3 + 25)).collidepoint(mouse_pos)
        leaderboard_hovered = draw_button("Leaderboard", (SCREEN.get_width() // 2, SCREEN.get_height() // 2), (SCREEN.get_width() // 2 - 100 <= mouse_pos[0] <= SCREEN.get_width() // 2 + 100) and (SCREEN.get_height() // 2 - 25 <= mouse_pos[1] <= SCREEN.get_height() // 2 + 25)).collidepoint(mouse_pos)
        quit_hovered = draw_button("Quit", (SCREEN.get_width() // 2, SCREEN.get_height() // 1.5), (SCREEN.get_width() // 2 - 100 <= mouse_pos[0] <= SCREEN.get_width() // 2 + 100) and (SCREEN.get_height() // 1.5 - 25 <= mouse_pos[1] <= SCREEN.get_height() // 1.5 + 25)).collidepoint(mouse_pos)

        draw_top_3()
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
                    start_time = 0
                    typing_started = False
                    scroll_offset = 0
                    state = STATE_GAME
                    return
                elif leaderboard_hovered:
                    state = STATE_LEADERBOARD
                elif quit_hovered:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
                SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

def main():
    global SCREEN, user_input, text_index, current_text, game_active, start_time, end_time, game_over, typing_started, scroll_offset, username, state

    clock = pygame.time.Clock()

    while True:
        if state == STATE_MAIN_MENU:
            main_menu()
        elif state == STATE_GAME:
            quit_hovered = False
            restart_hovered = False
            play_again_hovered = False
            main_menu_hovered = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif game_active and not game_over:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if quit_hovered:
                            game_active = False
                            state = STATE_MAIN_MENU  # Update state to main menu
                        elif restart_hovered:
                            game_active = True
                            game_over = False
                            user_input = ""
                            text_index = 0
                            current_text = texts[text_index]
                            start_time = 0
                            typing_started = False
                            scroll_offset = 0
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            user_input = user_input[:-1]
                            if not typing_started and user_input:
                                start_time = time.time()
                                typing_started = True
                        elif event.key == pygame.K_RETURN:
                            pass
                        elif event.key == pygame.K_q and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                            game_active = False
                            state = STATE_MAIN_MENU  # Update state to main menu
                        elif event.key == pygame.K_r and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                            game_active = True
                            game_over = False
                            user_input = ""
                            text_index = 0
                            current_text = texts[text_index]
                            start_time = 0
                            typing_started = False
                            scroll_offset = 0
                        else:
                            if not typing_started:
                                start_time = time.time()
                                typing_started = True
                            user_input += event.unicode
                            if user_input == current_text:
                                game_over = True
                                end_time = time.time()
                                elapsed_time = end_time - start_time
                                leaderboard = load_leaderboard()
                                if len(leaderboard) < 10 or elapsed_time < leaderboard[-1][1]:
                                    prompt_username(elapsed_time)
                                    update_leaderboard(username, elapsed_time)
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
                            start_time = 0
                            typing_started = False
                            scroll_offset = 0
                        elif main_menu_hovered:
                            game_active = False
                            state = STATE_MAIN_MENU  # Update state to main menu

            if game_active and not game_over:
                quit_hovered, restart_hovered = draw_text()
                mouse_pos = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed()[0]:
                    if quit_hovered:
                        game_active = False
                        state = STATE_MAIN_MENU  # Update state to main menu
                    elif restart_hovered:
                        game_active = True
                        game_over = False
                        user_input = ""
                        text_index = 0
                        current_text = texts[text_index]
                        start_time = 0
                        typing_started = False
                        scroll_offset = 0
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
                        start_time = 0
                        typing_started = False
                        scroll_offset = 0
                    elif main_menu_hovered:
                        game_active = False
                        state = STATE_MAIN_MENU  # Update state to main menu

            clock.tick(30)
        elif state == STATE_LEADERBOARD:
            while state == STATE_LEADERBOARD:
                back_hovered = draw_leaderboard()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if back_hovered:
                            state = STATE_MAIN_MENU  # Update state to main menu
                    elif event.type == pygame.VIDEORESIZE:
                        SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
                        SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

if __name__ == "__main__":
    main()

