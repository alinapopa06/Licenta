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
LEFT = 1
MIDDLE = 2
RIGHT = 3
MAPFILE = "map.txt"
TITLE = "Welcome to Tile World!"
FOOD_ENERGY = 10
display = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pixel_points_green = []
pixel_points_red = []
points_circle = []
wait = False
pixel_points_all = []

def draw_text(text, color, size, x, y):
    font_draw = pygame.font.Font(pygame.font.get_default_font(), size)
    text_obj = font_draw.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    window.blit(text_obj, text_rect)


def get_tile_color(tile_contents):
    tile_color = GOLD
    if tile_contents == "m":
        tile_color = WHITE
    if tile_contents == ".":
        tile_color = WHITE
    if tile_contents == "p":
        tile_color = WHITE
    if tile_contents == "n":
        tile_color = RED
    return tile_color


def draw_map(surface, map_tiles):
    for j, tile in enumerate(map_tiles):
        for i, tile_contents in enumerate(tile):
            # print("{},{}: {}".format(i, j, tile_contents))
            myrect = pygame.Rect(i * BLOCK_WIDTH, j * BLOCK_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT)
            # pygame.draw.rect(surface, get_tile_color(tile_contents), myrect)
            if tile_contents == 'g':
                pygame.draw.circle(window, GREEN, (i * BLOCK_WIDTH, j * BLOCK_HEIGHT), 5, 0)
                pixel_points_green.append((i * BLOCK_WIDTH, j * BLOCK_HEIGHT))
                pixel_points_all.append((i * BLOCK_WIDTH, j * BLOCK_HEIGHT))
            elif tile_contents == 'r':
                pygame.draw.circle(window, RED, (i * BLOCK_WIDTH, j * BLOCK_HEIGHT), 5, 0)
                pixel_points_red.append((i * BLOCK_WIDTH, j * BLOCK_HEIGHT))
                pixel_points_all.append((i * BLOCK_WIDTH, j * BLOCK_HEIGHT))
    draw_text('y', BLACK, 20, BLOCK_WIDTH / 2, BLOCK_HEIGHT / 2 + 10)
    draw_text('x', BLACK, 20, SCREEN_WIDTH - BLOCK_WIDTH / 2 - 10, SCREEN_HEIGHT - BLOCK_HEIGHT / 2)
    draw_text('0', BLACK, 20, BLOCK_WIDTH / 2, SCREEN_HEIGHT - BLOCK_HEIGHT / 2)
    t, k = 1, 11
    while t < 10 and k > 0:
        draw_text(str(t), BLACK, 20, BLOCK_WIDTH / 2, BLOCK_HEIGHT + BLOCK_HEIGHT * (k - 2))
        draw_text(str(t), BLACK, 20, BLOCK_WIDTH + BLOCK_WIDTH * t, SCREEN_HEIGHT - BLOCK_HEIGHT / 2)
        t += 1
        k -= 1


def draw_grid(surface):
    for i in range(NUMBER_OF_BLOCKS_WIDE):
        new_height = round(i * BLOCK_HEIGHT)
        new_width = round(i * BLOCK_WIDTH)
        pygame.draw.line(surface, DARKGREY, (BLOCK_HEIGHT, new_height), (SCREEN_WIDTH, new_height), 2)
        pygame.draw.line(surface, DARKGREY, (new_width, 0), (new_width, SCREEN_HEIGHT - BLOCK_HEIGHT), 2)
        pygame.draw.line(surface, BLACK, (0, SCREEN_HEIGHT - BLOCK_HEIGHT), (SCREEN_WIDTH, SCREEN_WIDTH - BLOCK_WIDTH), 2)
        pygame.draw.line(surface, BLACK, (BLOCK_WIDTH, 0), (BLOCK_HEIGHT, SCREEN_HEIGHT), 2)


def draw_knn(points, k=3):
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
    global pixel_points_green
    global pixel_points_red
    pointss = {'1' : pixel_points_green, '0' : pixel_points_red}
    pygame.event.clear()
    wait = True
    while wait:
        print('1')
        # event = pygame.event.wait()
        print(points)
        x_points = [x[0] for x in points]
        y_points = [x[1] for x in points]
        wait = False
        print('xd', x_points, 'xc', y_points)
    distance = []
    for group in pointss:
        for feature in pointss[group]:
            # calculate the euclidean distance of p from training points
            euclidean_distance = math.sqrt((feature[0] - x_points) ** 2 + (feature[1] - y_points) ** 2)
            # Add a tuple of form (distance,group) in the distance list
            distance.append((euclidean_distance, group))
    # sort the distance list in ascending order
    # and select first k distances
    distance = sorted(distance)[:k]
    freq1 = 0  # frequency of group 0
    freq2 = 0  # frequency og group 1

    for d in distance:
        if d[1] == 0:
            freq1 += 1
        elif d[1] == 1:
            freq2 += 1
    if freq1 > freq2:
        print(0)
        pygame.draw.circle(window, BLUE, (BLOCK_WIDTH,  BLOCK_HEIGHT), 5, 0)
    else:
        print(1)
        pygame.draw.circle(window, BLUE, (BLOCK_WIDTH, BLOCK_HEIGHT), 20, 0)


def game_loop(surface, world_map):

    draw_grid(surface)
    draw_map(surface, world_map)
    check_event()
    draw_knn()
    pygame.display.update()

def check_event():
    points = []
    draw_point_enable = True
    draw_circle_enabled = False
    draw_decision_enable = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT and draw_point_enable \
                        and draw_circle_enabled == False and draw_decision_enable == False:
                print("Click: ({})".format(event.pos))
                if len(points) == 0:
                    points.append(event.pos)
                print('pl', points)
                pygame.draw.circle(window, UGLY_PINK, event.pos, 5, 0)
                draw_point_enable = False
                draw_circle_enabled = True
                draw_decision_enable = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT and draw_point_enable == False and \
                    draw_circle_enabled and draw_decision_enable == False:
                print("Click: ({})".format(event.pos))
                points_circle.append(event.pos)
                print(points_circle, 'ok')
                if len(points_circle) < 4:
                    pygame.draw.circle(window, BLACK, event.pos, 10, 5)
                else:
                    draw_decision_enable = True
                    draw_circle_enabled = False
                    draw_point_enable = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT and draw_point_enable == False and draw_circle_enabled == False \
                    and draw_decision_enable:
                print("Click: ({})".format(event.pos))
                draw_text('+', BLACK, 20, event.pos[0], event.pos[1])
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT and draw_point_enable == False and draw_circle_enabled == False \
                    and draw_decision_enable:
                print("Click: ({})".format(event.pos))
                draw_text('-', BLACK, 20, event.pos[0], event.pos[1])
        print(points, 'ml')
        # draw_knn(points)
        pygame.display.update()


# def wait():
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 return

def initialize_game():
    pygame.init()
    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    surface.fill(WHITE)
    return surface


def read_map():
    # filepath = os.path.join("likenta", MAPFILE)
    with open(MAPFILE, 'r') as f:
        world_map = f.readlines()
    world_map = [line.strip() for line in world_map]
    return world_map


def main():
    world_map = read_map()
    surface = initialize_game()
    game_loop(surface, world_map)



if __name__ == "__main__":
    main()