import pygame, sys
import os, sys
import numpy as np
from sklearn.linear_model import LinearRegression

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 560

NUMBER_OF_BLOCKS_WIDE = 12
NUMBER_OF_BLOCKS_HIGH = 12
BLOCK_HEIGHT = round(SCREEN_HEIGHT / NUMBER_OF_BLOCKS_HIGH)
BLOCK_WIDTH = round(SCREEN_WIDTH / NUMBER_OF_BLOCKS_WIDE)

UP = 90
DOWN = -90
RIGHT = 0
LEFT = 180

GREY = (150, 150, 150)
RED = (255, 0, 0)
BLUE = (55, 55, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
DARKGREY = (200, 200, 200)
LIGHTGREY = (210, 210, 210)
UGLY_PINK = (255, 0, 255)
BROWN = (153, 76, 0)
GOLD = (153, 153, 0)
DARKGREEN = (0, 102, 0)
DARKORANGE = (255, 128, 0)
WHITE = (255, 255, 255)

VEL = 5

TITLE = "Linear regression"
display = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pixel_points = []


def initialize_game():
    pygame.init()
    pygame.display.set_caption(TITLE)
    window.fill(WHITE)
    return window


def draw_text(text, color, size, x, y):
    font_draw = pygame.font.Font(pygame.font.get_default_font(), size)
    text_obj = font_draw.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    window.blit(text_obj, text_rect)


def draw_grid():
    for i in range(NUMBER_OF_BLOCKS_WIDE):
        new_height = round(i * BLOCK_HEIGHT)
        new_width = round(i * BLOCK_WIDTH)
        pygame.draw.line(window, DARKGREY, (BLOCK_WIDTH, new_height - BLOCK_HEIGHT * 2), (SCREEN_WIDTH, new_height - BLOCK_HEIGHT * 2), 2)
        pygame.draw.line(window, DARKGREY, (new_width, 0), (new_width, SCREEN_HEIGHT - BLOCK_HEIGHT * 2), 2)
        pygame.draw.line(window, BLACK, (0, SCREEN_HEIGHT - BLOCK_HEIGHT * 2), (SCREEN_WIDTH, SCREEN_HEIGHT - BLOCK_HEIGHT * 2),
                          2)
        pygame.draw.line(window, BLACK, (BLOCK_WIDTH, 0), (BLOCK_WIDTH, SCREEN_HEIGHT - BLOCK_HEIGHT), 2)

    draw_text('y', BLACK, 20, BLOCK_WIDTH / 2, BLOCK_HEIGHT / 2 - 10)
    draw_text('x', BLACK, 20, SCREEN_WIDTH - BLOCK_WIDTH / 2 - 10, SCREEN_HEIGHT - BLOCK_HEIGHT * 2 + 20)
    draw_text('0', BLACK, 20, BLOCK_WIDTH / 2, SCREEN_HEIGHT - BLOCK_HEIGHT / 2 - BLOCK_HEIGHT)


    t, k = 1, 11
    while t < 10 and k > 0:
        draw_text(str(t), BLACK, 20, BLOCK_WIDTH / 2, BLOCK_HEIGHT + BLOCK_HEIGHT * (k - 2) - BLOCK_HEIGHT)
        draw_text(str(t), BLACK, 20, BLOCK_WIDTH + BLOCK_WIDTH * t, SCREEN_HEIGHT - BLOCK_HEIGHT / 2 - BLOCK_HEIGHT)
        t += 1
        k -= 1


def draw_map():
    points = []
    button_back = pygame.Rect(0, 510, 160, 60)  # left #top #width #height
    pygame.draw.rect(window, LIGHTGREY, button_back)
    button_points = pygame.Rect(160, 510, 80, 60)  # left #top #width #height
    pygame.draw.rect(window, LIGHTGREY, button_points)
    button_check = pygame.Rect(240, 510, 80, 60)  # left #top #width #height
    pygame.draw.rect(window, LIGHTGREY, button_check)
    button_retry = pygame.Rect(320, 510, 160, 60)  # left #top #width #height
    pygame.draw.rect(window, LIGHTGREY, button_retry)
    pygame.draw.line(window, BLACK, (0, 510), (510, 510), 2)
    pygame.draw.line(window, BLACK, (0, 558), (558, 558), 2)
    # pygame.draw.line(window, BLACK, (0, 510), (0, 558), 2)
    # pygame.draw.line(window, BLACK, (479, 510), (479, 558), 2)
    pygame.draw.line(window, BLACK, (158, 510), (158, 558), 2)
    pygame.draw.line(window, BLACK, (238, 510), (238, 558), 2)
    pygame.draw.line(window, BLACK, (318, 510), (318, 558), 2)
    draw_text('Back', BLACK, 20, 76, 534)
    draw_text('Draw', BLACK, 20, 198, 534)
    draw_text('Check', BLACK, 20, 278, 534)
    draw_text('Retry', BLACK, 20, 396, 534)
    all = pygame.Rect(40, 0, 480, 468)
    # pygame.draw.rect(window, BLACK, all)
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
                        pygame.draw.circle(window, BLACK, event.pos, 5, 0)
                        pixel_points.append(event.pos)
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
                        pygame.draw.circle(window, RED, event.pos, 5, 0)
                        points.append(event.pos)
            if len(points) > 1:
                pos1 = points.pop()
                pos2 = points.pop()
                x1, y1, w, h = all
                x2, y2 = x1 + w, y1 + h
                x, y = event.pos
                if x1 < x < x2:
                    if y1 < y < y2:
                        pygame.draw.line(window, RED, pos1, pos2)
                        print(f'line drawn pos1:{pos1} pos2:{pos2}')
                        drawing_enabled = False
            if button_check.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN \
                    and not draw_point_enabled:
                draw_linear_regression()
            if button_retry.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                main()
            if button_back.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                pass
        pygame.display.update()


def draw_linear_regression():
    global pixel_points
    x_points = np.array([x[0] for x in pixel_points]).reshape((-1, 1))
    y_points = np.array([x[1] for x in pixel_points])
    model = LinearRegression().fit(x_points, y_points)
    start_point = (BLOCK_WIDTH, SCREEN_HEIGHT - (model.intercept_ + model.coef_[0]))
    end_point = (SCREEN_WIDTH, SCREEN_HEIGHT - (model.intercept_ + SCREEN_WIDTH * model.coef_[0]))
    pygame.draw.line(window, UGLY_PINK, start_point, end_point, 2)


def main():
    initialize_game()
    draw_grid()
    draw_map()


if __name__ == "__main__":
    main()
