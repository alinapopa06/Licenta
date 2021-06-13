import sys
import pygame
# from instructions import draw_instr_dbscan
from sklearn.cluster import DBSCAN
from AlgorithmWindowClass import AlgorithmWindowClass


class AlgorithmDBSCAN(AlgorithmWindowClass):
    TITLE = "DBSCAN"

    def draw_dbscan(self):
        clustering = DBSCAN(eps=0.5, min_samples=5, metric='euclidean', metric_params=None, algorithm='auto', leaf_size=30, p=None, n_jobs=None).fit(self.pixel_points)
        print(self.pixel_points, clustering.labels_)
        ok = [[1, 2], [2, 2], [2, 3],
...               [8, 7], [8, 8], [25, 80]]
        for i in ok:

            for j in clustering.labels_:

                if j == -1:
                    pygame.draw.circle(self.window, self.RED, i, 5, 0)
                elif j == 0:
                    pygame.draw.circle(self.window, self.GREEN, i, 5, 0)
                elif j == 1:
                    pygame.draw.circle(self.window, self.BLUE, i, 5, 0)
                break
    
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
                elif event.type == pygame.MOUSEBUTTONDOWN and drawing_enabled and event.button == self.MIDDLE:
                    x1, y1, w, h = self.all
                    x2, y2 = x1 + w, y1 + h
                    x, y = event.pos
                    if x1 < x < x2:
                        if y1 < y < y2:
                            print("Click: ({})".format(event.pos))
                            self.window.set_at(event.pos, self.RED)
                            self.points.append(event.pos)

                            drawing_enabled = False
                if self.button_check.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN \
                        and not draw_point_enabled:
                    self.draw_dbscan()
                if self.button_retry.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                    self.main()
                if self.button_back.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                    self.window.fill(self.WHITE)
                    return
            pygame.display.update()


if __name__ == "__main__":
    AlgorithmDBSCAN().main()
