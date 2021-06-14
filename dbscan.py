import sys
import pygame
# from instructions import draw_instr_dbscan
from sklearn.cluster import DBSCAN
from AlgorithmWindowClass import AlgorithmWindowClass
import numpy as np
import time

class AlgorithmDBSCAN(AlgorithmWindowClass):
    TITLE = "DBSCAN"
    backcolor = None

    def draw_dbscan(self):
        model = DBSCAN(eps=3, min_samples=10)
        model.fit(np.array(self.pixel_points).reshape((-1, 1)))
        print(self.pixel_points, model.labels_)
        for j in model.labels_:
            for i in self.pixel_points:
                if j == -1:
                    pygame.draw.circle(self.window, self.RED, i, 5, 0)
                elif j == 0:
                    pygame.draw.circle(self.window, self.GREEN, i, 5, 0)
                elif j == 1:
                    pygame.draw.circle(self.window, self.BLUE, i, 5, 0)

    def draw_grid(self):
        pygame.init()
        name = ""
        font = pygame.font.Font(None, 40)
        run = True
        while run:
            for evt in pygame.event.get():
                if evt.type == pygame.KEYDOWN:
                    if not evt.unicode.isalpha():
                        name += evt.unicode
                    elif evt.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    if evt.key == pygame.K_RETURN:
                        name = ""
                        self.draw_game_grid()
                        run = False
                elif evt.type == pygame.QUIT:
                    return
            self.window.fill((0, 0, 0))
            block = font.render(name, True, self.WHITE)
            rect = block.get_rect()
            rect.center = self.window.get_rect().center
            self.window.blit(block, rect)
            self.draw_text('Please enter your input:', self.WHITE, 20, rect.centerx, rect.centery - 50)
            pygame.draw.line(self.window, self.WHITE, rect.topleft, rect.bottomleft, 2)
            pygame.draw.line(self.window, self.WHITE, rect.topleft, rect.topright, 2)
            pygame.draw.line(self.window, self.WHITE, rect.bottomright, rect.topright, 2)
            pygame.draw.line(self.window, self.WHITE, rect.bottomleft, rect.bottomright, 2)

            pygame.display.flip()

    def draw_game_grid(self):
        fade = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        fade.fill((255, 255, 255))
        for alpha in range(0, 255):
            fade.set_alpha(alpha)
            self.window.fill((0, 0, 0))
            self.window.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(5)
        self.window.fill(self.WHITE)
        pygame.display.update()
        pygame.draw.rect(self.window, self.LIGHTGREY, self.button_back)
        pygame.draw.rect(self.window, self.LIGHTGREY, self.button_draw)
        pygame.draw.rect(self.window, self.LIGHTGREY, self.button_check)
        pygame.draw.rect(self.window, self.LIGHTGREY, self.button_retry)
        pygame.draw.line(self.window, self.BLACK, (0, 510), (510, 510), 2)
        pygame.draw.line(self.window, self.BLACK, (0, 558), (558, 558), 2)
        pygame.draw.line(self.window, self.BLACK, (158, 510), (158, 558), 2)
        pygame.draw.line(self.window, self.BLACK, (238, 510), (238, 558), 2)
        pygame.draw.line(self.window, self.BLACK, (318, 510), (318, 558), 2)
        self.draw_text('Back', self.BLACK, 20, 76, 534)
        self.draw_text('Draw', self.BLACK, 20, 198, 534)
        self.draw_text('Check', self.BLACK, 20, 278, 534)
        self.draw_text('Retry', self.BLACK, 20, 396, 534)

        for i in range(self.NUMBER_OF_BLOCKS_WIDE):
            new_height = round(i * self.BLOCK_HEIGHT)
            new_width = round(i * self.BLOCK_WIDTH)
            pygame.draw.line(self.window, self.DARKGREY, (self.BLOCK_WIDTH, new_height - self.BLOCK_HEIGHT * 2),
                             (self.SCREEN_WIDTH, new_height - self.BLOCK_HEIGHT * 2), 2)
            pygame.draw.line(self.window, self.DARKGREY, (new_width, 0), (new_width, self.SCREEN_HEIGHT - self.BLOCK_HEIGHT * 2), 2)
            pygame.draw.line(self.window, self.BLACK, (0, self.SCREEN_HEIGHT - self.BLOCK_HEIGHT * 2),
                             (self.SCREEN_WIDTH, self.SCREEN_HEIGHT - self.BLOCK_HEIGHT * 2),
                             2)
            pygame.draw.line(self.window, self.BLACK, (self.BLOCK_WIDTH, 0), (self.BLOCK_WIDTH, self.SCREEN_HEIGHT - self.BLOCK_HEIGHT), 2)

        self.draw_text('y', self.BLACK, 20, self.BLOCK_WIDTH / 2, self.BLOCK_HEIGHT / 2 - 10)
        self.draw_text('x', self.BLACK, 20, self.SCREEN_WIDTH - self.BLOCK_WIDTH / 2 - 10, self.SCREEN_HEIGHT - self.BLOCK_HEIGHT * 2 + 20)
        self.draw_text('0', self.BLACK, 20, self.BLOCK_WIDTH / 2, self.SCREEN_HEIGHT - self.BLOCK_HEIGHT / 2 - self.BLOCK_HEIGHT)

        t, k = 1, 11
        while t < 10 and k > 0:
            self.draw_text(str(t), self.BLACK, 20, self.BLOCK_WIDTH / 2, self.BLOCK_HEIGHT + self.BLOCK_HEIGHT * (k - 2) - self.BLOCK_HEIGHT)
            self.draw_text(str(t), self.BLACK, 20, self.BLOCK_WIDTH + self.BLOCK_WIDTH * t, self.SCREEN_HEIGHT - self.BLOCK_HEIGHT / 2 - self.BLOCK_HEIGHT)
            t += 1
            k -= 1
        pygame.display.update()
        self.draw_map()

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
    AlgorithmDBSCAN().initialize_game()
    AlgorithmDBSCAN().draw_grid()

