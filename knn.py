import sys
import pygame
from AlgorithmWindowClass import AlgorithmWindowClass
from math import sqrt
from leaderboard import Leaderbord

class AlgorithmKNN(AlgorithmWindowClass):
    TITLE = "KNN"
    name = ''
    dist = []
    all_points = dict()
    dict_points = dict()
    dict_label = dict()
    pink_point = []
    points_x = []
    points = []
    pixel_points = []
    pixel_points_red = []
    pixel_points_green = []
    GREY = (100, 100, 100)
    flag = 0


    def draw_knn(self, k, user_id):
        count_red = 0
        final_distance = 0
        count_green = 0
        distance = lambda x, y: sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)
        for i in self.points:
            for j in self.pink_point:
                self.dict_points[i] = distance(i, j)
        equal_distance = sorted(self.dict_points.items(), key=lambda x: x[1])[:1]
        self.dict_points = sorted(self.dict_points.items(), key=lambda x: x[1])[:k]

        for i in self.dict_points:
            pygame.draw.circle(self.window, self.BLACK, i[0], 10, 5)
            distances = []
            for j in self.points_x:
                distances.append(distance(i[0], j))
            final_distance += min(distances)

        for items in self.all_points.items():
            for c in self.dict_points:
                if items[0] == c[0]:
                    if items[1] == 0:
                        count_red += 1
                    elif items[1] == 1:
                        count_green += 1

        percent = 100 - final_distance / (k * 880) * 100

        if count_green > count_red:
            pygame.draw.circle(self.window, self.GREEN, self.pink_point[0], 10, 0)
            if self.flag == 0:
                percent /= 2
        elif count_green < count_red:
            pygame.draw.circle(self.window, self.RED, self.pink_point[0], 10, 0)
            if self.flag == 1:
                percent /= 2
        else:
            for items in self.all_points.items():
                for c in equal_distance:
                    if items[0] == c[0]:
                        if items[1] == 0:
                            pygame.draw.circle(self.window, self.RED, self.pink_point[0], 10, 0)
                        elif items[1] == 1:
                            pygame.draw.circle(self.window, self.GREEN, self.pink_point[0], 10, 0)
        if percent < 0:
            percent = 0
        elif percent > 100:
            percent = 100
        params = (percent, user_id)
        self.cursor.execute(f"SELECT score_{self.TITLE} from users WHERE user_id = ?", [user_id])
        scor = self.cursor.fetchall()[0][0]
        if scor is None:
            self.cursor.execute(f"UPDATE users SET score_{self.TITLE} = ? WHERE user_id = ?", params)
            self.connection.commit()
        elif scor < percent:
            self.cursor.execute(f"UPDATE users SET score_{self.TITLE} = ? WHERE user_id = ?", params)
            self.connection.commit()
        self.draw_text(f"Score: {percent:.2f}%", self.BLACK, 25, 385, 450)
        return percent

    def draw_grid(self):
        pygame.init()
        font = pygame.font.Font(None, 40)
        run = True
        button_back = pygame.Rect(0, 510, 240, 60)
        button_start = pygame.Rect(240, 510, 240, 60)
        while run:
            for event in pygame.event.get():
                if button_back.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                    self.name = ""
                    return
                if button_start.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                    self.draw_game_grid()
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.unicode.isnumeric():
                        self.name += event.unicode
                    elif event.key == pygame.K_BACKSPACE:
                        self.name = self.name[:-1]
                    if event.key == pygame.K_RETURN:
                        self.draw_game_grid()
                        run = False
                elif event.type == pygame.QUIT:
                    return
            self.window.fill((0, 0, 0))
            block = font.render(self.name, True, self.WHITE)
            rect = block.get_rect()
            rect.center = self.window.get_rect().center
            self.window.blit(block, rect)
            self.draw_text('Please enter your input:', self.WHITE, 20, rect.centerx, rect.centery - 50)
            pygame.draw.line(self.window, self.WHITE, rect.bottomright, rect.topright, 2)
            pygame.draw.line(self.window, self.LIGHTGREY, (0, 510), (510, 510), 2)
            pygame.draw.line(self.window, self.LIGHTGREY, (238, 510), (238, 558), 2)
            self.draw_text('Back', self.WHITE, 20, 118, 534)
            self.draw_text('Start', self.WHITE, 20, 358, 534)
            pygame.display.flip()

    def draw_game_grid(self):
        fade = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        fade.fill((255, 255, 255))
        for alpha in range(0, 255):
            fade.set_alpha(alpha)
            self.window.fill((0, 0, 0))
            self.window.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(1)
        self.window.fill(self.WHITE)
        pygame.display.update()
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
            pygame.draw.line(self.window, self.DARKGREY, (new_width, 0),
                             (new_width, self.SCREEN_HEIGHT - self.BLOCK_HEIGHT * 2), 2)
            pygame.draw.line(self.window, self.BLACK, (0, self.SCREEN_HEIGHT - self.BLOCK_HEIGHT * 2),
                             (self.SCREEN_WIDTH, self.SCREEN_HEIGHT - self.BLOCK_HEIGHT * 2),
                             2)
            pygame.draw.line(self.window, self.BLACK, (self.BLOCK_WIDTH, 0),
                             (self.BLOCK_WIDTH, self.SCREEN_HEIGHT - self.BLOCK_HEIGHT), 2)

        self.draw_text('y', self.BLACK, 20, self.BLOCK_WIDTH / 2, self.BLOCK_HEIGHT / 2 - 10)
        self.draw_text('x', self.BLACK, 20, self.SCREEN_WIDTH - self.BLOCK_WIDTH / 2 - 10,
                       self.SCREEN_HEIGHT - self.BLOCK_HEIGHT * 2 + 20)
        self.draw_text('0', self.BLACK, 20, self.BLOCK_WIDTH / 2,
                       self.SCREEN_HEIGHT - self.BLOCK_HEIGHT / 2 - self.BLOCK_HEIGHT)

        t, k = 1, 11
        while t < 10 and k > 0:
            self.draw_text(str(t), self.BLACK, 20, self.BLOCK_WIDTH / 2,
                           self.BLOCK_HEIGHT + self.BLOCK_HEIGHT * (k - 2) - self.BLOCK_HEIGHT)
            self.draw_text(str(t), self.BLACK, 20, self.BLOCK_WIDTH + self.BLOCK_WIDTH * t,
                           self.SCREEN_HEIGHT - self.BLOCK_HEIGHT / 2 - self.BLOCK_HEIGHT)
            t += 1
            k -= 1
        pygame.display.update()

    def draw_map(self, user_id):
        self.draw_game_grid()
        draw_point_enabled = True
        leader = False
        draw_pink_enabled = False
        draw_circle_enabled = False
        draw_decision_enabled = False
        draw_enabled = True
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == self.LEFT and draw_point_enabled:
                    x1, y1, w, h = self.all
                    x2, y2 = x1 + w, y1 + h
                    x, y = event.pos
                    if x1 < x < x2:
                        if y1 < y < y2:
                            pygame.draw.circle(self.window, self.GREEN, event.pos, 5, 0)
                            self.pixel_points_green.append(event.pos)
                            self.points.append(event.pos)
                            self.all_points[event.pos] = 1
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == self.RIGHT and draw_point_enabled:
                    x1, y1, w, h = self.all
                    x2, y2 = x1 + w, y1 + h
                    x, y = event.pos
                    if x1 < x < x2:
                        if y1 < y < y2:
                            pygame.draw.circle(self.window, self.RED, event.pos, 5, 0)
                            self.pixel_points_red.append(event.pos)
                            self.points.append(event.pos)
                            self.all_points[event.pos] = 0
                if self.button_draw.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN \
                        and draw_enabled:
                    draw_point_enabled = False
                    draw_pink_enabled = True
                    draw_decision_enabled = False
                    draw_circle_enabled = False
                elif event.type == pygame.MOUSEBUTTONDOWN and draw_pink_enabled \
                        and not draw_circle_enabled and not draw_decision_enabled:
                    x1, y1, w, h = self.all
                    x2, y2 = x1 + w, y1 + h
                    x, y = event.pos
                    if x1 < x < x2:
                        if y1 < y < y2:
                            if len(self.pink_point) == 0:
                                self.pink_point.append(event.pos)
                            pygame.draw.circle(self.window, self.UGLY_PINK, event.pos, 5, 0)
                            draw_pink_enabled = False
                            draw_circle_enabled = True
                            draw_point_enabled = False
                            draw_decision_enabled = False
                            draw_enabled = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not draw_pink_enabled \
                        and draw_circle_enabled and not draw_decision_enabled:
                    x1, y1, w, h = self.all
                    x2, y2 = x1 + w, y1 + h
                    x, y = event.pos
                    if x1 < x < x2:
                        if y1 < y < y2:
                            self.draw_text('x', self.BLACK, 15, event.pos[0], event.pos[1])
                            self.points_x.append(event.pos)
                            if len(self.points_x) == int(self.name):
                                draw_decision_enabled = True
                                draw_circle_enabled = False
                                draw_pink_enabled = False
                                draw_point_enabled = False
                                draw_enabled = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == self.LEFT and not draw_pink_enabled \
                        and not draw_circle_enabled and draw_decision_enabled:
                    x1, y1, w, h = self.all
                    x2, y2 = x1 + w, y1 + h
                    x, y = event.pos
                    if x1 < x < x2:
                        if y1 < y < y2:
                            self.draw_text('+', self.BLACK, 20, event.pos[0], event.pos[1])
                            self.flag = 1
                            draw_decision_enabled = False
                            draw_circle_enabled = False
                            draw_pink_enabled = False
                            draw_point_enabled = False
                            draw_enabled = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == self.RIGHT and not draw_pink_enabled \
                        and not draw_circle_enabled and draw_decision_enabled:
                    x1, y1, w, h = self.all
                    x2, y2 = x1 + w, y1 + h
                    x, y = event.pos
                    if x1 < x < x2:
                        if y1 < y < y2:
                            self.draw_text('-', self.BLACK, 20, event.pos[0], event.pos[1])
                            self.flag = 0
                            draw_decision_enabled = False
                            draw_circle_enabled = False
                            draw_pink_enabled = False
                            draw_point_enabled = False
                            draw_enabled = False
                if self.button_check.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN \
                        and not draw_point_enabled and leader is not True:
                    self.draw_knn(int(self.name), user_id)
                    draw_decision_enabled = False
                    draw_circle_enabled = False
                    draw_pink_enabled = False
                    draw_point_enabled = False
                    draw_enabled = False
                    self.points_x = []
                    self.points = []
                    self.pink_point = []
                    self.pixel_points_red = []
                    self.pixel_points_green = []
                    self.pixel_points = []
                    self.name = ""
                    self.dict_points = dict()
                    self.button_leaderboard = pygame.Rect(160, 510, 160, 60)  # left #top #width #height
                    pygame.draw.rect(self.window, self.LIGHTGREY, self.button_leaderboard)
                    pygame.draw.line(self.window, self.BLACK, (0, 510), (510, 510), 2)
                    pygame.draw.line(self.window, self.BLACK, (0, 558), (558, 558), 2)
                    pygame.draw.line(self.window, self.BLACK, (158, 510), (158, 558), 2)
                    pygame.draw.line(self.window, self.BLACK, (318, 510), (318, 558), 2)
                    self.draw_text('Leaderboard', self.BLACK, 20, 240, 534)
                    leader = True
                elif self.button_leaderboard.collidepoint(
                        pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN \
                        and leader is True:
                    self.pixel_points = []
                    self.points = []
                    self.window.fill(self.GREY)
                    Leaderbord().main(self.TITLE)
                if self.button_retry.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                    self.points_x = []
                    self.points = []
                    self.pink_point = []
                    self.pixel_points_red = []
                    self.pixel_points_green = []
                    self.pixel_points = []
                    self.name = ""
                    self.dict_points = dict()
                    self.main(user_id)
                    draw_point_enabled = True
                    draw_pink_enabled = False
                    draw_circle_enabled = False
                    draw_decision_enabled = False
                    draw_enabled = True
                if self.button_back.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                    self.window.fill(self.GREY)
                    self.points_x = []
                    self.points = []
                    self.pink_point = []
                    self.pixel_points = []
                    self.dict_points = dict()
                    self.pixel_points_red = []
                    self.pixel_points_green = []
                    self.name = ""
                    return
            pygame.display.update()


if __name__ == "__main__":
    AlgorithmKNN().initialize_game()
    AlgorithmKNN().draw_grid()
