import pygame
import os
import math
import random


# Setup display
pygame.init()
WIDTH, HEIGHT = 1000, 700
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game!")

# Button variables
RADIUS = 25
GAP = 15
LETTERS = []
X_START = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
Y_START = 400
A = 65
MAX_ATTEMPTS = 6
ALPHABET_SIZE = 26
BUTTONS_PER_ROW = 13

for i in range(ALPHABET_SIZE):
    x = X_START + GAP * 2 + ((RADIUS * 2 + GAP) * (i % BUTTONS_PER_ROW))
    y = Y_START + ((i // BUTTONS_PER_ROW) * (GAP + RADIUS * 2))
    LETTERS.append([x, y, chr(A + i), True])

# Fonts
LETTER_FONT = pygame.font.SysFont('arial', 30)
WORD_FONT = pygame.font.SysFont('arial', 60, bold=True)
TITLE_FONT = pygame.font.SysFont('arial', 70, bold=True)

# Colors
WHITE = (242, 242, 242)
DARK_GREY = (51, 51, 51)
BLUE = (44, 107, 255)
PASTEL_BLUE = (161, 198, 255)
GREEN = (76, 175, 80)
ORANGE = (255, 112, 67)
HOVER_COLOR = (200, 200, 255)

# Game variables
HANGMAN_STATUS = 0
guessed = []

# Load images
IMAGES = []
for i in range(7):
    image_path = f"images/hangman{i}.png"
    if os.path.exists(image_path):
        IMAGES.append(pygame.image.load(image_path))
    else:
        IMAGES.append(pygame.Surface((200, 200)))


def load_words_from_file(filename):
    with open(filename, 'r') as file:
        words = file.readlines()
    return [word.strip().upper() for word in words]


WORDS = load_words_from_file('words.txt')
word = random.choice(WORDS)


def draw_game():
    """Function to draw the game screen"""
    # Draw background
    win.fill(WHITE)

    # Draw title
    text = TITLE_FONT.render("DEVELOPER HANGMAN", 1, BLUE)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, 20))

    display_word = ' '.join([letter if letter in guessed else '_' for letter in word])
    text = WORD_FONT.render(display_word, 1, DARK_GREY)
    win.blit(text, (400, 200))

    # Draw buttons with hover effect
    m_x, m_y = pygame.mouse.get_pos()
    for letter in LETTERS:
        x, y, ltr, visible = letter
        if visible:
            dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)
            if dis < RADIUS:
                pygame.draw.circle(win, HOVER_COLOR, (x, y), RADIUS, 0)
                pygame.draw.circle(win, DARK_GREY, (x, y), RADIUS, 3)
            else:
                pygame.draw.circle(win, PASTEL_BLUE, (x, y), RADIUS, 0)
                pygame.draw.circle(win, DARK_GREY, (x, y), RADIUS, 3)

            text = LETTER_FONT.render(ltr, 1, DARK_GREY)
            win.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

    # Draw hangman status
    win.blit(IMAGES[HANGMAN_STATUS], (150, 150))
    pygame.display.update()


def display_message(message, color=DARK_GREY):
    """Function to display a message"""
    pygame.time.delay(1000)
    win.fill(WHITE)
    text = WORD_FONT.render(message, 1, color)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(3000)


def ask_play_again_game():
    """Function to ask the player if they want to play again"""
    win.fill(WHITE)
    text = WORD_FONT.render("Do you want to play again? (Y/N)", 1, DARK_GREY)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True
                if event.key == pygame.K_n:
                    pygame.quit()
                    return False


def reset_game():
    """Function to reset the game"""
    global HANGMAN_STATUS, word, guessed, LETTERS

    HANGMAN_STATUS = 0
    word = random.choice(WORDS)
    guessed = []

    for i in range(ALPHABET_SIZE):
        LETTERS[i][3] = True


def main():
    """Main game loop"""
    global HANGMAN_STATUS

    FPS = 60
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in LETTERS:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)
                        if dis < RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                HANGMAN_STATUS += 1

        draw_game()

        won = all(letter in guessed for letter in word)
        if won:
            display_message('You won!', GREEN)
            if ask_play_again_game():
                reset_game()
                break
            else:
                run = False
                break

        if HANGMAN_STATUS == MAX_ATTEMPTS:
            display_message('You lost!', ORANGE)
            if ask_play_again_game():
                reset_game()
                break
            else:
                run = False
                break


if __name__ == "__main__":
    while True:
        main()
    pygame.quit()



