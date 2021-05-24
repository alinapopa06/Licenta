import pygame
import sys

pygame.init()
running, playing = True, False
UP_KEY, DOWN_KEY, START_KEY, BACK_KEY = False, False, False, False
DISPLAY_W, DISPLAY_H = 480, 480
display = pygame.Surface((DISPLAY_W, DISPLAY_H))
window = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))
font_name = pygame.font.get_default_font()
WHITE, BLUE, GREEN, RED, BLACK = (255, 255, 255), (0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 0, 0)
mid_w, mid_h = DISPLAY_W / 2, DISPLAY_H / 2
run_display = True
run_difficulty = True
cursor_rect = pygame.Rect(0, 0, 20, 20)
offset = - 100
state = "First game"
First_x, First_y = mid_w, mid_h + 30
Second_x, Second_y = mid_w, mid_h + 50
Third_x, Third_y = mid_w, mid_h + 70
cursor_rect.center = (First_x + offset, First_y)

def draw_text(text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    display.blit(text_surface, text_rect)


def draw_cursor():
    draw_text('*', 35, cursor_rect.x+20, cursor_rect.y+20)


def blit_screen():
    window.blit(display, (0, 0))
    pygame.display.update()
    reset_keys()


def display_menu():
    global run_display
    run_display = True
    while run_display:
        check_events()
        check_input()
        display.fill(BLACK)
        draw_cursor()
        draw_text('Main Menu', 20, DISPLAY_W / 2, DISPLAY_H / 2 - 20)
        draw_text("First game", 20, First_x, First_y)
        draw_text("Second game", 20, Second_x, Second_y)
        draw_text("Third game", 20, Third_x, Third_y)
        blit_screen()
        #reset_keys()


def display_menu_difficulty():
    global run_display
    while run_difficulty:
        reset_keys()
        check_events()
        check_input_difficulty()
        display.fill(BLACK)
        draw_text('Choose difficulty', 20, DISPLAY_W / 2, DISPLAY_H / 2 - 20)
        draw_text("Easy", 20, First_x, First_y)
        draw_text("Medium", 20, Second_x, Second_y)
        draw_text("Hard", 20, Third_x, Third_y)
        draw_cursor()
        blit_screen()


def move_cursor():
    global state
    if DOWN_KEY:
        if state == 'First game':
            cursor_rect.center = (Second_x + offset, Second_y)
            state = 'Second game'
        elif state == 'Second game':
            cursor_rect.center = (Third_x + offset, Third_y)
            state = 'Third game'
        elif state == 'Third game':
            cursor_rect.center = (First_x + offset, First_y)
            state = 'First game'
    elif UP_KEY:
        if state == 'First game':
            cursor_rect.center = (Third_x + offset, Third_y)
            state = 'Third game'
        elif state == 'Second game':
            cursor_rect.center = (First_x + offset, First_y)
            state = 'First game'
        elif state == 'Third game':
            cursor_rect.center = (Second_x + offset, Second_y)
            state = 'Second game'


def check_input():
    global run_display, run_difficulty
    move_cursor()
    first = False
    second = False
    third = False
    if START_KEY:
        if state == 'First game':
            first = True
            display_menu_difficulty()
        elif state == 'Second game':
            second = True
            display_menu_difficulty()
        elif state == 'Third game':
            third = True
            display_menu_difficulty()
        run_display = False
        run_difficulty = False


def check_input_difficulty():
    global run_display, run_difficulty
    move_cursor()
    # first = check_input().first
    if START_KEY:
        if state == 'Easy':
            # if first == True:
            print('hai')
            display_first_game()
            if (state == 'Second game'):
                display_second_game()
            if (state == 'Third game'):
                display_third_game()
        elif state == 'Medium':
            if (state == 'First game'):
                display_first_game()
            if (state == 'Second game'):
                display_second_game()
            if (state == 'Third game'):
                display_third_game()
        elif state == 'Hard':
            if (state == 'First game'):
                display_first_game()
            if (state == 'Second game'):
                display_second_game()
            if (state == 'Third game'):
                display_third_game()
        run_display = False
        run_difficulty = False

def display_first_game():
    print('ok')

def display_second_game():
    global run_display
    while run_difficulty:
        reset_keys()
        check_events()
        check_input_difficulty()
        display.fill(BLACK)
        draw_text('Choose difficulty', 20, DISPLAY_W / 2, DISPLAY_H / 2 - 20)
        draw_text("Easy", 20, First_x, First_y)
        draw_text("Medium", 20, Second_x, Second_y)
        draw_text("Hard", 20, Third_x, Third_y)
        draw_cursor()
        blit_screen()
def display_third_game():
    pass

def game_loop():
    global playing
    while playing:
        check_events()
        if START_KEY:
            playing = False
        display.fill(BLACK)
        draw_text('Thanks for Playing', 20, DISPLAY_W / 2, DISPLAY_H / 2)
        window.blit(display, (0, 0))
        pygame.display.update()
        reset_keys()


def check_events(): #verifica ce apasa playerul pe tastatura
    global run_difficulty, run_display
    global running, playing, UP_KEY, DOWN_KEY, START_KEY, BACK_KEY
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running, playing, run_difficulty, run_display = False, False, False, False
            # pygame.quit()
            # sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN: #enter
                START_KEY = True
            if event.key == pygame.K_ESCAPE:
                BACK_KEY = True
            if event.key == pygame.K_DOWN:
                DOWN_KEY = True
            if event.key == pygame.K_UP:
                UP_KEY = True


def reset_keys(): #resetez butoanele
    global UP_KEY, DOWN_KEY, START_KEY, BACK_KEY
    UP_KEY, DOWN_KEY, START_KEY, BACK_KEY = False, False, False, False


def main():
    display_menu()
    game_loop()

if __name__ == "__main__":
    main()
