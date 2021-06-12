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
        '''
         This function finds the classification of p using
         k nearest neighbor algorithm. It assumes only two
         groups and returns 0 if p belongs to group 0, else
          1 (belongs to group 1).
          Parameters -
              points: Dictionary of training points having two keys - 0 and 1
                       Each key have a list of training data points belong to that
              p : A tuple, test data point of the form (x,y)
              k : number of nearest neighbour to consider, default is 3
        '''
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

        if freq1 > freq2:
            pygame.draw.circle(self.window, self.BLUE, points[0], 5, 0)
        else:
            pygame.draw.circle(self.window, self.DARKORANGE, points[0], 5, 0)

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
                    x1, y1, w, h = all
                    x2, y2 = x1 + w, y1 + h
                    x, y = event.pos
                    if x1 < x < x2:
                        if y1 < y < y2:
                            pygame.draw.circle(self.window, self.GREEN, event.pos, 5, 0)
                            self.pixel_points_green.append(event.pos)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == self.RIGHT and draw_point_enabled:
                    x1, y1, w, h = all
                    x2, y2 = x1 + w, y1 + h
                    x, y = event.pos
                    if x1 < x < x2:
                        if y1 < y < y2:
                            pygame.draw.circle(self.window, self.RED, event.pos, 5, 0)
                            self.pixel_points_red.append(event.pos)
                # de ce daca apaas draw se pune iar punct??? :(:(:(:(:(
                if button_points.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN \
                        and draw_enabled:
                    draw_point_enabled = False
                    draw_pink_enabled = True
                    draw_decision_enabled = False
                    draw_circle_enabled = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == self.LEFT and draw_pink_enabled \
                        and not draw_circle_enabled and not draw_decision_enabled:
                    x1, y1, w, h = all
                    x2, y2 = x1 + w, y1 + h
                    x, y = event.pos
                    if x1 < x < x2:
                        if y1 < y < y2:
                            print("Click pink: ({})".format(event.pos))
                            if len(points) == 0:
                                points.append(event.pos)
                            pygame.draw.circle(self.window, self.UGLY_PINK, event.pos, 5, 0)
                            draw_pink_enabled = False
                            draw_circle_enabled = True
                            draw_point_enabled = False
                            draw_decision_enabled = False
                            draw_enabled = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == self.LEFT and not draw_pink_enabled \
                        and draw_circle_enabled and not draw_decision_enabled:
                    x1, y1, w, h = all
                    x2, y2 = x1 + w, y1 + h
                    x, y = event.pos
                    if x1 < x < x2:
                        if y1 < y < y2:
                            print("Click circle: ({})".format(event.pos))
                            pygame.draw.circle(self.window, self.BLACK, event.pos, 10, 5)
                            self.points_circle.append(event.pos)
                            if len(self.points_circle) == 3:
                                draw_decision_enabled = True
                                draw_circle_enabled = False
                                draw_pink_enabled = False
                                draw_point_enabled = False
                                draw_enabled = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == self.LEFT and not draw_pink_enabled \
                        and not draw_circle_enabled and draw_decision_enabled:
                    x1, y1, w, h = all
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
                    x1, y1, w, h = all
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
                if button_check.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN \
                        and not draw_point_enabled:
                    self.draw_knn(points)
                    draw_decision_enabled = False
                    draw_circle_enabled = False
                    draw_pink_enabled = False
                    draw_point_enabled = False
                    draw_enabled = False
                if button_retry.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                    self.main()
                # if button_back.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                #     instructions.draw_instr_knn()
            pygame.display.update()


if __name__ == "__main__":
    AlgorithmKNN().main()
