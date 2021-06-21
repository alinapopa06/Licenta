import sys
import pygame
from sklearn.cluster import KMeans
from AlgorithmWindowClass import AlgorithmWindowClass
# import instructions
from math import sqrt
from leaderboard import Leaderbord
import sqlite3


class AlgorithmKMEANS(AlgorithmWindowClass):
    TITLE = "K_Means"
    points_circle = []
    backcolor = None
    name = ''
    GREY = (100, 100, 100)

    def draw_kmeans(self, points, n_clusters, user_id):
        kmeans = KMeans(n_clusters).fit(points)
        final_distance = 0
        for i in kmeans.cluster_centers_:
            pygame.draw.circle(self.window, self.BLUE, i, 5, 0)
            dist_func = lambda x, y: sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)

            distances = []
            for j in self.points_circle:
                distances.append(dist_func(i, j))
            final_distance += min(distances)
        percent = 100 - final_distance / (n_clusters * 880) * 100
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
        drawing_enabled = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and draw_point_enabled and not drawing_enabled:
                    x1, y1, w, h = self.all
                    x2, y2 = x1 + w, y1 + h
                    x, y = event.pos
                    if x1 < x < x2:
                        if y1 < y < y2:
                            pygame.draw.circle(self.window, self.BLACK, event.pos, 5, 0)
                            self.points.append(event.pos)
                if self.button_draw.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN \
                        and draw_point_enabled and not drawing_enabled:
                    draw_point_enabled = False
                    drawing_enabled = True
                elif event.type == pygame.MOUSEBUTTONDOWN and drawing_enabled:
                    x1, y1, w, h = self.all
                    x2, y2 = x1 + w, y1 + h
                    x, y = event.pos
                    if x1 < x < x2:
                        if y1 < y < y2:
                            self.draw_text('x', self.BLACK, 15, event.pos[0], event.pos[1])
                            self.points_circle.append(event.pos)
                            if len(self.points_circle) == int(self.name):
                                drawing_enabled = False
                if self.button_check.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN \
                        and not draw_point_enabled and leader is not True:
                    self.draw_kmeans(self.points, int(self.name), user_id)
                    self.points = []
                    self.points_circle = []
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
                    self.points = []
                    self.points_circle = []
                    self.__init__()
                    self.main(user_id)
                if self.button_back.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                    self.points = []
                    self.points_circle = []
                    self.window.fill(self.GREY)
                    return
            pygame.display.update()

# if __name__ == "__main__":
#     AlgorithmKMEANS().main(user_id)
