import sys

import numpy as np
import pygame
from sklearn import metrics, svm
from sklearn.model_selection import train_test_split
from AlgorithmWindowClass import AlgorithmWindowClass
# import instructions
import sklearn

class AlgorithmSVM(AlgorithmWindowClass):
    TITLE = "SVM"
    pixel_points_red = []
    pixel_points_green = []

    def draw_svm(self, points):
        model = svm.SVC(kernel='linear')  # Linear Kernel
        model.fit(np.array(points).reshape((-1, 2)), self.pixel_points)

        w = model.coef_[0]
        a = -w[0] / w[1]
        b_down = model.support_vectors_[0]
        b_up = model.support_vectors_[-1]

        if a >= 0:
            x_start = self.BLOCK_WIDTH
            y_start = a * x_start - (model.intercept_[0]) / w[1]
            start_point = (x_start, y_start)

            x_start_down = self.BLOCK_WIDTH
            y_start_down = (b_down[1] - a * b_down[0]) + x_start_down * a
            print(x_start_down * a, (b_down[1] - a * b_down[0]))
            start_point_down = (x_start_down, y_start_down)

            x_start_up = self.BLOCK_WIDTH
            y_start_up = a * x_start_up + (b_up[1] - a * b_up[0])
            start_point_up = (x_start_up, y_start_up)

            y_end = 468
            x_end = (y_end + (model.intercept_[0]) / w[1]) / a
            end_point = (x_end, y_end)

            y_end_down = 468
            x_end_down = (y_end_down - (b_down[1] - a * b_down[0])) / a
            end_point_down = (x_end_down, y_end_down)

            y_end_up = 468
            x_end_up = (y_end_up - (b_up[1] - a * b_up[0])) / a
            end_point_up = (x_end_up, y_end_up)
        else:
            y_start = 468
            x_start = (y_start + (model.intercept_[0]) / w[1]) / a
            start_point = (x_start, y_start)

            y_start_down = 468
            x_start_down = (y_start_down - (b_down[1] - a * b_down[0])) / a
            start_point_down = (x_start_down, y_start_down)

            y_start_up = 468
            x_start_up = (y_start_up - (b_up[1] - a * b_up[0])) / a
            start_point_up = (x_start_up, y_start_up)

            x_end = self.SCREEN_WIDTH
            y_end = a * x_end - (model.intercept_[0]) / w[1]
            end_point = (x_end, y_end)

            x_end_down = self.SCREEN_WIDTH
            y_end_down = a * x_end_down + (b_down[1] - a * b_down[0])
            end_point_down = (x_end_down, y_end_down)

            x_end_up = self.SCREEN_WIDTH
            y_end_up = a * x_end_up + (b_up[1] - a * b_up[0])
            end_point_up = (x_end_up, y_end_up)

        pygame.draw.line(self.window, self.UGLY_PINK, start_point, end_point, 2)
        pygame.draw.line(self.window, self.BLACK, start_point_down, end_point_down, 2)
        pygame.draw.line(self.window, self.DARKORANGE, start_point_up, end_point_up, 2)

    def draw_map(self):
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
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == self.RIGHT and draw_point_enabled:
                    x1, y1, w, h = self.all
                    x2, y2 = x1 + w, y1 + h
                    x, y = event.pos
                    if x1 < x < x2:
                        if y1 < y < y2:
                            pygame.draw.circle(self.window, self.RED, event.pos, 5, 0)
                            self.pixel_points_red.append(event.pos)
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
                            print("Click: ({})".format(event.pos))
                            self.window.set_at(event.pos, self.RED)
                            self.points.append(event.pos)
                            if len(self.points) > 1:
                                pos1 = self.points.pop()
                                pos2 = self.points.pop()
                                pygame.draw.line(self.window, self.UGLY_PINK, pos1, pos2)
                                print(f'line drawn pos1:{pos1} pos2:{pos2}')
                                for i in self.pixel_points_green:
                                    self.pixel_points.append('1')
                                    self.points.append(i)
                                for i in self.pixel_points_red:
                                    self.pixel_points.append('0')
                                    self.points.append(i)
                                draw_decision_enabled = False
                if self.button_check.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN \
                        and not draw_decision_enabled:
                    self.draw_svm(self.points)
                if self.button_retry.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                    self.pixel_points = []
                    self.pixel_points_green = []
                    self.pixel_points_red = []
                    points = []
                    self.main()
                if self.button_back.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                    self.window.fill(self.WHITE)
                    return
            pygame.display.update()


if __name__ == "__main__":
    AlgorithmSVM().main()