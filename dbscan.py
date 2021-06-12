import sys
import pygame
# from instructions import draw_instr_dbscan
from sklearn.cluster import DBSCAN
from AlgorithmWindowClass import AlgorithmWindowClass


class AlgorithmDBSCAN(AlgorithmWindowClass):
    TITLE = "DBSCAN"

    def draw_dbscan(self):
        clustering = DBSCAN(eps=0.1, min_samples=2).fit(self.pixel_points)
        for i in self.pixel_points:
            for j in clustering.labels_:
                if j == -1:
                    pygame.draw.circle(self.window, self.RED, i, 5, 0)
                elif j == 0:
                    pygame.draw.circle(self.window, self.GREEN, i, 5, 0)
                elif j == 1:
                    pygame.draw.circle(self.window, self.BLUE, i, 5, 0)
                break
    
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
                elif event.type == pygame.MOUSEBUTTONDOWN and drawing_enabled and event.button == self.MIDDLE:
                    x1, y1, w, h = all
                    x2, y2 = x1 + w, y1 + h
                    x, y = event.pos
                    if x1 < x < x2:
                        if y1 < y < y2:
                            print("Click: ({})".format(event.pos))
                            self.window.set_at(event.pos, self.RED)
                            points.append(event.pos)
                            if len(points) > 1:
                                pos1 = points.pop()
                                pos2 = points.pop()
                                pygame.draw.line(self.window, (0, 0, 0), pos1, pos2)
                                print(f'line drawn pos1:{pos1} pos2:{pos2}')
                            drawing_enabled = False
                if button_check.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN \
                        and not draw_point_enabled:
                    self.draw_dbscan()
                if button_retry.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                    self.main()
                # if button_back.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                #     draw_instr_dbscan()
            pygame.display.update()


if __name__ == "__main__":
    AlgorithmDBSCAN().main()
