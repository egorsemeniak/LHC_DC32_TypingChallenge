# v0.0.1

""" 
Typing Challenge for DEF CON 32
This challenge will be hosted at the LHC Room
"""


# Importing Packages
import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Typing Minigame")

# Fonts and Colors
FONT = pygame.font.Font(None, 36)
COLOR_BG = (30, 30, 30)
COLOR_TEXT_FADED = (100, 100, 100)
COLOR_TEXT_CORRECT = (255, 255, 255)
COLOR_TEXT_INCORRECT = (255, 0, 0)

# Hard-coded texts, for now... Will add 3 challenges later on.
texts = [
    "The quick brown fox jumps over the lazy dog."
]

# Game state
current_text = texts[0]
user_input = ""
text_index = 0

def draw_text():
    SCREEN.fill(COLOR_BG)
    for i, char in enumerate(current_text):
        if i < len(user_input):
            if user_input[i] == char:
                color = COLOR_TEXT_CORRECT
            else:
                color = COLOR_TEXT_INCORRECT
        else:
            color = COLOR_TEXT_FADED
        text_surface = FONT.render(char, True, color)
        SCREEN.blit(text_surface, (50 + i * 20, 300))
    pygame.display.flip()

def main():
    global user_input, text_index, current_text

    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.key == pygame.K_RETURN:
                    if user_input == current_text:
                        text_index = (text_index + 1) % len(texts)
                        current_text = texts[text_index]
                        user_input = ""
                else:
                    user_input += event.unicode

        draw_text()
        clock.tick(30)

if __name__ == "__main__":
    main()
