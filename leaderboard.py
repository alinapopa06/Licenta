import sys
import pygame
import sqlite3

class Leaderbord:
    TITLE = "Leaderboard"
    backcolor = None
    first_name = ''
    last_name = ''
    email = ''
    password = ''
    cf_pass = ''
    SCREEN_WIDTH = 480
    SCREEN_HEIGHT = 560

    MID_HEIGHT = SCREEN_HEIGHT / 2
    MID_WIDTH = SCREEN_WIDTH / 2

    RIGHT = 1
    MIDDLE = 2
    LEFT = 3

    RED = (255, 0, 0)
    BLUE = (55, 55, 255)
    WHITE = (255, 255, 255)
    GREEN = (0, 200, 0)
    DARKGREY = (200, 200, 200)
    GREY = (100, 100, 100)
    LIGHTGREY = (200, 200, 200)
    UGLY_PINK = (255, 0, 255)
    BROWN = (153, 76, 0)
    GOLD = (153, 153, 0)
    DARKGREEN = (0, 102, 0)
    DARKORANGE = (255, 128, 0)
    BLACK = (0, 0, 0)

    display = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    button_1 = pygame.Rect(100, 130, 300, 30)
    button_2 = pygame.Rect(100, 170, 300, 30)
    button_3 = pygame.Rect(100, 210, 300, 30)
    button_4 = pygame.Rect(100, 250, 300, 30)
    button_5 = pygame.Rect(100, 290, 300, 30)
    button_6 = pygame.Rect(100, 330, 300, 30)
    button_7 = pygame.Rect(100, 370, 300, 30)
    button_8 = pygame.Rect(100, 410, 300, 30)
    button_9 = pygame.Rect(100, 450, 300, 30)
    button_10 = pygame.Rect(100, 490, 300, 30)

    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    def initialize_game(self):
        pygame.init()
        pygame.display.set_caption(self.TITLE)
        self.window.fill(self.GREY)
        return self.window

    def draw_text(self, text, color, size, x, y):
        font_draw = pygame.font.Font(pygame.font.get_default_font(), size)
        text_obj = font_draw.render(text, True, color)
        text_rect = text_obj.get_rect()
        text_rect.center = (x, y)
        self.window.blit(text_obj, text_rect)

    def main(self, TITLE):
        self.initialize_game()
        run = True
        self.cursor.execute(f"SELECT first_name, last_name, score_{TITLE} FROM users WHERE score_{TITLE} is not NULL order by score_{TITLE} desc LIMIT 10")
        results = self.cursor.fetchall()
        print(results)
        self.draw_text('Top 10 users', self.WHITE, 30, 250, 80)
        for i in results:
            self.draw_text(str(results.index(i) + 1) + '. ' + i[0] + ' ' + i[1] + ' ' + str(round(i[2], 2)) + '%', self.WHITE, 20, eval("self.button_{number}.centerx".format(number=(results.index(i) + 1))), eval("self.button_{number}.centery".format(number=results.index(i) + 1)))
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            pygame.display.update()

# if __name__ == "__main__":
#     Leaderbord().main()
