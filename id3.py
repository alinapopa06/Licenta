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
pixel_points = []


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
            elif tile_contents == 'r':
                pygame.draw.circle(window, RED, (i * BLOCK_WIDTH, j * BLOCK_HEIGHT), 5, 0)
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



def game_loop(surface, world_map):
    points = []
    drawing_enabled = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and drawing_enabled and event.button == MIDDLE:
                print("Click: ({})".format(event.pos))
                window.set_at(event.pos, RED)
                points.append(event.pos)
                if len(points) > 1:
                    pos1 = points.pop()
                    pos2 = points.pop()
                    pygame.draw.line(window, (0, 0, 0), pos1, pos2)
                    print(f'line drawn pos1:{pos1} pos2:{pos2}')
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT and drawing_enabled:
                print("Click: ({})".format(event.pos))
                pygame.draw.circle(window, WHITE, event.pos, 5, 0)
                draw_text('+', BLACK, 20, event.pos[0], event.pos[1])
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT and drawing_enabled:
                print("Click: ({})".format(event.pos))
                pygame.draw.circle(window, WHITE, event.pos, 5, 0)
                draw_text('-', BLACK, 20, event.pos[0], event.pos[1])

            # if event.type == pygame.K_BACKSPACE and drawing_enabled:
            #     print("Click: ({})".format(event.pos))
            #     window.set_at(event.pos, RED)
            #     pygame.draw.circle(window, RED, event.pos, 5, 0)
            #     points.append(event.pos)
            #     if len(points) > 1:
            #         pos1 = points.pop()
            #         pos2 = points.pop()
            #         pygame.draw.line(window, (0, 0, 0), pos1, pos2)
            #         print(f'line drawn pos1:{pos1} pos2:{pos2}')
            #         drawing_enabled = False
        draw_grid(surface)
        draw_map(surface, world_map)
        pygame.display.update()


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

# # Python3 program to find groups of unknown
# # Points using K nearest neighbour algorithm.
#
# import math
#
# def classifyAPoint(points,p,k=3):
# 	'''
# 	This function finds the classification of p using
# 	k nearest neighbor algorithm. It assumes only two
# 	groups and returns 0 if p belongs to group 0, else
# 	1 (belongs to group 1).
#
# 	Parameters -
# 		points: Dictionary of training points having two keys - 0 and 1
# 				Each key have a list of training data points belong to that
#
# 		p : A tuple, test data point of the form (x,y)
#
# 		k : number of nearest neighbour to consider, default is 3
# 	'''
#
# 	distance=[]
# 	for group in points:
# 		for feature in points[group]:
#
# 			#calculate the euclidean distance of p from training points
# 			euclidean_distance = math.sqrt((feature[0]-p[0])**2 +(feature[1]-p[1])**2)
#
# 			# Add a tuple of form (distance,group) in the distance list
# 			distance.append((euclidean_distance,group))
#
# 	# sort the distance list in ascending order
# 	# and select first k distances
# 	distance = sorted(distance)[:k]
#
# 	freq1 = 0 #frequency of group 0
# 	freq2 = 0 #frequency og group 1
#
# 	for d in distance:
# 		if d[1] == 0:
# 			freq1 += 1
# 		elif d[1] == 1:
# 			freq2 += 1
#
# 	return 0 if freq1>freq2 else 1
#
# # driver function
# def main():
#
# 	# Dictionary of training points having two keys - 0 and 1
# 	# key 0 have points belong to class 0
# 	# key 1 have points belong to class 1
#
# 	points = {0:[(1,12),(2,5),(3,6),(3,10),(3.5,8),(2,11),(2,9),(1,7)],
# 			1:[(5,3),(3,2),(1.5,9),(7,2),(6,1),(3.8,1),(5.6,4),(4,2),(2,5)]}
#
# 	# testing point p(x,y)
# 	p = [(2.5,7), (2,5)]
#
# 	# Number of neighbours
# 	k = 3
#
# 	print("The value classified to unknown point is: {}".format(classifyAPoint(points,p,k)))
#
# if __name__ == '__main__':
# 	main()
#
# # This code is contributed by Atul Kumar (www.fb.com/atul.kr.007)
