import pygame
import sys
from instructions import Instructions
import string


class Menu:
    SCREEN_WIDTH = 480
    SCREEN_HEIGHT = 560

    MID_HEIGHT = SCREEN_HEIGHT / 2
    MID_WIDTH = SCREEN_WIDTH / 2

    RIGHT = 1
    MIDDLE = 2
    LEFT = 3

    GREY = (50, 50, 50)
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

    VEL = 5
    offset = - 100
    TITLE = "Main menu"
    cursor_rect = pygame.Rect(0, 0, 20, 20)

    First_x, First_y = MID_WIDTH, MID_HEIGHT - 20
    Second_x, Second_y = MID_WIDTH, MID_HEIGHT
    Third_x, Third_y = MID_WIDTH, MID_HEIGHT + 20
    Fourth_x, Fourth_y = MID_WIDTH, MID_HEIGHT + 40
    Fifth_x, Fifth_y = MID_WIDTH, MID_HEIGHT + 60
    Sixth_x, Sixth_y = MID_WIDTH, MID_HEIGHT + 80
    cursor_rect.center = (First_x + offset, First_y)
    display = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    button_dbscan = pygame.Rect(MID_WIDTH - 30, MID_HEIGHT - 30, 50, 20)
    button_adaboost = pygame.Rect(MID_WIDTH - 50, MID_HEIGHT - 10, 100, 20)
    button_lr = pygame.Rect(MID_WIDTH - 90, MID_HEIGHT + 10, 180, 20)
    button_kmeans = pygame.Rect(MID_WIDTH - 100, MID_HEIGHT + 30, 200, 20)
    button_knn = pygame.Rect(MID_WIDTH - 105, MID_HEIGHT + 50, 210, 20)
    button_svm = pygame.Rect(MID_WIDTH - 120, MID_HEIGHT + 70, 240, 20)

    def initialize_game(self):
        pygame.init()
        pygame.display.set_caption(self.TITLE)
        self.window.fill(self.BLACK)
        return self.window

    def draw_text(self, text, color, size, x, y):
        font_draw = pygame.font.Font(pygame.font.get_default_font(), size)
        text_obj = font_draw.render(text, True, color)
        text_rect = text_obj.get_rect()
        text_rect.center = (x, y)
        self.window.blit(text_obj, text_rect)

    def draw_cursor(self):
        self.draw_text('-', self.WHITE, 35, self.cursor_rect.x - 20, self.cursor_rect.y + 10)
        self.draw_text('-', self.WHITE, 35, self.cursor_rect.x + 240, self.cursor_rect.y + 10)

    def menu(self):
        self.initialize_game()
        state = "DBSCAN"
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_adaboost.collidepoint(pygame.mouse.get_pos()):
                        Instructions().draw_instr('adaboost')
                    if self.button_dbscan.collidepoint(pygame.mouse.get_pos()):
                        Instructions().draw_instr('dbscan')
                    if self.button_lr.collidepoint(pygame.mouse.get_pos()):
                        Instructions().draw_instr('lr')
                    if self.button_kmeans.collidepoint(pygame.mouse.get_pos()):
                        Instructions().draw_instr('kmeans')
                    if self.button_knn.collidepoint(pygame.mouse.get_pos()):
                        Instructions().draw_instr('knn')
                    if self.button_svm.collidepoint(pygame.mouse.get_pos()):
                        Instructions().draw_instr('svm')
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_RETURN:  # enter
                        if state == 'DBSCAN':
                            Instructions().draw_instr('DBSCAN')
                        elif state == 'AdaBoost':
                            Instructions().draw_instr('AdaBoost')
                        elif state == 'k-means clustering':
                            Instructions().draw_instr('kmeans')
                        elif state == 'Linear regression':
                            Instructions().draw_instr('lr')
                        elif state == 'k-nearest neighbours':
                            Instructions().draw_instr('knn')
                        elif state == 'Support vector machine':
                            Instructions().draw_instr('svm')
                    if event.key == pygame.K_DOWN:
                        if state == 'DBSCAN':
                            self.cursor_rect.center = (self.Second_x + self.offset, self.Second_y)
                            state = 'AdaBoost'
                        elif state == 'AdaBoost':
                            self.cursor_rect.center = (self.Third_x + self.offset, self.Third_y)
                            state = 'Linear regression'
                        elif state == 'Linear regression':
                            self.cursor_rect.center = (self.Fourth_x + self.offset, self.Fourth_y)
                            state = 'k-means clustering'
                        elif state == 'k-means clustering':
                            self.cursor_rect.center = (self.Fifth_x + self.offset, self.Fifth_y)
                            state = 'k-nearest neighbours'
                        elif state == 'k-nearest neighbours':
                            self.cursor_rect.center = (self.Sixth_x + self.offset, self.Sixth_y)
                            state = 'Support vector machine'
                        elif state == 'Support vector machine':
                            self.cursor_rect.center = (self.First_x + self.offset, self.First_y)
                            state = 'DBSCAN'
                    if event.key == pygame.K_UP:
                        if state == 'DBSCAN':
                            self.cursor_rect.center = (self.Sixth_x + self.offset, self.Sixth_y)
                            state = 'Support vector machine'
                        elif state == 'AdaBoost':
                            self.cursor_rect.center = (self.First_x + self.offset, self.First_y)
                            state = 'DBSCAN'
                        elif state == 'Linear regression':
                            self.cursor_rect.center = (self.Second_x + self.offset, self.Second_y)
                            state = 'AdaBoost'
                        elif state == 'k-means clustering':
                            self.cursor_rect.center = (self.Third_x + self.offset, self.Third_y)
                            state = 'Linear regression'
                        elif state == 'k-nearest neighbours':
                            self.cursor_rect.center = (self.Fourth_x + self.offset, self.Fourth_y)
                            state = 'k-means clustering'
                        elif state == 'Support vector machine':
                            self.cursor_rect.center = (self.Fifth_x + self.offset, self.Fifth_y)
                            state = 'k-nearest neighbours'
                self.blit_screen()
                pygame.display.update()

    def blit_screen(self):
        self.window.blit(self.display, (0, 0))
        self.draw_cursor()
        # pygame.draw.rect(self.window, self.BLUE, self.button_id3)
        # pygame.draw.rect(self.window, self.BLUE, self.button_dbscan)
        # pygame.draw.rect(self.window, self.BLUE, self.button_lr)
        # pygame.draw.rect(self.window, self.BLUE, self.button_kmeans)
        # pygame.draw.rect(self.window, self.BLUE, self.button_knn)
        # pygame.draw.rect(self.window, self.BLUE, self.button_svm)
        self.draw_text('Main menu', self.WHITE, 20, self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2 + self.offset)
        self.draw_text("DBSCAN", self.WHITE, 20, self.First_x, self.First_y)
        self.draw_text("AdaBoost", self.WHITE, 20, self.Second_x, self.Second_y)
        self.draw_text("Linear regression", self.WHITE, 20, self.Third_x, self.Third_y)
        self.draw_text("k-means clustering", self.WHITE, 20, self.Fourth_x, self.Fourth_y)
        self.draw_text("k-nearest neighbours", self.WHITE, 20, self.Fifth_x, self.Fifth_y)
        self.draw_text("Support vector machine", self.WHITE, 20, self.Sixth_x, self.Sixth_y)

        pygame.display.update()

    # def main():
    #     initialize_game()
    #     menu()

if __name__ == "__main__":
    Menu().menu()


