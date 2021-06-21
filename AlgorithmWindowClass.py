import pygame
import sqlite3

class AlgorithmWindowClass:
    SCREEN_WIDTH = 480
    SCREEN_HEIGHT = 560

    NUMBER_OF_BLOCKS_WIDE = 12
    NUMBER_OF_BLOCKS_HIGH = 12
    BLOCK_HEIGHT = round(SCREEN_HEIGHT / NUMBER_OF_BLOCKS_HIGH)
    BLOCK_WIDTH = round(SCREEN_WIDTH / NUMBER_OF_BLOCKS_WIDE)

    UP = 90
    DOWN = -90
    RIGHT = 1
    MIDDLE = 2
    LEFT = 3

    GREY = (150, 150, 150)
    RED = (255, 0, 0)
    BLUE = (55, 55, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 200, 0)
    DARKGREY = (200, 200, 200)
    LIGHTGREY = (210, 210, 210)
    UGLY_PINK = (255, 0, 255)
    BROWN = (153, 76, 0)
    GOLD = (153, 153, 0)
    DARKGREEN = (0, 102, 0)
    DARKORANGE = (255, 128, 0)
    WHITE = (255, 255, 255)

    COLOR_LIST = [RED, BLUE, GREEN, GOLD, DARKGREEN, DARKORANGE, DARKGREY, LIGHTGREY, UGLY_PINK, BROWN, GREY, BLACK]

    VEL = 5

    points = []
    pixel_points = []

    TITLE = ""

    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    all = pygame.Rect(40, 0, 480, 468)
    button_back = pygame.Rect(0, 510, 160, 60)  # left #top #width #height
    button_draw = pygame.Rect(160, 510, 80, 60)  # left #top #width #height
    button_check = pygame.Rect(240, 510, 80, 60)  # left #top #width #height
    button_retry = pygame.Rect(320, 510, 160, 60)  # left #top #width #height
    button_leaderboard = pygame.Rect(0, 0, 0, 0)

    def __init__(self):
        self.display = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.window = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

    def initialize_game(self):
        pygame.init()
        pygame.display.set_caption(self.TITLE)
        self.window.fill(self.WHITE)
        return self.window

    def draw_text(self, text, color, size, x, y):
        font_draw = pygame.font.Font(pygame.font.get_default_font(), size)
        text_obj = font_draw.render(text, True, color)
        text_rect = text_obj.get_rect()
        text_rect.center = (x, y)
        self.window.blit(text_obj, text_rect)

    def draw_grid(self):
        pygame.draw.rect(self.window, self.LIGHTGREY, self.button_back)
        pygame.draw.rect(self.window, self.LIGHTGREY, self.button_draw)
        pygame.draw.rect(self.window, self.LIGHTGREY, self.button_check)
        pygame.draw.rect(self.window, self.LIGHTGREY, self.button_retry)
        pygame.draw.line(self.window, self.BLACK, (0, 510), (510, 510), 2)
        pygame.draw.line(self.window, self.BLACK, (0, 558), (558, 558), 2)
        pygame.draw.line(self.window, self.BLACK, (158, 510), (158, 558), 2)
        pygame.draw.line(self.window, self.BLACK, (238, 510), (238, 558), 2)
        pygame.draw.line(self.window, self.BLACK, (318, 510), (318, 558), 2)
        self.draw_text('Back', self.BLACK, 20, 76, 534)
        self.draw_text('Draw', self.BLACK, 20, 198, 534)
        self.draw_text('Check', self.BLACK, 20, 278, 534)
        self.draw_text('Retry', self.BLACK, 20, 396, 534)

        for i in range(self.NUMBER_OF_BLOCKS_WIDE):
            new_height = round(i * self.BLOCK_HEIGHT)
            new_width = round(i * self.BLOCK_WIDTH)
            pygame.draw.line(self.window, self.DARKGREY, (self.BLOCK_WIDTH, new_height - self.BLOCK_HEIGHT * 2),
                             (self.SCREEN_WIDTH, new_height - self.BLOCK_HEIGHT * 2), 2)
            pygame.draw.line(self.window, self.DARKGREY, (new_width, 0), (new_width, self.SCREEN_HEIGHT - self.BLOCK_HEIGHT * 2), 2)
            pygame.draw.line(self.window, self.BLACK, (0, self.SCREEN_HEIGHT - self.BLOCK_HEIGHT * 2),
                             (self.SCREEN_WIDTH, self.SCREEN_HEIGHT - self.BLOCK_HEIGHT * 2),
                             2)
            pygame.draw.line(self.window, self.BLACK, (self.BLOCK_WIDTH, 0), (self.BLOCK_WIDTH, self.SCREEN_HEIGHT - self.BLOCK_HEIGHT), 2)

        self.draw_text('y', self.BLACK, 20, self.BLOCK_WIDTH / 2, self.BLOCK_HEIGHT / 2 - 10)
        self.draw_text('x', self.BLACK, 20, self.SCREEN_WIDTH - self.BLOCK_WIDTH / 2 - 10, self.SCREEN_HEIGHT - self.BLOCK_HEIGHT * 2 + 20)
        self.draw_text('0', self.BLACK, 20, self.BLOCK_WIDTH / 2, self.SCREEN_HEIGHT - self.BLOCK_HEIGHT / 2 - self.BLOCK_HEIGHT)

        t, k = 1, 11
        while t < 10 and k > 0:
            self.draw_text(str(t), self.BLACK, 20, self.BLOCK_WIDTH / 2, self.BLOCK_HEIGHT + self.BLOCK_HEIGHT * (k - 2) - self.BLOCK_HEIGHT)
            self.draw_text(str(t), self.BLACK, 20, self.BLOCK_WIDTH + self.BLOCK_WIDTH * t, self.SCREEN_HEIGHT - self.BLOCK_HEIGHT / 2 - self.BLOCK_HEIGHT)
            t += 1
            k -= 1

    def draw_map(self, user_id):
        # TODO: To be implemented with every child class
        pass

    def main(self, user_id):
        self.initialize_game()
        self.draw_grid()
        self.draw_map(user_id)
