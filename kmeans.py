import sys
import pygame
from sklearn.cluster import KMeans
from AlgorithmWindowClass import AlgorithmWindowClass
# import instructions


class AlgorithmKMEANS(AlgorithmWindowClass):
    TITLE = "K-Means"
    points_circle = []
    pixel_points_all = []
    pixel_points_red = []
    pixel_points_green = []
    
    def draw_kmeans(self, points):
        kmeans = KMeans(n_clusters=3).fit(points)
        for i in kmeans.cluster_centers_:
            pygame.draw.circle(self.window, self.BLUE, i, 5, 0)
    
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
                            self.points.append(event.pos)
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
                            self.draw_text('x', self.BLACK, 15, event.pos[0], event.pos[1])
                            # pygame.draw.circle(self.window, self.BLACK, event.pos, 10, 5)
                            self.points_circle.append(event.pos)
                            if len(self.points_circle) == 3:
                                drawing_enabled = False
                if self.button_check.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN \
                        and not draw_point_enabled:
                    self.draw_kmeans(self.points)
                if self.button_retry.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                    self.__init__()
                    self.main()
                if self.button_back.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                    self.window.fill(self.WHITE)
                    return
            pygame.display.update()


if __name__ == "__main__":
    AlgorithmKMEANS().main()
