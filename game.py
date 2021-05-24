import time

import pygame

# defining the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.init()

screen = pygame.display.set_mode((640, 480))
# loading the font to be used at drawing time
font = pygame.font.SysFont(None, 55)

pygame.display.set_caption('Drawing')

screen.fill(BLACK)

# drawing at the surface
pygame.draw.line(screen, WHITE, [10, 100], [630, 100], 5)
pygame.draw.rect(screen, BLUE, [200, 210, 40, 20])
pygame.draw.ellipse(screen, RED, [300, 200, 40, 40])
pygame.draw.polygon(screen, GREEN, [[420, 200], [440, 240], [400, 240]])

pygame.display.flip()

time.sleep(5)

screen.fill(BLACK)

# writing pygame at the buffer
text = font.render('pygame', True, WHITE)
# coping the text to the screen
screen.blit(text, [250, 200])

pygame.display.flip()

time.sleep(5)

# from menu import *
#
# pygame.init()
# running, playing = True, False
# UP_KEY, DOWN_KEY, START_KEY, BACK_KEY = False, False, False, False
# DISPLAY_W, DISPLAY_H = 900, 500
# display = pygame.Surface((DISPLAY_W, DISPLAY_H))
# window = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))
# font_name = pygame.font.get_default_font()
# BLACK, WHITE = (0, 0, 0), (255, 255, 255)
# main_menu = display_menu()
# first_game = display_menu_game1()
# second_game = display_menu_game2()
# third_game = display_menu_game3()
# curr_menu = main_menu
#
#
# def game_loop():
#     global playing
#     while playing:
#         check_events()
#         if START_KEY:
#             playing = False
#         display.fill(BLACK)
#         draw_text('Thanks for Playing', 20, DISPLAY_W / 2, DISPLAY_H / 2)
#         window.blit(display, (0, 0))
#         pygame.display.update()
#         reset_keys()
#
#
# def check_events():
#     global running, playing, UP_KEY, DOWN_KEY, START_KEY, BACK_KEY
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running, playing = False, False
#             curr_menu.run_display = False
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_RETURN:
#                 START_KEY = True
#             if event.key == pygame.K_BACKSPACE:
#                 BACK_KEY = True
#             if event.key == pygame.K_DOWN:
#                 DOWN_KEY = True
#             if event.key == pygame.K_UP:
#                 UP_KEY = True
#
#
# def reset_keys():
#     global UP_KEY, DOWN_KEY, START_KEY, BACK_KEY
#     UP_KEY, DOWN_KEY, START_KEY, BACK_KEY = False, False, False, False
#
#
# def draw_text(text, size, x, y):
#     font = pygame.font.Font(font_name, size)
#     text_surface = font.render(text, True, WHITE)
#     text_rect = text_surface.get_rect()
#     text_rect.center = (x, y)
#     display.blit(text_surface, text_rect)
