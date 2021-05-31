import pygame, sys
import os, sys
import math
import numpy as np
from sklearn.linear_model import LinearRegression

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480

NUMBER_OF_BLOCKS_WIDE = 12
NUMBER_OF_BLOCKS_HIGH = 12
BLOCK_HEIGHT = round(SCREEN_HEIGHT / NUMBER_OF_BLOCKS_HIGH)
BLOCK_WIDTH = round(SCREEN_WIDTH / NUMBER_OF_BLOCKS_WIDE)

UP = 90
DOWN = -90
RIGHT = 1
MIDDLE = 2
LEFT = 3

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

TITLE = "ID3"
FOOD_ENERGY = 10
display = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pixel_points = []
pixel_points_green = []
pixel_points_red = []


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
        pygame.draw.line(window, DARKGREY, (BLOCK_HEIGHT, new_height), (SCREEN_WIDTH, new_height), 2)
        pygame.draw.line(window, DARKGREY, (new_width, 0), (new_width, SCREEN_HEIGHT - BLOCK_HEIGHT), 2)
        pygame.draw.line(window, BLACK, (0, SCREEN_HEIGHT - BLOCK_HEIGHT), (SCREEN_WIDTH, SCREEN_WIDTH - BLOCK_WIDTH),
                         2)
        pygame.draw.line(window, BLACK, (BLOCK_WIDTH, 0), (BLOCK_HEIGHT, SCREEN_HEIGHT), 2)
        draw_text('y', BLACK, 20, BLOCK_WIDTH / 2, BLOCK_HEIGHT / 2 + 10)
        draw_text('x', BLACK, 20, SCREEN_WIDTH - BLOCK_WIDTH / 2 - 10, SCREEN_HEIGHT - BLOCK_HEIGHT / 2)
        draw_text('0', BLACK, 20, BLOCK_WIDTH / 2, SCREEN_HEIGHT - BLOCK_HEIGHT / 2)
        t, k = 1, 11
        while t < 10 and k > 0:
            draw_text(str(t), BLACK, 20, BLOCK_WIDTH / 2, BLOCK_HEIGHT + BLOCK_HEIGHT * (k - 2))
            draw_text(str(t), BLACK, 20, BLOCK_WIDTH + BLOCK_WIDTH * t, SCREEN_HEIGHT - BLOCK_HEIGHT / 2)
            t += 1
            k -= 1


def draw_map():
    points = []
    button = pygame.Rect(350, 50, 200, 50)
    pygame.draw.rect(window, GREEN, button)
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
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT and draw_point_enabled:
                pygame.draw.circle(window, GREEN, event.pos, 5, 0)
                pixel_points_green.append(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT and draw_point_enabled:
                pygame.draw.circle(window, RED, event.pos, 5, 0)
                pixel_points_red.append(event.pos)
            if button.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN \
                    and draw_point_enabled:
                draw_point_enabled = False
                draw_decision_enabled = True
            elif event.type == pygame.MOUSEBUTTONDOWN and draw_decision_enabled and event.button == MIDDLE \
                    and draw_decision_enabled:
                print("Click: ({})".format(event.pos))
                window.set_at(event.pos, RED)
                points.append(event.pos)
                if len(points) > 1:
                    pos1 = points.pop()
                    pos2 = points.pop()
                    pygame.draw.line(window, (0, 0, 0), pos1, pos2)
                    print(f'line drawn pos1:{pos1} pos2:{pos2}')
        pygame.display.update()


def main():
    initialize_game()
    draw_grid()
    draw_map()


if __name__ == "__main__":
    main()
