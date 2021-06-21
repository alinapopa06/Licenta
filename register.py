import sys
import pygame
from menu import Menu
from login import Login
import sqlite3

class Register:
    TITLE = "Register"
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

    offset = - 100

    First_x, First_y = MID_WIDTH, MID_HEIGHT - 20
    Second_x, Second_y = MID_WIDTH, MID_HEIGHT
    Third_x, Third_y = MID_WIDTH, MID_HEIGHT + 20
    Fourth_x, Fourth_y = MID_WIDTH, MID_HEIGHT + 40
    Fifth_x, Fifth_y = MID_WIDTH, MID_HEIGHT + 60
    Sixth_x, Sixth_y = MID_WIDTH, MID_HEIGHT + 80
    # cursor_rect.center = (First_x + offset, First_y)
    display = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    button_dbscan = pygame.Rect(MID_WIDTH - 210, MID_HEIGHT - 120, 200, 40)
    button_adaboost = pygame.Rect(MID_WIDTH + 10, MID_HEIGHT - 120, 200, 40)
    button_lr = pygame.Rect(MID_WIDTH - 150, MID_HEIGHT - 60, 300, 40)
    button_kmeans = pygame.Rect(MID_WIDTH - 150, MID_HEIGHT, 300, 40)
    button_knn = pygame.Rect(MID_WIDTH - 150, MID_HEIGHT + 60, 300, 40)
    button_enter = pygame.Rect(150, 400, 190, 40)
    button_login = pygame.Rect(150, 455, 190, 20)
    button_noacc = pygame.Rect(140, 480, 210, 20)

    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    create_table = """CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT, last_name TEXT,
            email TEXT, password TEXT, score_AdaBoost REAL, score_K_Means REAL, score_KNN REAL, score_Linear_regression REAL, score_SVM REAL)"""
    cursor.execute(create_table)

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

    def main(self):
        self.initialize_game()
        pygame.init()
        font = pygame.font.Font(None, 35)
        run = True
        self.draw_text('Register:', self.WHITE, 30, 240, 120)
        pygame.draw.rect(self.window, self.BLUE, self.button_adaboost)
        pygame.draw.rect(self.window, self.BLUE, self.button_dbscan)
        pygame.draw.rect(self.window, self.BLUE, self.button_lr)
        pygame.draw.rect(self.window, self.BLUE, self.button_kmeans)
        pygame.draw.rect(self.window, self.BLUE, self.button_knn)
        pygame.draw.rect(self.window, self.BLUE, self.button_enter)
        self.draw_text('First name', self.WHITE, 20, self.button_dbscan.centerx - 40, self.button_dbscan.centery)
        self.draw_text('Last name', self.WHITE, 20, self.button_adaboost.centerx - 40, self.button_adaboost.centery)
        self.draw_text('Email', self.WHITE, 20, self.button_lr.centerx - 110, self.button_lr.centery)
        self.draw_text('Password', self.WHITE, 20, self.button_kmeans.centerx - 90, self.button_kmeans.centery)
        self.draw_text('Confirm password', self.WHITE, 20, self.button_knn.centerx - 50, self.button_knn.centery)
        self.draw_text('Confirm', self.WHITE, 25, 240, 420)
        self.draw_text('I already have an account', self.WHITE, 15, 245, 465)
        self.draw_text('Continue without an account', self.WHITE, 15, 245, 490)
        while run:
            for event in pygame.event.get():
                if self.button_login.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                    Login().main()
                    self.first_name = ""
                    self.last_name = ''
                    self.password = ''
                    self.cf_pass = ''
                    self.email = ''
                    return
                if self.button_enter.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                    params = (self.email, self.first_name, self.last_name, self.password)
                    self.cursor.execute("INSERT INTO users VALUES (NULL, ?, ?, ?, ?, NULL, NULL, NULL, NULL, NULL)", params)
                    self.connection.commit()
                    self.cursor.execute("SELECT * FROM users")
                    results = self.cursor.fetchall()
                    self.window.fill(self.GREY)
                    Login().main()
                    self.first_name = ''
                    self.last_name = ''
                    self.password = ''
                    self.cf_pass = ''
                    self.email = ''
                if self.button_noacc.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                    self.window.fill(self.GREY)
                    self.cursor.execute("SELECT user_id FROM users")
                    self.id = self.cursor.fetchall()[0][0]
                    Menu().menu(self.id)
                    self.first_name = ""
                    self.last_name = ''
                    self.password = ''
                    self.cf_pass = ''
                    self.email = ''
                    run = False
                if self.button_dbscan.collidepoint(pygame.mouse.get_pos()):
                    if event.type == pygame.KEYDOWN:
                        pygame.draw.rect(self.window, self.BLUE, self.button_dbscan)
                        if event.unicode.isalpha():
                            self.first_name += event.unicode
                            block = font.render(self.first_name, True, self.WHITE)
                            self.window.blit(block, (self.button_dbscan.left, self.button_dbscan.centery - 10))
                        elif event.key == pygame.K_BACKSPACE:
                            self.first_name = self.first_name[:-1]
                            pygame.draw.rect(self.window, self.BLUE, self.button_dbscan)
                            block = font.render(self.first_name, True, self.WHITE)
                            self.window.blit(block, (self.button_dbscan.left, self.button_dbscan.centery - 10))
                            # block = font.render(self.name, True, self.WHITE)
                            # self.window.blit(block, self.button_dbscan.center)
                            # print(self.name)
                elif self.button_adaboost.collidepoint(pygame.mouse.get_pos()):
                    if event.type == pygame.KEYDOWN:
                        pygame.draw.rect(self.window, self.BLUE, self.button_adaboost)
                        if event.unicode:
                            self.last_name += event.unicode
                            block = font.render(self.last_name, True, self.WHITE)
                            self.window.blit(block, (self.button_adaboost.left, self.button_adaboost.centery - 10))
                        elif event.key == pygame.K_BACKSPACE:
                            self.last_name = self.last_name[:-1]
                            pygame.draw.rect(self.window, self.BLUE, self.button_adaboost)
                            block = font.render(self.last_name, True, self.WHITE)
                            self.window.blit(block, (self.button_adaboost.left, self.button_adaboost.centery - 10))
                if self.button_lr.collidepoint(pygame.mouse.get_pos()):
                    if event.type == pygame.KEYDOWN:
                        pygame.draw.rect(self.window, self.BLUE, self.button_lr)
                        if event.unicode.isalpha():
                            self.email += event.unicode
                            block = font.render(self.email, True, self.WHITE)
                            self.window.blit(block, (self.button_lr.left, self.button_lr.centery - 10))
                        elif event.key == pygame.K_BACKSPACE:
                            self.email = self.email[:-1]
                            pygame.draw.rect(self.window, self.BLUE, self.button_lr)
                            block = font.render(self.email, True, self.WHITE)
                            self.window.blit(block, (self.button_lr.left, self.button_lr.centery - 10))
                if self.button_kmeans.collidepoint(pygame.mouse.get_pos()):
                    if event.type == pygame.KEYDOWN:
                        pygame.draw.rect(self.window, self.BLUE, self.button_kmeans)
                        if event.unicode.isalpha():
                            self.password += event.unicode
                            passs = len(self.password) * '*'
                            block = font.render(passs, True, self.WHITE)
                            self.window.blit(block, (self.button_kmeans.left, self.button_kmeans.centery - 10))
                        elif event.key == pygame.K_BACKSPACE:
                            self.password = self.password[:-1]
                            pygame.draw.rect(self.window, self.BLUE, self.button_kmeans)
                            passs = len(self.password) * '*'
                            block = font.render(passs, True, self.WHITE)
                            self.window.blit(block, (self.button_kmeans.left, self.button_kmeans.centery - 10))
                if self.button_knn.collidepoint(pygame.mouse.get_pos()):
                    if event.type == pygame.KEYDOWN:
                        pygame.draw.rect(self.window, self.BLUE, self.button_knn)
                        if event.unicode.isalpha():
                            self.cf_pass += event.unicode
                            cf_passs = len(self.cf_pass) * '*'
                            block = font.render(cf_passs, True, self.WHITE)
                            self.window.blit(block, (self.button_knn.left, self.button_knn.centery - 10))
                        elif event.key == pygame.K_BACKSPACE:
                            self.cf_pass = self.cf_pass[:-1]
                            pygame.draw.rect(self.window, self.BLUE, self.button_knn)
                            cf_passs = len(self.cf_pass) * '*'
                            block = font.render(cf_passs, True, self.WHITE)
                            self.window.blit(block, (self.button_knn.left, self.button_knn.centery - 10))
                elif event.type == pygame.QUIT:
                    return
            pygame.display.update()

if __name__ == "__main__":
    Register().main()
