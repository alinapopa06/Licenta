import math
import sys
import numpy as np
import pygame
import test
from AlgorithmWindowClass import AlgorithmWindowClass
from math import sqrt
from leaderboard import Leaderbord

class AlgorithmADABOOST(AlgorithmWindowClass):
    pixel_points_green = []
    pixel_points_red = []
    points = []
    pixel_points = []
    dict = dict()
    points_line = []
    y_prediction = []
    TITLE = "AdaBoost"
    lista = []
    polarity = 1
    feature_idx = None
    threshold = None
    alpha = None
    n_clf = None
    predictions = []
    thresholds_x = []
    thresholds_y = []
    clfs = []
    X_column = []
    Y_column = []
    w = []
    score = []

    def draw_adaboost(self, X, y, n_clf, user_id):
        X = np.asarray(X)
        y = np.asarray(y, dtype=np.int32)
        adaboost = test.Adaboost(n_clf=n_clf)
        adaboost.fit(X, y)
        y_pred, clfs = adaboost.predict(X)

        def accuracy(y_true, y_pred):
            accuracy = np.sum(y_true == y_pred) / len(y_true)
            return accuracy

        print('orere', y_pred)
        acc = accuracy(y, y_pred)
        print("Accuracy:", acc)

        dist_func = lambda x, y: sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)
        final_distance = 0

        for clf in clfs:
            if clf.feature_idx == 0:
                start_point = (clf.threshold, 0)
                end_point = (clf.threshold, 468)
                if clf.polarity == 1:
                    point_plus = (clf.threshold - 10, 10)
                    point_minus = (clf.threshold + 10, 10)
                else:
                    point_plus = (clf.threshold + 10, 10)
                    point_minus = (clf.threshold - 10, 10)
            else:
                start_point = (0, clf.threshold)
                end_point = (468, clf.threshold)
                if clf.polarity == 1:
                    point_plus = (10, clf.threshold - 10)
                    point_minus = (10, clf.threshold + 10)
                else:
                    point_plus = (10, clf.threshold + 10)
                    point_minus = (10, clf.threshold - 10)

            self.draw_text('-', self.BLACK, 20, point_plus[0], point_plus[1])
            self.draw_text('+', self.BLACK, 20, point_minus[0], point_minus[1])
            pygame.draw.line(self.window, self.UGLY_PINK, start_point, end_point, 2)

            closest_distance = math.inf
            for line in self.score:
                dist1 = dist_func(start_point, line[0])
                dist2 = dist_func(start_point, line[1])
                dist3 = dist_func(end_point, line[0])
                dist4 = dist_func(end_point, line[1])
                if min(dist1, dist2) + min(dist3, dist4) < closest_distance:
                    closest_distance = min(dist1, dist2) + min(dist3, dist4)
            final_distance += closest_distance

        percent = 100 - final_distance / (880 * len(clfs) * 100)
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
        leader = False
        draw_point_enabled = True
        draw_decision_enabled = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == self.LEFT and draw_point_enabled:
                    x1, y1, w, h = self.all
                    x2, y2 = x1 + w, y1 + h
                    x, y = event.pos
                    if x1 < x < x2:
                        if y1 < y < y2:
                            pygame.draw.circle(self.window, self.GREEN, event.pos, 5, 0)
                            self.pixel_points_green.append(event.pos)
                            self.pixel_points.append('1')
                            self.points.append(event.pos)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == self.RIGHT and draw_point_enabled:
                    x1, y1, w, h = self.all
                    x2, y2 = x1 + w, y1 + h
                    x, y = event.pos
                    if x1 < x < x2:
                        if y1 < y < y2:
                            pygame.draw.circle(self.window, self.RED, event.pos, 5, 0)
                            self.pixel_points_red.append(event.pos)
                            self.pixel_points.append('-1')
                            self.points.append(event.pos)
                if self.button_draw.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN \
                        and draw_point_enabled:
                    draw_point_enabled = False
                    draw_decision_enabled = True
                elif event.type == pygame.MOUSEBUTTONDOWN and draw_decision_enabled and event.button == self.MIDDLE \
                        and draw_decision_enabled:
                    x1, y1, w, h = self.all
                    x2, y2 = x1 + w, y1 + h
                    x, y = event.pos
                    if x1 < x < x2:
                        if y1 < y < y2:
                            self.window.set_at(event.pos, self.RED)
                            self.points_line.append(event.pos)
                            if len(self.points_line) > 1:
                                pos1 = self.points_line.pop()
                                pos2 = self.points_line.pop()
                                self.score.append((pos1, pos2))
                                pygame.draw.line(self.window, (0, 0, 0), pos1, pos2)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == self.LEFT and draw_decision_enabled:
                    x1, y1, w, h = self.all
                    x2, y2 = x1 + w, y1 + h
                    x, y = event.pos
                    if x1 < x < x2:
                        if y1 < y < y2:
                            pygame.draw.circle(self.window, self.WHITE, event.pos, 5, 0)
                            self.draw_text('+', self.BLACK, 20, event.pos[0], event.pos[1])
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == self.RIGHT and draw_decision_enabled:
                    x1, y1, w, h = self.all
                    x2, y2 = x1 + w, y1 + h
                    x, y = event.pos
                    if x1 < x < x2:
                        if y1 < y < y2:
                            pygame.draw.circle(self.window, self.WHITE, event.pos, 5, 0)
                            self.draw_text('-', self.BLACK, 20, event.pos[0], event.pos[1])
                if self.button_check.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN \
                        and not draw_point_enabled:
                    self.draw_adaboost(self.points, self.pixel_points, 5, user_id)
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
                    self.main(user_id)
                if self.button_back.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                    self.window.fill(self.WHITE)
                    return
            pygame.display.update()

#
# if __name__ == "__main__":
#     AlgorithmADABOOST().main(user_id)