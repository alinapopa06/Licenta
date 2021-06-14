import sys
import pygame
import numpy as np
from AlgorithmWindowClass import AlgorithmWindowClass
from sklearn.linear_model import LinearRegression
# import instructions


class AlgorithmLR(AlgorithmWindowClass):
    TITLE = "Linear regression"

    def draw_linear_regression(self):
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

    def draw_map(self):
        draw_point_enabled = True
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
                            self.pixel_points.append(event.pos)
                if self.button_draw.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN \
                        and draw_point_enabled and not drawing_enabled:
                    draw_point_enabled = False
                    drawing_enabled = True
                elif event.type == pygame.MOUSEBUTTONDOWN and drawing_enabled:
                    print("Click: ({})".format(event.pos))
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
                                drawing_enabled = False
                if self.button_check.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN \
                        and not draw_point_enabled:
                    # drawing_enabled = False
                    self.draw_linear_regression()
                if self.button_retry.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                    self.pixel_points = []
                    self.main()
                if self.button_back.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                    self.window.fill(self.WHITE)
                    return

            pygame.display.update()


if __name__ == "__main__":
    AlgorithmLR().main()