import sys
import pygame
from AlgorithmWindowClass import AlgorithmWindowClass
from math import sqrt


class AlgorithmDBSCAN(AlgorithmWindowClass):
    TITLE = "DBSCAN"
    backcolor = None
    name = ''

    def range_search(self, p, ds, dist_func, eps):
        res = []
        distances = list(map(lambda x: dist_func(x, p), ds))
        # print(distances)
        for index in range(len(distances)):
            if distances[index] == 0.: continue
            if distances[index] <= eps:
                print('k', distances[index])
                res.append(ds[index])
        return res

    def draw_dbscan(self, min_pts, eps):
        dist_func = lambda x, y: sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)
        C = 1
        label = dict()
        for p in self.pixel_points:
            label[p] = 0

        for point in self.pixel_points:
            if label[point] != 0: continue
            neighbors = self.range_search(point, self.pixel_points, dist_func, eps)
            nr_neighbors = len(neighbors)
            if nr_neighbors < min_pts:
                label[point] = -1
                continue

            C += 1
            label[point] = C
            index = 0
            while index < nr_neighbors:
                if label[neighbors[index]] == -1: label[neighbors[index]] = C
                if label[neighbors[index]] != 0:
                    index += 1
                    continue
                label[neighbors[index]] = C

                new_neighbors = self.range_search(neighbors[index], self.pixel_points, dist_func, eps)
                if len(new_neighbors) >= min_pts:
                    neighbors += new_neighbors
                    nr_neighbors += len(new_neighbors)
                index += 1
        print(label)
        for i in label:
            j = label[i]
            if j == -1:
                pygame.draw.circle(self.window, self.RED, i, 5, 0)
            elif j == 0:
                pygame.draw.circle(self.window, self.GREEN, i, 5, 0)
            elif j == 1:
                pygame.draw.circle(self.window, self.BLUE, i, 5, 0)

    def draw_grid(self):
        pygame.init()
        font = pygame.font.Font(None, 40)
        run = True
        button_back = pygame.Rect(0, 510, 240, 60)  # left #top #width #height
        button_start = pygame.Rect(240, 510, 240, 60)  # left #top #width #height
        while run:
            for event in pygame.event.get():
                if button_back.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                    self.name = ""
                    return
                if button_start.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                    # self.name = ""
                    self.draw_game_grid()
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.unicode.isnumeric() or event.unicode in [',', '.']:
                        self.name += event.unicode
                    elif event.key == pygame.K_BACKSPACE:
                        self.name = self.name[:-1]
                    if event.key == pygame.K_RETURN:
                        # self.name = ""
                        self.draw_game_grid()
                        run = False
                elif event.type == pygame.QUIT:
                    return
            self.window.fill((0, 0, 0))
            block = font.render(self.name, True, self.WHITE)
            rect = block.get_rect()
            rect.center = self.window.get_rect().center
            self.window.blit(block, rect)
            self.draw_text('Please enter your input:', self.WHITE, 20, rect.centerx, rect.centery - 50)
            pygame.draw.line(self.window, self.WHITE, rect.bottomright, rect.topright, 2)
            pygame.draw.line(self.window, self.LIGHTGREY, (0, 510), (510, 510), 2)
            pygame.draw.line(self.window, self.LIGHTGREY, (238, 510), (238, 558), 2)
            self.draw_text('Back', self.WHITE, 20, 118, 534)
            self.draw_text('Start', self.WHITE, 20, 358, 534)
            pygame.display.flip()

    def draw_game_grid(self):
        fade = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        fade.fill((255, 255, 255))
        for alpha in range(0, 255):
            fade.set_alpha(alpha)
            self.window.fill((0, 0, 0))
            self.window.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(1)
        self.window.fill(self.WHITE)
        pygame.display.update()
        pygame.draw.rect(self.window, self.LIGHTGREY, self.button_back)
        pygame.draw.rect(self.window, self.LIGHTGREY, self.button_draw)
        pygame.draw.rect(self.window, self.LIGHTGREY, self.button_check)
        pygame.draw.rect(self.window, self.LIGHTGREY, self.button_retry)
        pygame.draw.line(self.window, self.BLACK, (0, 510), (510, 510), 2)
        pygame.draw.line(self.window, self.BLACK, (0, 558), (558, 558), 2)
        pygame.draw.line(self.window, self.BLACK, (158, 510), (158, 558), 2)
        # pygame.draw.line(self.window, self.BLACK, (238, 510), (238, 558), 2)
        pygame.draw.line(self.window, self.BLACK, (318, 510), (318, 558), 2)
        self.draw_text('Back', self.BLACK, 20, 76, 534)
        # self.draw_text('Draw', self.BLACK, 20, 198, 534)
        self.draw_text('Check', self.BLACK, 20, 240, 534)
        self.draw_text('Retry', self.BLACK, 20, 396, 534)

        for i in range(self.NUMBER_OF_BLOCKS_WIDE):
            new_height = round(i * self.BLOCK_HEIGHT)
            new_width = round(i * self.BLOCK_WIDTH)
            pygame.draw.line(self.window, self.DARKGREY, (self.BLOCK_WIDTH, new_height - self.BLOCK_HEIGHT * 2),
                             (self.SCREEN_WIDTH, new_height - self.BLOCK_HEIGHT * 2), 2)
            pygame.draw.line(self.window, self.DARKGREY, (new_width, 0),
                             (new_width, self.SCREEN_HEIGHT - self.BLOCK_HEIGHT * 2), 2)
            pygame.draw.line(self.window, self.BLACK, (0, self.SCREEN_HEIGHT - self.BLOCK_HEIGHT * 2),
                             (self.SCREEN_WIDTH, self.SCREEN_HEIGHT - self.BLOCK_HEIGHT * 2),
                             2)
            pygame.draw.line(self.window, self.BLACK, (self.BLOCK_WIDTH, 0),
                             (self.BLOCK_WIDTH, self.SCREEN_HEIGHT - self.BLOCK_HEIGHT), 2)

        self.draw_text('y', self.BLACK, 20, self.BLOCK_WIDTH / 2, self.BLOCK_HEIGHT / 2 - 10)
        self.draw_text('x', self.BLACK, 20, self.SCREEN_WIDTH - self.BLOCK_WIDTH / 2 - 10,
                       self.SCREEN_HEIGHT - self.BLOCK_HEIGHT * 2 + 20)
        self.draw_text('0', self.BLACK, 20, self.BLOCK_WIDTH / 2,
                       self.SCREEN_HEIGHT - self.BLOCK_HEIGHT / 2 - self.BLOCK_HEIGHT)

        t, k = 1, 11
        while t < 10 and k > 0:
            self.draw_text(str(t), self.BLACK, 20, self.BLOCK_WIDTH / 2,
                           self.BLOCK_HEIGHT + self.BLOCK_HEIGHT * (k - 2) - self.BLOCK_HEIGHT)
            self.draw_text(str(t), self.BLACK, 20, self.BLOCK_WIDTH + self.BLOCK_WIDTH * t,
                           self.SCREEN_HEIGHT - self.BLOCK_HEIGHT / 2 - self.BLOCK_HEIGHT)
            t += 1
            k -= 1
        pygame.display.update()
        self.draw_map()

    def draw_map(self):
        draw_point_enabled = True
        # drawing_enabled = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and draw_point_enabled:
                    x1, y1, w, h = self.all
                    x2, y2 = x1 + w, y1 + h
                    x, y = event.pos
                    if x1 < x < x2:
                        if y1 < y < y2:
                            pygame.draw.circle(self.window, self.BLACK, event.pos, 5, 0)
                            self.pixel_points.append(event.pos)
                # if self.button_draw.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN \
                #         and draw_point_enabled and not drawing_enabled:
                #     draw_point_enabled = False
                    # drawing_enabled = True
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == self.MIDDLE:
                    x1, y1, w, h = self.all
                    x2, y2 = x1 + w, y1 + h
                    x, y = event.pos
                    if x1 < x < x2:
                        if y1 < y < y2:
                            print("Click: ({})".format(event.pos))
                            self.window.set_at(event.pos, self.RED)
                            self.points.append(event.pos)
                if self.button_check.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                    draw_point_enabled = False
                    print(self.name)
                    self.draw_dbscan(10, float(self.name))
                    self.name = ""
                    self.pixel_points = []
                if self.button_retry.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                    self.pixel_points = []
                    self.name = ""
                    self.main()
                if self.button_back.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                    self.pixel_points = []
                    self.window.fill(self.WHITE)
                    self.name = ""
                    return
            pygame.display.update()


if __name__ == "__main__":
    AlgorithmDBSCAN().initialize_game()
    AlgorithmDBSCAN().draw_grid()
