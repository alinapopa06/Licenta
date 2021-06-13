import sys
import pygame
from AlgorithmWindowClass import AlgorithmWindowClass
# import instructions


class AlgorithmID3(AlgorithmWindowClass):
    pixel_points_green = []
    pixel_points_red = []
    TITLE = "ID3"

    def draw_map(self):
        points = []
        button_back = pygame.Rect(0, 510, 160, 60)  # self.LEFT #top #width #height
        pygame.draw.rect(self.window, self.LIGHTGREY, button_back)
        button_points = pygame.Rect(160, 510, 80, 60)  # self.LEFT #top #width #height
        pygame.draw.rect(self.window, self.LIGHTGREY, button_points)
        button_check = pygame.Rect(240, 510, 80, 60)  # self.LEFT #top #width #height
        pygame.draw.rect(self.window, self.LIGHTGREY, button_check)
        button_retry = pygame.Rect(320, 510, 160, 60)  # self.LEFT #top #width #height
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
        draw_decision_enabled = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == self.LEFT and draw_point_enabled:
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
                if button_points.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN \
                        and draw_point_enabled:
                    draw_point_enabled = False
                    draw_decision_enabled = True
                elif event.type == pygame.MOUSEBUTTONDOWN and draw_decision_enabled and event.button == self.MIDDLE \
                        and draw_decision_enabled:
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
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == self.LEFT and draw_decision_enabled:
                    x1, y1, w, h = all
                    x2, y2 = x1 + w, y1 + h
                    x, y = event.pos
                    if x1 < x < x2:
                        if y1 < y < y2:
                            print("Click: ({})".format(event.pos))
                            pygame.draw.circle(self.window, self.WHITE, event.pos, 5, 0)
                            self.draw_text('+', self.BLACK, 20, event.pos[0], event.pos[1])
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == self.RIGHT and draw_decision_enabled:
                    x1, y1, w, h = all
                    x2, y2 = x1 + w, y1 + h
                    x, y = event.pos
                    if x1 < x < x2:
                        if y1 < y < y2:
                            print("Click: ({})".format(event.pos))
                            pygame.draw.circle(self.window, self.WHITE, event.pos, 5, 0)
                            self.draw_text('-', self.BLACK, 20, event.pos[0], event.pos[1])
                if button_check.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN \
                        and not draw_point_enabled:
                    pass
                if button_retry.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                    self.main()
                if button_back.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                    self.window.fill(self.WHITE)
                    return
            pygame.display.update()


if __name__ == "__main__":
    AlgorithmID3().main()
