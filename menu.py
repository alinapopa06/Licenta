import pygame
import sys
from instructions import Instructions


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
    BLACK = (255, 255, 255)
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
    TITLE = "Main menu"
    state = "dbscan"

    First_x, First_y = MID_WIDTH, MID_HEIGHT - 20
    Second_x, Second_y = MID_WIDTH, MID_HEIGHT
    Third_x, Third_y = MID_WIDTH, MID_HEIGHT + 20
    Fourth_x, Fourth_y = MID_WIDTH, MID_HEIGHT + 40
    Fifth_x, Fifth_y = MID_WIDTH, MID_HEIGHT + 60
    Sixth_x, Sixth_y = MID_WIDTH, MID_HEIGHT + 80
    # cursor_rect.center = (First_x + offset, First_y)
    display = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    button_dbscan = pygame.Rect(MID_WIDTH - 60, MID_HEIGHT - 30, 120, 20)
    button_adaboost = pygame.Rect(MID_WIDTH - 65, MID_HEIGHT - 10, 130, 20)
    button_lr = pygame.Rect(MID_WIDTH - 95, MID_HEIGHT + 10, 190, 20)
    button_kmeans = pygame.Rect(MID_WIDTH - 110, MID_HEIGHT + 30, 220, 20)
    button_knn = pygame.Rect(MID_WIDTH - 120, MID_HEIGHT + 50, 240, 20)
    button_svm = pygame.Rect(MID_WIDTH - 130, MID_HEIGHT + 70, 260, 20)

    def initialize_game(self):
        pygame.init()
        pygame.display.set_caption(self.TITLE)
        self.window.fill(self.GREY)
        self.draw_cursor(eval(f'self.button_{self.state.lower()}'))
        self.draw_text('Main menu', self.BLACK, 20, self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2 + self.offset)
        self.draw_text("DBSCAN", self.BLACK, 20, self.First_x, self.First_y)
        self.draw_text("AdaBoost", self.BLACK, 20, self.Second_x, self.Second_y)
        self.draw_text("Linear regression", self.BLACK, 20, self.Third_x, self.Third_y)
        self.draw_text("k-means clustering", self.BLACK, 20, self.Fourth_x, self.Fourth_y)
        self.draw_text("k-nearest neighbours", self.BLACK, 20, self.Fifth_x, self.Fifth_y)
        self.draw_text("Support vector machine", self.BLACK, 20, self.Sixth_x, self.Sixth_y)
        return self.window

    def draw_text(self, text, color, size, x, y):
        font_draw = pygame.font.Font(pygame.font.get_default_font(), size)
        text_obj = font_draw.render(text, True, color)
        text_rect = text_obj.get_rect()
        text_rect.center = (x, y)
        self.window.blit(text_obj, text_rect)

    def draw_cursor(self, cursor_rect):
        self.draw_text('-', self.LIGHTGREY, 50, cursor_rect.right, cursor_rect.centery)
        self.draw_text('-', self.LIGHTGREY, 50, cursor_rect.left, cursor_rect.centery)

    def delete_cursor(self, cursor_rect):
        self.draw_text('-', self.GREY, 60, cursor_rect.right, cursor_rect.centery)
        self.draw_text('-', self.GREY, 60, cursor_rect.left, cursor_rect.centery)

    def menu(self, user_id):
        self.initialize_game()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_adaboost.collidepoint(pygame.mouse.get_pos()):
                        Instructions().draw_instr('adaboost', user_id)
                        self.state = 'adaboost'
                        self.initialize_game()
                    if self.button_dbscan.collidepoint(pygame.mouse.get_pos()):
                        Instructions().draw_instr('dbscan', user_id)
                        self.state = 'dbscan'
                        self.initialize_game()
                    if self.button_lr.collidepoint(pygame.mouse.get_pos()):
                        Instructions().draw_instr('lr', user_id)
                        self.state = 'lr'
                        self.initialize_game()
                    if self.button_kmeans.collidepoint(pygame.mouse.get_pos()):
                        Instructions().draw_instr('kmeans', user_id)
                        self.state = 'kmeans'
                        self.initialize_game()
                    if self.button_knn.collidepoint(pygame.mouse.get_pos()):
                        Instructions().draw_instr('knn', user_id)
                        self.state = 'knn'
                        self.initialize_game()
                    if self.button_svm.collidepoint(pygame.mouse.get_pos()):
                        Instructions().draw_instr('svm', user_id)
                        self.state = 'svm'
                        self.initialize_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_RETURN:  # enter
                        if self.state == 'dbscan':
                            Instructions().draw_instr('dbscan', user_id)
                            self.initialize_game()
                        elif self.state == 'adaboost':
                            Instructions().draw_instr('adaboost', user_id)
                            self.initialize_game()
                        elif self.state == 'kmeans':
                            Instructions().draw_instr('kmeans', user_id)
                            self.initialize_game()
                        elif self.state == 'lr':
                            Instructions().draw_instr('lr', user_id)
                            self.initialize_game()
                        elif self.state == 'knn':
                            Instructions().draw_instr('knn', user_id)
                            self.initialize_game()
                        elif self.state == 'svm':
                            Instructions().draw_instr('svm', user_id)
                            self.initialize_game()
                    if event.key == pygame.K_DOWN:
                        if self.state == 'dbscan':
                            self.delete_cursor(self.button_dbscan)
                            self.draw_cursor(self.button_adaboost)
                            self.state = 'adaboost'
                        elif self.state == 'adaboost':
                            self.delete_cursor(self.button_adaboost)
                            self.draw_cursor(self.button_lr)
                            self.state = 'lr'
                        elif self.state == 'lr':
                            self.delete_cursor(self.button_lr)
                            self.draw_cursor(self.button_kmeans)
                            self.state = 'kmeans'
                        elif self.state == 'kmeans':
                            self.delete_cursor(self.button_kmeans)
                            self.draw_cursor(self.button_knn)
                            self.state = 'knn'
                        elif self.state == 'knn':
                            self.delete_cursor(self.button_knn)
                            self.draw_cursor(self.button_svm)
                            self.state = 'svm'
                        elif self.state == 'svm':
                            self.delete_cursor(self.button_svm)
                            self.draw_cursor(self.button_dbscan)
                            self.state = 'dbscan'
                    if event.key == pygame.K_UP:
                        if self.state == 'dbscan':
                            self.delete_cursor(self.button_dbscan)
                            self.draw_cursor(self.button_svm)
                            self.state = 'svm'
                        elif self.state == 'adaboost':
                            self.delete_cursor(self.button_adaboost)
                            self.draw_cursor(self.button_dbscan)
                            self.state = 'dbscan'
                        elif self.state == 'lr':
                            self.delete_cursor(self.button_lr)
                            self.draw_cursor(self.button_adaboost)
                            self.state = 'adaboost'
                        elif self.state == 'kmeans':
                            self.delete_cursor(self.button_kmeans)
                            self.draw_cursor(self.button_lr)
                            self.state = 'lr'
                        elif self.state == 'knn':
                            self.delete_cursor(self.button_knn)
                            self.draw_cursor(self.button_kmeans)
                            self.state = 'kmeans'
                        elif self.state == 'svm':
                            self.delete_cursor(self.button_svm)
                            self.draw_cursor(self.button_knn)
                            self.state = 'knn'
                # pygame.draw.rect(self.window, self.BLUE, self.button_adaboost)
                # pygame.draw.rect(self.window, self.BLUE, self.button_dbscan)
                # pygame.draw.rect(self.window, self.BLUE, self.button_lr)
                # pygame.draw.rect(self.window, self.BLUE, self.button_kmeans)
                # pygame.draw.rect(self.window, self.BLUE, self.button_knn)
                # pygame.draw.rect(self.window, self.BLUE, self.button_svm)
            # self.initialize_game()
            pygame.display.update()


# if __name__ == "__main__":
#     # Menu().initialize_game()
#     Menu().menu()


