import sys
import pygame
from sklearn.cluster import KMeans
from AlgorithmWindowClass import AlgorithmWindowClass
# import instructions


class AlgorithmKMeans(AlgorithmWindowClass):
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
                            points.append(event.pos)
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
                            pygame.draw.circle(self.window, self.BLACK, event.pos, 10, 5)
                            self.points_circle.append(event.pos)
                            if len(self.points_circle) == 3:
                                drawing_enabled = False
                if button_check.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN \
                        and not draw_point_enabled:
                    self.draw_kmeans(points)
                if button_retry.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                    self.main()
                # if button_back.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                #     instructions.draw_instr_kmeans()
            pygame.display.update()


if __name__ == "__main__":
    AlgorithmKMeans().main()
