import sys
import pygame
import numpy as np
from AlgorithmWindowClass import AlgorithmWindowClass
from sklearn.linear_model import LinearRegression
# import instructions


class AlgorithmLinearRegression(AlgorithmWindowClass):
    TITLE = "Linear regression"

    def draw_linear_regression(self):
        x_points = np.array([x[0] for x in self.pixel_points]).reshape((-1, 1))
        y_points = np.array([x[1] for x in self.pixel_points])
        model = LinearRegression().fit(x_points, y_points)
        start_point = (self.BLOCK_WIDTH, self.SCREEN_HEIGHT - (model.intercept_ + model.coef_[0]))
        end_point = (self.SCREEN_WIDTH, self.SCREEN_HEIGHT - (model.intercept_ + self.SCREEN_WIDTH * model.coef_[0]))
        pygame.draw.line(self.window, self.UGLY_PINK, start_point, end_point, 2)

    def draw_map(self):
        points = []
        button_back = pygame.Rect(0, 510, 160, 60)  # left #top #width #height
        pygame.draw.rect(self.window, self.LIGHTGREY, button_back)
        button_points = pygame.Rect(160, 510, 80, 60)  # left #top #width #height
        pygame.draw.rect(self.window, self.LIGHTGREY, button_points)
        button_check = pygame.Rect(240, 510, 80, 60)  # left #top #width #height
        pygame.draw.rect(self.window, self.LIGHTGREY, button_check)
        button_retry = pygame.Rect(320, 510, 160, 60)  # left #top #width #height
        pygame.draw.rect(self.window, self.LIGHTGREY, button_retry)
        pygame.draw.line(self.window, self.BLACK, (0, 510), (510, 510), 2)
        pygame.draw.line(self.window, self.BLACK, (0, 558), (558, 558), 2)
        # pygame.draw.line(self.window, self.BLACK, (0, 510), (0, 558), 2)
        # pygame.draw.line(self.window, self.BLACK, (479, 510), (479, 558), 2)
        pygame.draw.line(self.window, self.BLACK, (158, 510), (158, 558), 2)
        pygame.draw.line(self.window, self.BLACK, (238, 510), (238, 558), 2)
        pygame.draw.line(self.window, self.BLACK, (318, 510), (318, 558), 2)
        self.draw_text('Back', self.BLACK, 20, 76, 534)
        self.draw_text('Draw', self.BLACK, 20, 198, 534)
        self.draw_text('Check', self.BLACK, 20, 278, 534)
        self.draw_text('Retry', self.BLACK, 20, 396, 534)
        all = pygame.Rect(40, 0, 480, 468)
        # pygame.draw.rect(self.window, self.BLACK, all)
        # mx, my = pygame.mouse.get_pos()
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
                    x1, y1, w, h = all
                    x2, y2 = x1 + w, y1 + h
                    x, y = event.pos
                    if x1 < x < x2:
                        if y1 < y < y2:
                            pygame.draw.circle(self.window, self.BLACK, event.pos, 5, 0)
                            self.pixel_points.append(event.pos)
                if button_points.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN \
                        and draw_point_enabled and not drawing_enabled:
                    draw_point_enabled = False
                    drawing_enabled = True
                elif event.type == pygame.MOUSEBUTTONDOWN and drawing_enabled:
                    print("Click: ({})".format(event.pos))
                    x1, y1, w, h = all
                    x2, y2 = x1 + w, y1 + h
                    x, y = event.pos
                    if x1 < x < x2:
                        if y1 < y < y2:
                            pygame.draw.circle(self.window, self.RED, event.pos, 5, 0)
                            points.append(event.pos)

                if button_check.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN \
                        and not draw_point_enabled:
                    self.draw_linear_regression()
                if button_retry.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                    self.main()
                # if button_back.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                #     instructions.draw_instr_lr()

            pygame.display.update()


if __name__ == "__main__":
    AlgorithmLinearRegression().main()
