import sys
import math
import pygame
from AlgorithmWindowClass import AlgorithmWindowClass


# import instructions


class AlgorithmKNN(AlgorithmWindowClass):
    TITLE = "KNN"
    points_circle = []
    pixel_points_all = []
    pixel_points_red = []
    pixel_points_green = []

    def draw_knn(self, points, k=3):
        pointss = {'1': self.pixel_points_green, '0': self.pixel_points_red}
        x_points = [x[0] for x in points]
        y_points = [x[1] for x in points]
        distance = []
        for group in pointss:
            for feature in pointss[group]:
                # calculate the euclidean distance of p from training points
                euclidean_distance = math.sqrt((feature[0] - x_points[0]) ** 2 + (feature[1] - y_points[0]) ** 2)
                # Add a tuple of form (distance,group) in the distance list
                distance.append((euclidean_distance, group))
        # sort the distance list in ascending order
        # and select first k distances
        distance = sorted(distance)[:k]
        freq1 = 0  # frequency of group 0
        freq2 = 0  # frequency og group 1

        for d in distance:
            if d[1] == '0':
                freq1 += 1
            elif d[1] == '1':
                freq2 += 1

        if freq1 < freq2:
            pygame.draw.circle(self.window, self.GREEN, points[0], 5, 0)
            # self.draw_text('+', self.BLACK, 20, points[0][0], points[0][1])
        else:
            pygame.draw.circle(self.window, self.RED, points[0], 5, 0)
            # self.draw_text('-', self.BLACK, 20, points[0][0], points[0][1])

    def draw_map(self):
        draw_point_enabled = True
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
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == self.RIGHT and draw_point_enabled:
                    x1, y1, w, h = self.all
                    x2, y2 = x1 + w, y1 + h
                    x, y = event.pos
                    if x1 < x < x2:
                        if y1 < y < y2:
                            pygame.draw.circle(self.window, self.RED, event.pos, 5, 0)
                            self.pixel_points_red.append(event.pos)
                if self.button_draw.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN \
                        and draw_enabled:
                    draw_point_enabled = False
                    draw_pink_enabled = True
                    draw_decision_enabled = False
                    draw_circle_enabled = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == self.LEFT and draw_pink_enabled \
                        and not draw_circle_enabled and not draw_decision_enabled:
                    x1, y1, w, h = self.all
                    x2, y2 = x1 + w, y1 + h
                    x, y = event.pos
                    if x1 < x < x2:
                        if y1 < y < y2:
                            print("Click pink: ({})".format(event.pos))
                            if len(self.points) == 0:
                                self.points.append(event.pos)
                            pygame.draw.circle(self.window, self.UGLY_PINK, event.pos, 5, 0)
                            draw_pink_enabled = False
                            draw_circle_enabled = True
                            draw_point_enabled = False
                            draw_decision_enabled = False
                            draw_enabled = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == self.LEFT and not draw_pink_enabled \
                        and draw_circle_enabled and not draw_decision_enabled:
                    x1, y1, w, h = self.all
                    x2, y2 = x1 + w, y1 + h
                    x, y = event.pos
                    if x1 < x < x2:
                        if y1 < y < y2:
                            print("Click circle: ({})".format(event.pos))
                            self.draw_text('x', self.BLACK, 15, event.pos[0], event.pos[1])
                            self.points_circle.append(event.pos)
                            if len(self.points_circle) == 3:
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
                            print("Click plus: ({})".format(event.pos))
                            self.draw_text('+', self.BLACK, 20, event.pos[0], event.pos[1])
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
                            print("Click minus: ({})".format(event.pos))
                            self.draw_text('-', self.BLACK, 20, event.pos[0], event.pos[1])
                            draw_decision_enabled = False
                            draw_circle_enabled = False
                            draw_pink_enabled = False
                            draw_point_enabled = False
                            draw_enabled = False
                if self.button_check.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN \
                        and not draw_point_enabled:
                    self.draw_knn(self.points)
                    draw_decision_enabled = False
                    draw_circle_enabled = False
                    draw_pink_enabled = False
                    draw_point_enabled = False
                    draw_enabled = False
                if self.button_retry.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                    self.main()
                if self.button_back.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                    self.window.fill(self.WHITE)
                    return
            pygame.display.update()


if __name__ == "__main__":
    AlgorithmKNN().main()
