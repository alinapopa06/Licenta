import pygame
import sys
import math

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 560

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
TITLE = "k-NN"
display = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pixel_points_green = []
pixel_points_red = []
points_circle = []
pixel_points_all = []


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
    draw_point_enabled = True
    draw_pink_enabled = False
    draw_circle_enabled = False
    draw_decision_enabled = False
    draw_enabled = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT and draw_point_enabled:
                x1, y1, w, h = all
                x2, y2 = x1 + w, y1 + h
                x, y = event.pos
                if x1 < x < x2:
                    if y1 < y < y2:
                        pygame.draw.circle(window, GREEN, event.pos, 5, 0)
                        pixel_points_green.append(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT and draw_point_enabled:
                x1, y1, w, h = all
                x2, y2 = x1 + w, y1 + h
                x, y = event.pos
                if x1 < x < x2:
                    if y1 < y < y2:
                        pygame.draw.circle(window, RED, event.pos, 5, 0)
                        pixel_points_red.append(event.pos)
            # de ce daca apaas draw se pune iar punct??? :(:(:(:(:(
            if button_points.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN \
                    and draw_enabled:
                draw_point_enabled = False
                draw_pink_enabled = True
                draw_decision_enabled = False
                draw_circle_enabled = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT and draw_pink_enabled \
                    and not draw_circle_enabled and not draw_decision_enabled:
                x1, y1, w, h = all
                x2, y2 = x1 + w, y1 + h
                x, y = event.pos
                if x1 < x < x2:
                    if y1 < y < y2:
                        print("Click pink: ({})".format(event.pos))
                        if len(points) == 0:
                            points.append(event.pos)
                        pygame.draw.circle(window, UGLY_PINK, event.pos, 5, 0)
                        draw_pink_enabled = False
                        draw_circle_enabled = True
                        draw_point_enabled = False
                        draw_decision_enabled = False
                        draw_enabled = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT and not draw_pink_enabled \
                    and draw_circle_enabled and not draw_decision_enabled:
                x1, y1, w, h = all
                x2, y2 = x1 + w, y1 + h
                x, y = event.pos
                if x1 < x < x2:
                    if y1 < y < y2:
                        print("Click circle: ({})".format(event.pos))
                        pygame.draw.circle(window, BLACK, event.pos, 10, 5)
                        points_circle.append(event.pos)
                        if len(points_circle) == 3:
                            draw_decision_enabled = True
                            draw_circle_enabled = False
                            draw_pink_enabled = False
                            draw_point_enabled = False
                            draw_enabled = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT and not draw_pink_enabled \
                    and not draw_circle_enabled and draw_decision_enabled:
                x1, y1, w, h = all
                x2, y2 = x1 + w, y1 + h
                x, y = event.pos
                if x1 < x < x2:
                    if y1 < y < y2:
                        print("Click plus: ({})".format(event.pos))
                        draw_text('+', BLACK, 20, event.pos[0], event.pos[1])
                        draw_decision_enabled = False
                        draw_circle_enabled = False
                        draw_pink_enabled = False
                        draw_point_enabled = False
                        draw_enabled = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT and not draw_pink_enabled \
                    and not draw_circle_enabled and draw_decision_enabled:
                x1, y1, w, h = all
                x2, y2 = x1 + w, y1 + h
                x, y = event.pos
                if x1 < x < x2:
                    if y1 < y < y2:
                        print("Click minus: ({})".format(event.pos))
                        draw_text('-', BLACK, 20, event.pos[0], event.pos[1])
                        draw_decision_enabled = False
                        draw_circle_enabled = False
                        draw_pink_enabled = False
                        draw_point_enabled = False
                        draw_enabled = False
            if button_check.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN \
                    and not draw_point_enabled:
                draw_knn(points)
                draw_decision_enabled = False
                draw_circle_enabled = False
                draw_pink_enabled = False
                draw_point_enabled = False
                draw_enabled = False
            if button_retry.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                main()
            if button_back.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                pass
        pygame.display.update()


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
    pointss = {'1': pixel_points_green, '0': pixel_points_red}
    x_points = [x[0] for x in points]
    y_points = [x[1] for x in points]
    distance = []
    for group in pointss:
        for feature in pointss[group]:
            # calculate the euclidean distance of p from training points
            euclidean_distance = math.sqrt((feature[0] - x_points[0]) ** 2 + (feature[1] - y_points[0]) ** 2)
            # Add a tuple of form (distance,group) in the distance list
            distance.append((euclidean_distance, group))
    # sort the distance list in ascending order
    # and select first k distances
    distance = sorted(distance)[:k]
    freq1 = 0  # frequency of group 0
    freq2 = 0  # frequency og group 1

    for d in distance:
        if d[1] == '0':
            freq1 += 1
        elif d[1] == '1':
            freq2 += 1

    if freq1 > freq2:
        pygame.draw.circle(window, BLUE, points[0], 5, 0)
    else:
        pygame.draw.circle(window, DARKORANGE, points[0], 5, 0)


def main():
    initialize_game()
    draw_grid()
    draw_map()


if __name__ == "__main__":
    main()
