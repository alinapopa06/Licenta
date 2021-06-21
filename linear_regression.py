import sys
import pygame
import numpy as np
from AlgorithmWindowClass import AlgorithmWindowClass
from sklearn.linear_model import LinearRegression
from leaderboard import Leaderbord
# from login import Login
# import instructions
from math import sqrt


class AlgorithmLR(AlgorithmWindowClass):
    TITLE = "Linear_regression"
    score = []
    GREY = (100, 100, 100)

    def draw_linear_regression(self, user_id):
        x_points = np.array([x[0] for x in self.pixel_points]).reshape((-1, 1))
        y_points = np.array([x[1] for x in self.pixel_points])
        model = LinearRegression().fit(x_points, y_points)
        if model.coef_[0] >= 0:
            start_point = (self.BLOCK_WIDTH, model.intercept_)
            end_point = ((468 - model.intercept_) / model.coef_[0], 468)
        else:
            start_point = ((468 - model.intercept_) / model.coef_[0], 468)
            end_point = (self.SCREEN_WIDTH, model.intercept_ + self.SCREEN_WIDTH * model.coef_[0])
        pygame.draw.line(self.window, self.UGLY_PINK, start_point, end_point, 2)

        dist_func = lambda x, y: sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)
        dist1 = dist_func(start_point, self.score[0])
        dist2 = dist_func(start_point, self.score[1])
        dist3 = dist_func(end_point, self.score[0])
        dist4 = dist_func(end_point, self.score[1])
        final_distance = min(dist1, dist2) + min(dist3, dist4)
        percent = 100 - final_distance / 880 * 100
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

    def draw_map(self, user_id):
        draw_point_enabled = True
        drawing_enabled = False
        leader = False
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
                            self.pixel_points.append(event.pos)
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
                            pygame.draw.circle(self.window, self.RED, event.pos, 1, 0)
                            self.points.append(event.pos)
                            if len(self.points) > 1:
                                pos1 = self.points.pop()
                                pos2 = self.points.pop()
                                pygame.draw.line(self.window, self.RED, pos1, pos2, 2)
                                self.score.append(pos1)
                                self.score.append(pos2)
                                drawing_enabled = False
                if self.button_check.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN \
                        and not draw_point_enabled and not leader:
                    self.draw_linear_regression(user_id)
                    self.pixel_points = []
                    self.points = []
                    self.button_leaderboard = pygame.Rect(160, 510, 160, 60)  # left #top #width #height
                    pygame.draw.rect(self.window, self.LIGHTGREY, self.button_leaderboard)
                    pygame.draw.line(self.window, self.BLACK, (0, 510), (510, 510), 2)
                    pygame.draw.line(self.window, self.BLACK, (0, 558), (558, 558), 2)
                    pygame.draw.line(self.window, self.BLACK, (158, 510), (158, 558), 2)
                    pygame.draw.line(self.window, self.BLACK, (318, 510), (318, 558), 2)
                    self.draw_text('Leaderboard', self.BLACK, 20, 240, 534)
                    leader = True
                elif self.button_leaderboard.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN \
                        and leader is True:
                    self.pixel_points = []
                    self.points = []
                    self.window.fill(self.GREY)
                    Leaderbord().main(self.TITLE)
                if self.button_retry.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                    self.pixel_points = []
                    self.points = []
                    self.main(user_id)
                if self.button_back.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                    self.window.fill(self.GREY)
                    self.pixel_points = []
                    self.points = []
                    return
            pygame.display.update()

#
# if __name__ == "__main__":
#     AlgorithmLR().main()
