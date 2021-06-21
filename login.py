import sys
import pygame
import sqlite3
from menu import Menu

class Login:
    TITLE = "Login"
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
    button_email = pygame.Rect(MID_WIDTH - 150, MID_HEIGHT - 60, 300, 40)
    button_password = pygame.Rect(MID_WIDTH - 150, MID_HEIGHT, 300, 40)
    button_confirm = pygame.Rect(MID_WIDTH - 80, MID_HEIGHT + 60, 150, 40)
    button_noacc = pygame.Rect(130, 400, 210, 20)
    # id = 0
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

    def main(self):
        self.initialize_game()
        pygame.init()
        font = pygame.font.Font(None, 35)
        run = True
        self.draw_text('Log in:', self.WHITE, 30, 240, 140)

        pygame.draw.rect(self.window, self.BLUE, self.button_email)
        pygame.draw.rect(self.window, self.BLUE, self.button_password)
        pygame.draw.rect(self.window, self.BLUE, self.button_confirm)
        pygame.draw.rect(self.window, self.BLUE, self.button_noacc)
        self.draw_text('Email', self.WHITE, 20, self.button_email.centerx - 110, self.button_email.centery)
        self.draw_text('Password', self.WHITE, 20, self.button_password.centerx - 90, self.button_password.centery)
        self.draw_text('Confirm', self.WHITE, 20, self.button_confirm.centerx, self.button_confirm.centery)
        self.draw_text('Continue without an account', self.WHITE, 15, self.button_noacc.centerx, self.button_noacc.centery)
        while run:
            for event in pygame.event.get():
                if self.button_noacc.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                    self.window.fill(self.GREY)
                    Menu().menu(self.id)
                    self.password = ''
                    self.email = ''
                if self.button_email.collidepoint(pygame.mouse.get_pos()):
                    if event.type == pygame.KEYDOWN:
                        pygame.draw.rect(self.window, self.BLUE, self.button_email)
                        if event.unicode.isalpha():
                            self.email += event.unicode
                            block = font.render(self.email, True, self.WHITE)
                            self.window.blit(block, (self.button_email.left, self.button_email.centery - 10))
                        elif event.key == pygame.K_BACKSPACE:
                            self.email = self.email[:-1]
                            pygame.draw.rect(self.window, self.BLUE, self.button_email)
                            block = font.render(self.email, True, self.WHITE)
                            self.window.blit(block, (self.button_email.left, self.button_email.centery - 10))
                if self.button_password.collidepoint(pygame.mouse.get_pos()):
                    if event.type == pygame.KEYDOWN:
                        pygame.draw.rect(self.window, self.BLUE, self.button_password)
                        if event.unicode.isalpha():
                            self.password += event.unicode
                            passs = len(self.password) * '*'
                            block = font.render(passs, True, self.WHITE)
                            self.window.blit(block, (self.button_password.left, self.button_password.centery - 10))
                        elif event.key == pygame.K_BACKSPACE:
                            self.password = self.password[:-1]
                            pygame.draw.rect(self.window, self.BLUE, self.button_password)
                            passs = len(self.password) * '*'
                            block = font.render(passs, True, self.WHITE)
                            self.window.blit(block, (self.button_password.left, self.button_password.centery - 10))
                if self.button_confirm.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                    self.cursor.execute("SELECT email, password FROM users")
                    results = self.cursor.fetchall()
                    for i in results:
                        if self.email == i[0] and self.password == i[1]:
                            paramss = (i[0], i[1])
                            self.cursor.execute("SELECT user_id FROM users WHERE email = ? AND password = ?", paramss)
                            self.id = self.cursor.fetchall()[0][0]
                            print(self.id)
                            self.window.fill(self.GREY)
                            Menu().menu(self.id)
                    else:
                        self.draw_text('Incorrect email and/or password', self.RED, 20, 250, 460)
                    self.password = ''
                    self.email = ''
                elif event.type == pygame.QUIT:
                    return
            pygame.display.update()


if __name__ == "__main__":
    Login().main()
